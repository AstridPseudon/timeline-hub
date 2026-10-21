#!/usr/bin/env bash
set -euo pipefail
umask 077

worker=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
app=/home/user/work/wt/app-pin-0d432391
home_app=/home/user/work/app
agent=/home/user/work/wt/agt-pin-d0a5072b
runtime=/home/user/work/wt/rt-pin-8f105c26
node=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
stage_root=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage
remotion=$stage_root/remotion
dist=/home/user/work/wt/app-pin-d00a6613/dist
run_dir=${RUN_DIR:?run.sh must provide RUN_DIR}
mode=${1:---run}
case "$mode" in --run|--preflight|--plant-missing-dist) ;; *) echo 'usage: run.sh [--preflight|--plant-missing-dist]' >&2; exit 2 ;; esac
[ "$#" -le 1 ] || exit 2
tmpdir=$(mktemp -d "$worker/tmp-XXXXXX")
test_process_tmpdir=$(mktemp -d /tmp/vw-XXXXXX)
chmod 700 "$test_process_tmpdir"
/home/user/work/venv-agent/bin/python -B "$worker/short-player-temp-controls.py" --claim "$test_process_tmpdir"
cleanup_owned_process_tmpdir() {
  status=$?
  if ! /home/user/work/venv-agent/bin/python -B "$worker/short-player-temp-controls.py" --cleanup "$test_process_tmpdir"; then
    echo "refusing unsafe short Player temp cleanup" >&2
    status=1
  fi
  rm -rf -- "$tmpdir"
  exit "$status"
}
trap cleanup_owned_process_tmpdir EXIT

test -e /proc/self/fd/9
flock -n 9
printf 'browser-lock=fd9 inherited-from=run.sh held-through=preflight-and-physical-cleanup\n'
unset NODE_OPTIONS NODE_PATH
unset TAB_AUDIO_RUN TAB_AUDIO_RUN_MODE TAB_AUDIO_FINAL_SHA TAB_AUDIO_PREFLIGHT_PATH
unset TAB_AUDIO_GRANT_PATH TAB_AUDIO_RUN_MARKER VIEWING_FRAME_SOURCE_TUPLE
export HOME=/root
export LANG=C.UTF-8
export PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/home/user/work/venv-agent/bin:/usr/local/bin:/usr/bin:/bin
export VIEWING_BROWSER_FLOCK_HELD=1
export ASTRID_CHECKOUT=$agent
export ASTRID_PACK_HOST_HELPER_CHECKOUT=/home/user/work/wt/agt-pin-b70b9d56
export ASTRID_RUNTIME_CHECKOUT=$runtime
export ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python
export ASTRID_PYTHON=/home/user/work/venv-agent/bin/python
export ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.11/site-packages
export PYTHONPATH=$runtime:$agent
export ASTRID_APP_DIRECT_DIST=$dist
export ASTRID_REMOTION_PROJECT_DIR=$remotion
export ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
export ASTRID_NODE_EXECUTABLE=$node
export TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-5a4e9b72
export TIMELINE_VIEWING_APP_SOURCE=0d4323913b92c4e0e3830bf14ec7f35d981475ca
export TIMELINE_VIEWING_APP_TREE=5a1e0e85d0f336f642426b91ccf3b3f1984ebd14
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TSX_DISABLE_CACHE=1
[ "$(realpath "$worker")" = "$worker" ]
[ "$(realpath "$home_app")" = "$home_app" ]
[ "$(realpath "$stage_root")" = "$stage_root" ]
[ "$(realpath "$remotion")" = "$remotion" ]
[ "$(git -C "$home_app" rev-parse --is-inside-work-tree)" = true ]
git -C "$home_app" merge-base --is-ancestor d00a66134f330672ea7471dc69db38c1566d94cf "$(git -C "$home_app" rev-parse HEAD)"
mkdir -p "$worker/evidence"
[ "$(realpath "$worker/evidence")" = "$worker/evidence" ]
[ "$(realpath "$run_dir")" = "$run_dir" ]
"$node" "$worker/stage-audit.mjs" "$stage_root" >"$worker/evidence/stage-audit.json"
export PREFLIGHT_DIR
PREFLIGHT_DIR=$(mktemp -d "$worker/evidence/preflight-XXXXXX")
[ "$(realpath "$PREFLIGHT_DIR")" = "$PREFLIGHT_DIR" ]
export TMPDIR=$test_process_tmpdir TMP=$test_process_tmpdir TEMP=$test_process_tmpdir
export PWTEST_CACHE_DIR=$tmpdir/playwright-cache
export PLAYWRIGHT_OUTPUT_DIR=$tmpdir/playwright-output
export RUN_DIR=$run_dir
cd "$app"
env -i \
  HOME=/root LANG=C.UTF-8 PATH="$PATH" TMPDIR="$test_process_tmpdir" TMP="$test_process_tmpdir" TEMP="$test_process_tmpdir" \
  PREFLIGHT_DIR="$PREFLIGHT_DIR" RUN_DIR="$RUN_DIR" APP_CHECKOUT="$app" \
  ASTRID_CHECKOUT="$agent" ASTRID_PACK_HOST_HELPER_CHECKOUT=/home/user/work/wt/agt-pin-b70b9d56 \
  ASTRID_RUNTIME_CHECKOUT="$runtime" ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python PYTHONPATH="$runtime:$agent" \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.11/site-packages \
  ASTRID_APP_DIRECT_DIST="$dist" ASTRID_REMOTION_PROJECT_DIR="$remotion" \
  ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell \
  ASTRID_NODE_EXECUTABLE="$node" TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-5a4e9b72 \
  TIMELINE_VIEWING_APP_SOURCE=0d4323913b92c4e0e3830bf14ec7f35d981475ca \
  TIMELINE_VIEWING_APP_TREE=5a1e0e85d0f336f642426b91ccf3b3f1984ebd14 \
  VIEWING_BROWSER_FLOCK_HELD=1 \
  PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TSX_DISABLE_CACHE=1 \
  "$node" --import "$app/node_modules/tsx/dist/loader.mjs" "$worker/prepare.mjs" "$mode"
