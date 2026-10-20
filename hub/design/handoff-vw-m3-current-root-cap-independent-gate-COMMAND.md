# Independent gate commands

```sh
D=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design
P=$D/handoff-vw-m3-current-root-cap-three-stills-prep-
PY=/home/user/work/venv-agent/bin/python
OWN=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep

$PY -B - <<'PY'
import ast
from pathlib import Path
p = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design')
base = 'handoff-vw-m3-current-root-cap-three-stills-prep-'
for name in ('controller.py', 'replay.py', 'offline-checks.py'):
    ast.parse((p / (base + name)).read_text(), filename=name)
print('PASS: 3 Python files AST parsed')
PY
$OWN/node --check ${P}render.mjs
$OWN/node --check ${P}resolve.mjs
$PY -B ${P}controller.py preflight
$PY -B ${P}offline-checks.py
```

No capture command is included here. The manager-only capture command remains the exact literal command in the frozen preparation `COMMAND.md` and is reproduced in the independent report.
