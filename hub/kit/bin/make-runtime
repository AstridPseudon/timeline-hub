#!/bin/bash
# make-runtime NAME AGENT_SHA [LOCK_SHA256] — host dispatcher builder.
# The public API is unchanged; only the host-selected exact Node toolchain may
# run npm ci, and every runtime is published once under a new immutable name.
set -u -o pipefail

O=${RUNTIME_ORCH_ROOT:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
A=${RUNTIME_AGENT_CHECKOUT:-/home/user/work/agent}
W=${RUNTIME_WORK_ROOT:-/home/user/work}
NODE_BIN=${RUNTIME_NODE_BIN:-}
NODE_VERSION=20.19.4
NPM_VERSION=10.8.2

N=${1:-}
S=${2:-}
L=${3:-}
case "$N" in
  agent-remotion-[0-9a-z-]*) ;;
  *) echo "REFUSED: name must be agent-remotion-<version>"; exit 2 ;;
esac
[ -n "$S" ] || { echo "REFUSED: agent commit is required"; exit 2; }

D=$W/runtimes/$N
if [ -e "$D" ] || [ -L "$D" ]; then
  echo "exists: $D (runtimes are immutable; pick a new name)"
  exit 0
fi

# Do not use ambient Node 22 (or an unpinned Node 20). A host dispatcher may
# select another exact path through RUNTIME_NODE_BIN.
if [ -z "$NODE_BIN" ]; then
  for candidate in \
    "$W/toolchain/node-v$NODE_VERSION-linux-x64/bin" \
    "/opt/node-v$NODE_VERSION-linux-x64/bin" \
    "/opt/node$NODE_VERSION/bin"; do
    if [ -x "$candidate/node" ] && [ -x "$candidate/npm" ]; then
      NODE_BIN=$candidate
      break
    fi
  done
fi

missing=()
require_command() { command -v "$1" >/dev/null 2>&1 || missing+=("command:$1"); }
for command_name in git tar sha256sum cut grep find mkdir mv chmod df awk; do
  require_command "$command_name"
done
[ -d "$W" ] || missing+=("directory:$W")
[ -d "$W/runtimes" ] || missing+=("directory:$W/runtimes")
[ -d "$A" ] || missing+=("directory:$A")
[ -d "$O/tests" ] || missing+=("directory:$O/tests")
[ -w "$O/tests" ] || missing+=("writable:$O/tests")
[ -r "$O/tests/agent-remotion-0012.env" ] || missing+=("template:$O/tests/agent-remotion-0012.env")
[ -w "$O/tests/suites.conf" ] || missing+=("writable:$O/tests/suites.conf")
[ -n "$NODE_BIN" ] || missing+=("exact-toolchain:Node-$NODE_VERSION/npm-$NPM_VERSION")
[ -x "${NODE_BIN:-/nonexistent}/node" ] || missing+=("executable:${NODE_BIN:-unset}/node")
[ -x "${NODE_BIN:-/nonexistent}/npm" ] || missing+=("executable:${NODE_BIN:-unset}/npm")

NODE_ACTUAL=
NPM_ACTUAL=
if [ -x "${NODE_BIN:-/nonexistent}/node" ]; then
  NODE_ACTUAL=$("$NODE_BIN/node" --version 2>/dev/null || true)
fi
if [ -x "${NODE_BIN:-/nonexistent}/npm" ]; then
  NPM_ACTUAL=$(PATH="$NODE_BIN:$PATH" "$NODE_BIN/npm" --version 2>/dev/null || true)
fi
[ "$NODE_ACTUAL" = "v$NODE_VERSION" ] || missing+=("node-version:expected=v$NODE_VERSION actual=${NODE_ACTUAL:-unavailable}")
[ "$NPM_ACTUAL" = "$NPM_VERSION" ] || missing+=("npm-version:expected=$NPM_VERSION actual=${NPM_ACTUAL:-unavailable}")

if ! git -C "$A" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  missing+=("agent-checkout:$A")
fi
if ! git -C "$A" cat-file -e "$S^{commit}" >/dev/null 2>&1; then
  missing+=("agent-commit:$S")
fi
if ! git -C "$A" cat-file -e "$S:remotion/package-lock.json" >/dev/null 2>&1; then
  missing+=("agent-lock:$S:remotion/package-lock.json")
fi
if ! git -C "$A" cat-file -e "$S:remotion/package.json" >/dev/null 2>&1; then
  missing+=("agent-package:$S:remotion/package.json")
fi
if ! df -P -B1 "$W" >/dev/null 2>&1; then
  missing+=("disk:$W")
fi
DISK_AVAILABLE_BYTES=$(df -P -B1 "$W" 2>/dev/null | awk 'NR == 2 { print $4 }')

