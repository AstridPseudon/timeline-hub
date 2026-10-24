# D73 exact-submit request recipe (no body request is made by this worker)

Run this recipe only after the reviewed D71 Agent source and matching Runtime
source are in the four integration homes. It captures the tuple once, asks the
existing checkout service for each exact SHA, and waits for each normal receipt
before rendering the two owned rows from `tests/suites.conf.candidate`. The
rendered rows are the only service registration input; do not edit the central
registry directly. Keep the UTC/0600 CAS installer and its outside-row byte
comparison from the existing service route.

```bash
set -euo pipefail
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
WORKER=$ORCH/workers/agt-P4-D73-pinned-1711
EVIDENCE=$WORKER/evidence/d73-exact-submit
mkdir -p "$EVIDENCE"

# Capture the four names before any checkout request. These values are never
# recomputed during service execution.
AGENT_SHA=$(git -C /home/user/work/agent rev-parse HEAD)
RUNTIME_SHA=$(git -C /home/user/work/runtime rev-parse HEAD)
APP_SHA=$(git -C /home/user/work/app rev-parse HEAD)
COMPOSITION_SHA=$(git -C /home/user/work/composition rev-parse HEAD)
for item in "$AGENT_SHA" "$RUNTIME_SHA" "$APP_SHA" "$COMPOSITION_SHA"; do
  [[ "$item" =~ ^[0-9a-f]{40}$ ]]
done

# Existing normal request-checkout/receipt route. Do not substitute a current
# home, a recycled worktree, or a copied source tree for any receipt path.
"$ORCH/bin/request-checkout" agent "$AGENT_SHA" 'D73 P4 exact submit Agent pin'
"$ORCH/bin/request-checkout" runtime "$RUNTIME_SHA" 'D73 P4 exact submit Runtime pin'
"$ORCH/bin/request-checkout" app "$APP_SHA" 'D73 P4 exact submit App pin'
"$ORCH/bin/request-checkout" composition "$COMPOSITION_SHA" 'D73 P4 exact submit Composition pin'

receipt_path() {
  local repo=$1 sha=$2 receipt="$ORCH/queue/done/checkout-$1-$2"
  while test ! -s "$receipt"; do sleep 1; done
  test "$(awk '/^created / { print $2; exit }' "$receipt")" != ""
  printf '%s\n' "$(awk '/^created / { print $2; exit }' "$receipt")"
}
AGENT_PATH=$(receipt_path agent "$AGENT_SHA")
RUNTIME_PATH=$(receipt_path runtime "$RUNTIME_SHA")
APP_PATH=$(receipt_path app "$APP_SHA")
COMPOSITION_PATH=$(receipt_path composition "$COMPOSITION_SHA")
for pair in "agent:$AGENT_PATH:$AGENT_SHA" "runtime:$RUNTIME_PATH:$RUNTIME_SHA" "app:$APP_PATH:$APP_SHA" "composition:$COMPOSITION_PATH:$COMPOSITION_SHA"; do
  IFS=: read -r name path sha <<<"$pair"
  test "$(git -C "$path" rev-parse HEAD)" = "$sha"
  test -z "$(git -C "$path" status --porcelain --untracked-files=all)"
done

PYTHON=/home/user/work/venv-agent/bin/python
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
PROFILE=/home/user/work/runtimes/agent-remotion-v3-819acf-1110
SCHEMA=/home/user/work/venv-agent/lib/python3.13/site-packages
ARCHIVE=$($PYTHON -P - "$PROFILE" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
print((p / json.loads((p / 'package.json').read_text())['dependencies']['@banodoco/timeline-composition'].removeprefix('file:')).resolve())
PY
)
cat > "$EVIDENCE/tuple.env" <<EOF
format=p4-d73-v1
agent_sha=$AGENT_SHA
agent_tree=$(git -C "$AGENT_PATH" rev-parse HEAD^{tree})
agent_parents=$(git -C "$AGENT_PATH" rev-list --parents -n 1 HEAD)
agent_path=$AGENT_PATH
runtime_sha=$RUNTIME_SHA
runtime_tree=$(git -C "$RUNTIME_PATH" rev-parse HEAD^{tree})
runtime_path=$RUNTIME_PATH
app_sha=$APP_SHA
app_tree=$(git -C "$APP_PATH" rev-parse HEAD^{tree})
app_path=$APP_PATH
composition_sha=$COMPOSITION_SHA
composition_tree=$(git -C "$COMPOSITION_PATH" rev-parse HEAD^{tree})
composition_path=$COMPOSITION_PATH
python=$PYTHON
node=$NODE
profile=$PROFILE
schema=$SCHEMA
node_version=$($NODE --version)
profile_lock_sha=$(sha256sum "$PROFILE/package-lock.json" | awk '{print $1}')
profile_archive_sha=$(sha256sum "$ARCHIVE" | awk '{print $1}')
profile_registry_sha=$(sha256sum "$PROFILE/.astrid-registry-state.json" | awk '{print $1}')
composition_version=$(python3 -c 'import json; print(json.load(open("'"$PROFILE"'/node_modules/@banodoco/timeline-composition/package.json"))["version"])')
original_p4_test_hash=$(sha256sum "$AGENT_PATH/tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py" "$AGENT_PATH/tests/editing_conformance/test_p4_ten_note_v2_runtime.py" "$AGENT_PATH/tests/editing_conformance/test_p4_note_rerun_v2_runtime.py" | sha256sum | awk '{print $1}')
service_versions=agent:$AGENT_SHA,runtime:$RUNTIME_SHA,node:$($NODE --version),composition:$composition_version
junit_paths=$EVIDENCE/p4-current-single.xml,$EVIDENCE/p4-current-becfe-http-3legs.xml
EOF
chmod 600 "$EVIDENCE/tuple.env"

# Render only the two owned rows. The renderer replaces every token and
# rejects unresolved tokens; the output is a durable candidate, not a worktree.
python3 - "$EVIDENCE/tuple.env" tests/suites.conf.candidate "$EVIDENCE/suites.conf.d73" <<'PY'
import sys
from pathlib import Path
values = {}
for line in Path(sys.argv[1]).read_text().splitlines():
    if line and not line.startswith('#') and '=' in line:
        key, value = line.split('=', 1)
        values['__P4_D73_' + key.upper() + '__'] = value
evidence = Path(sys.argv[3]).parent
values.update({
    '__P4_D73_MANIFEST__': str(Path(sys.argv[1]).resolve()),
    '__P4_D73_EVIDENCE__': str(evidence.resolve()),
    '__P4_D73_REQUEST_ID_3LEGS__': 'p4-current-becfe-http-3legs',
    '__P4_D73_REQUEST_ID_SINGLE__': 'p4-current-single',
})
text = Path(sys.argv[2]).read_text()
for key, value in values.items():
    text = text.replace(key, value)
if '__P4_D73_' in text:
    raise SystemExit('unresolved D73 render token')
Path(sys.argv[3]).write_text(text)
PY
bash -n "$EVIDENCE/suites.conf.d73"

# Real-service dry preflight only: the stub must be reached once and its
# nonzero exit must be returned unchanged. This is not a pytest/body request.
STUB=$EVIDENCE/harmless-stub.sh
COUNT=$EVIDENCE/harmless-stub.count
printf '#!/bin/sh\nprintf "called\\n" >> "$COUNT"\nexit 17\n' > "$STUB"
chmod 700 "$STUB"
set +e
P4_D73_EVIDENCE="$EVIDENCE" P4_D73_REQUEST_ID=d73-dry-preflight \
  "$AGENT_PATH/tools/p4-d73-pinned-launch.sh" "$EVIDENCE/tuple.env" dry -- "$STUB"
DRY_RC=$?
set -e
test "$DRY_RC" = 17
test "$(wc -l < "$COUNT")" = 1

# Use the existing guarded CAS+UTC/0600 service-registration route to replace
# only p4-current-single and p4-current-becfe-http-3legs. Record its request
# ID, manifests, service log, JUnit, and exit under this evidence directory.
# The exact body request is supplied by the manager after this recipe is
# reviewed; this worker intentionally makes no body request.
# Once the candidate is installed, these are the exact two body requests; keep
# the returned IDs and wait-test logs beside the tuple manifest.
R_SINGLE=$("$ORCH/bin/request-test" integration:agent p4-current-single)
printf '%s\n' "$R_SINGLE" > "$EVIDENCE/request-p4-current-single.id"
R_THREE=$("$ORCH/bin/request-test" integration:agent p4-current-becfe-http-3legs)
printf '%s\n' "$R_THREE" > "$EVIDENCE/request-p4-current-becfe-http-3legs.id"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R_SINGLE" > "$EVIDENCE/p4-current-single.wait.log"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R_THREE" > "$EVIDENCE/p4-current-becfe-http-3legs.wait.log"
```