if [ "$mode" != --run ]; then
  echo "PREFLIGHT PASS: $PREFLIGHT_DIR/preflight.json; token-issued:false; no browser or Runtime launched"
  exit 0
fi

env -i \
  HOME=/root LANG=C.UTF-8 PATH="$PATH" TMPDIR="$test_process_tmpdir" TMP="$test_process_tmpdir" TEMP="$test_process_tmpdir" \
  PREFLIGHT_DIR="$PREFLIGHT_DIR" RUN_DIR="$RUN_DIR" APP_CHECKOUT="$app" \
  ASTRID_CHECKOUT="$agent" ASTRID_PACK_HOST_HELPER_CHECKOUT=/home/user/work/wt/agt-pin-b70b9d56 \
  ASTRID_RUNTIME_CHECKOUT="$runtime" ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python \
  ASTRID_PYTHON=/home/user/work/venv-agent/bin/python PYTHONPATH="$runtime:$agent" \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.11/site-packages \
  ASTRID_APP_DIRECT_DIST="$dist" ASTRID_REMOTION_PROJECT_DIR="$remotion" \
  ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell \
  ASTRID_NODE_EXECUTABLE="$node" TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-5a4e9b72 \
  TIMELINE_VIEWING_APP_SOURCE=0d4323913b92c4e0e3830bf14ec7f35d981475ca \
  TIMELINE_VIEWING_APP_TREE=5a1e0e85d0f336f642426b91ccf3b3f1984ebd14 \
  VIEWING_BROWSER_FLOCK_HELD=1 \
  PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TSX_DISABLE_CACHE=1 \
  "$node" --import "$app/node_modules/tsx/dist/loader.mjs" "$worker/issue.mjs"
