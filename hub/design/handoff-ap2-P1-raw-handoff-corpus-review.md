# P1 independent Luna review: raw handoff corpus

## Result: FAIL

Reviewed App commit `45642677bc781b1d6bc3f375f108c27aef64227e` / tree `208aa6dc0cb3ae611170c96be85d7410cb23ab69` against PLAN §3 P1 and contract §§1–3/5/7. The diff is exactly one new test over base `02a161cae3dc3f42c792430a157acd6fe26cfc45`:

```text
A src/tools/video-editor/hooks/p1RawHandoffCorpus.test.ts
```

No product/test repair, report, fixture hash, schema, generated-file, or pin edit was made.

## Test packet

The mandated targeted command produced the requested counts:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/hooks/p1RawHandoffCorpus.test.ts src/tools/video-editor/hooks/timelineLocalSaveHandoff.test.ts src/tools/video-editor/commands/p1FeasibilityCorpus.test.ts
23 passed, 2 failed (3 files: 1 passed, 2 failed)
```

The two failures are distinct:

1. The new trim proof fails because two expected `remove` effects are absent.
2. The unchanged corpus provenance harness check fails: expected `2ba2164ba7fd2d76ccca94d0645e6b79236c85ab4e53e82e84ae1af250c7d815`, actual `b243b340177c2d905f841ec4c7307b03e7afd4f43f0096701c20bf132f202534`.

The new test's other two cases pass. The third fixture-only assertion checks opaque/null/absent/raw-sibling preservation and is not extra product coverage.

## Trim disposition: real A2 regression

The red trim assertion is a real loss of authored intent, not a bad fixture or an invalid parent-only mapping.

- The original fixture input has `app.astrid.for = 19` and `app.astrid.until = null` in both parent clip mirrors.
- The original fixture output omits both keys but retains `app.astrid.opaque = [null, false]` and all unrelated fields.
- `tests/fixtures/p1-feasibility/cases.json` independently declares both paths as `clear`.
- Main's actual producer, `src/tools/video-editor/commands/clipTrimCapture.ts`, uses `clearIntent` to delete `until` and `for` before writing the resulting `app` value (`:58-75`, called from `:136-150`). Its existing source-unit test passes the exact output and preservation expectations.
- The projection used by `sourceFor` canonicalizes the real document pair but does not add those omitted keys back; the serializer preserves the app extension and its opaque sibling values.
- The failing handoff path is `src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:128-145`: it clones raw authored state, then walks only keys present in `next`. Omitted `for`/`until` are therefore classified as partial-view omissions and remain in the raw document, so `documentPatchIntent` emits no removals.

Ownership is App A2: the handoff/source mapping must preserve intentional omission clears without turning every partial editor view omission into a delete. The proof must retain the two expected removals; there is no proof-only correction that makes this red result legitimate to ignore.

## Production caller / v2 activation

The production caller does not use the reviewed handoff:

```text
useTimelineState.ts:622
  -> useTimelineSave(...)
useTimelineSave.ts:105-121
  -> useTimelinePersistence({...}) with no localDocumentSave
useTimelinePersistence.ts:408-412
  -> documentSave.flush() only when supplied; otherwise saveTimelineAtHead/saveTimeline
```

`originalLocalSaveBasis` is staged and returned from `useTimelineSave.ts:414`, but it is not used to construct a `LocalSaveSession`/handoff. Non-test searches find no mounted `createTimelineLocalSaveHandoff` or `createLocalSaveSession` caller. `useTimeline.ts` and `runtime/element-adapter.ts` are additional direct old-save callers. Runtime's `commitTimeline` adapter exists, but the editor path does not mount it. Thus the handoff session and v2 emission are still unmounted. Ownership: App A2/integration, with any generated-client/contract adoption owned by the corresponding R0/U4p integration lane.

The new test correctly stays at the local proof boundary; it does not handwrite a v2 request or substitute a local outbox result for Runtime acceptance. Full v2 remains unproven: ABI-1 scope/base revision+publication, commands, label, steps (`id`, `label`, `intent`, `tags`, `command_ordinals`, patch, optional reads), `merge`, request reads, `dry_run`, and `Idempotency-Key`; accepted/merged canonical closure/digest/heads/receipt/commands/authoritative steps/dependencies/merge mode; conflict reason/head; invalid code/path/hint/suggested command; and authenticated preview/history. The current provider acceptance check also still admits `accepted`/`rebased`, not the contract's new `merged` success.

## Mapping and assertion quality

`parentOnly()` is an appropriate proof adaptation for this parent-only handoff: the source fixture has dependent shots/occurrences that the handoff explicitly refuses, so the test removes that real dependent closure in memory while retaining the authored parent payload. It fabricates no child IDs, revisions, or Runtime identities.

The label case is meaningful: it starts with an absent `parent.config.tracks[id:picture].label`, applies `Picture é 🎬`, and checks the complete resulting canonical document in the local session. The trim case checks exact before values, explicit clears, sets, and untouched opaque/null/absent/raw siblings. The full-document equality is meaningful for this local chain, but it is not acceptance evidence.

## Provenance disposition

The corpus pins `tests/e2e/local/support/harness.ts` at commit `3a10199e78e5a41ee6f6d7f4573ce2f11b33a87b` and its then-current SHA. The current file was modified by later commits `1a036a917` and `15d9df3ce`, producing the observed SHA mismatch. This is base provenance drift, not evidence against the new handoff test. The check must remain strict; no hash/pin was changed in this review.

## Other verification

```text
node node_modules/typescript/bin/tsc --noEmit
PASS (exit 0)

node node_modules/eslint/bin/eslint.js src/tools/video-editor/hooks/p1RawHandoffCorpus.test.ts --max-warnings 0
PASS (exit 0)

git diff --check
PASS (exit 0)
```

No install, browser, socket, full/heavy suite, product/test repair, fixture hash edit, or generated-file edit was performed. An arbitrary `tsx` child-process probe was rejected by the sandbox with `EPERM`; use the normal test service for child-process/browser verification. Provenance assertions remain intact.

## Disposition / next owner actions

Do not merge as a green P1 proof. A2 must fix the exact handoff omission-vs-clear path and mount the session/v2 caller. The corpus owner must separately disposition the stale harness pin. Re-run the targeted corpus with the original trim clear expectations unchanged; only then reassess P1/no-GO.
