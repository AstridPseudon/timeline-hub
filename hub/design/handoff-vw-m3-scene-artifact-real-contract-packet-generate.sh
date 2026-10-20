#!/usr/bin/env bash
set -euo pipefail

REPO=/home/user/work/wt/vw-m3-scene-artifact-real-contract-packet
NODE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current-root-cap-three-stills-prep/node
PEERS=/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules
OUT=${1:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-scene-artifact-real-contract-packet-examples}

test -x "$NODE"
test "$("$NODE" --version)" = v20.19.4
test -d "$PEERS/esbuild"
test "$(realpath "$PEERS")" != /home/user/work/app/node_modules
test ! -e "$OUT"
STAGE=$(mktemp -d /tmp/vw-m3-scene-artifact-contract.XXXXXX)
trap 'rm -rf -- "$STAGE"' EXIT

cd "$REPO"
ASTRID_NODE_EXECUTABLE="$NODE" \
ASTRID_TEST_NODE_MODULES="$PEERS" \
ASTRID_SCENE_ARTIFACT_EXAMPLES="$OUT" \
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=. \
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  --basetemp="$STAGE" \
  tests/packs/rendering/test_scene_artifact_contract.py \
  -k scene_only_bundle

test -f "$OUT/manifest.json"
test "$(find "$OUT" -type f -printf '%s\n' | awk '{total += $1} END {print total + 0}')" -lt 51200
