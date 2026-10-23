#!/bin/bash
# request-runtime NAME AGENT_SHA [LOCK_SHA256] — ask the dispatcher to build or
# reuse a read-only Remotion runtime. The maker performs the authenticated
# tree-only lookup before any toolchain/build work.
# /home/user/work/runtimes/NAME (agent-remotion-<version>) from the Agent remotion/ dir at AGENT_SHA. Result in
# $ORCH/queue/done/runtime-NAME. Runtimes are immutable: a new version gets a new NAME. No escalation needed.
if [[ -z "${RUNTIME_ORCH_ROOT:-}" ]]; then
  echo 'REFUSED: RUNTIME_ORCH_ROOT must name the private ORCH root' >&2; exit 2
fi
O=$RUNTIME_ORCH_ROOT
[[ "$O" = /* && "$O" != *[!a-zA-Z0-9_./-]* && "/$O/" != */../* && "/$O/" != */./* ]] || {
  echo 'REFUSED: ORCH root must be a safe absolute path' >&2; exit 2;
}
[[ -d "$O/queue/pending" && -w "$O/queue/pending" ]] || {
  echo 'REFUSED: private pending queue is unavailable' >&2; exit 2;
}
case $# in
  2|3|7) ;;
  *) echo "usage: request-runtime NAME AGENT_SHA [LOCK_SHA256] [AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA TEMPLATE_SUITE]" >&2; exit 2 ;;
esac
[[ "$1" =~ ^agent-remotion-[0-9a-z][0-9a-z-]*$ && "$2" =~ ^[0-9a-f]{40}$ ]] || { echo 'REFUSED: invalid runtime name or Agent SHA' >&2; exit 2; }
if [ "$#" -ge 3 ]; then [[ "$3" =~ ^[0-9a-f]{64}$ ]] || { echo 'REFUSED: invalid lock SHA-256' >&2; exit 2; }; fi
if [ "$#" = 7 ]; then
  for path in "$4" "$5"; do [[ "$path" = /* && "$path" != *[!a-zA-Z0-9_./-]* && "/$path/" != */../* && "/$path/" != */./* ]] || { echo 'REFUSED: unsafe source checkout' >&2; exit 2; }; done
  [[ "$6" =~ ^[0-9a-f]{40}$ ]] || { echo 'REFUSED: invalid Runtime SHA' >&2; exit 2; }
  [[ "$7" = agent-remotion-0013-nodes || "$7" = remotion-env-nodes ]] || { echo 'REFUSED: unapproved registration template' >&2; exit 2; }
fi
{ printf 'RUNTIME'; printf ' %s' "$@"; printf '\n'; } > "$O/queue/pending/runtime-$1"
echo "runtime $1 queued; maker will return reuse or build receipt in $O/queue/done/runtime-$1"
