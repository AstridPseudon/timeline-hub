# AP2-M2 parent mounted negative conversion review

## Verdict

**HOLD — do not approve the exact candidate yet.** The predecessor's
test-only source-guard correction is directionally safe, but its retained
422 evidence does not satisfy this review's acceptance condition. The only
retained 422 came from the old mounted run using
`object_id=sha256:wrong-selection`. That is malformed input and the response
was `{"code":"validation_error",...}`; it is not final95 semantic
selection-refusal evidence.

Frozen Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` validates the complete
five-field selection before lookup (`runtime_protocol/timeline_commit_port.py`
835–840). Its managed lookup raises `NotFoundError` for a syntactically valid
but unregistered object (`:744–755`), and its error taxonomy maps that to 404
`not_found` (`runtime_protocol/errors.py`:45–47). Its verified-media tests
also distinguish valid object mismatch 404 from malformed object/catalog
values 422 (`tests/test_timeline_verified_media_http.py`:65–72).

Therefore the candidate cannot be approved with a 422 assertion, and the
existing `[404, 409]` assertion is too broad for this review.

## Cohort and evidence

Final95 is identified as:

- App `25155ccb22728780a3ecd6379a929cad75cc1400`, tree
  `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7`;
- App pin `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`;
- Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`;
- Runtime/producer `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`;
- public13 archive SHA-256
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.

The actual 422 browser evidence was from the separate old013/old202 cohort
(Agent `3c4f...`, Runtime `202074...`, producer `a0dca...`), so it cannot be
relabelled as final95 proof. The later retained old-cohort evidence reached
the valid one-hex mismatch and recorded 404 `not_found`, but it likewise does
not qualify final95.

## Concrete correction required

Keep the current one-to-one fixture correction in
`tests/e2e/local/three-products.spec.ts`: assert the original
`sha256:<64-hex>` object ID and flip exactly one hex digit, preserving the
other four selection fields. Tighten the refusal check to the pinned semantic
case:

```ts
expect(wrongVerified.status()).toBe(404);
await expect(wrongVerified.json()).resolves.toEqual({
  code: 'not_found',
  message: 'selected media is not a managed project generation/variant/object',
});
```

Do not add 422 for the malformed old fixture, retain `[404, 409]`, broaden
status acceptance, change timeout/navigation/retry behavior, or weaken source
guards. The predecessor's driver-only source-identity update should remain a
small committed test-driver correction, but it does not substitute for a
final95 actual response/body proof.

The equivalent original valid ADD remains one-to-one and must stay intact:
the positive path retains the original five-field selection, `clip.add-media`
with parent selection, no replacement/removal/`afterClipId` fields, and the
existing imported-entry identity assertions. The existing lost-ACK, dependent
edit, restart, exact retry, reload, undo, raw opaque-data, duplicate, and
`wire.legacy === []` assertions remain in the same journey. No shared spec
case or live caller was changed by the predecessor correction.

## Live callers

No live callers changed. The existing mounted ADD chain remains:

`handleFileDrop` → `dispatchTimelineDrop` → `useTimelineState` →
`useAssetManagement` → native `addClip` facade, with
`useExternalDrop.ts`, `external-drop-utils.ts`,
`useTimelineCommandsService.ts`, and the commit-session/outbox path as the
existing neighbors.

## Focused verification

Run directly on the clean review worktree:

```text
node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real mounted manual video drop' --list tests/e2e/local/three-products.spec.ts
  PASS — 1 test collected
./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/three-products.spec.ts
  PASS
sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh
  PASS
git diff --check
  PASS
git status --short --branch
  clean; HEAD ce7152ee4, tree b3a8ba54
```

No browser, localhost/socket, full suite, actual gate, dependency install, or
source modification was performed. The existing suite command to run only
after the exact correction is committed and independently accepted is:

```sh
sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh run "$PWD"
```

That run must use the final95 tuple and separately report any old013 evidence;
it must retain the full positive ADD and recovery tail listed above.
