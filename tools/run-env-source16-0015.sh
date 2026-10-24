#!/usr/bin/env bash
set -Eeuo pipefail

ROOT=$(pwd -P)
PYTHON=/home/user/work/venv-agent/bin/python
RUNTIME=/home/user/work/wt/rt-pin-8ea0766f
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
RUNTIME_SITE=/home/user/work/bench-store/entries/child-c886d448c07fe72421bfbc708db0dc9399c2833a66b7dadc67625a3df0d4da0e/lib/python3.13/site-packages

export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:"$RUNTIME"
export ASTRID_HOST_EXECUTION_PROFILE=source
export ASTRID_RUNTIME_CHECKOUT="$RUNTIME"
export ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME"
export PATH="$(dirname "$NODE"):/usr/bin:/bin"

# These source fixtures own their fake host/registry authority. Do not let a
# managed Remotion profile turn them into installed/global registry cases.
unset ASTRID_REMOTION_PROJECT_DIR ASTRID_NODE_EXECUTABLE ASTRID_TEST_NODE_MODULES
unset ASTRID_TIMELINE_SCHEMA_PYTHONPATH ASTRID_REMOTION_VALIDATION_PATH
unset ASTRID_REMOTION_VALIDATION_SHA256 ASTRID_REMOTION_VALIDATION_LAUNCH
unset ASTRID_REMOTION_VALIDATION_ROLE

TEST_FILES=(
  tests/core/execution/test_generic_host_actions_v3.py
  tests/sdk/test_host_bootstrap_source_identity.py
)
EXPECTED_TEST_SHA256=(
  32e8958cce8bbcae19f1771f131e043171d0ac5f62732bfdefe8a1dbcd54708d
  b36abb16207845a52411eca1ecf4799d0cb3652dcbc53217b0f1167d8392270b
)
NODEIDS=(
  tests/core/execution/test_generic_host_actions_v3.py::test_private_imports_add_no_repository_or_pack_pythonpath
  tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_passes_inventory_identity_and_restarts_on_change
  tests/sdk/test_host_bootstrap_source_identity.py::test_bootstrap_stops_on_correlated_terminal_registration_failure
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_birth-False-1-None]'
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_instance-False-1-None]'
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_pid-False-1-None]'
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-foreign_source-False-1-None]'
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-1-terminal-False-1-None]'
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-25-ready-True-25-None]'
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-400-ready-True-400-400]'
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-exit-False-1-30]'
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-exit-False-1-None]'
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-ready-False-120-None]'
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[120-None-ready-False-150.3-30]'
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[None-25-ready-True-25-None]'
  'tests/sdk/test_host_bootstrap_source_identity.py::test_startup_budget_polling_preserves_identity_and_original_cleanup[None-None-ready-False-300.0-None]'
)

printf '%s\n' 'SOURCE16_PREFLIGHT_BEGIN'
printf 'ROOT=%s\nPYTHON=%s\nRUNTIME=%s\nRUNTIME_SITE=%s\nNODE=%s\nPROFILE=%s\nTMPDIR=%s\n' \
  "$ROOT" "$PYTHON" "$RUNTIME" "$RUNTIME_SITE" "$NODE" "$PROFILE" "${TMPDIR:-unset}"
test "$(pwd -P)" = "$ROOT"
test -x "$PYTHON"
test -x "$NODE"
test -d "$RUNTIME/runtime_protocol"
test -f "$RUNTIME_SITE/runtime_protocol/__init__.py"
test -d "$PROFILE/node_modules"
test "$("$NODE" --version)" = v20.19.4
test "$(git rev-parse HEAD^)" = c36ca8c94b695b0e25b7d42c89f194661f187423
test "$(git -C "$RUNTIME" rev-parse HEAD)" = 8ea0766f5e9fb23cea26c7398770a8aaac06b258
test "$(git -C "$RUNTIME" rev-parse HEAD^{tree})" = 6047ac3033c3594b8f83db3afd8bb2c47cafa6d6
test -z "$(git -C "$RUNTIME" status --porcelain)"

allowed_status=$(git status --porcelain | grep -Ev '^\?\? tools/run-env-source16-0015\.sh$' || true)
test -z "$allowed_status"

for index in "${!TEST_FILES[@]}"; do
  file=${TEST_FILES[$index]}
  test "$(sha256sum "$file" | awk '{print $1}')" = "${EXPECTED_TEST_SHA256[$index]}"
  printf 'TEST_BODY_SHA256 %s %s\n' "$file" "${EXPECTED_TEST_SHA256[$index]}"
