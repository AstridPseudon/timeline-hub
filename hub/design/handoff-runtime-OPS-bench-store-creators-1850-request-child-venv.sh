#!/bin/bash
# request-child-venv NAME AGENT_SHA [BASE_SUITE REMOTION_GRAPH]
# Child store key retains exact Agent + backend + generated client custody.
set -u -o pipefail
O=${CHILD_VENV_ORCH_ROOT:-/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch}
W=${CHILD_VENV_WORK_ROOT:-/home/user/work}
A=${CHILD_VENV_AGENT_CHECKOUT:-/home/user/work/agent}
R=${CHILD_VENV_RUNTIME_CHECKOUT:-/home/user/work/runtime}
N=${1:-}; S=${2:-}; BS=${3:-}; REMOTION=${4:-}
refuse() { echo "REFUSED: $*" >&2; exit 2; }
case "$O:$W:$A:$R" in /*:/*:/*:/*) ;; *) refuse 'roots must be absolute';; esac
[[ "$N" =~ ^venv-agent-child-[a-z0-9-]+$ ]] || refuse 'invalid child name'
[[ "$S" =~ ^[0-9a-f]{40}$ ]] || refuse 'exact 40-character Agent commit required'
[ "$#" -le 4 ] || refuse 'call shape is NAME AGENT_SHA [BASE_SUITE REMOTION_GRAPH]'
source_state() {
  local checkout=$1 wanted=$2 actual status
  actual=$(git -C "$checkout" rev-parse --verify HEAD^{commit} 2>/dev/null) || return 1
  [ "$actual" = "$wanted" ] || return 1
  status=$(git -C "$checkout" status --porcelain --untracked-files=all 2>/dev/null) || return 1
  [ -z "$status" ]
}
source_state "$A" "$S" || refuse 'requested Agent checkout/commit is unavailable, mismatched or dirty'
RUNTIME_SHA=$(git -C "$R" rev-parse --verify HEAD^{commit} 2>/dev/null) || refuse 'Runtime source unavailable'
source_state "$R" "$RUNTIME_SHA" || refuse 'Runtime checkout is dirty'
CLIENT_IDENTITY=$(git -C "$R" ls-tree -r --name-only "$RUNTIME_SHA" packages/python/astrid_runtime_client/ | while IFS= read -r path; do
  [ -n "$path" ] || continue; printf '%s=' "$path"; git -C "$R" show "$RUNTIME_SHA:$path" | sha256sum | cut -d' ' -f1
done) || refuse 'client source unavailable'
[ -n "$CLIENT_IDENTITY" ] || refuse 'generated Runtime client identity is incomplete'
# The installed dispatcher uses word splitting, not eval. Keep this exact legacy payload unquoted.
for arg in "$@"; do [[ "$arg" =~ ^[a-zA-Z0-9_-]+$ ]] || refuse 'dispatcher arguments must be simple names'; done
printf 'CHILDVENV %s %s%s%s\n' "$N" "$S" "${BS:+ $BS}" "${REMOTION:+ $REMOTION}" > "$O/queue/pending/childvenv-$N"
echo "child venv $N queued; result in $O/queue/done/childvenv-$N"
