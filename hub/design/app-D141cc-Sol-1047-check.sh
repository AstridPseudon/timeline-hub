#!/usr/bin/env bash
set -euo pipefail

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
EVIDENCE=$(CDPATH= cd -- "$ROOT/.." && pwd)
RUN_ROOT="$EVIDENCE/private-controls/runs/$(date -u +%Y%m%dT%H%M%S)-$$"
mkdir -p "$RUN_ROOT"
export PYTHONPYCACHEPREFIX="$RUN_ROOT/pycache"
export PYTHONDONTWRITEBYTECODE=1
export GIT_OPTIONAL_LOCKS=0

printf '%s\n' 'AST, private-cache compile, bash syntax, native control syntax, Ruff F'
python3 - "$ROOT/controller.py" "$EVIDENCE/private-controls/controls.py" "$EVIDENCE/private-controls/verify_history.py" <<'PY'
import ast
from pathlib import Path
import py_compile
import sys

for name in sys.argv[1:]:
    ast.parse(Path(name).read_text())
    py_compile.compile(name, doraise=True)
PY
bash -n "$0"
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --check "$EVIDENCE/private-controls/native.mjs"
ruff check --cache-dir "$RUN_ROOT/ruff-cache" --select F "$ROOT/controller.py" "$EVIDENCE/private-controls/controls.py" "$EVIDENCE/private-controls/verify_history.py"

printf '%s\n' 'Actual unchanged builder: pure bindings, intercepted native submit, custody controls, outside source conservation'
python3 "$EVIDENCE/private-controls/controls.py" "$RUN_ROOT/fixtures" | tee "$RUN_ROOT/summary.json"
python3 "$EVIDENCE/private-controls/verify_history.py" | tee "$RUN_ROOT/historical-summary.json"
printf '%s\n' "PASS: same-script source-only controls; evidence at $RUN_ROOT"
