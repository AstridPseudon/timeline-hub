#!/usr/bin/env bash
# D139/D139a documentary source reference only.
#
# This file is unconditionally inert.  It is intentionally not an executable
# controller: it exits before reading bindings or invoking any requester,
# checker, helper, import, manifest, launcher, Store, child, or core service.
# A future reviewed worker may transcribe the references below only after all
# guards in controller-brief.md and the JSON packet are bound by their actual
# owners.  Do not remove this exit to make the packet runnable.
set -euo pipefail
exit 0

# Source-backed reference sequence (comments are documentation, not shell):
#
# 1. One ordinary request-child-venv call, with the exact source-carrier API:
#    request-child-venv NAME AGENT_SHA [BASE_SUITE REMOTION_GRAPH] \
#      --source-carrier AGENT_CHECKOUT RUNTIME_CHECKOUT RUNTIME_SHA
#    Capture its authentic stage stdout/stderr privately.  Its exit 0 means
#    only that queue/pending/childvenv-N was written.  Wait for that SAME N in
#    queue/done/childvenv-N or queue/refused/childvenv-N.  A done result is
#    usable only with the genuine Store child and maker provision report; a
#    refused result preserves the exact row, authentic stage stderr (or the
#    source's explicit EXACTMISSING), and private hashes, then stops.  No retry,
#    fallback, alternate name, rename, or result substitution is permitted.
#
# 2. After a genuine child-complete check only, create one fresh supported
#    normal manifest and run the existing D73 report-all positive control once
#    (17 positive calls) and the poison control with zero calls.  These are
#    source references owned by the normal helper/manifest route, not new APIs.
#
# 3. At core dispatch, after the one-time 4700000000-byte start guard and the
#    ongoing 4000000000-byte stop guard, request exactly one named service:
#    R=$(request-test <worker-name> agent-core-full) && wait-test "$R"
#    A manager owns this normal service request.  The p4-d73 launcher row is
#    an input to that service and is not a second manual launcher execution.
#    Preserve the existing 22 roots and argv exactly:
#    -m pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45
