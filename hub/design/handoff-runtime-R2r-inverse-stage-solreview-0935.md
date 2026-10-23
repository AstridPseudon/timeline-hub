# Runtime R2r inverse-stage Sol review handoff

Result: **FAIL** on candidate `b3367ab8fe53676caa8e90e17030f410e9ac7074`, base
`a01e9d806e08ee4ff6d35bad18dddafa1f09f862`.

The exact named acceptance passed (`109 passed` for auth/inverse/read-basis;
`10 passed, 68 deselected` for inverse/history integration), and static and
preservation checks were clean: auth/store Pyright current/parent both 76 with
zero source-line-mapped identity deltas; whole touched-file Ruff current/parent
both 11 inherited store diagnostics; auth/new-test Ruff clean; frozen77 and all
276 existing tests unchanged; compile and diff-check passed. Actual Agent was
`2e21af300abbefc8afbad217189fa4715cf82616`.

Blocking finding: native write identity is not bound to authenticated source
history. `_inverse_stage_boundaries` authenticates native range length and
sequential/final values, but does not authenticate each native write's ref/path
identity. An isolated normal Runtime store/provider probe replaced the first
inverse native write with the no-op
`parent/["config","forged-native-write"]`, before=absent, after=absent, while
leaving the canonical effect image and ranges unchanged. The candidate returned
`accepted` and the forged write was present in the durable last history record:

```text
accepted {'after': {'state': 'absent'}, 'before': {'state': 'absent'}, 'path': ['config', 'forged-native-write'], 'ref': 'parent'}
```

This violates the mandatory exact native-write/stage provenance control in
PLAN §3 R2r and approved `commit-v2.md` §§2/5, before durable write/history
replay. The prior real-Agent projection regression is fixed, but this new
forgery is merge-blocking. No repository repair was made; no full suite was
run. See the worker report for commands and preservation counts.

