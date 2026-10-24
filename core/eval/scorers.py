"""
Deterministic scorers for the eval harness (hardened).

Each scorer receives (check: dict, ctx: dict) and returns (passed: bool, detail: str).
ctx = {"workspace": <abs path to cow>}

Security contract
-----------------
* Every path is resolved through `_safe_path`, which rejects absolute paths,
  `..` traversal, and any resolved path that escapes the workspace root
  (symlinks included). A rejected path is a FAILED check, never an exception.
* Unknown check types fail closed.
* A broken check never crashes the suite.

Supported check types
---------------------
file_exists   : {"type": "file_exists", "path": "AGENT.md"}
file_missing  : {"type": "file_missing", "path": "tmp/junk.bin"}
contains      : {"type": "contains", "path": "AGENT.md", "value": "สลี่"}
not_contains  : {"type": "not_contains", "path": "MEMORY.md", "value": "ครับ"}
regex         : {"type": "regex", "path": "AGENT.md", "pattern": r"สลี่.*บอส", "negate": false}
file_count_max: {"type": "file_count_max", "path": "memory", "glob": "*.md", "max": 60}
json_valid    : {"type": "json_valid", "path": "system/models.json"}
no_leak       : {"type": "no_leak", "path": "MEMORY.md", "patterns": ["sk-", ...]}
no_leak_bulk  : {"type": "no_leak_bulk", "paths": ["MEMORY.md", "USER.md"], "patterns": [...]}
index_has     : {"type": "index_has", "path": "knowledge/index.md", "value": "sources/"}
min_bytes     : {"type": "min_bytes", "path": "AGENT.md", "min": 800}
max_bytes     : {"type": "max_bytes", "path": "MEMORY.md", "max": 40000}
"""
import glob as _glob
import json
import os
import re


class PathRejected(Exception):
    """Raised when a check path escapes the workspace or is otherwise unsafe."""


def _safe_path(ctx, rel, allow_missing=True):
    """Resolve `rel` under the workspace, refusing escapes.

    Rejects absolute paths and `..` traversal. Resolves symlinks and verifies the
    real path stays inside the real workspace root.
    """
    if not isinstance(rel, str) or not rel:
        raise PathRejected("empty path")
    if os.path.isabs(rel):
        raise PathRejected(f"absolute path refused: {rel}")
    if "\x00" in rel:
        raise PathRejected("NUL byte in path")

    root = os.path.realpath(ctx["workspace"])
    candidate = os.path.join(root, rel)
    real = os.path.realpath(candidate)

    # must stay inside root (root itself equals real for a file check only if rel == ".")
    if real != root and not real.startswith(root + os.sep):
        raise PathRejected(f"path escapes workspace: {rel} -> {real}")
    return candidate


def _read(ctx, rel):
    p = _safe_path(ctx, rel)
    if not os.path.isfile(p):
        return None
    try:
        with open(p, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except Exception:
        return None


def _secret_hits(content, patterns):
    """Return list of (pattern, sample) hits. Supports literal and 're:' prefixes."""
    hits = []
    for p in patterns:
        try:
            if p.startswith("re:"):
                m = re.search(p[3:], content)
                if m:
                    hits.append((p, m.group(0)[:12] + "..."))
            elif p in content:
                idx = content.find(p)
                hits.append((p, content[idx:idx + len(p) + 4]))
        except re.error:
            hits.append((p, "<bad regex>"))
    return hits


def _scorer(check, ctx):
    t = check.get("type")

    if t == "file_exists":
        p = _safe_path(ctx, check["path"])
        ok = os.path.isfile(p)  # must be a regular file, not dir/symlink-to-dir
        return ok, ("found" if ok else "missing") + f": {check['path']}"

    if t == "file_missing":
        p = _safe_path(ctx, check["path"])
        ok = not os.path.exists(p)
        return ok, ("absent" if ok else "STILL PRESENT") + f": {check['path']}"

    if t in ("contains", "not_contains"):
        content = _read(ctx, check["path"])
        if content is None:
            return False, f"file not found: {check['path']}"
        found = check["value"] in content
        if t == "contains":
            return found, f"{'has' if found else 'MISSING'} '{check['value']}' in {check['path']}"
        return (not found), f"{'clean' if not found else 'HAS FORBIDDEN'} '{check['value']}' in {check['path']}"

    if t == "regex":
        content = _read(ctx, check["path"])
        if content is None:
            return False, f"file not found: {check['path']}"
        try:
            m = re.search(check["pattern"], content, re.MULTILINE)
        except re.error as e:
            return False, f"bad regex ({e}): {check['path']}"
        if check.get("negate"):
            return (not m), f"regex {'UNEXPECTEDLY matched' if m else 'clean (no match)'} in {check['path']}"
        return bool(m), f"regex {'matched' if m else 'NO MATCH'} in {check['path']}"

    if t == "json_valid":
        content = _read(ctx, check["path"])
        if content is None:
            return False, f"file not found: {check['path']}"
        try:
            json.loads(content)
            return True, f"valid JSON: {check['path']}"
        except Exception as e:
            return False, f"invalid JSON ({e}): {check['path']}"

    if t == "file_count_max":
        base = _safe_path(ctx, check["path"])
        g = check.get("glob", "*")
        if os.sep in g or ".." in g:
            return False, f"unsafe glob refused: {g}"
        n = len([x for x in _glob.glob(os.path.join(base, g)) if os.path.isfile(x)])
        ok = n <= int(check["max"])
        return ok, f"{n} files (max {check['max']}) in {check['path']}"

    if t == "no_leak":
        content = _read(ctx, check["path"])
        if content is None:
            return False, f"file not found: {check['path']}"
        hits = _secret_hits(content, check.get("patterns", []))
        return (not hits), ("no secret pattern" if not hits else f"LEAK: {[h[0] for h in hits]}")

    if t == "no_leak_bulk":
        bad = []
        for rel in check.get("paths", []):
            content = _read(ctx, rel)
            if content is None:
                bad.append((rel, "MISSING"))
                continue
            hits = _secret_hits(content, check.get("patterns", []))
            if hits:
                bad.append((rel, [h[0] for h in hits]))
        return (not bad), ("no secret pattern in any file" if not bad else f"LEAK: {bad}")

    if t == "index_has":
        content = _read(ctx, check["path"])
        if content is None:
            return False, f"file not found: {check['path']}"
        found = check["value"] in content
        return found, f"{'indexed' if found else 'NOT INDEXED'}: {check['value']}"

    if t == "min_bytes":
        p = _safe_path(ctx, check["path"])
        if not os.path.isfile(p):
            return False, f"file not found: {check['path']}"
        n = os.path.getsize(p)
        ok = n >= int(check["min"])
        return ok, f"{n} bytes (min {check['min']}): {check['path']}"

    if t == "max_bytes":
        p = _safe_path(ctx, check["path"])
        if not os.path.isfile(p):
            return False, f"file not found: {check['path']}"
        n = os.path.getsize(p)
        ok = n <= int(check["max"])
        return ok, f"{n} bytes (max {check['max']}): {check['path']}"

    return False, f"unknown check type: {t}"


def run_check(check, ctx):
    try:
        return _scorer(check, ctx)
    except PathRejected as e:
        return False, f"path refused: {e}"
    except KeyError as e:
        return False, f"missing field {e} in check {check.get('type')}"
    except Exception as e:  # defensive: a broken check must never crash the suite
        return False, f"scorer error: {e}"
