# D13 final binding command contract review

Result: the tracked setup helper is repaired and the proof body remains
untouched. The later named run is not claimed here.

## Repairs

- `ASTRID_RUNTIME_CHECKOUT` is now an explicit caller argument and is not
  derived from the Agent source root. The ready command must pass
  `/home/user/work/runtime`, which is Runtime `b92d3e7a05eec65c142294ef4873edd059e9b31d`, tree
  `6abc2f117391de8e7e35c0283f575a002199894d`.
- The exported pytest target is the relative current test selector, so no
  recycled `agt-m4-d13-reviewed-bindings-final-source-0927` path enters argv.
- The constructed `env -i` includes the existing profile path, the explicit
  `ASTRID_D13_EXPECTED_BINDINGS` seven-key carrier, all existing resource
  digest flags, and the short `TMPDIR`/`XDG_RUNTIME_DIR` roots.
- The command builder requires an absolute short per-run root and a separate
  existing Runtime checkout. It does not add a source/import fallback,
  authority, credential, grant, DTO, or proof execution.

## Exact ready command

Run from the tracked Agent test source root. The manager must first provide the
existing seven-key JSON carrier through `ASTRID_D13_EXPECTED_BINDINGS`; its
absence is the only missing materialized input found in the approved 0908/0917
profile handoff. The carrier must contain exactly:

```text
agent_commit, agent_tree, agent_wheel, agent_wheel_sha256,
source_checkout, source_digest, runtime_environment
```

The command below is the complete later-run shape. It includes a pure
preflight selector and a separate exact collection check; it does not execute
the native proof in this review.

