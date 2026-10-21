#!/usr/bin/env bash
set -Eeuo pipefail
umask 077

worker=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
node=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
python=/home/user/work/venv-agent/bin/python
app=/home/user/work/wt/app-pin-0d432391
agent=/home/user/work/wt/agt-pin-d0a5072b
runtime=/home/user/work/wt/rt-pin-8f105c26
helper=/home/user/work/wt/agt-pin-b70b9d56
composition=/home/user/work/wt/vw-pin-5a4e9b72
stage_root=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage
remotion=$stage_root/remotion
dist=/home/user/work/wt/app-pin-d00a6613/dist
browser=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
physical_run_dir=$worker/gate6-20261021T1153
run_dir=$physical_run_dir
mode=${1:---run}
case "$mode" in --run|--preflight) ;; *) echo 'usage: run.sh [--preflight]' >&2; exit 2 ;; esac
test "$#" -le 1
grant_note=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/viewing/notes/grant-discovery-readiness-1153.md
marker_path=$physical_run_dir/one-shot-marker.json
test -f "$grant_note"
grep -F "$stage_root" "$grant_note" >/dev/null
grep -F "$worker" "$grant_note" >/dev/null
grep -F "$marker_path" "$grant_note" >/dev/null
grep -Eiq 'fresh' "$grant_note"
echo 'fresh-manager-grant=PASS'
invocation_log=$(mktemp "$worker/invocation-${mode#--}-XXXXXX.log")
exec > >(tee -a "$invocation_log") 2>&1
if [ "$mode" = --preflight ]; then
  test ! -e "$physical_run_dir"
  diagnostic_dir=$(mktemp -d "$worker/diagnostic-XXXXXX")
  run_dir=$diagnostic_dir/run
  mkdir "$run_dir"
  diagnostic_cleanup=1
else
  diagnostic_dir=
  diagnostic_cleanup=0
  test ! -e "$run_dir"
  mkdir "$run_dir"
fi
cleanup_diagnostic() {
  if [ "$diagnostic_cleanup" -eq 1 ]; then
    rm -rf -- "$diagnostic_dir"
  fi
}
trap cleanup_diagnostic EXIT
floor=10737418240
central_snapshot=2290636
measured_stage=405573632
known_threshold=11320247244

test "$(realpath "$worker")" = "$worker"
test "$(realpath "$app")" = "$app"
test "$(realpath "$agent")" = "$agent"
test "$(realpath "$runtime")" = "$runtime"
test "$(realpath "$helper")" = "$helper"
test "$(realpath "$composition")" = "$composition"
test "$(realpath "$stage_root")" = "$stage_root"
test "$(realpath "$remotion")" = "$remotion"
test "$(realpath "$browser")" = "$browser"
exec 9>>/tmp/timeline-viewing-browser.lock
flock -x 9
printf 'browser-lock=fd9 owner=run.sh inherited-by=preflight.sh held-through=physical-cleanup\n'

free_bytes() { df -B1 --output=avail /home/user/work | tail -1 | tr -d ' '; }
all_bytes() {
  find "$worker" -maxdepth 1 -type f -printf '%s\n' | awk '{sum += $1} END {print sum + 0}'
}
check_budget() {
  local free=$1 stage=$2
  printf 'storage free=%s floor=%s central_snapshot=%s measured_stage=%s known_threshold=%s owned_bytes=%s phase=%s\n' \
    "$free" "$floor" "$central_snapshot" "$measured_stage" "$known_threshold" "$(all_bytes)" "$stage"
  test "$free" -ge "$known_threshold"
  test "$free" -ge "$floor"
}

check_budget "$(free_bytes)" before-preflight
export RUN_DIR=$run_dir

bash -n "$worker/run.sh" "$worker/preflight.sh"
"$node" --check "$worker/prepare.mjs"
"$node" --check "$worker/issue.mjs"
"$node" --check "$worker/dist-availability.mjs"
"$node" --check "$worker/stage-audit.mjs"
"$node" --check "$worker/packet-ready.mjs"
"$node" --check "$worker/discovery-readiness.mjs"
python -B - "$worker/prepare-validation-diagnostic.py" <<'PY'
import ast
import pathlib
import sys
ast.parse(pathlib.Path(sys.argv[1]).read_text(), filename=sys.argv[1])
print("python-syntax=PASS")
PY
(cd -- "$worker" && sha256sum -c "$worker/SHA256SUMS")
echo 'static-checks=PASS'

