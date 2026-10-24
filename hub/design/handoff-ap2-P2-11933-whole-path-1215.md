## Result

No repository files were changed. The investigation classifies both failures:

- **Popup V2 → plate:** proven App selection-state defect. Normal pointer selection in `useClipDrag.ts:284–364,436–450` selects the clip but does not update `selectedTrackId`; initial selection defaults to the first track in `useTimelineCommit.ts:243–250`. The popup then chooses `editor.selectedTrackId`/first visual track (`ShotTimelineMediaControls.tsx:123–125,155–185`), so the fixture’s `plate|V2` order (`three-products.p2-popup.spec.ts:760–765`) can submit `plate` despite V2 being selected. Provider forwards the row unchanged (`shotTimelineDataProvider.ts:813–853`), and Agent validates/creates the supplied track without remapping (`native_occurrence_media_commands.py:188–211`). Actual retained POST/response bytes are **UNKNOWN**.

- **Parent receipt-ID mismatch:** proven P2 oracle defect. Runtime creates `receipt_id = "txn-" + new_id()` separately from `Idempotency-Key` (`store.py:3415–3467`; receipt mapping `service.py:1840–1844`). App correctly adopts `receipt.receipt_id` as publication identity (`dataProvider.ts:815–827`). P1 likewise pins from `receipt.receipt_id` (`three-products.p1-chain.spec.ts:149–150,1465–1466`). P2 incorrectly requires `receipt_id === post.key` and joins history/head/Undo by `post.key` (`three-products.p2-tour.spec.ts:299–300,651–685`; invoked at line 690). Smallest fix: retain `post.key` only for idempotency, and use the authoritative receipt/publication ID for history and heads. Exact current expected/received IDs are not retained locally; producer1158 must provide the finite same-ID fact from its existing packet.

Element Apply remains **UNKNOWN/pending**, with no backend cause inferred.

## Verification

- `git diff --check` — passed.
- `git status --short` — clean.
- Confirmed App HEAD/tree: `d6ed8cb... / 542b772...`.
- Confirmed Agent333b: `333b44b... / 1094bf3...`.
- Confirmed Runtime37eb: `37eb6c7... / be411470...`.
- No suites rerun because source was unchanged.

Required `commit-msg` and `DONE` markers were created.