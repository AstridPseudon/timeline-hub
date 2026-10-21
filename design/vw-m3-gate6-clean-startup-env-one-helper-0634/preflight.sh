#!/usr/bin/env bash
set -euo pipefail
umask 077

worker=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
app=/home/user/work/wt/app-pin-d00a6613
home_app=/home/user/work/app
agent=/home/user/work/wt/agt-pin-d0a5072b
runtime=/home/user/work/wt/rt-pin-8f105c26
node=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
run_dir=$worker/gate6-20261021T0634
mode=${1:---run}
case "$mode" in --run|--preflight|--plant-missing-dist) ;; *) echo 'usage: run.sh [--preflight|--plant-missing-dist]' >&2; exit 2 ;; esac
[ "$#" -le 1 ] || exit 2
tmpdir=$(mktemp -d "$worker/tmp-XXXXXX")
trap 'rm -rf -- "$tmpdir"' EXIT

exec 9>>/tmp/timeline-viewing-browser.lock
flock -x 9
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
export PYTHONPATH=$runtime:$agent
export ASTRID_APP_DIRECT_DIST=$app/dist
export ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b
export ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
export ASTRID_NODE_EXECUTABLE=$node
export TIMELINE_COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-5a4e9b72
export TIMELINE_VIEWING_APP_SOURCE=d00a66134f330672ea7471dc69db38c1566d94cf
export TIMELINE_VIEWING_APP_TREE=a8bf53d5d5e865aa88825bbc20f6f530bfbaa7ba
export PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 TSX_DISABLE_CACHE=1
[ "$(realpath "$worker")" = "$worker" ]
[ "$(realpath "$home_app")" = "$home_app" ]
[ "$(git -C "$home_app" rev-parse --is-inside-work-tree)" = true ]
git -C "$home_app" merge-base --is-ancestor d00a66134f330672ea7471dc69db38c1566d94cf "$(git -C "$home_app" rev-parse HEAD)"
[ "$(realpath "$worker/evidence")" = "$worker/evidence" ]
[ "$(realpath "$run_dir")" = "$run_dir" ]
export PREFLIGHT_DIR
mkdir -p "$worker/evidence"
PREFLIGHT_DIR=$(mktemp -d "$worker/evidence/preflight-XXXXXX")
[ "$(realpath "$PREFLIGHT_DIR")" = "$PREFLIGHT_DIR" ]
export TMPDIR=$tmpdir TMP=$tmpdir TEMP=$tmpdir
export PWTEST_CACHE_DIR=$tmpdir/playwright-cache
export PLAYWRIGHT_OUTPUT_DIR=$tmpdir/playwright-output
export RUN_DIR=$run_dir
cd "$app"
"$node" --import "$app/node_modules/tsx/dist/loader.mjs" "$worker/prepare.mjs" "$mode"
if [ "$mode" != --run ]; then
  echo "PREFLIGHT PASS: $PREFLIGHT_DIR/preflight.json; token-issued:false; no browser or Runtime launched"
  exit 0
fi

"$node" --import "$app/node_modules/tsx/dist/loader.mjs" "$worker/issue.mjs"
export VIEWING_FRAME_SOURCE_TUPLE=$run_dir/source-tuple.json
export TAB_AUDIO_GRANT_PATH=$run_dir/manager-grant.json
export TAB_AUDIO_RUN_MARKER=$run_dir/one-shot-marker.json
export PLAYWRIGHT_OUTPUT_DIR=$run_dir/playwright-output
"$node" tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs --ready "$app" "$agent" "$runtime"
"$node" node_modules/@playwright/test/cli.js test --config playwright.viewing-parity.normal-profile-native1920.config.ts --project=native-codec-chrome155 --workers=1
