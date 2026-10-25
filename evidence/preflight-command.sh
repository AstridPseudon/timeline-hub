#!/usr/bin/env bash
set -euo pipefail

# D134 authorized DRY controls only.  The launcher evidence and stdout/stderr
# stay in the caller-owned private directory; only counters and safe fields
# are published in this worktree.
: "${D134_PRIVATE_DIR:?bind a private scratch directory for raw dry output}"
ROOT=$(cd "$(dirname "$0")/.." && pwd)
AGENT_CHECKOUT=/home/user/work/wt/agt-pin-a4e016b6
RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-5e9ad1c6
APP_CHECKOUT=/home/user/work/wt/app-pin-d8a1cd40
COMPOSITION_CHECKOUT=/home/user/work/wt/vw-pin-635f4de0
P4_D73_MANIFEST="$ROOT/evidence/positive.manifest"
P4_D73_POISON_MANIFEST="$ROOT/evidence/poison.manifest"
P4_D73_EVIDENCE="$D134_PRIVATE_DIR/launcher-evidence"
MAIN_POSITIVE_CONTROL=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-core-rehearsal-2234/evidence/positive-stub.sh
mkdir -p "$P4_D73_EVIDENCE"
test "$(sha256sum "$MAIN_POSITIVE_CONTROL" | awk '{print $1}')" = 38afc8a5b177801f86f33b0166c8ecd4489ee997629e91b336b9c248ca360ad0

positive_counter=$(mktemp "$D134_PRIVATE_DIR/positive-counter.XXXXXX")
poison_counter=$(mktemp "$D134_PRIVATE_DIR/poison-counter.XXXXXX")
positive_stdout="$D134_PRIVATE_DIR/positive.stdout"
positive_stderr="$D134_PRIVATE_DIR/positive.stderr"
poison_stdout="$D134_PRIVATE_DIR/poison.stdout"
poison_stderr="$D134_PRIVATE_DIR/poison.stderr"

set +e
env -i \
  HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  VIRTUAL_ENV=/home/user/work/venv-agent \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full-preflight-positive \
  P4_STUB_COUNT="$positive_counter" /bin/bash --noprofile --norc -c \
  'set -eu; test "$(git -C "$0" remote get-url origin)" = https://github.com/peteromallet/astrid-agent; exec "$0/tools/p4-d73-pinned-launch.sh" "$1" dry -- "$2"' \
  "$AGENT_CHECKOUT" "$P4_D73_MANIFEST" "$MAIN_POSITIVE_CONTROL" \
  >"$positive_stdout" 2>"$positive_stderr"
positive_rc=$?
set -e
cp "$positive_counter" "$ROOT/evidence/positive-counter.txt"
test "$positive_rc" = 17
test "$(wc -l < "$positive_counter")" = 1

set +e
env -i \
  HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  VIRTUAL_ENV=/home/user/work/venv-agent \
  P4_D73_MANIFEST="$P4_D73_POISON_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full-preflight-poison \
  P4_STUB_COUNT="$poison_counter" /bin/bash --noprofile --norc -c \
  'set -eu; test "$(git -C "$0" remote get-url origin)" = https://github.com/peteromallet/astrid-agent; exec "$0/tools/p4-d73-pinned-launch.sh" "$1" dry -- "$2"' \
  "$AGENT_CHECKOUT" "$P4_D73_POISON_MANIFEST" "$MAIN_POSITIVE_CONTROL" \
  >"$poison_stdout" 2>"$poison_stderr"
poison_rc=$?
set -e
cp "$poison_counter" "$ROOT/evidence/poison-counter.txt"
test "$poison_rc" = 1
test "$(wc -l < "$poison_counter")" = 0
grep -Fq 'D73 launcher: agent SHA mismatch' "$poison_stderr"

printf 'positive_rc=%s\n' "$positive_rc"
printf 'positive_calls=%s\n' "$(wc -l < "$positive_counter")"
printf 'poison_rc=%s\n' "$poison_rc"
printf 'poison_calls=%s\n' "$(wc -l < "$poison_counter")"
printf 'poison_refusal=D73 launcher: agent SHA mismatch\n'