```bash
set -euo pipefail
SOURCE_ROOT="$(git rev-parse --show-toplevel)"
RUNTIME=/home/user/work/runtime
PROFILE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/profile/astrid.json
BINDINGS="${ASTRID_D13_EXPECTED_BINDINGS:?set the existing seven-key D13 JSON carrier}"
PY=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/bin/python
SITE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m4-d13-private-entrypoint-custody-profile-repair-0908/private-profile-f4edcb4b/venv/lib/python3.13/site-packages
REMOTION=/home/user/work/runtimes/agent-remotion-f4ed-0013
NODE=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node
RUN_ROOT="$(mktemp -d /tmp/d13-XXXXXX)"
trap 'rm -rf "$RUN_ROOT"' EXIT
mkdir -p "$RUN_ROOT/home" "$RUN_ROOT/tmp"
test -f "$PROFILE" && test ! -L "$PROFILE"
test -f "$BINDINGS" && test ! -L "$BINDINGS"
test "$(git -C "$RUNTIME" rev-parse HEAD)" = b92d3e7a05eec65c142294ef4873edd059e9b31d
test "$(git -C "$RUNTIME" rev-parse HEAD^{tree})" = 6abc2f117391de8e7e35c0283f575a002199894d
test -x "$PY" && test -d "$SITE" && test -d "$REMOTION/node_modules" && test -x "$NODE"
env -i \
  HOME="$RUN_ROOT/home" LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  PATH="$(dirname "$NODE"):/usr/bin:/bin" \
  PYTHONDONTWRITEBYTECODE=1 TMPDIR="$RUN_ROOT/tmp" XDG_RUNTIME_DIR="$RUN_ROOT/tmp" \
  ASTRID_HOST_EXECUTION_PROFILE=installed \
  ASTRID_PACK_HOST_PYTHON="$PY" \
  ASTRID_PACKS_PATH="$SITE/astrid/packs/rendering" \
  ASTRID_REMOTION_PROJECT_DIR="$REMOTION" \
  ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  ASTRID_NODE_EXECUTABLE="$NODE" \
  ASTRID_TEST_NODE_MODULES="$REMOTION/node_modules" \
  ASTRID_FFMPEG_EXECUTABLE=/usr/bin/ffmpeg \
  ASTRID_FFPROBE_EXECUTABLE=/usr/bin/ffprobe \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SITE" \
  ASTRID_RUNTIME_SOURCE_MANIFEST="$PROFILE" \
  ASTRID_D13_SOURCE_PROFILE="$PROFILE" \
  ASTRID_D13_EXPECTED_BINDINGS="$BINDINGS" \
  ASTRID_D13_NODE_SHA256=43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490 \
  ASTRID_D13_REMOTION_LOCK_SHA256=c4d7030bd5418d35f2246269b5aba7952d0ed69ccd0084815a0043dfbb7a4e24 \
  ASTRID_D13_BROWSER_SHA256=85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95 \
  ASTRID_D13_FFMPEG_SHA256=ed16af623947494a72e284b6eb8ff225f2da22b38b5d5069c2fd4b4ba3384e41 \
  ASTRID_D13_FFPROBE_SHA256=272f6ebc634a63d9c8b4ca68e964119d980f25154e5aa2c35e5487da48e9a58f \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME" \
  "$PY" -B -m pytest -o addopts= -p no:cacheprovider \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_d13_installed_native_preflight -q
COLLECTED="$(env -i \
  HOME="$RUN_ROOT/home" LANG=C.UTF-8 LC_ALL=C.UTF-8 \
  PATH="$(dirname "$NODE"):/usr/bin:/bin" \
  PYTHONDONTWRITEBYTECODE=1 TMPDIR="$RUN_ROOT/tmp" XDG_RUNTIME_DIR="$RUN_ROOT/tmp" \
  ASTRID_HOST_EXECUTION_PROFILE=installed ASTRID_PACK_HOST_PYTHON="$PY" \
  ASTRID_PACKS_PATH="$SITE/astrid/packs/rendering" ASTRID_REMOTION_PROJECT_DIR="$REMOTION" \
  ASTRID_REMOTION_BROWSER_EXECUTABLE=/opt/pw-browsers/chromium-1194/chrome-linux/chrome \
  ASTRID_NODE_EXECUTABLE="$NODE" ASTRID_TEST_NODE_MODULES="$REMOTION/node_modules" \
  ASTRID_FFMPEG_EXECUTABLE=/usr/bin/ffmpeg ASTRID_FFPROBE_EXECUTABLE=/usr/bin/ffprobe \
  ASTRID_TIMELINE_SCHEMA_PYTHONPATH="$SITE" ASTRID_RUNTIME_SOURCE_MANIFEST="$PROFILE" \
  ASTRID_D13_SOURCE_PROFILE="$PROFILE" ASTRID_D13_EXPECTED_BINDINGS="$BINDINGS" \
  ASTRID_RUNTIME_CHECKOUT="$RUNTIME" "$PY" -B -m pytest -o addopts= -p no:cacheprovider \
  tests/packs/video_editing/test_runtime_publication_chain.py::test_daemon_backed_host_executes_authoring_and_final_render \
  --collect-only -q)"
printf '%s\n' "$COLLECTED"
test "$(printf '%s\n' "$COLLECTED" | sed -nE 's/^([0-9]+) test collected.*/\1/p' | tail -1)" = 1
```

The actual later proof replaces only the final `--collect-only -q` collection
command with the original exact target invocation. The original proof body and
assertions are not changed by this worker.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/d13-review-bindings-pytest tests/packs/video_editing/test_d13_bindings.py`: **3 passed**.
- `/home/user/work/venv-agent/bin/python -m ruff check tests/packs/video_editing/d13_bindings.py tests/packs/video_editing/test_d13_bindings.py`: **passed**.
- `git diff --check`: **passed**.
- Exact named native selector with the approved private interpreter and
  `env -i`, `--collect-only -q`: **1 test collected in 0.92s**. No fixture body,
  Runtime, daemon, HTTP, socket, browser, renderer, native proof, or full
  suite ran.
- `source_archive_matches_checkout(...)` against
  `/home/user/work/wt/agt-pin-f4edcb4b` for f4ed/tree `1cbd1801...1208e6`:
  **[]**.

Tracked changes are limited to:

- `tests/packs/video_editing/d13_bindings.py`
- `tests/packs/video_editing/test_d13_bindings.py`