done

"$PYTHON" -P - "$ROOT" "$RUNTIME" "$NODE" <<'PY'
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

root, runtime, node = map(Path, sys.argv[1:])
import astrid
import astrid_runtime_client
import banodoco_timeline_schema
import runtime_protocol

origins = {
    "astrid": str(Path(astrid.__file__).resolve()),
    "astrid_runtime_client": str(Path(astrid_runtime_client.__file__).resolve()),
    "banodoco_timeline_schema": str(Path(banodoco_timeline_schema.__file__).resolve()),
    "runtime_protocol": str(Path(runtime_protocol.__file__).resolve()),
}
assert origins["astrid"] == str(root / "astrid/__init__.py")
assert origins["astrid_runtime_client"] == str(root / "astrid_runtime_client/__init__.py")
assert origins["runtime_protocol"] == str(runtime / "runtime_protocol/__init__.py")
assert origins["banodoco_timeline_schema"].startswith("/home/user/work/venv-agent/")
assert os.environ["PYTHONPATH"] == f".:{runtime}"
assert os.environ["ASTRID_HOST_EXECUTION_PROFILE"] == "source"
assert os.environ["ASTRID_RUNTIME_CHECKOUT"] == str(runtime)
assert os.environ["ASTRID_RUNTIME_SOURCE_ROOT"] == str(runtime)
for name in (
    "ASTRID_REMOTION_PROJECT_DIR", "ASTRID_NODE_EXECUTABLE", "ASTRID_TEST_NODE_MODULES",
    "ASTRID_TIMELINE_SCHEMA_PYTHONPATH", "ASTRID_REMOTION_VALIDATION_PATH",
    "ASTRID_REMOTION_VALIDATION_SHA256", "ASTRID_REMOTION_VALIDATION_LAUNCH",
    "ASTRID_REMOTION_VALIDATION_ROLE",
):
    assert name not in os.environ, name
assert subprocess.run([str(node), "--version"], check=True, capture_output=True, text=True).stdout.strip() == "v20.19.4"
print("MODULE_ORIGINS", json.dumps(origins, sort_keys=True))
print("SYS_PATH", json.dumps([str(item) for item in sys.path]))
print("ENV_BINDINGS", json.dumps({name: os.environ.get(name) for name in (
    "PYTHONPATH", "ASTRID_HOST_EXECUTION_PROFILE", "ASTRID_RUNTIME_CHECKOUT",
    "ASTRID_RUNTIME_SOURCE_ROOT", "ASTRID_REMOTION_PROJECT_DIR", "ASTRID_NODE_EXECUTABLE",
    "ASTRID_TEST_NODE_MODULES", "ASTRID_TIMELINE_SCHEMA_PYTHONPATH",
)}, sort_keys=True))
print("RUNTIME_PROTOCOL_SHA256", hashlib.sha256((runtime / "runtime_protocol/__init__.py").read_bytes()).hexdigest())
print("NODE_VERSION", subprocess.run([str(node), "--version"], check=True, capture_output=True, text=True).stdout.strip())
PY

profile_manifest() {
  "$PYTHON" -P - "$PROFILE" <<'PY'
import hashlib
import sys
from pathlib import Path

profile = Path(sys.argv[1])
digest = hashlib.sha256()
count = 0
for path in sorted(item for item in profile.rglob("*") if item.is_file()):
    relative = path.relative_to(profile).as_posix().encode()
    digest.update(relative + b"\0")
    digest.update(hashlib.sha256(path.read_bytes()).digest())
    count += 1
print(f"PROFILE_FILE_INVENTORY count={count} sha256={digest.hexdigest()}")
for name in ("package.json", "package-lock.json", ".astrid-registry-state.json"):
    path = profile / name
    if path.is_file():
        print(f"PROFILE_REGISTRY_FILE {name} {hashlib.sha256(path.read_bytes()).hexdigest()}")
PY
}

printf '%s\n' 'SOURCE16_CUSTODY_BEFORE'
git status --short
printf 'SOURCE_HEAD %s\nSOURCE_TREE %s\nRUNTIME_HEAD %s\nRUNTIME_TREE %s\n' \
  "$(git rev-parse HEAD)" "$(git rev-parse HEAD^{tree})" \
  "$(git -C "$RUNTIME" rev-parse HEAD)" "$(git -C "$RUNTIME" rev-parse HEAD^{tree})"
