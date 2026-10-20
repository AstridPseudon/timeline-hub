#!/usr/bin/env bash
set -euo pipefail

# Test-service wrapper for the one post-root-merge App full.  It owns only the
# snapshot's dependency root and caches; the private12 graph and all source
# inputs are read-only.  The full mode is deliberately manager-gated.

ROOT=$(pwd -P)
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)
PRIVATE12_NODE_MODULES=${PRIVATE12_NODE_MODULES:-/tmp/app-coherent-deps12/node_modules}
PRELOAD=${TIMELINE_SNAPSHOT_PRELOAD:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs}
LOG_DIR=${TIMELINE_ROOT_FULL_LOG_DIR:-"/tmp/timeline-app-root-full-${PPID}"}

die() { echo "app-root-full-environment: $*" >&2; exit 2; }
[[ -f "$ROOT/package.json" && -e "$ROOT/.git" ]] || die "run from an App test-service snapshot";
[[ -d "$PRIVATE12_NODE_MODULES" ]] || die "missing verified private12 graph: $PRIVATE12_NODE_MODULES";
[[ -f "$PRELOAD" ]] || die "missing Vitest preload: $PRELOAD";

mkdir -p "$LOG_DIR"
export TMPDIR=${TMPDIR:-"$LOG_DIR/tmp"}
export npm_config_cache=${npm_config_cache:-"$LOG_DIR/npm-cache"}
export VITEST_CACHE_DIR=${VITEST_CACHE_DIR:-"$LOG_DIR/vitest-cache"}
export XDG_CACHE_HOME=${XDG_CACHE_HOME:-"$LOG_DIR/xdg-cache"}
mkdir -p "$TMPDIR" "$npm_config_cache" "$VITEST_CACHE_DIR" "$XDG_CACHE_HOME"
unset ASTRID_PUBLIC_CHECKOUT ASTRID_APP_DIRECT_DIST

ORIGINAL_NODE_MODULES_LINK=''
OVERLAY_CREATED=0
if [[ -L "$ROOT/node_modules" ]]; then
  ORIGINAL_NODE_MODULES_LINK=$(readlink "$ROOT/node_modules")
elif [[ -e "$ROOT/node_modules" ]]; then
  die "refusing to replace a real node_modules directory: $ROOT/node_modules"
fi
restore_overlay() {
  if [[ "$OVERLAY_CREATED" != 1 ]]; then return; fi
  rm -rf "$ROOT/node_modules"
  if [[ -n "$ORIGINAL_NODE_MODULES_LINK" ]]; then
    ln -s "$ORIGINAL_NODE_MODULES_LINK" "$ROOT/node_modules"
  fi
}
trap restore_overlay EXIT

snapshot() {
  python3 - "$ROOT" "$PRIVATE12_NODE_MODULES" "$LOG_DIR/$1.json" <<'PY'
import hashlib
import json
import os
import pathlib
import subprocess
import sys

root = pathlib.Path(sys.argv[1])
private = pathlib.Path(sys.argv[2])
out = pathlib.Path(sys.argv[3])

def git(*args, cwd=root):
    return subprocess.check_output(['git', '-C', str(cwd), *args], text=True).strip()

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def external(name, value):
    if not value:
        return {'path': None}
    path = pathlib.Path(value)
    item = {'path': str(path)}
    if not path.is_absolute() or not path.is_dir():
        item['error'] = 'missing-or-not-absolute'
        return item
    try:
        item.update(head=git('rev-parse', 'HEAD', cwd=path), tree=git('rev-parse', 'HEAD^{tree}', cwd=path),
                    status=git('status', '--porcelain=v1', '--untracked-files=normal', cwd=path))
    except subprocess.CalledProcessError as error:
        item['error'] = f'git:{error.returncode}'
    return item

package = json.loads((root / 'package.json').read_text())
lock = json.loads((root / 'runtime.lock.json').read_text())
provenance = json.loads((root / 'vendor/astrid-browser/provenance.json').read_text())
result = {
    'app': {
        'head': git('rev-parse', 'HEAD'),
        'tree': git('rev-parse', 'HEAD^{tree}'),
        'status': git('status', '--porcelain=v1', '--untracked-files=normal'),
        'sparseCheckout': subprocess.run(['git', '-C', str(root), 'config', '--get', 'core.sparseCheckout'], text=True, capture_output=True).stdout.strip() or None,
        'packageSha256': sha(root / 'package.json'),
        'packageLockSha256': sha(root / 'package-lock.json'),
        'runtimeLockSha256': sha(root / 'runtime.lock.json'),
    },
    'package': {
        'composition': package['dependencies']['@banodoco/timeline-composition'],
        'compositionVersion': json.loads((private / '@banodoco/timeline-composition/package.json').read_text())['version'],
        'compositionArchiveSha256': sha(root / 'vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz'),
        'runtimeSourceCommit': lock['source_commit'],
        'runtimeProducerVersion': lock['producer_version'],
    },
    'publicBrowserBundle': {
        'astridCommit': provenance['astrid_commit'],
        'astridTree': provenance['astrid_tree'],
        'provenanceSha256': sha(root / 'vendor/astrid-browser/provenance.json'),
        'files': len(provenance['files']),
        'ASTRID_PUBLIC_CHECKOUT': os.environ.get('ASTRID_PUBLIC_CHECKOUT'),
    },
    'external': {
        'ASTRID_CHECKOUT': external('agent', os.environ.get('ASTRID_CHECKOUT')),
        'ASTRID_RUNTIME_CHECKOUT': external('runtime', os.environ.get('ASTRID_RUNTIME_CHECKOUT')),
        'TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT': external('runtime-producer', os.environ.get('TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT')),
        'expectedAgentSha': os.environ.get('TIMELINE_ROOT_FULL_AGENT_SHA'),
        'expectedRuntimeSha': os.environ.get('TIMELINE_ROOT_FULL_RUNTIME_SHA'),
    },
    'private12NodeModules': str(private),
}
out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
print(json.dumps(result, indent=2, sort_keys=True))
PY
}

