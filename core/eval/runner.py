#!/usr/bin/env python3
"""
Eval Harness runner — measures whether a self-evolution actually improved things.

Fitness = weighted pass ratio across all tasks (0.0 - 1.0).
Compares against baseline.json, records every run into archive/, and warns on regression.

Hardening (v2)
--------------
* Task schema is validated. A malformed / empty / zero-weight / negative-weight
  task makes the whole suite FAIL (exit 2) instead of being silently skipped.
* A "hard gate" set of categories (security) can block: if any hard-gate task is
  not at 100%, `regression` is forced true regardless of overall fitness.
* archive/baseline writes are atomic (tmp + os.replace).
* `--json` always prints a well-formed record; on suite error it prints an error
  record and exits non-zero so callers (gate.sh) fail closed.

Usage:
    python3 core/eval/runner.py            # human-readable report + update archive/baseline
    python3 core/eval/runner.py --json     # machine-readable JSON only
    python3 core/eval/runner.py --accept   # set current score as the new baseline
    python3 core/eval/runner.py --list     # list tasks
    python3 core/eval/runner.py --no-write # dry run, touch nothing
"""
import argparse
import glob
import json
import math
import os
import sys
import tempfile
from datetime import datetime, timezone, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.abspath(os.path.join(HERE, "..", ".."))
TASKS_DIR = os.path.join(HERE, "tasks")
ARCHIVE_DIR = os.path.join(HERE, "archive")
BASELINE = os.path.join(HERE, "baseline.json")
TZ = timezone(timedelta(hours=7))

# Categories that must be perfect or the run is treated as a regression.
HARD_GATE_CATEGORIES = {"security"}

VALID_CHECK_TYPES = {
    "file_exists", "file_missing", "contains", "not_contains", "regex",
    "json_valid", "file_count_max", "no_leak", "no_leak_bulk", "index_has",
    "min_bytes", "max_bytes",
}

sys.path.insert(0, HERE)
from scorers import run_check  # noqa: E402


class TaskError(Exception):
    """Raised when a task file is malformed. Fails the whole suite."""


def _num(v, name, where):
    """Require a finite real number (rejects bool, str, NaN, Infinity)."""
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise TaskError(f"{where}: '{name}' must be a finite number (got {v!r})")
    return v


def _str(v, name, where):
    if not isinstance(v, str) or not v:
        raise TaskError(f"{where}: '{name}' must be a non-empty string")
    return v


def _str_list(v, name, where, allow_empty=False):
    if not isinstance(v, list) or (not v and not allow_empty):
        raise TaskError(f"{where}: '{name}' must be a {'possibly empty ' if allow_empty else 'non-empty '}list")
    for x in v:
        if not isinstance(x, str) or not x:
            raise TaskError(f"{where}: '{name}' items must be non-empty strings")
    return v


def validate_task(t, path):
    if not isinstance(t, dict):
        raise TaskError(f"{path}: task must be an object")
    _str(t.get("id"), "id", path)
    w = t.get("weight", 1)
    _num(w, "weight", path)
    if w <= 0:
        raise TaskError(f"{path}: weight must be > 0 (got {w})")
    checks = t.get("checks")
    if not isinstance(checks, list) or not checks:
        raise TaskError(f"{path}: 'checks' must be a non-empty list")

    NEED_PATH = {"file_exists", "file_missing", "json_valid", "index_has",
                 "contains", "not_contains", "regex", "min_bytes", "max_bytes",
                 "no_leak", "file_count_max"}
    for i, c in enumerate(checks):
        where = f"{path}: check[{i}]"
        if not isinstance(c, dict):
            raise TaskError(f"{where} must be an object")
        typ = c.get("type")
        if typ not in VALID_CHECK_TYPES:
            raise TaskError(f"{where} unknown type {typ!r}")
        if typ in NEED_PATH:
            _str(c.get("path"), "path", where)
        if typ in {"contains", "not_contains", "index_has"}:
            _str(c.get("value"), "value", where)
        if typ == "regex":
            _str(c.get("pattern"), "pattern", where)
            if "negate" in c and not isinstance(c["negate"], bool):
                raise TaskError(f"{where}: 'negate' must be boolean")
        if typ == "min_bytes":
            _num(c.get("min"), "min", where)
        if typ == "max_bytes":
            _num(c.get("max"), "max", where)
        if typ == "file_count_max":
            _str(c.get("glob", "*"), "glob", where)
            _num(c.get("max"), "max", where)
        if typ == "no_leak":
            _str_list(c.get("patterns"), "patterns", where)
        if typ == "no_leak_bulk":
            _str_list(c.get("paths"), "paths", where)
            _str_list(c.get("patterns"), "patterns", where)
    return t


