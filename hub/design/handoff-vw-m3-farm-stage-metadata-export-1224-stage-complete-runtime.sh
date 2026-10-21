#!/usr/bin/env bash
set -euo pipefail

SOURCE=/home/user/work/runtimes/agent-remotion-viewing13-d0a5072b
CAPSULE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-scenesurface-owned-source-carrier-1028/packet.pnylvl/positive
ROOT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-storage-cleared-complete-runtime-stage-1054/owned-stage
REQUIRED=11714413516
ALLOCATED=394166272

realpath -e "$SOURCE" >/dev/null
realpath -e "$CAPSULE" >/dev/null
if [ -e "$ROOT" ]; then
  echo "refusing to replace existing leased stage: $ROOT" >&2
  exit 1
fi
[ ! -e "$ROOT" ]
free=$(df -B1 --output=avail /tmp | tail -1 | tr -d ' ')
[ "$free" -ge "$REQUIRED" ]
mkdir -p "$ROOT"
[ "$(realpath -e "$ROOT")" = "$ROOT" ]
mkdir -p "$ROOT/remotion"
if ! cp -a --reflink=always "$SOURCE/." "$ROOT/remotion/"; then
  find "$ROOT" -depth -delete
  free=$(df -B1 --output=avail /tmp | tail -1 | tr -d ' ')
  [ "$free" -ge "$REQUIRED" ]
  mkdir -p "$ROOT/remotion"
  cp -a --reflink=never --no-preserve=links "$SOURCE/." "$ROOT/remotion/"
fi
mkdir -p "$ROOT/astrid/packs/rendering/editor/live-scenes"
for name in SceneSurface.tsx authoring.ts diagnostics.ts extension.tsx identity.ts runtime.ts; do
  cp -a --reflink=never --no-preserve=links "$CAPSULE/astrid/packs/rendering/editor/live-scenes/$name" \
      "$ROOT/astrid/packs/rendering/editor/live-scenes/$name"
done

post=$(df -B1 --output=avail /tmp | tail -1 | tr -d ' ')
[ "$post" -ge 11320247244 ]
printf '%s\n' "$ROOT"
