#!/usr/bin/env bash
set -eu

GRAPH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph
SOURCE_ARCHIVE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph-source.tar
PROBE=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-ap2-m2-locked-graph-probe.ts
EXPECTED_SOURCE_SHA256=895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
EXPECTED_COMPOSITION_SHA256=9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738

test -d "$GRAPH/node_modules"
test -f "$SOURCE_ARCHIVE"
test -f "$PROBE"
test "$(sha256sum "$SOURCE_ARCHIVE" | cut -d' ' -f1)" = "$EXPECTED_SOURCE_SHA256"

RUN=$(mktemp -d /tmp/app-ap2-m2-locked-run.XXXXXX)
trap 'find -P "$RUN" -type f -exec unlink {} \; 2>/dev/null || true; find -P "$RUN" -type l -exec unlink {} \; 2>/dev/null || true; find -P "$RUN" -depth -type d -exec rmdir {} \; 2>/dev/null || true' EXIT
mkdir -p "$RUN/tmp" "$RUN/.vite-temp" "$RUN/xdg-cache" "$RUN/npm-cache"
tar -xf "$SOURCE_ARCHIVE" -C "$RUN"
test "$(sha256sum "$RUN/vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz" | cut -d' ' -f1)" = "$EXPECTED_COMPOSITION_SHA256"
test "$(node -p "require('$GRAPH/node_modules/@banodoco/timeline-composition/package.json').version")" = 0.0.13
ln -s "$GRAPH/node_modules" "$RUN/node_modules"
cp "$PROBE" "$RUN/app-ap2-m2-locked-graph-probe.ts"

export TMPDIR="$RUN/tmp"
export VITE_CACHE_DIR="$RUN/.vite-temp"
export XDG_CACHE_HOME="$RUN/xdg-cache"
export npm_config_cache="$RUN/npm-cache"
cd "$RUN"

set +e
NODE_OPTIONS=--max-old-space-size=4096 node "$GRAPH/node_modules/typescript/bin/tsc" --noEmit --pretty false -p tsconfig.app.json > "$RUN/tsc.log" 2>&1
TSC_STATUS=$?
node --import "$GRAPH/node_modules/tsx/dist/loader.mjs" "$RUN/app-ap2-m2-locked-graph-probe.ts"
PROBE_STATUS=$?
set -e

printf 'source_archive_sha256=%s\n' "$EXPECTED_SOURCE_SHA256"
printf 'tsc_status=%s\n' "$TSC_STATUS"
printf 'ordinary_probe_status=%s\n' "$PROBE_STATUS"
if [ "$TSC_STATUS" -ne 0 ]; then
  printf '%s\n' 'tsc_diagnostics:'
  sed -n '1,240p' "$RUN/tsc.log"
fi

if [ "$TSC_STATUS" -ne 0 ]; then exit "$TSC_STATUS"; fi
exit "$PROBE_STATUS"