verify_private12() {
  python3 - "$ROOT" "$PRIVATE12_NODE_MODULES" <<'PY'
import hashlib
import json
import pathlib
import sys
import tarfile

root, target = map(pathlib.Path, sys.argv[1:])
archive = root / 'vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz'
assert hashlib.sha256(archive.read_bytes()).hexdigest() == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
installed = target / '@banodoco/timeline-composition'
with tarfile.open(archive, 'r:gz') as tar:
    members = [member for member in tar.getmembers() if member.isfile()]
    assert len(members) == 77, len(members)
    names = set()
    for member in members:
        relative = pathlib.Path(member.name).relative_to('package')
        assert not relative.is_absolute() and '..' not in relative.parts
        names.add(str(relative))
        assert (installed / relative).read_bytes() == tar.extractfile(member).read(), member.name
assert {str(path.relative_to(installed)) for path in installed.rglob('*') if path.is_file()} == names
for name, version in {
    'react': '18.3.1', 'react-dom': '18.3.1', 'remotion': '4.0.509',
    '@remotion/player': '4.0.509', '@remotion/three': '4.0.509',
    '@remotion/layout-utils': '4.0.509', '@remotion/media': '4.0.509',
}.items():
    assert json.loads((target / name / 'package.json').read_text())['version'] == version, name
print('private12 Composition archive: 77/77 bytes; React/Remotion peers: fixed')
PY
}

