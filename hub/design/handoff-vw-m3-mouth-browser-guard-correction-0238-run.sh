#!/usr/bin/env bash
set -euo pipefail

root=${ASTRID_CHECKOUT:?central runner must select the committed Agent snapshot}
root=$(realpath -- "$root")
runtime=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b
peers=$runtime/node_modules
artifact=$runtime/artifacts/banodoco-timeline-composition-0.0.13.tgz
node=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
python=/home/user/work/venv-agent/bin/python
browser=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell

test -d "$root" && test "$(realpath -- "$root")" = "$root"
test -d "$runtime" && test "$(realpath -- "$runtime")" = "$runtime"
test -d "$peers" && test "$(realpath -- "$peers")" = "$peers"
test -f "$artifact" && test -x "$node" && test -x "$python" && test -x "$browser"
test "$(git -C "$root" status --porcelain --untracked-files=all)" = ""
source_revision=$(git -C "$root" rev-parse HEAD)
source_tree=$(git -C "$root" rev-parse HEAD^{tree})
test "${#source_revision}" = 40 && test "${#source_tree}" = 40
if test -n "${VIEWING_CROP_REVISION:-}"; then
    test "$VIEWING_CROP_REVISION" = "$source_revision"
fi

source_hash() {
    git -C "$root" ls-files -z |
        while IFS= read -r -d '' name; do sha256sum -- "$root/$name"; done |
        sha256sum | awk '{print $1}'
}

sha() { sha256sum -- "$1" | awk '{print $1}'; }
browser_realpath=$(realpath -- "$browser")
test "$browser_realpath" = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
browser_sha=$(sha "$browser")
test "$browser_sha" = 63eca986a3fe7f523d2d6e79d9f13daf4f1c73c1d9013c2c4a05b123510145b4
artifact_sha=$(sha "$artifact")
test "$artifact_sha" = 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
node_sha=$(sha "$node")
test "$node_sha" = 43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
test "$("$node" --version)" = v20.19.4
test "$(tar -tzf "$artifact" | awk '$0 ~ /^package\/[^/]+/ {count++} END {print count + 0}')" = 77

declare -A peer_sha=(
    ["@remotion/player/dist/cjs/PlayerUI.js"]=5dc9b4b89310609f57a718c641334d530b72ecf284fc1682610afcec208a4fbb
    ["@remotion/player/dist/cjs/use-player-methods.js"]=ff50ab8b4ae86423fab18aa1ecf6c48c41501c4f7b527f05a55c2c36598def46
    ["@remotion/player/dist/cjs/use-playback.js"]=6c8369a19d7a29eab5dab4642799172d4f2a7e11dad39125edcb673ec5729fb0
    ["@remotion/player/dist/esm/index.mjs"]=d3ef9728584c78e0e01cdb71ad72e3c6ddb36f96bfef90a4231d8b795e906b12
    ["remotion/dist/esm/index.mjs"]=9fdfe58f3f34e6a72564a811ac5d374d1c97a0f535e2a0e3aac198670d9b7ff8
    ["remotion/dist/cjs/audio/shared-audio-tags.js"]=471b33916a91f5b9529c477bdf0ec586cb700d5a7179ab910a82dd932e172f6c
)
for name in "${!peer_sha[@]}"; do
    test -f "$peers/$name"
    test "$(sha "$peers/$name")" = "${peer_sha[$name]}"
done

test "${VIEWING_BROWSER_FLOCK_HELD:-}" = 1
test "${VIEWING_CROP_CENTRAL:-}" = 1
test "$(flock -n /tmp/timeline-viewing-browser.lock true; echo $?)" != 0
before_source=$(source_hash)
before_artifact=$artifact_sha
before_node=$node_sha
before_browser=$browser_sha
declare -A before_peer_sha=()
for name in "${!peer_sha[@]}"; do before_peer_sha[$name]=$(sha "$peers/$name"); done

scratch=$(mktemp -d /tmp/vw-m3-mouth-public13-0223-XXXXXX)
keep=0
cleanup() {
    if test "$keep" = 0; then
        find "$scratch" -depth -delete 2>/dev/null || true
    else
        echo "RETAINED_TEMP=$scratch"
    fi
}
trap cleanup EXIT
printf '%s\n' "SOURCE_REVISION=$source_revision" "SOURCE_TREE=$source_tree" \
    "SOURCE_HASH=$before_source" "BROWSER_REALPATH=$browser_realpath" \
    "BROWSER_SHA=$before_browser" "ARTIFACT_SHA=$before_artifact" "NODE_SHA=$before_node" > "$scratch/preflight.txt"

set +e
env -i HOME=/root LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
    PATH="$(dirname "$node"):$peers/.bin:/usr/local/bin:/usr/bin:/bin" \
    PYTHONPATH="$root" ASTRID_CHECKOUT="$root" \
    ASTRID_REMOTION_PROJECT_DIR="$runtime" \
    ASTRID_NODE_EXECUTABLE="$node" \
    ASTRID_COMPOSITION_TEST_NODE_MODULES="$peers" \
    ASTRID_COMPOSITION_TEST_ARTIFACT="$artifact" \
    VIEWING_BROWSER_FLOCK_HELD=1 VIEWING_CROP_CENTRAL=1 TMPDIR="$scratch" \
    "$python" -m pytest -q -s -o addopts= -o tmp_path_retention_policy=all \
    -p no:cacheprovider --tb=short tests/packs/rendering/presenter_crop_capture.py \
    --basetemp="$scratch/pytest"
status=$?
set -e
keep=1

test "$(realpath -- "$browser")" = "/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell"
test "$(sha "$browser")" = "$before_browser"
test "$(sha "$browser")" = 63eca986a3fe7f523d2d6e79d9f13daf4f1c73c1d9013c2c4a05b123510145b4
test "$(source_hash)" = "$before_source"
test "$(sha "$artifact")" = "$before_artifact"
test "$(sha "$node")" = "$before_node"
for name in "${!peer_sha[@]}"; do test "$(sha "$peers/$name")" = "${before_peer_sha[$name]}"; done
if test "$status" != 0; then exit "$status"; fi
printf '%s\n' "RETAINED_SUCCESS_TEMP=$scratch"
printf '%s\n' "PASS: source revision/tree, Chromium1194 path/hash, package77/Node43d6/readonly-peer hashes unchanged"
