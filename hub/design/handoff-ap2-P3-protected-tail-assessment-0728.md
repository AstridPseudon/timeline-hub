## P3 protected-tail source report

- Source compatibility: **FAIL**
  - Existing setup matcher/helper still require `clip.move` at `three-products.spec.ts:1540–1548` and `gate5-reset-precondition.ts:52–58`; prior shape worker owns this correction. I did not duplicate or modify it.
  - Protected tail has a separate concrete mismatch at `three-products.spec.ts:1640–1641`: strict equality omits `created`, but production serialization emits `created: []`:
    - `documentPatchIntent.ts:131, 216–223`
    - `localSaveSession.ts:167–185`

- Other fields are source-consistent: `doc.patch`, `select: null`, guarded `args.changes`, reads, `merge: fields`, label, step intent/patch, v2 envelope, source, dry-run, and idempotency flow.

- Smallest correction, not applied: add `created: []` to the expected command at line 1640.
  - Protected tail current SHA256: `f7e7abd9233a332adfeea03155d78af05a5d631ffffbecd64691c7014936bb67`
  - Virtual corrected-tail SHA256: `4b267cb513d863b46931cb793e995dbbe7169be2a56b46f15112655a945458ec`

- Original reset `200`, outbox, retry, restart, history, canonical-document, and undo assertions remain protected and unchanged.

- Actual browser/daemon/downstream result: **UNKNOWN**. No live request, browser, backend, socket, or full suite was run.

Checks:

- `git diff --check` — passed
- Worktree remains clean at base `66354161950d1e747965c095ea97b881d2592708`
- No source/test/generated files edited
- Commit message and `DONE` marker created.