LOCK_SHA=
if git -C "$A" cat-file -e "$S:remotion/package-lock.json" >/dev/null 2>&1; then
  LOCK_SHA=$(git -C "$A" show "$S:remotion/package-lock.json" | sha256sum | cut -d' ' -f1)
  if [ -n "$L" ] && [ "$LOCK_SHA" != "$L" ]; then
    missing+=("lock-sha256:expected=$L actual=$LOCK_SHA")
  fi
fi

if [ "${#missing[@]}" -ne 0 ]; then
  printf '%s runtime PREFLIGHT FAILED name=%s agent=%s expected_node=v%s expected_npm=%s\n' \
    "$(date -u +%FT%TZ)" "$N" "$S" "$NODE_VERSION" "$NPM_VERSION" >&2
  printf 'inventory=node:%s npm:%s lock_sha256:%s free_bytes:%s\n' \
    "${NODE_ACTUAL:-unavailable}" "${NPM_ACTUAL:-unavailable}" \
    "${LOCK_SHA:-unavailable}" "${DISK_AVAILABLE_BYTES:-unavailable}" >&2
  printf 'missing_prerequisite=%s\n' "${missing[@]}" >&2
  exit 2
fi

RUN_ID=$(date -u +%Y%m%dT%H%M%SZ)-$$
T=$D.partial.$RUN_ID
mkdir -p "$T"

if ! git -C "$A" archive "$S" remotion | tar -x -C "$T" --strip-components=1; then
  printf 'status=failed\nstage=archive\nagent_sha=%s\nlock_sha256=%s\npartial=%s\n' \
    "$S" "$LOCK_SHA" "$T" > "$T/.provision-failure" 2>/dev/null || true
  echo "archive failed (partial retained: $T)" >&2
  exit 1
fi
if ! ( cd "$T" && PATH="$NODE_BIN:$PATH" "$NODE_BIN/npm" ci --no-audit --no-fund --loglevel=error ); then
  printf 'status=failed\nstage=npm-ci\nagent_sha=%s\nlock_sha256=%s\nnode=%s\nnpm=%s\npartial=%s\n' \
    "$S" "$LOCK_SHA" "$NODE_ACTUAL" "$NPM_ACTUAL" "$T" > "$T/.provision-failure"
  echo "npm ci failed (partial retained: $T)" >&2
  exit 1
fi

printf '%s\n' "$S" > "$T/.astrid-agent-source-commit"
printf '%s\n' "$LOCK_SHA" > "$T/.astrid-package-lock-sha256"
printf '%s\n' "$NODE_ACTUAL" > "$T/.astrid-node-version"
printf '%s\n' "$NPM_ACTUAL" > "$T/.astrid-npm-version"
{
  printf 'remotion=%s\n' "$(cd "$T" && PATH="$NODE_BIN:$PATH" "$NODE_BIN/node" -e "console.log(require('./node_modules/remotion/package.json').version)")"
  printf 'timeline_composition=%s\n' "$(cd "$T" && PATH="$NODE_BIN:$PATH" "$NODE_BIN/node" -e "console.log(require('./node_modules/@banodoco/timeline-composition/package.json').version)")"
  printf 'package_lock_sha256=%s\n' "$LOCK_SHA"
} > "$T/.astrid-installed-module-origins"
find "$T" \( -path '*/node_modules/.cache' -o -path '*/node_modules/.vite*' \) -prune -o -type f -exec chmod a-w {} +

if [ -e "$D" ] || [ -L "$D" ]; then
  printf 'status=failed\nstage=immutable-publish-race\nagent_sha=%s\nlock_sha256=%s\npartial=%s\n' \
    "$S" "$LOCK_SHA" "$T" > "$T/.provision-failure"
  echo "REFUSED: destination appeared during build; partial retained: $T" >&2
  exit 1
fi
mv -T "$T" "$D"

sed "s#agent-remotion-0012#$N#g" "$O/tests/agent-remotion-0012.env" > "$O/tests/$N.env"
grep -q "^agent $N-nodes " "$O/tests/suites.conf" || grep '^agent remotion-0012-nodes ' "$O/tests/suites.conf" | sed "s#remotion-0012-nodes#$N-nodes#; s#agent-remotion-0012#$N#g" >> "$O/tests/suites.conf"
echo "created $D from agent ${S:0:12} (lock $LOCK_SHA, node $NODE_ACTUAL/npm $NPM_ACTUAL), read-only; env tests/$N.env; suite '$N-nodes'; remotion $(PATH="$NODE_BIN:$PATH" "$NODE_BIN/node" -e "console.log(require('$D/node_modules/remotion/package.json').version)" 2>/dev/null)"