export VIEWING_FRAME_SOURCE_TUPLE=$run_dir/source-tuple.json
export TAB_AUDIO_GRANT_PATH=$run_dir/manager-grant.json
export TAB_AUDIO_RUN_MARKER=$run_dir/one-shot-marker.json
export PLAYWRIGHT_OUTPUT_DIR=$run_dir/playwright-output
env -i \
  HOME=/root LANG=C.UTF-8 PATH="$PATH" TMPDIR="$test_process_tmpdir" TMP="$test_process_tmpdir" TEMP="$test_process_tmpdir" \
  APP_CHECKOUT="$app" ASTRID_CHECKOUT="$agent" ASTRID_RUNTIME_CHECKOUT="$runtime" \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.11/site-packages \
  PYTHONPATH="$runtime:$agent" ASTRID_APP_DIRECT_DIST="$dist" \
  ASTRID_PACK_HOST_HELPER_CHECKOUT=/home/user/work/wt/agt-pin-b70b9d56 \
  ASTRID_REMOTION_PROJECT_DIR="$remotion" \
  ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell \
  ASTRID_NODE_EXECUTABLE="$node" TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-5a4e9b72 \
  TIMELINE_VIEWING_APP_SOURCE=0d4323913b92c4e0e3830bf14ec7f35d981475ca \
  TIMELINE_VIEWING_APP_TREE=5a1e0e85d0f336f642426b91ccf3b3f1984ebd14 \
  VIEWING_BROWSER_FLOCK_HELD=1 VIEWING_FRAME_SOURCE_TUPLE="$VIEWING_FRAME_SOURCE_TUPLE" \
  TAB_AUDIO_GRANT_PATH="$TAB_AUDIO_GRANT_PATH" TAB_AUDIO_RUN_MARKER="$TAB_AUDIO_RUN_MARKER" \
  PLAYWRIGHT_OUTPUT_DIR="$PLAYWRIGHT_OUTPUT_DIR" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TSX_DISABLE_CACHE=1 \
  "$node" "$worker/packet-ready.mjs" "$app" "$agent" "$runtime" "$stage_root"
env -i \
  HOME=/root LANG=C.UTF-8 PATH="$PATH" TMPDIR="$test_process_tmpdir" TMP="$test_process_tmpdir" TEMP="$test_process_tmpdir" \
  APP_CHECKOUT="$app" ASTRID_CHECKOUT="$agent" ASTRID_RUNTIME_CHECKOUT="$runtime" \
  ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python ASTRID_PYTHON=/home/user/work/venv-agent/bin/python \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH=/home/user/work/venv-agent/lib/python3.11/site-packages \
  PYTHONPATH="$runtime:$agent" ASTRID_APP_DIRECT_DIST="$dist" \
  ASTRID_PACK_HOST_HELPER_CHECKOUT=/home/user/work/wt/agt-pin-b70b9d56 \
  ASTRID_REMOTION_PROJECT_DIR="$remotion" \
  ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell \
  ASTRID_NODE_EXECUTABLE="$node" TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-5a4e9b72 \
  TIMELINE_VIEWING_APP_SOURCE=0d4323913b92c4e0e3830bf14ec7f35d981475ca \
  TIMELINE_VIEWING_APP_TREE=5a1e0e85d0f336f642426b91ccf3b3f1984ebd14 \
  VIEWING_BROWSER_FLOCK_HELD=1 VIEWING_FRAME_SOURCE_TUPLE="$VIEWING_FRAME_SOURCE_TUPLE" \
  TAB_AUDIO_GRANT_PATH="$TAB_AUDIO_GRANT_PATH" TAB_AUDIO_RUN_MARKER="$TAB_AUDIO_RUN_MARKER" \
  PLAYWRIGHT_OUTPUT_DIR="$PLAYWRIGHT_OUTPUT_DIR" PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TSX_DISABLE_CACHE=1 \
  "$node" node_modules/@playwright/test/cli.js test --config playwright.viewing-parity.normal-profile-native1920.config.ts --project=native-codec-chrome155 --workers=1
