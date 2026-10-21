#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

# One central, helper-only readiness diagnostic. The central test service runs
# this from its snapshot; all generated evidence therefore stays in that
# throwaway snapshot and disappears with it.
worker=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
node=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
floor=10737418240

free_bytes() { df -B1 --output=avail /home/user/work | tail -1 | tr -d ' '; }

before=$(free_bytes)
tracked_bytes=$(git -C "$worker/../.." ls-files -z | xargs -0 -r stat -c '%s' | awk '{sum += $1} END {print sum + 0}')
snapshot_bytes=$((tracked_bytes + 1048576))
stage_bytes=1048576
realm_bytes=67108864
forecast=$((snapshot_bytes + stage_bytes + realm_bytes))
printf 'allocation-forecast central-snapshot=%sB stage-links-and-metadata=%sB empty-realm-helper-reserve=%sB total=%sB free=%sB floor=%sB\n' \
  "$snapshot_bytes" "$stage_bytes" "$realm_bytes" "$forecast" "$before" "$floor"
test "$((before - forecast))" -ge "$floor"

test "$(realpath "$worker")" = "$worker"
bash -n "$worker/COMMAND"
bash -n "$worker/preflight.sh"
"$node" --check "$worker/prepare.mjs"
"$node" --check "$worker/issue.mjs"
"$node" --check "$worker/dist-availability.mjs"
printf 'static-checks=PASS\n'

# Preserve the diagnosed negative witness, then prove the exact corrected
# environment is accepted by the frozen validator. No helper or Runtime runs.
agent=/home/user/work/wt/agt-pin-d0a5072b
python=/home/user/work/venv-agent/bin/python
path_value=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/local/bin:/usr/bin:/bin
witness_tmp=$(mktemp -d "$worker/witness-XXXXXX")
trap 'rm -rf -- "$witness_tmp"' EXIT
env -i HOME=/root LANG=C.UTF-8 PATH="$path_value" TMPDIR="$witness_tmp" \
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$agent" PYTHONNOUSERSITE=1 "$python" -I -c '
import os, sys
sys.path.insert(0, "/home/user/work/wt/agt-pin-d0a5072b")
from astrid.core.rendering.remotion_runtime import RemotionValidationError, probe_context
try:
    probe_context(environment=os.environ, python_executable=sys.executable)
except RemotionValidationError as error:
    print("negative-witness=PASS: " + type(error).__name__ + ": " + str(error))
    raise SystemExit(0)
raise SystemExit("negative witness unexpectedly accepted PYTHONNOUSERSITE")
'
env -i HOME=/root LANG=C.UTF-8 PATH="$path_value" TMPDIR="$witness_tmp" \
  PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$agent" "$python" -I -c '
import os, sys
sys.path.insert(0, "/home/user/work/wt/agt-pin-d0a5072b")
from astrid.core.rendering.remotion_runtime import probe_context
context = probe_context(environment=os.environ, python_executable=sys.executable)
assert context["policy"] == "clean-schema-env/v1"
print("corrected-witness=PASS: policy=" + context["policy"] + " python=" + context["python_executable"])
'

set +e
bash "$worker/preflight.sh" --preflight
preflight_rc=$?
set -e
if [ "$preflight_rc" -ne 0 ]; then
  echo "preflight=FAIL exit=$preflight_rc; helper=NOT_RUN"
  exit "$preflight_rc"
fi

latest_preflight=$(find "$worker/evidence" -type f -name preflight.json -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)
test -n "$latest_preflight"
"$node" --input-type=module -e '
  import fs from "node:fs";
  const result = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
  if (result.status !== "PASS") throw new Error(`preflight status ${result.status}`);
  if (result.tokenIssued || result.browserLaunched || result.runtimeStarted) throw new Error("preflight crossed helper boundary");
  if (result.tuple.sources.app.commit !== "d00a66134f330672ea7471dc69db38c1566d94cf" || result.tuple.sources.app.tree !== "a8bf53d5d5e865aa88825bbc20f6f530bfbaa7ba") throw new Error("wrong App tuple");
  if (result.appGraph.sha256 !== "8bdc44e93ce6f712f2a26fc44f1f8e904215c1785f54ed97f826a98fe0145c5b" || result.appGraph.fileCount !== 32393) throw new Error("wrong App graph");
  if (result.runtimeGraph.graph.sha256 !== "4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c" || result.runtimeGraph.graph.fileCount !== 21455) throw new Error("wrong Runtime graph");
  if (result.freeBytes < 10737418240) throw new Error(`preflight free space ${result.freeBytes} below floor`);
  console.log(JSON.stringify({preflight: "PASS", freeBytes: result.freeBytes, appGraph: result.appGraph, runtimeGraph: result.runtimeGraph.graph, discovery: result.discovery, availability: result.availability}, null, 2));
' "$latest_preflight"

after_preflight=$(free_bytes)
test "$after_preflight" -ge "$floor"
echo "preflight=PASS; invoking corrected existing helper-only driver exactly once free_bytes=$after_preflight floor=$floor"
set +e
bash "$worker/COMMAND" --run
helper_rc=$?
set -e
echo "helper_exit=$helper_rc"
exit "$helper_rc"
