# F D141l independent binding review — FAIL

Reviewed the author packet at the required absolute evidence root, Composition
base `6a2d1c22ec800229812f4d756d7198aece8111ed`, all six 0731 findings, the
0735 author brief/addendum, Runtime0640’s published finite continuation, and
`design/commit-v2.md`. No product, test, registry, request, queue, service,
body, or source repair was made.

## F-D141L-REVIEW-001 — blocking: exact author check is not reproducible

The required exact command is:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -P /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D141l-binding-return-0735/evidence/check-source.py check
```

It now exits `78` with:
`REFUSED: [Errno 2] No such file or directory: .../tests/agent-agent-core-full-1026025151-24049/exit`.
The author manifest lists 45 retained original/control paths and all 45 are
currently absent. Missing groups are: 0249 result (5 files), 26496 result
(10), 27388 result (9), 10086 result (10), 0318 findings (1), 0309 controls
(3), 0515 controls (6), and 0508 findings (1). These are finite missing
inputs; no historical bytes were fabricated or substituted.

## F-D141L-REVIEW-002 — blocking: pristine pins are unavailable

The author source manifest points the pristine Agent and Runtime inputs at
`/home/user/work/wt/agt-pin-64197afa` and
`/home/user/work/wt/rt-pin-fa9cd546`. Both paths are absent. Consequently the
exact source selector, clean-tree, and pristine command verification cannot
run, even though the manifest records the intended commits
`64197afa297f86f1e738238d5e80aff6d33e303a` and
`fa9cd5464a8b37b02f971de375e56be846cd69e2`.

## F-D141L-REVIEW-003 — blocking: source checker retains a stale live-row gate

`check-source.py:463-470` requires a current `agent agent-core-full` row and
requires that row to contain the historical 0309 path. The current
`orch/tests/suites.conf` has Agent `full`, `targeted`, and `conformance` rows,
but no `agent-core-full` row. The author manifest simultaneously declares
`SOURCE_READY_NO_LIVE_REGISTRATION` and `rows_installed=false`.

The absence of an installed row during source preparation is expected and is
not independently treated as a product failure. It does mean the advertised
exact author check cannot qualify the packet in the current environment, and
its historical-row assertion does not match the settled source-only scope.

## F-D141L-REVIEW-004 — blocking: future controller cannot establish the row

The new controller has genuine isolated ordering (`controller-continuation.sh`:
`read_row`/`cas_row`, 36–65; `dispatch_phase`, 122–177; `dispatch`, 180–217),
and it correctly calls the normal `request-test`, `test-run`, and `wait-test`
routes after CAS. However, `dispatch` first calls `read_row` (194) and
`cas_row` only replaces an exactly matching existing row (48–65). With no
current `agent-core-full` row, the real future invocation cannot reach
`request-test`; no supported row-install step is present. This is distinct
from the expected source-only uninstalled state: the runnable future path must
be able to establish the owned row before request creation, without inventing
a service ID or changing the registry interface.

## F-D141L-REVIEW-005 — blocking: required production launcher control is not
verified

The unchanged tiny control was run directly. The positive case exited `1` with
`0` stub calls instead of `17/1`; it failed because the pinned runtime profile
has no `package-lock.json`/`package.json`, the pinned Node executable is absent,
and the launcher consequently cannot run. The script aborts before poison, so
`1/0` is not evidenced by this review. No install, cache repair, or fixture
substitution was performed.

## Passed bounded controls

- All five operational shell scripts passed `bash -n` (exit 0).
- Both operational Python files passed stdlib AST parsing (exit 0).
- The controller `check` command passed source-only (exit 0); it did not call
  any live route.
- Isolated controller fixtures passed: two distinct generated IDs, request
  bytes, native row, immutable brief, receipt, terminal result, and row
  restoration. The consumer passed 10 isolated admission cases: 1 positive and
  9 negative cases.
- Isolated lifecycle controls passed all 36 cases with the recorded expected
  exit codes. These controls authorize no live admission.
- Integrated Agent/Runtime/App/Composition tuples are clean and match the
  author manifest, including App `82e9e13ddf1d7ec6c736521b2eb091dca9877598`
  / tree `6a6e49eb4461b5ca1a7fa1247653bc794f26d710`. Historical App `4de…`
  receipt data was not retargeted.

The packet is therefore `FAIL_FINITE_BLOCKERS`, not `READY_SOURCE`: the
isolated route is useful evidence for a later receiving pass but cannot claim
genuine admission, pair qualification, REG0, or shipping.
