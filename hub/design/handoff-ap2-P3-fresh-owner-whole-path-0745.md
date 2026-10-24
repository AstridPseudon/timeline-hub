## P3 report — FAIL confirmed, no source edits

The independent 0739 failure is source-confirmed.

### Whole-path ownership

- `openCommandTimeline()` only waits for “some” new settled owner, then discards its ID: [three-products.spec.ts:1264](/home/user/work/wt/ap2-P3-fresh-owner-whole-path-0745/tests/e2e/local/three-products.spec.ts:1264).
- Gate 5 later selects the first settled owner matching project/timeline: [three-products.spec.ts:1541](/home/user/work/wt/ap2-P3-fresh-owner-whole-path-0745/tests/e2e/local/three-products.spec.ts:1541).
- Durable `list()` returns all historical owners in the same realm/actor/scope: [commitOutbox.ts:240](/home/user/work/wt/ap2-P3-fresh-owner-whole-path-0745/src/tools/video-editor/commands/commitOutbox.ts:240).
- Production correctly creates a new owner when no pending/intented owner needs recovery, and receives the actual generated ID at the claim boundary: [localSaveSession.ts:217](/home/user/work/wt/ap2-P3-fresh-owner-whole-path-0745/src/tools/video-editor/commands/localSaveSession.ts:217).

The smallest supported correction is test/setup plumbing: snapshot `previousOwnerIds` before navigation, require exactly one owner satisfying the qualified P1 predicate

```text
same project/timeline scope
AND ownerId not in previousOwnerIds
AND no pending request
AND intents.length === 0
```

then return that exact `ownerId` to Gate 5. Do not select by scope alone.

### Diagnostics are not an owner authority

The production session state has `ownerId`, but public diagnostics project only:

- `ownerPresent`
- process-local `ownerAlias`
- generation/lifecycle flags
- mounted/original heads

See [timeline-diagnostics.ts:169](/home/user/work/wt/ap2-P3-fresh-owner-whole-path-0745/src/tools/video-editor/lib/timeline-diagnostics.ts:169). `ownerAlias` is a `WeakMap` alias and cannot identify the durable IndexedDB owner. No diagnostic change is justified or needed.

### Request/response ownership correlations

Available at each boundary:

- Before gesture: verified canonical basis, exact base revision/publication, immutable pre-gesture document, derived read closure.
- During dispatch: persisted `pending.request` containing complete body and generated `Idempotency-Key`: [commitOutbox.ts:464](/home/user/work/wt/ap2-P3-fresh-owner-whole-path-0745/src/tools/video-editor/commands/commitOutbox.ts:464).
- On success: `{data, receipt}`, accepted revision, canonical document, digest, provider/compiler, publisher, normalized commands and steps.
- After persistence: owner `accepted.head`, `accepted.value.response`, receipt and canonical result are available and must match the observed setup response: [gate5-reset-precondition.ts:252](/home/user/work/wt/ap2-P3-fresh-owner-whole-path-0745/tests/e2e/local/support/gate5-reset-precondition.ts:252).
- History: authoritative receipt/publication and head; no owner ID is supplied by Runtime history.

### Reply validation expectation

The current helper checks required claim/step keys only and permits arbitrary extras: [gate5-reset-precondition.ts:176](/home/user/work/wt/ap2-P3-fresh-owner-whole-path-0745/tests/e2e/local/support/gate5-reset-precondition.ts:176).

Sol0745 should validate:

- exact request-controlled command fields and patch/reads;
- provider claim fields by value and structure, not presence only;
- step identity, label, intent, tags, ordinals, patch and reads;
- optional provider `dependencies` when present, without requiring it when the C0 schema legitimately omits empty dependencies;
- the complete C0 accepted envelope and receipt correlations.

Use a schema-defined allowlist for known optional full-DTO fields (`records`, `effects`, `dependencies`, `history`, `undo_steps`, etc.), rather than exact equality against the abbreviated fixture. C0’s authoritative reply rules are [commit-v2.md:703](/home/user/work/runtime/contract/commit-v2.md:703).

### Verification

- `git status --short`: clean.
- `git diff --check`: passed.
- `git diff --name-only`: empty.
- Current tree: `3fefe21ec9d65bb19e086c84537925fd95b74cd9`.
- No browser, backend, HTTP, socket, service, full-suite, or live claim was run.
- No tracked files were changed. Commit message and `DONE` marker were created.