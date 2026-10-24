#!/usr/bin/env python3
"""Night Watchman: read-only security/junk/process scanner."""
from __future__ import annotations
import argparse, datetime as dt, os, re, stat, subprocess
from pathlib import Path
from typing import List, Dict

SECRET_KEYS = re.compile(r"(?i)(api[_-]?key|token|password|secret|private[_-]?key|credential)")
SECRET_VALUE = re.compile(r"(?i)(api[_-]?key|token|password|secret|private[_-]?key|credential)\s*[:=]\s*(['\"]?)[^\s,'\"}]+")
SUSPICIOUS_PROC = re.compile(r"(?i)(curl|wget|nc\b|ncat|netcat|socat|base64\s+-d|/dev/tcp|rm\s+-rf|chmod\s+777|python.*-c|perl.*-e|bash\s+-c)")
JUNK_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "node_modules", ".DS_Store"}
BACKUP_SUFFIXES = (".bak", ".bak2", ".tmp", ".swp", ".orig", ".old")

def run(argv: List[str], timeout: int = 8) -> str:
    try:
        p = subprocess.run(argv, capture_output=True, text=True, timeout=timeout, check=False)
        return (p.stdout + p.stderr).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        return f"unavailable: {type(exc).__name__}"

def mask(text: str) -> str:
    text = SECRET_VALUE.sub(lambda m: f"{m.group(1)}={m.group(2)}[REDACTED]", text)
    text = re.sub(r"(?i)(sk-[A-Za-z0-9_-]{8,}|AIza[A-Za-z0-9_-]{12,}|gh[pousr]_[A-Za-z0-9_]{10,})", "[REDACTED_TOKEN]", text)
    return text[:500]

def human_size(n: int) -> str:
    for unit in ("B", "KiB", "MiB", "GiB"):
        if n < 1024 or unit == "GiB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024
    return str(n)

def safe_rel(path: Path, root: Path) -> str:
    try: return str(path.resolve().relative_to(root.resolve()))
    except ValueError: return str(path)

def findings_security(root: Path) -> List[Dict[str, str]]:
    out = []
    tracked = run(["git", "-C", str(root), "ls-files"]).splitlines()
    secret_like = [p for p in tracked if SECRET_KEYS.search(Path(p).name) or Path(p).name in {".preview_secret", "config.json", "config.json.bak"}]
    if secret_like:
        out.append({"severity":"HIGH", "title":"Tracked or repository-local secret-like files", "evidence":", ".join(mask(x) for x in secret_like[:20]), "options":"Rotate exposed credentials; remove them from history; use environment/secret storage; add CI secret scanning."})
    public = run(["ss", "-lntup"]) or run(["netstat", "-lntup"])
    public_lines = [x for x in public.splitlines() if "0.0.0.0:" in x or "[::]:" in x]
    if public_lines:
        out.append({"severity":"MEDIUM", "title":"Services listening on all interfaces", "evidence":mask("; ".join(public_lines[:10])), "options":"Bind to loopback; place behind authenticated reverse proxy; restrict firewall exposure; verify every listener's owner."})
    for p in [root, Path.home()]:
        try:
            mode = stat.S_IMODE(p.stat().st_mode)
            if mode & stat.S_IWOTH:
                out.append({"severity":"HIGH", "title":"World-writable directory", "evidence":f"{p} mode={oct(mode)}", "options":"Restrict permissions; move runtime state to a private directory; audit files created there before changing mode."})
        except OSError: pass
    return out

def findings_junk(root: Path) -> List[Dict[str, str]]:
    out, counts, backup, large = [], {name:0 for name in JUNK_NAMES}, [], []
    try:
        for p in root.rglob("*"):
            if any(part in {".git", ".venv", "node_modules"} for part in p.parts): continue
            try:
                if p.is_dir() and p.name in counts: counts[p.name] += 1
                elif p.is_file():
                    if p.name.endswith(BACKUP_SUFFIXES): backup.append(safe_rel(p, root))
                    size = p.stat().st_size
                    if size >= 50 * 1024 * 1024: large.append((safe_rel(p, root), size))
            except OSError: continue
    except OSError as exc:
        out.append({"severity":"LOW", "title":"Partial junk scan", "evidence":type(exc).__name__, "options":"Review filesystem access and rerun manually; no automatic cleanup is performed."})
    existing = [f"{k}={v}" for k,v in counts.items() if v]
    if existing: out.append({"severity":"LOW", "title":"Generated cache directories", "evidence":", ".join(existing), "options":"Review whether each cache is disposable; add safe paths to ignore rules; remove only after human confirmation."})
    if backup: out.append({"severity":"MEDIUM", "title":"Backup/swap artifacts", "evidence":", ".join(backup[:30]), "options":"Classify before deletion; move sensitive backups outside the repository; add retention policy and ignore rules."})
    if large: out.append({"severity":"MEDIUM", "title":"Large files/log artifacts", "evidence":", ".join(f"{p} ({human_size(s)})" for p,s in large[:20]), "options":"Archive or rotate after review; configure log retention; do not delete evidence blindly."})
    return out

