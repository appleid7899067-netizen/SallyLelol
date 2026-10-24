#!/usr/bin/env bash
# Post-evolution fitness gate (fail-closed).
# Run AFTER an evolution writes files and BEFORE accepting the change.
# Exit code 0 = no regression (safe to keep), 1 = regression OR any failure.
#
# Fail-closed contract: if the runner crashes, emits invalid JSON, or any step
# fails, this script exits 1. Never let an unverifiable run look like a pass.
set -Eeuo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

# Run the eval; --no-write so the gate never mutates baseline/archive.
if ! python3 "$HERE/runner.py" --json --no-write >"$tmp" 2>/dev/null; then
  echo "⚠️  GATE FAIL-CLOSED: runner.py exited non-zero — treating as failure." >&2
  exit 1
fi

# Parse with a strict helper. Any parse error -> exit 1.
if ! eval "$(python3 - "$tmp" <<'PY'
import json, sys
try:
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        d = json.load(f)
    fit = d["fitness"]
    delta = d.get("delta")
    reg = bool(d["regression"])
except Exception as e:
    sys.stderr.write(f"gate: cannot parse runner output: {e}\n")
    sys.exit(1)
print(f"FIT={fit!r} DELTA={delta!r} REG={reg!r}")
PY
)"; then
  echo "⚠️  GATE FAIL-CLOSED: could not parse runner output." >&2
  exit 1
fi

echo "fitness=$FIT delta=${DELTA:-n/a} regression=$REG"

if [ "$REG" = "True" ]; then
  echo "⚠️  REGRESSION detected — review the change or run evolution_undo." >&2
  exit 1
fi
exit 0