# The full preflight runs before issuance and rechecks source, imports, ancestry,
# dist, graphs, peer bindings, toolchain, browser, authority, lifecycle and
# cleanup guards. Its child receives only the reviewed explicit environment.
bash "$worker/preflight.sh" --preflight
latest_preflight=$(find "$worker/evidence" -type f -name preflight.json -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)
test -n "$latest_preflight"
"$node" --input-type=module -e '
  import fs from "node:fs";
  const result = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
  if (result.status !== "PASS") throw new Error(`preflight status ${result.status}`);
  if (result.tokenIssued || result.browserLaunched || result.runtimeStarted) throw new Error("preflight crossed issuance boundary");
  if (result.tuple.sources.app.commit !== "0d4323913b92c4e0e3830bf14ec7f35d981475ca" || result.tuple.sources.app.tree !== "5a1e0e85d0f336f642426b91ccf3b3f1984ebd14") throw new Error("wrong App tuple");
  if (result.tuple.appSource.files !== 5902 || result.tuple.appSource.sha256 !== "sha256:4fb1e53b2dce325f826b6b071d0782544e5ba2c7b27418b6170f8c947c450435") throw new Error("wrong App source binding");
  if (result.appGraph.sha256 !== "8bdc44e93ce6f712f2a26fc44f1f8e904215c1785f54ed97f826a98fe0145c5b" || result.appGraph.fileCount !== 32393) throw new Error("wrong App graph");
  if (result.runtimeGraph.graph.sha256 !== "4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c" || result.runtimeGraph.graph.fileCount !== 21455) throw new Error("wrong Runtime graph");
  if (result.dist.files !== 339 || result.dist.index !== "aeb5d83399b453b15a8cbc67b31260cf2820f8d65770ccd458986ddd551e257b") throw new Error("wrong retained dist");
  if (result.discovery !== "discovered exactly 5 current native-codec-chrome155 parity cases") throw new Error("wrong discover() return contract");
  if (JSON.stringify(result.discoveryControls) !== JSON.stringify({wrongCount: "refused", wrongName: "refused", noTests: "refused", helperError: "refused"})) throw new Error("discovery refusal controls incomplete");
  if (result.normalDiscovery.match(/^Total: 5 tests in 1 file$/m) === null) throw new Error("wrong case collection");
  if (result.availability.status !== 200 || !result.availability.exact) throw new Error("GET 200 guard failed");
  console.log(JSON.stringify({preflight: "PASS", freeBytes: result.freeBytes, appSource: result.tuple.appSource, appGraph: result.appGraph, runtimeGraph: result.runtimeGraph.graph, dist: result.dist, availability: result.availability, cases: "exactly5"}));
' "$latest_preflight"
check_budget "$(free_bytes)" after-preflight

# Exercise the same frozen full production validation transaction under the
# explicit clean child environment, before issue.mjs creates any fresh grant.
validation_tmp=$(mktemp -d "$worker/validation-XXXXXX")
cleanup_validation() {
  find "$validation_tmp" -depth -type f -delete 2>/dev/null || true
  find "$validation_tmp" -depth -type l -delete 2>/dev/null || true
  find "$validation_tmp" -depth -type d -empty -delete 2>/dev/null || true
  cleanup_diagnostic
}
trap cleanup_validation EXIT
env -i \
  HOME=/root LANG=C.UTF-8 \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/local/bin:/usr/bin:/bin \
  TMPDIR="$validation_tmp" \
  ASTRID_CHECKOUT="$agent" ASTRID_PACK_HOST_HELPER_CHECKOUT="$helper" \
  ASTRID_RUNTIME_CHECKOUT="$runtime" ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  ASTRID_PYTHON="$python" ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.11/site-packages \
  ASTRID_APP_DIRECT_DIST="$dist" ASTRID_REMOTION_PROJECT_DIR="$remotion" \
  ASTRID_REMOTION_BROWSER_EXECUTABLE="$browser" ASTRID_NODE_EXECUTABLE="$node" \
  TIMELINE_COMPOSITION_CHECKOUT="$composition" \
  TIMELINE_VIEWING_APP_SOURCE=0d4323913b92c4e0e3830bf14ec7f35d981475ca \
  TIMELINE_VIEWING_APP_TREE=5a1e0e85d0f336f642426b91ccf3b3f1984ebd14 \
  PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TSX_DISABLE_CACHE=1 \
  "$python" -I "$worker/prepare-validation-diagnostic.py"
check_budget "$(free_bytes)" after-full-validation
if [ "$mode" = --preflight ]; then
  test ! -e "$physical_run_dir"
  test ! -e "$run_dir/source-tuple.json"
  test ! -e "$run_dir/manager-grant.json"
  test ! -e "$run_dir/one-shot-marker.json"
  test ! -d "$run_dir/playwright-output"
  echo 'full_prepare_render_validation=PASS; token-issued:false; no issue, marker, grant, Runtime, helper, or browser'
  exit 0
fi
echo 'full_prepare_render_validation=PASS; issue and physical controller now run once'

# Existing issue.mjs creates this fresh tuple/grant/marker exactly once; the
# preflight and full validation above are deliberately complete before it.
bash "$worker/preflight.sh" --run
test -f "$run_dir/source-tuple.json"
test -f "$run_dir/manager-grant.json"
test -f "$run_dir/one-shot-marker.json"
test -d "$run_dir/playwright-output"
echo 'physical-five-case-invocation=PASS'
