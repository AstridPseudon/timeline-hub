# Handoff: ap2-P2-popup-review-1011

## Verdict

**FAIL** for faithful current real-mounted popup coverage.

The fixture has good source-level ingredients: authentic Runtime media import and
selection custody, two mounted ADD/SWAP gestures, shared-occurrence fork plus
media command ordering, and exact one-file commit scope. Labels match the
separate A3 caller branch; that unmerged caller was not treated as a failure.

## Blocking issues

- The test requires request `reads`, per-step `reads`, `rationale`, and
  `group_id`, but the current A2 shared-command path appends only commands and
  `localSaveSession` emits no such metadata for that branch. The Runtime adapter
  forwards the body unchanged.
- The canonical delta oracle omits complete sibling/order/closure and raw,
  opaque, null, absence, registry, and source-mapping preservation. It also
  compares the copied occurrence's post-action placement with the source's
  placement instead of the copy's own pre-action placement.
- Reload does not reopen the popup or assert exact reloaded fields before Undo.
- Reply/history checks cover only a subset of the required v2 closure; old-route
  monitoring is limited to two known legacy paths.
- The repository-root TypeScript command passes while excluding tests. An
  explicit test-inclusive check reports 44 diagnostics, including three in the
  new spec.

## Evidence

Scoped ESLint, Playwright discovery (2 tests), and `git diff --check` passed.
No browser/service/body/full-suite execution was run. Commit delta is exactly
one new file, blob `f0213316cae9efd31a0036d2602e5ac1b299006e`, from base tree
`654a66946da8a4da65248576a9eb5e32a9e8d382` to current tree
`43d1a77920133b09e7ad3eb3dda60b8b18db8dab`.
