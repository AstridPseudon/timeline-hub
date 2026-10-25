#!/usr/bin/env bash
set -euo pipefail

# D141/D54a pristine comparator.  This is a preparation artifact only; the
# worker did not execute it.  The controller must bind normal lead checkout
# receipts and the supported external launcher/manifest inputs before use.

EVIDENCE_ROOT=${EVIDENCE_ROOT:-"$(cd -- "$(dirname -- "$0")" && pwd)"}
ORCH=${ORCH:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
PYTHON=${PYTHON:-/home/user/work/venv-agent/bin/python}
NODE=${NODE:-/home/user/work/toolchain/node-v20.19.4-linux-x64/bin/node}
PROFILE=${PROFILE:-/home/user/work/runtimes/agent-remotion-v3-819acf-1110}
SCHEMA=${SCHEMA:-/home/user/work/venv-agent/lib/python3.13/site-packages}
START_BYTES=4700000000
STOP_BYTES=4000000000

AGENT_SHA=8b6ed2116fd1803d24b2be5bc08bd9490407fe4a
AGENT_TREE=0a3691a49b63fd7b0c22fb3478e9cf1947f266ed
RUNTIME_SHA=fa9cd5464a8b37b02f971de375e56be846cd69e2
RUNTIME_TREE=124e10dbcd54fb90219e783ec11aa34f8c91590c
APP_SHA=7ca61bb3280beca21d98a854af266a382f7ce5df
APP_TREE=974de7cd08900872eeb0bd6f6004d44323e01fab
COMPOSITION_SHA=67b8aa3d0d6831d3e3504a340ff583c3da253707
COMPOSITION_TREE=62f4456b71234a9d4d4ad9e2aa58cf7fe0de1120

: "${AGENT_CHECKOUT:?bind a normal lead checkout receipt path}"
: "${RUNTIME_CHECKOUT:?bind a normal lead checkout receipt path}"
: "${APP_CHECKOUT:?bind a normal lead checkout receipt path}"
: "${COMPOSITION_CHECKOUT:?bind a normal lead checkout receipt path}"
: "${PRISTINE_LAUNCHER:?bind a supported external launcher; no launcher is in pristine Agent}"
: "${PRISTINE_MANIFEST_GENERATOR:?bind the supported external manifest-maker source}"
: "${POSITIVE_MANIFEST:?bind the freshly generated positive manifest}"
: "${POISON_MANIFEST:?bind its fresh agent_sha=40zero comparison}"
: "${CONTROL_STUB:?bind the retained 2234 stub}"
: "${POSITIVE_COUNTER:?bind a fresh positive counter}"
: "${POISON_COUNTER:?bind a fresh poison counter}"

errors=0
fail() { printf 'NOT_READY: %s\n' "$*" >&2; errors=$((errors + 1)); }
check_eq() { local actual=$1 expected=$2 label=$3; test "$actual" = "$expected" || fail "$label (actual=$actual expected=$expected)"; }
check_file() { test -f "$1" || fail "missing file: $1"; }
check_dir() { test -d "$1" || fail "missing directory: $1"; }

for pair in \
  "agent:$AGENT_CHECKOUT:$AGENT_SHA:$AGENT_TREE:https://github.com/peteromallet/astrid-agent" \
  "runtime:$RUNTIME_CHECKOUT:$RUNTIME_SHA:$RUNTIME_TREE:https://github.com/banodoco/banodoco-workspace-runtime" \
  "app:$APP_CHECKOUT:$APP_SHA:$APP_TREE:https://github.com/banodoco/reigh-app" \
  "composition:$COMPOSITION_CHECKOUT:$COMPOSITION_SHA:$COMPOSITION_TREE:https://github.com/peteromallet/timeline-composition"; do
  IFS=: read -r name path sha tree origin <<<"$pair"
  check_dir "$path"
  if test -d "$path"; then
    check_eq "$(git -C "$path" rev-parse HEAD 2>/dev/null || true)" "$sha" "$name commit"
    check_eq "$(git -C "$path" rev-parse HEAD^{tree} 2>/dev/null || true)" "$tree" "$name tree"
    check_eq "$(git -C "$path" remote get-url origin 2>/dev/null || true)" "$origin" "$name origin"
    test -z "$(git -C "$path" status --porcelain --untracked-files=all 2>/dev/null || true)" || fail "$name checkout is dirty"
  fi
done

# The immutable frozen source must be the exact upstream checkout.  This list
# is deliberately the same 22 selector roots as agent-core-full.
ROOTS=(
  tests/editing_conformance
  tests/sdk
  tests/timeline
  tests/core/timeline
  tests/core/test_timeline_element_orphan_cleanup.py
  tests/core/test_timeline_element_publication.py
  tests/core/test_timeline_element_publication_runtime.py
  tests/core/rendering/test_timeline_visualize_cli_grammar.py
  tests/core/rendering/test_local_schema.py
  tests/packs/timeline
  tests/packs/rendering/test_composition_package.py
  tests/packs/rendering/test_live_scene_composition.py
  tests/packs/rendering/test_render_export_task_adapter.py
  tests/packs/rendering/test_timeline_filmstrip_cards.py
  tests/packs/rendering/test_timeline_filmstrip_execution.py
  tests/packs/video_editing/test_runtime_publication_chain.py
  tests/stage1/test_cold_launch_autobootstrap.py
  tests/test_installer_schema.py
  tests/test_installer_sources.py
  tests/test_installer_bootstrap_schema.py
  tests/test_timeline_clip_replacement.py
  tests/v10/test_timelines_create.py
)
test "${#ROOTS[@]}" = 22 || fail 'root inventory is not exactly 22'
for root in "${ROOTS[@]}"; do test -e "$AGENT_CHECKOUT/$root" || fail "pristine root absent: $root"; done

check_file "$PRISTINE_LAUNCHER"
check_file "$PRISTINE_MANIFEST_GENERATOR"
check_file "$POSITIVE_MANIFEST"
check_file "$POISON_MANIFEST"
check_file "$CONTROL_STUB"
test "$(sha256sum "$CONTROL_STUB" 2>/dev/null | awk '{print $1}')" = 38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0 || fail '2234 control stub hash mismatch'
test "$(sha256sum "$PRISTINE_LAUNCHER" 2>/dev/null | awk '{print $1}')" = 9f668e398b1ea4cce48a6c610102723e0a3dab27a764be4191015aa7fc4110cd || fail 'external launcher is not the reviewed D73 source'
test "$(sha256sum "$PRISTINE_MANIFEST_GENERATOR" 2>/dev/null | awk '{print $1}')" = 782fb81cea67ce71b785dd5dbf891bb1d32df74c136425d83d53e938bdf8b51c || fail 'external manifest-maker source is not the reviewed D134 source'

# Report all ordinary dependency/retention inputs before refusing.  No import,
# control, collection, pytest, or provider body is performed here.
check_file "$PYTHON"
check_file "$NODE"
check_dir "$PROFILE"
check_dir "$SCHEMA"
test -e "$PROFILE/node_modules" || fail 'profile node_modules missing'
test -L "$PROFILE/node_modules" && fail 'profile node_modules must be a real directory'
test -e "$PROFILE/package-lock.json" || fail 'profile package-lock missing'
test -e "$PROFILE/.astrid-registry-state.json" || fail 'profile registry state missing'

mkdir -p "$EVIDENCE_ROOT/preflight" "$EVIDENCE_ROOT/raw" "$EVIDENCE_ROOT/junit" "$EVIDENCE_ROOT/disk" "$EVIDENCE_ROOT/keep"
{
  printf 'status=%s\n' "$([ "$errors" -eq 0 ] && echo READY || echo NOT_READY)"
  printf 'tuple=PRISTINE\nagent_sha=%s\nruntime_sha=%s\napp_sha=%s\ncomposition_sha=%s\n' "$AGENT_SHA" "$RUNTIME_SHA" "$APP_SHA" "$COMPOSITION_SHA"
  printf 'root_count=%s\nxdist_workers=3\naddopts=\ncache_plugin=disabled\ntimeout_seconds=45\nstart_bytes=%s\nstop_bytes=%s\n' "${#ROOTS[@]}" "$START_BYTES" "$STOP_BYTES"
  printf 'raw_root=%s\njunit_root=%s\ndisk_root=%s\nkeep_root=%s\n' "$EVIDENCE_ROOT/raw" "$EVIDENCE_ROOT/junit" "$EVIDENCE_ROOT/disk" "$EVIDENCE_ROOT/keep"
} > "$EVIDENCE_ROOT/preflight/bindings.txt"
if test "$errors" -ne 0; then
  printf 'NOT_READY with %s finding(s); see preflight-inventory.json and bindings.txt.\n' "$errors" >&2
  exit 1
fi

positive_calls_before=$(wc -l < "$POSITIVE_COUNTER" 2>/dev/null || echo 0)
poison_calls_before=$(wc -l < "$POISON_COUNTER" 2>/dev/null || echo 0)
test "$positive_calls_before" = 0 || fail 'positive counter is not fresh'
test "$poison_calls_before" = 0 || fail 'poison counter is not fresh'

# The controller runs the external generator before this body.  Its generated
# manifests must be field-compared before either launcher call.
"$PYTHON" -P - "$POSITIVE_MANIFEST" "$POISON_MANIFEST" <<'PY'
import sys
from pathlib import Path

def parse(path):
    out = {}
    for line in Path(path).read_text().splitlines():
        if line and not line.startswith('#'):
            key, sep, value = line.partition('=')
            if not sep or key in out:
                raise SystemExit(f'invalid manifest: {path}')
            out[key] = value
    return out

positive = parse(sys.argv[1])
poison = parse(sys.argv[2])
if set(positive) != set(poison):
    raise SystemExit('manifest key sets differ')
for key in positive:
    if key != 'agent_sha' and positive[key] != poison[key]:
        raise SystemExit(f'manifest differs outside agent_sha: {key}')
if poison.get('agent_sha') != '0' * 40:
    raise SystemExit('poison agent_sha is not forty zeroes')
PY

df -Pk "$EVIDENCE_ROOT" > "$EVIDENCE_ROOT/disk/start.df"
date -u +%FT%H:%M:%SZ > "$EVIDENCE_ROOT/disk/start.utc"
set +e
env -i HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  VIRTUAL_ENV=/home/user/work/venv-agent ASTRID_RUNTIME_CHECKOUT="$RUNTIME_CHECKOUT" ASTRID_RUNTIME_SOURCE_ROOT="$RUNTIME_CHECKOUT" \
  P4_D73_MANIFEST="$POSITIVE_MANIFEST" P4_D73_EVIDENCE="$EVIDENCE_ROOT" P4_D73_REQUEST_ID=pristine-comparator \
  "$PRISTINE_LAUNCHER" "$POSITIVE_MANIFEST" run -- \
  -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45 \
  --junitxml="$EVIDENCE_ROOT/junit/pristine-comparator.xml" "${ROOTS[@]}" \
  > >(tee "$EVIDENCE_ROOT/raw/pristine-comparator.log") 2>&1
body_rc=$?
set -e
printf '%s\n' "$body_rc" > "$EVIDENCE_ROOT/raw/body.exit"
date -u +%FT%H:%M:%SZ > "$EVIDENCE_ROOT/disk/stop.utc"
df -Pk "$EVIDENCE_ROOT" > "$EVIDENCE_ROOT/disk/stop.df"
exit "$body_rc"
