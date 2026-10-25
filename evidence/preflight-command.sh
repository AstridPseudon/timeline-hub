#!/usr/bin/env bash
set -eu

# Source/preflight recipe only.  MAIN must supply all bindings and run this
# after its 20:00Z decision; this worker deliberately did not invoke either
# dry control or the suite launcher.
: "${D134_CLOCK_GATE:?MAIN must bind D134_CLOCK_GATE=OPEN at/after 20:00Z}"
: "${D134_CUSTODY_E2E_AT_20Z:?MAIN must bind the genuine 20:00Z custody verdict}"
: "${D134_DISPATCH:?MAIN must bind D134_DISPATCH=AUTHORIZED}"
test "$D134_CLOCK_GATE" = OPEN
test "$D134_CUSTODY_E2E_AT_20Z" = NOT_GREEN
test "$D134_DISPATCH" = AUTHORIZED

: "${AGENT_CHECKOUT:?MAIN must bind the frozen Agent checkout}"
: "${RUNTIME_CHECKOUT:?MAIN must bind the frozen Runtime checkout}"
: "${P4_D73_MANIFEST:?MAIN must bind an existing exact-tuple D73 manifest}"
: "${P4_D73_EVIDENCE:?MAIN must bind the existing D73 evidence directory}"
: "${MAIN_POSITIVE_CONTROL:?MAIN must bind the existing positive parsed-row control}"
: "${MAIN_POSITIVE_COUNTER:?MAIN must bind a fresh positive counter path}"
: "${MAIN_POISON_CONTROL:?MAIN must bind the existing poison parsed-row control}"
: "${MAIN_POISON_COUNTER:?MAIN must bind a fresh poison counter path}"

set +e
env -i \
  HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  VIRTUAL_ENV=/home/user/work/venv-agent \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full-preflight-positive \
  P4_STUB_COUNT="$MAIN_POSITIVE_COUNTER" /bin/bash --noprofile --norc -c \
  'set -eu; test "$(git -C "$0" remote get-url origin)" = https://github.com/peteromallet/astrid-agent; exec "$0/tools/p4-d73-pinned-launch.sh" "$1" dry -- "$2"' \
  "$AGENT_CHECKOUT" "$P4_D73_MANIFEST" "$MAIN_POSITIVE_CONTROL"
positive_rc=$?
set -e
test "$positive_rc" != 0
test "$positive_rc" = 17
test "$(wc -l < "$MAIN_POSITIVE_COUNTER")" = 1

set +e
env -i \
  HOME=/root LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 PYTHONNOUSERSITE=1 \
  PYTHONPATH="$AGENT_CHECKOUT:$RUNTIME_CHECKOUT" \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  VIRTUAL_ENV=/home/user/work/venv-agent \
  P4_D73_MANIFEST="$P4_D73_MANIFEST" P4_D73_EVIDENCE="$P4_D73_EVIDENCE" \
  P4_D73_REQUEST_ID=agent-core-full-preflight-poison \
  P4_STUB_COUNT="$MAIN_POISON_COUNTER" /bin/bash --noprofile --norc -c \
  'set -eu; test "$(git -C "$0" remote get-url origin)" = https://github.com/peteromallet/astrid-agent; exec "$0/tools/p4-d73-pinned-launch.sh" "$1" dry -- "$2"' \
  "$AGENT_CHECKOUT" "$P4_D73_MANIFEST" "$MAIN_POISON_CONTROL"
poison_rc=$?
set -e
test "$poison_rc" != 0
test "$(wc -l < "$MAIN_POISON_COUNTER")" = 0
