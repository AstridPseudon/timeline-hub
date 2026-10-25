#!/usr/bin/env bash
set -euo pipefail

# D124.6/D77: copyable Farm recipe.  This file is preparation only; it must
# not be run on Main.  Farm supplies all paths and receipts after admission.
ORCH=${ORCH:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
WORK=${WORK:-/home/user/work}
RESULT_ROOT=${RESULT_ROOT:?private durable result directory on Farm}
RUN_ROOT=${RUN_ROOT:?private run root on Farm}
mkdir -p "$RESULT_ROOT" "$RUN_ROOT/home" "$RUN_ROOT/tmp"

# The guard repair is a hard prerequisite for every later phase.  The current
# Sol1243 report is not a substitute for Farm's independently recorded PASS.
: "${SOL1243_GUARD_STATUS:?set to PASS only after independent Sol1243 PASS}"
[[ "$SOL1243_GUARD_STATUS" == PASS ]] || { echo 'Sol1243 guard is not PASS; no phase may start' >&2; exit 42; }
: "${SOL1243_GUARD_RECEIPT:?path to independently verified Sol1243 receipt}"
test -s "$SOL1243_GUARD_RECEIPT"

# These are the only source identities admitted by this handoff.
AGENT_SHA=91398e9de4500ce16c8e55741209ba3609cb1694
AGENT_TREE=523893dcf54dbe756db8fe2915d14055b1da660b
RUNTIME_SHA=1daca2a33f6d7b10053e07c539a54843e3984e19
RUNTIME_TREE=a522511414947e48e317a5e5c2103483b121a750
VIBECOMFY_SHA=31f90bb03d330283b76e7dbdda51197be787090d
VIBECOMFY_TREE=101744f0d87eebe5ddf6752c10f01f52dc94e3e9
OMP_SHA=9e282751c0059e37d2f6fbc14ffa0b450710bd23
OMP_TREE=2074d7a2e26cc954b5cf3d77e91f3efbb25ad34f
OMP_SOURCE_SHA256=3a84ac8be7d11434de8b22f4f0f1d643582ecc01c644e347bb0e056401da7b2e
OMP_BUN_LOCK_SHA256=f08eab1fd7e0519e8b131697d6a35815fd71d9b0a61a8d70cc57b499bcba53ee
REMOTION_LOCK_SHA256=f4fc0a32a8822e956dfa21ff35d19c0c83d147c754cdb3546f91c84e330be18d

: "${AGENT_CHECKOUT:?normal request-checkout result for Agent}"
: "${RUNTIME_CHECKOUT:?normal request-checkout result for Runtime}"
: "${INSTALL_MANIFEST:?Farm-authenticated normal installer manifest}"
: "${ASTRID_RUN:?normal installed astrid/run-astrid launcher}"
: "${PROGRAM_ROOT:?private Farm program root}"
: "${DATA_ROOT:?private Farm data root}"
: "${UV:?normal pinned uv executable}"
: "${VIBECOMFY_CHECKOUT:?normal VibeComfy checkout at the exact pin}"

# Farm must perform request-checkout, request-runtime, and request-child-venv
# first, then supply and verify their receipts before invoking this recipe. No
# archive, ZIP, ad-hoc copy, or shared venv/node_modules/runtime/cache is accepted.
git -C "$AGENT_CHECKOUT" rev-parse HEAD^{tree}
git -C "$RUNTIME_CHECKOUT" rev-parse HEAD^{tree}
[[ "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD)" == "$AGENT_SHA" ]]
[[ "$(git -C "$AGENT_CHECKOUT" rev-parse HEAD^{tree})" == "$AGENT_TREE" ]]
[[ "$(git -C "$RUNTIME_CHECKOUT" rev-parse HEAD)" == "$RUNTIME_SHA" ]]
[[ "$(git -C "$RUNTIME_CHECKOUT" rev-parse HEAD^{tree})" == "$RUNTIME_TREE" ]]
[[ -z "$(git -C "$AGENT_CHECKOUT" status --short)" ]]
[[ -z "$(git -C "$RUNTIME_CHECKOUT" status --short)" ]]

# Ordinary install path: the authenticated release manifest carries the local
# source pins and VibeComfy pin.  This is the production gateway/installer path
# (not python -m astrid.installer.cli and not a direct Backend call).
env -i HOME="$RUN_ROOT/home" LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  PATH="$(dirname "$ASTRID_RUN"):/usr/bin:/bin" \
  PYTHONDONTWRITEBYTECODE=1 TMPDIR="$RUN_ROOT/tmp" XDG_RUNTIME_DIR="$RUN_ROOT/tmp" \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT" \
  "$ASTRID_RUN" install --root "$PROGRAM_ROOT" --data-root "$DATA_ROOT" \
  --manifest "$INSTALL_MANIFEST" --uv "$UV" \
  >"$RESULT_ROOT/stage.stdout" 2>"$RESULT_ROOT/stage.stderr"

# All values below are Farm's actual post-stage receipt, not guessed paths.
: "${PROFILE:?actual installed profile from normal stage receipt}"
: "${BINDINGS:?actual seven-key JSON carrier from normal stage receipt}"
: "${PY:?actual installed pack-host Python from profile/receipt}"
: "${SITE:?actual installed source site from profile/receipt}"
: "${RUNTIME:?actual exact Runtime checkout from profile/receipt}"
: "${REMOTION:?actual installed Remotion project from profile/receipt}"
: "${NODE:?actual pinned Node executable from profile/receipt}"
: "${BROWSER:?actual pinned browser executable from profile/receipt}"
: "${FFMPEG:?actual pinned ffmpeg executable from profile/receipt}"
: "${FFPROBE:?actual pinned ffprobe executable from profile/receipt}"
: "${ASTRID_PACKS_PATH:?actual installed rendering pack path from profile/receipt}"

RENDER_ENV=(
  HOME="$RUN_ROOT/home" LANG=C.UTF-8 LC_ALL=C.UTF-8
  PATH="$(dirname "$NODE"):/usr/bin:/bin"
  PYTHONDONTWRITEBYTECODE=1 TMPDIR="$RUN_ROOT/tmp" XDG_RUNTIME_DIR="$RUN_ROOT/tmp"
  ASTRID_HOST_EXECUTION_PROFILE=installed
  ASTRID_PACK_HOST_PYTHON="$PY"
  ASTRID_PACKS_PATH="$ASTRID_PACKS_PATH"
  ASTRID_REMOTION_PROJECT_DIR="$REMOTION"
  ASTRID_REMOTION_BROWSER_EXECUTABLE="$BROWSER"
  ASTRID_NODE_EXECUTABLE="$NODE"
  ASTRID_TEST_NODE_MODULES="$REMOTION/node_modules"
  ASTRID_FFMPEG_EXECUTABLE="$FFMPEG"
  ASTRID_FFPROBE_EXECUTABLE="$FFPROBE"
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SITE"
  ASTRID_RUNTIME_SOURCE_MANIFEST="$PROFILE"
  ASTRID_D13_SOURCE_PROFILE="$PROFILE"
  ASTRID_D13_EXPECTED_BINDINGS="$BINDINGS"
  ASTRID_D13_NODE_SHA256=43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490
  ASTRID_D13_REMOTION_LOCK_SHA256="$REMOTION_LOCK_SHA256"
  ASTRID_D13_BROWSER_SHA256=85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95
  ASTRID_D13_FFMPEG_SHA256=ed16af623947494a72e284b6eb8ff225f2da22b38b5d5069c2fd4b4ba3384e41
  ASTRID_D13_FFPROBE_SHA256=272f6ebc634a63d9c8b4ca68e964119d980f25154e5aa2c35e5487da48e9a58f
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME"
)

# Genuine selectors: preflight, then daemon-backed authoring/final render.
env -i "${RENDER_ENV[@]}" "$PY" -B -m pytest -q -o addopts= -p no:cacheprovider \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight \
  >"$RESULT_ROOT/preflight.stdout" 2>"$RESULT_ROOT/preflight.stderr"
env -i "${RENDER_ENV[@]}" "$PY" -B -m pytest -q -o addopts= -p no:cacheprovider -m integration \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render \
  >"$RESULT_ROOT/render.stdout" 2>"$RESULT_ROOT/render.stderr"

# Keep private receipts/results durable under RESULT_ROOT.  Do not send these
# bytes through ordinary source sync; Farm controls their custody.
printf '%s\n' "$AGENT_SHA $AGENT_TREE $RUNTIME_SHA $RUNTIME_TREE $OMP_SHA $OMP_TREE" \
  >"$RESULT_ROOT/source-identities.txt"
printf '%s\n' 'stage=PASS' 'preflight=PASS' 'render=PASS' >"$RESULT_ROOT/status.txt"
