# Commands and central result

```sh
/home/user/work/venv-agent/bin/python -B \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-root-scene-six-clean-terminal/run-integration-clean.py \
  --preflight
# PASS; preflight-local.json records the exact source origins and tuple.

# Private cleanup verification, after preflight:
/home/user/work/venv-agent/bin/python -B - <<'PY'
import importlib.util
from pathlib import Path
worker = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-root-scene-six-clean-terminal')
spec = importlib.util.spec_from_file_location('owned_wrapper', worker / 'run-integration-clean.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
assert module.cleanup_stage() is True
assert not module.STAGE.exists()
print('private cleanup helper: PASS')
PY
# PASS; OWN stage absent.

R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  vw-m3-root-scene-six-clean-terminal \
  integration-viewing-root-scene-six-clean-terminal --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
# PASS; test ID: vw-m3-root-scene-six-clean-terminal-integration-viewing-root-scene-six-clean-terminal-1020161758-7407
```

Central result log:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-root-scene-six-clean-terminal-integration-viewing-root-scene-six-clean-terminal-1020161758-7407/log.txt`

Result summary:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-root-scene-six-clean-terminal-integration-viewing-root-scene-six-clean-terminal-1020161758-7407/summary`