def load_tasks():
    files = sorted(glob.glob(os.path.join(TASKS_DIR, "*.json")))
    if not files:
        raise TaskError("no task files found — refusing to report a score")
    tasks = []
    for path in files:
        try:
            with open(path, "r", encoding="utf-8") as f:
                t = json.load(f)
        except Exception as e:
            raise TaskError(f"{os.path.basename(path)}: cannot parse JSON ({e})")
        tasks.append(validate_task(t, os.path.basename(path)))
    return tasks


def run_suite(tasks, ctx):
    results = []
    for t in tasks:
        checks = []
        passed = 0
        for c in t.get("checks", []):
            ok, detail = run_check(c, ctx)
            checks.append({"check": c.get("type"), "passed": ok, "detail": detail})
            passed += 1 if ok else 0
        total = len(checks)
        ratio = (passed / total) if total else 0.0
        results.append({
            "id": t["id"],
            "category": t.get("category", "general"),
            "weight": t.get("weight", 1),
            "passed": passed,
            "total": total,
            "ratio": round(ratio, 4),
            "checks": checks,
        })

    wsum = sum(r["weight"] for r in results) or 1
    fitness = sum(r["ratio"] * r["weight"] for r in results) / wsum

    gate_fail = [r["id"] for r in results
                 if r["category"] in HARD_GATE_CATEGORIES and r["ratio"] < 1.0]
    return results, round(fitness, 4), gate_fail


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def save_json(path, data):
    """Atomic JSON write: unique temp file in the same dir + fsync file & dir."""
    d = os.path.dirname(path)
    os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".tmp-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)  # atomic within same filesystem
        try:
            dfd = os.open(d, os.O_RDONLY)
            os.fsync(dfd)
            os.close(dfd)
        except OSError:
            pass  # dir fsync unsupported on some FS (Termux/Android) — best effort
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--accept", action="store_true")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args()

    try:
        tasks = load_tasks()
    except TaskError as e:
        err = {"error": "task-validation-failed", "detail": str(e),
               "fitness": None, "regression": True}
        if args.json:
            print(json.dumps(err, ensure_ascii=False, indent=2))
        else:
            print(f"[FATAL] {e}", file=sys.stderr)
        return 2

    if args.list:
        for t in tasks:
            print(f"{t['id']:22} w={t.get('weight',1)}  {t.get('description','')}")
        return 0

    ctx = {"workspace": WORKSPACE}
    try:
        results, fitness, gate_fail = run_suite(tasks, ctx)
    except Exception as e:
        err = {"error": "suite-crashed", "detail": str(e),
               "fitness": None, "regression": True}
        if args.json:
            print(json.dumps(err, ensure_ascii=False, indent=2))
        else:
            print(f"[FATAL] suite crashed: {e}", file=sys.stderr)
        return 2

    baseline = load_json(BASELINE)
    prev = baseline.get("fitness") if baseline else None
    delta = round(fitness - prev, 4) if prev is not None else None
    regression = bool((delta is not None and delta < -0.001) or gate_fail)

    now = datetime.now(TZ)
    record = {
        "timestamp": now.isoformat(timespec="seconds"),
        "fitness": fitness,
        "previous": prev,
        "delta": delta,
        "regression": regression,
        "hard_gate_fail": gate_fail,
        "tasks": results,
    }

    if not args.no_write:
        fname = now.strftime("%Y%m%d-%H%M%S-") + f"{now.microsecond:06d}" + ".json"
        save_json(os.path.join(ARCHIVE_DIR, fname), record)
        if args.accept or prev is None:
            save_json(BASELINE, {"fitness": fitness, "timestamp": record["timestamp"],
                                 "tasks": results})

    if args.json:
        print(json.dumps(record, ensure_ascii=False, indent=2))
        return 1 if regression else 0

    print(f"\n  EVAL HARNESS  ·  {record['timestamp']}")
    print("  " + "─" * 52)
    for r in results:
        mark = "✅" if r["ratio"] == 1 else ("⚠️ " if r["ratio"] > 0 else "❌")
        print(f"  {mark} {r['id']:22} {r['passed']:>2}/{r['total']:<2}  ({r['ratio']*100:5.1f}%)  w={r['weight']}")
        for c in r["checks"]:
            if not c["passed"]:
                print(f"        ↳ FAIL: {c['detail']}")
    print("  " + "─" * 52)
    line = f"  FITNESS: {fitness*100:.2f}%"
    if delta is not None:
        sign = "▲" if delta > 0 else ("▼" if delta < 0 else "=")
        line += f"   (prev {prev*100:.2f}%  {sign}{abs(delta)*100:.2f}%)"
    if regression:
        line += "   ⚠️ REGRESSION"
    print(line)
    if gate_fail:
        print(f"  🚫 HARD-GATE FAIL: {', '.join(gate_fail)}")
    if args.accept:
        print("  baseline updated ✔")
    print()
    return 1 if regression else 0


if __name__ == "__main__":
    sys.exit(main())