def findings_processes() -> List[Dict[str, str]]:
    out = []
    ps = run(["ps", "-eo", "pid=,ppid=,user=,lstart=,stat=,args="])
    # The scanner's own interpreter/shell command can match broad patterns such as
    # ``python -c`` or ``bash -c``. Exclude only this run, never other processes.
    self_markers = ("night_watchman.py", "skills/night-watchman")
    suspicious = [
        line for line in ps.splitlines()
        if SUSPICIOUS_PROC.search(line)
        and not any(marker in line for marker in self_markers)
    ]
    zombies = [line for line in ps.splitlines() if re.search(r"\bZ\b", line)]
    if suspicious: out.append({"severity":"HIGH", "title":"Processes matching suspicious command patterns", "evidence":"\n".join(mask(x) for x in suspicious[:20]), "options":"Identify owner and parent; inspect executable and network activity; isolate/stop only with explicit approval."})
    if zombies: out.append({"severity":"LOW", "title":"Zombie processes", "evidence":"\n".join(mask(x) for x in zombies[:20]), "options":"Find the parent process; fix child reaping; restart only after impact review."})
    deleted = run(["sh", "-c", "for f in /proc/[0-9]*/exe; do t=$(readlink \"$f\" 2>/dev/null); case \"$t\" in *' (deleted)') echo \"$f $t\";; esac; done"])
    if deleted: out.append({"severity":"HIGH", "title":"Processes whose executable is deleted", "evidence":mask(deleted[:2000]), "options":"Record PID/owner and inspect before restart; determine whether it is an expected upgrade or persistence indicator."})
    return out

def section(title: str, items: List[Dict[str, str]]) -> str:
    lines = [f"## {title}"]
    if not items: return "\n".join(lines + ["\n✅ ไม่พบประเด็นจากการตรวจหมวดนี้ (ไม่ได้แปลว่าปลอดภัยสมบูรณ์)"])
    for i,item in enumerate(items,1):
        lines += [f"\n### {i}. [{item['severity']}] {item['title']}", f"- **หลักฐาน:** `{item['evidence']}`", f"- **ทางเลือก:** {item['options']}"]
    return "\n".join(lines)

def main() -> int:
    ap = argparse.ArgumentParser(description="Read-only Night Watchman scanner")
    ap.add_argument("--project", default=os.getcwd()); ap.add_argument("--output", default="knowledge/security-report.md")
    args = ap.parse_args(); root = Path(args.project).expanduser().resolve(); output = Path(args.output).expanduser().resolve()
    started = dt.datetime.now(dt.timezone.utc).astimezone().isoformat(timespec="seconds")
    sec, junk, proc = findings_security(root), findings_junk(root), findings_processes()
    report = f"""# Night Watchman Security Report

- **สแกนเมื่อ:** {started}
- **ขอบเขต:** `{root}` และ process/listener ที่ผู้ใช้ปัจจุบันอ่านได้
- **โหมด:** READ-ONLY; เขียนเฉพาะไฟล์รายงานนี้
- **ข้อจำกัด:** ไม่ใช่ antivirus/forensic proof; process และ network เปลี่ยนแปลงได้ตลอดเวลา; ค่าลับถูก mask

## Executive Summary

- Security findings: **{len(sec)}**
- Junk/artifact findings: **{len(junk)}**
- Process findings: **{len(proc)}**

{section('Security', sec)}

{section('Junk / Artifacts', junk)}

{section('Unusual Processes', proc)}

## วิธีตรวจโดยย่อ

- Git-tracked names, permission metadata, listening sockets (`ss`/`netstat`)
- Cache/backup/large-file inventory โดยไม่อ่านเนื้อหาเพื่อ cleanup
- Process table และ deleted executables ผ่าน `/proc`
- ไม่มีการแก้ระบบ, ลบไฟล์, kill process หรือ rotate secret

## ข้อเสนอแนะรวม

1. ตรวจสอบหลักฐานแต่ละรายการโดยมนุษย์ก่อนดำเนินการ
2. เลือกทางเลือกที่กระทบน้อยที่สุดและทำ backup ก่อนแก้จริง
3. แยก incident response ออกจาก cleanup; อย่าลบหลักฐานก่อนเก็บข้อมูล
"""
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text(report, encoding="utf-8")
    print(f"Wrote read-only report: {output}"); return 0

if __name__ == "__main__": raise SystemExit(main())