printf 'SOURCE_PARENT %s\n' "$(git rev-parse HEAD^)"
profile_manifest

printf '%s\n' 'SOURCE16_NODEIDS_BEGIN'
printf 'NODE_COUNT=%s\n' "${#NODEIDS[@]}"
printf 'NODE_ID %s\n' "${NODEIDS[@]}"
printf '%s\n' 'SOURCE16_NODEIDS_END'

printf '%s\n' 'SOURCE16_PYTEST_BEGIN'
set +e
LOG=$(mktemp "${TMPDIR:-/tmp}/astrid-env-source16-0015.XXXXXX.log")
printf '%s\n' 'SOURCE16_PRIVATE_CASE_BEGIN' >>"$LOG"
printf 'PYTHONPATH=%s\n' ".:$RUNTIME:$RUNTIME_SITE" >>"$LOG"
env PYTHONPATH=".:$RUNTIME:$RUNTIME_SITE" "$PYTHON" -P -m pytest -vv -rA -o addopts= -p no:cacheprovider "${NODEIDS[0]}" >>"$LOG" 2>&1
private_status=$?
printf 'SOURCE16_PRIVATE_CASE_EXIT=%s\n' "$private_status" >>"$LOG"
printf '%s\n' 'SOURCE16_SOURCE_CASE_BEGIN' >>"$LOG"
printf 'PYTHONPATH=%s\n' "$PYTHONPATH" >>"$LOG"
"$PYTHON" -P -m pytest -vv -rA -o addopts= -p no:cacheprovider "${NODEIDS[@]:1}" >>"$LOG" 2>&1
source_status=$?
printf 'SOURCE16_SOURCE_CASE_EXIT=%s\n' "$source_status" >>"$LOG"
status=$(( private_status || source_status ))
cat "$LOG"
printf 'SOURCE16_PYTEST_LOG=%s\nSOURCE16_PYTEST_EXIT=%s\n' "$LOG" "$status"
set -e

printf '%s\n' 'SOURCE16_CUSTODY_AFTER'
git status --short
printf 'SOURCE_HEAD %s\nSOURCE_TREE %s\nRUNTIME_HEAD %s\nRUNTIME_TREE %s\n' \
  "$(git rev-parse HEAD)" "$(git rev-parse HEAD^{tree})" \
  "$(git -C "$RUNTIME" rev-parse HEAD)" "$(git -C "$RUNTIME" rev-parse HEAD^{tree})"
printf 'SOURCE_PARENT %s\n' "$(git rev-parse HEAD^)"
profile_manifest
"$PYTHON" -P - "$ROOT" "$RUNTIME" <<'PY'
import json
import os
import sys
from pathlib import Path

root, runtime = map(Path, sys.argv[1:])
import astrid
import astrid_runtime_client
import banodoco_timeline_schema
import runtime_protocol
origins = {
    "astrid": str(Path(astrid.__file__).resolve()),
    "astrid_runtime_client": str(Path(astrid_runtime_client.__file__).resolve()),
    "banodoco_timeline_schema": str(Path(banodoco_timeline_schema.__file__).resolve()),
    "runtime_protocol": str(Path(runtime_protocol.__file__).resolve()),
}
assert origins["astrid"] == str(root / "astrid/__init__.py")
assert origins["astrid_runtime_client"] == str(root / "astrid_runtime_client/__init__.py")
assert origins["runtime_protocol"] == str(runtime / "runtime_protocol/__init__.py")
assert origins["banodoco_timeline_schema"].startswith("/home/user/work/venv-agent/")
print("MODULE_ORIGINS", json.dumps(origins, sort_keys=True))
print("ENV_BINDINGS", json.dumps({name: os.environ.get(name) for name in (
    "PYTHONPATH", "ASTRID_HOST_EXECUTION_PROFILE", "ASTRID_RUNTIME_CHECKOUT",
    "ASTRID_RUNTIME_SOURCE_ROOT", "ASTRID_REMOTION_PROJECT_DIR", "ASTRID_NODE_EXECUTABLE",
    "ASTRID_TEST_NODE_MODULES", "ASTRID_TIMELINE_SCHEMA_PYTHONPATH",
)}, sort_keys=True))
PY
git diff --check
allowed_status=$(git status --porcelain | grep -Ev '^\?\? tools/run-env-source16-0015\.sh$' || true)
test -z "$allowed_status"
exit "$status"
