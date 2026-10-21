# Runtime RT07 — current b92 held cut

Status: staging only; not endpoint retirement, merge authorization, or ledger
`DELETED` disposition.

## Port

The sole source change is `runtime_protocol/service.py`, porting the reviewed
`67ea129f6a1a96f633ec409d04ff811a89eeb4c6` `publish_timeline_render` hunk onto
current base `b92d3e7a05eec65c142294ef4873edd059e9b31d`.

The direct legacy render writer is removed. New and prepared legacy publication
requests refuse without compatibility writes. An authenticated exact retry of
a durable published checkpoint remains read-only and returns that checkpoint's
result without consulting live target, document, CAS, task, or history state.
The method hash is
`dbd7f6c9a2c3a6a225824ee15adc891e32122d22df502585cf11b2fc5ad3fafc`, matching
the reviewed method exactly. All other b92 blobs, including current Runtime
owner-token, source/target scope, tracked-target refusal, catalog/headless,
occupancy, retention, transcript/Speech, bootstrap, launcher, and artifact
bytes, remain unchanged.

## Evidence

- `python -m py_compile runtime_protocol/service.py` — pass.
- `git diff --check` — pass.
- Direct legacy no-write/retry neighbors — 24 passed, 35 deselected.
- Direct authority no-write neighbors — 13 passed, 4 deselected.
- Existing direct publication positives remain strict and red on this held cut:
  13 passed, 6 failed, 1 deselected; no xfail, skip, deletion, or assertion
  weakening was added.
- No full, browser, socket, registered-renderer, old 7012/10910, install, or
  native-consumer run was performed.

## Missing gate

The Agent safe-installed native-consumer gate and its security/native proof,
including the approved one-to-one mapping, are still absent. Keep this cut held
until that gate is present and the orchestrator decides disposition.