make_overlay() {
  local modules="$ROOT/node_modules"
  if [[ -L "$modules" ]]; then
    unlink "$modules"
  elif [[ -e "$modules" ]]; then
    die "refusing to replace a real node_modules directory: $modules"
  fi
  mkdir "$modules"
  OVERLAY_CREATED=1
  touch "$modules/.timeline-root-full-overlay"
  while IFS= read -r -d '' entry; do
    local name=${entry##*/}
    [[ "$name" == .vite || "$name" == .vite-temp || "$name" == .timeline-root-full-overlay ]] && continue
    if [[ "$name" == @* || "$name" == .bin ]]; then
      local scope="$modules/$name"
      mkdir "$scope"
      while IFS= read -r -d '' child; do
        ln -s "$(readlink -f "$child")" "$scope/${child##*/}"
      done < <(find "$entry" -mindepth 1 -maxdepth 1 -print0 | sort -z)
    else
      ln -s "$(readlink -f "$entry")" "$modules/$name"
    fi
  done < <(find "$PRIVATE12_NODE_MODULES" -mindepth 1 -maxdepth 1 -print0 | sort -z)
  mkdir "$modules/.vite" "$modules/.vite-temp"
}

run_vitest() {
  env -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_CHECKOUT \
    NODE_OPTIONS="${NODE_OPTIONS:+$NODE_OPTIONS }--require=$PRELOAD" \
    node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts \
    --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism "$@"
}

preflight() {
  verify_private12
  make_overlay
  snapshot preflight-before
  node config/vite/timelineCompositionPackage.test.mjs
  run_vitest src/tools/video-editor/compositions/TimelineComposition.media-conformance.test.tsx
  run_vitest src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/components/TimelineEditor/TrackLabel.command.test.tsx
  snapshot preflight-after
  cmp "$LOG_DIR/preflight-before.json" "$LOG_DIR/preflight-after.json"
  echo 'bounded offline preflight passed; source/pins/external tuple unchanged'
}

full() {
  [[ ${TIMELINE_ROOT_FULL_MANAGER_APPROVED:-} == 1 ]] || die 'full mode is manager-owned; set TIMELINE_ROOT_FULL_MANAGER_APPROVED=1'
  for name in TIMELINE_ROOT_FULL_APP_SHA TIMELINE_ROOT_FULL_APP_TREE TIMELINE_ROOT_FULL_AGENT_SHA TIMELINE_ROOT_FULL_AGENT_TREE TIMELINE_ROOT_FULL_RUNTIME_SHA TIMELINE_ROOT_FULL_RUNTIME_TREE; do
    [[ ${!name:-} =~ ^[0-9a-f]{40}$ ]] || die "$name must be a literal manager-supplied commit"
  done
  [[ $(git -C "$ROOT" rev-parse HEAD) == "$TIMELINE_ROOT_FULL_APP_SHA" ]] || die 'App HEAD does not match manager pin'
  [[ $(git -C "$ROOT" rev-parse HEAD^{tree}) == "$TIMELINE_ROOT_FULL_APP_TREE" ]] || die 'App tree does not match manager pin'
  [[ -z $(git -C "$ROOT" status --porcelain=v1 --untracked-files=normal) ]] || die 'full snapshot App source is not clean'
  [[ -n ${ASTRID_CHECKOUT:-} && -n ${ASTRID_RUNTIME_CHECKOUT:-} && -n ${TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT:-} ]] || die 'manager must bind exact Agent, Runtime, and producer checkouts'
  [[ -z $(git -C "$ASTRID_CHECKOUT" status --porcelain=v1 --untracked-files=normal) ]] || die 'Agent checkout is not clean'
  [[ -z $(git -C "$ASTRID_RUNTIME_CHECKOUT" status --porcelain=v1 --untracked-files=normal) ]] || die 'Runtime checkout is not clean'
  [[ -z $(git -C "$TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT" status --porcelain=v1 --untracked-files=normal) ]] || die 'Runtime producer checkout is not clean'
  [[ $(git -C "$ASTRID_CHECKOUT" rev-parse HEAD) == "$TIMELINE_ROOT_FULL_AGENT_SHA" ]] || die 'ASTRID_CHECKOUT HEAD does not match manager pin'
  [[ $(git -C "$ASTRID_CHECKOUT" rev-parse HEAD^{tree}) == "$TIMELINE_ROOT_FULL_AGENT_TREE" ]] || die 'ASTRID_CHECKOUT tree does not match manager pin'
  [[ $(git -C "$ASTRID_RUNTIME_CHECKOUT" rev-parse HEAD) == "$TIMELINE_ROOT_FULL_RUNTIME_SHA" ]] || die 'ASTRID_RUNTIME_CHECKOUT HEAD does not match manager pin'
  [[ $(git -C "$ASTRID_RUNTIME_CHECKOUT" rev-parse HEAD^{tree}) == "$TIMELINE_ROOT_FULL_RUNTIME_TREE" ]] || die 'ASTRID_RUNTIME_CHECKOUT tree does not match manager pin'
  [[ $(git -C "$TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT" rev-parse HEAD) == "$TIMELINE_ROOT_FULL_RUNTIME_SHA" ]] || die 'Runtime producer HEAD does not match manager pin'
  [[ $(git -C "$TIMELINE_CURRENT013_RUNTIME_PRODUCER_CHECKOUT" rev-parse HEAD^{tree}) == "$TIMELINE_ROOT_FULL_RUNTIME_TREE" ]] || die 'Runtime producer tree does not match manager pin'
  [[ $(python3 -c 'import json; print(json.load(open("runtime.lock.json"))["source_commit"])') == "$TIMELINE_ROOT_FULL_RUNTIME_SHA" ]] || die 'App runtime.lock.json does not name manager Runtime pin'
  verify_private12
  make_overlay
  snapshot full-before
  env NODE_OPTIONS="${NODE_OPTIONS:+$NODE_OPTIONS }--require=$PRELOAD" \
    npm test -- --maxWorkers=2 --configLoader=runner --no-cache
  snapshot full-after
  cmp "$LOG_DIR/full-before.json" "$LOG_DIR/full-after.json"
  echo 'full suite passed; source/pins/external tuple unchanged'
}

case "${1:-preflight}" in
  preflight) preflight ;;
  full) full ;;
  *) die "usage: $0 {preflight|full}" ;;
esac
