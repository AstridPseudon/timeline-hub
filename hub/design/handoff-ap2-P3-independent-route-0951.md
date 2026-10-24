## P3 report — PASS

Static qualification establishes that original Gate5 is independent of popup/fork-add-media repair.

- Selected Gate5: [`three-products.spec.ts:1543-1739`](/home/user/work/wt/ap2-P3-independent-route-0951/tests/e2e/local/three-products.spec.ts:1543)
- Transitive path:
  - `openCommandTimeline`: lines 1264–1285
  - `prepareAfterAckLossMountedDocuments`: lines 1347–1372
  - drag-only helper: [`app.ts:273-290`](/home/user/work/wt/ap2-P3-independent-route-0951/tests/e2e/local/support/app.ts:273)
  - fault wire only intercepts `/commit`, loses the first ACK: lines 785–820
- Preserved real `0→5`, reset `5→0`, lost ACK, reload, restart, exact retry, merged response, history, inverse/undo, and legacy-traffic assertions.
- Native calls occur only in pre-mounted `seed3` harness setup: `capture_initialize`, `capture_clip_add_media`, `capture_occurrence_create`, and `capture_occurrence_add_media` (`harness.ts:732-930`). They are baseline fixture construction, not popup or fork-add-media UI.
- No selected-path call reaches `dropFileOnTimeline`, popup actions, duplicate/fork actions, or held popup repair.
- Production path is mounted capture → persisted outbox → generated POST with `Idempotency-Key` → Runtime sole writer/provider (`useTimelineSave.ts:137-164, 318-323`; `localSaveSession.ts:165-205`; `generated.ts:202-205`).

Source identity:

- HEAD: `82cb5c0005df7abe0fcb8673f7be192a6c9e9183`
- Tree: `6fa0a0f32b212dbdae7c2ecaca1813de68907e67`
- All three Gate5 blobs exactly match `f56128d540ff96013c9532d79f3f4e767beba820`.
- Full spec SHA-256: `26c1ae764013f8907ff7f3664dbcee016c88bc17a797f66800d012e618165d5b`
- Protected current tail (anchor range 1608–1741): `5ede6f374857a66a327da3cea0e85de0457a04267003f3f66e3d40ee4f380912`

Evidence discrepancy disclosed: the 0833 prose records body hash `3819…`, but its exact command log computes the current `[1534,1704]` slice as `0deda15b…`; this is a stale/range-reporting inconsistency, not a source difference. The protected tail and full source identity are exact.

Checks:

- `git diff --exit-code f56128d5 -- <three Gate5 paths>` — PASS
- `git diff --check HEAD` — PASS
- Reused unchanged 0900/0833 evidence by exact tree/blob identity: 20 controls PASS, three serialized TypeScript checks PASS, three-path ESLint PASS, Playwright list-only 15 tests PASS.
- No browser, live Runtime, popup, full suite, or live-credit run.

Worktree remained clean. Required `commit-msg` and `DONE` markers were created.