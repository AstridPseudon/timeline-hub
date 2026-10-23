# U3b initial failed candidate bounded independent findings

## Verdict

**FAIL / HOLD P1, P2, P3 and freeze.** Reviewed candidate 7978ed829e8c12ca4058676f43208a882e381966 (tl/app-U3b-live-refresh-sol-2013) against PLAN §3 U3/A2, C0 and D24. No product or test files were changed by this review.

The retained qualification evidence remains 280 PASS / 2 FAIL, 39 Node PASS, 60 changed-file lint PASS, and one App TS2307. Per the brief, tests were not rerun; this report classifies the retained failures and performs source/provenance audit only.

## Concrete findings

1. Retained mounted positive fails on an explicitly present filename-equal label.

src/tools/video-editor/hooks/useTimelineCommit.test.tsx:143-210, case label p1-video.mp4, expects the split halves to retain the raw label field. The retained assertion at line 185 receives both halves without label.

The candidate source path explains the failure:

- assembleTimelineData in src/tools/video-editor/lib/timeline-data.ts keeps the raw config in current.config, but classifies a label equal to the current derived display name as absent in meta.label.
- rowsToConfig (same file, lines 360-368) preserves a raw label for an existing authored clip; this is the rows projection/save behavior.
- The config mutation production path is useClipSplitting.ts -> withAuthoredClipLabels -> useTimelineCommit.ts config mutation -> serializeResolvedConfigForSave.
- serializeResolvedConfigForSave in src/tools/video-editor/lib/timeline-mutation-engine.ts:146-179 calls withoutDerivedLabels, which removes the existing clip label whenever meta.label is absent and the resolved label equals meta.displayName. That removes the raw p1-video.mp4 field before serializeResolvedTimelineEdit can preserve it.

2. Upstream legacy cleanup fails on save/reload after an asset rename.

src/tools/video-editor/lib/timeline-data.test.ts:632-638, treats a label saved before this rule (equal to the current derived name) as unset, expects second take.mp4 after saving the legacy first take.mp4 label and reloading with the renamed asset; the retained candidate produces first take.mp4.

3. The two label obligations are separable, not an identical-input impossibility.

The initial value is similar, but the exercised operations differ:

- The upstream cleanup test calls the rows serialization helper (rowsToConfig) and then reloads. This is the projection/save/reload cleanup path.
- The retained positive performs a user split through the config mutation path. A2 requires preservation of an explicitly authored raw field through that edit, including when its value happens to equal the asset filename.

The existing code already has the needed separation seam: withAuthoredClipLabels plus serializeResolvedTimelineEdit preserves unchanged raw labels for config edits, while rows serialization can continue treating meta.label === undefined as derived and omit it. The candidate's withoutDerivedLabels currently collapses those two paths. Therefore this is a concrete source-resolution obligation, not a new C0 policy decision and not permission to weaken either unchanged test. If the owner instead declares filename-equal labels universally derived even during an authored split, the two expectations would become a genuine contract conflict; that would contradict the settled A2 disposition in the brief.

4. The new BrowserTourEditor has an ordinary missing component dependency.

src/app/onboarding/BrowserTourEditor.tsx:17 imports TourChatPanel.tsx, and line 80 renders it in the new tour pane. The candidate has neither TourChatPanel.tsx nor its test.

The exact upstream source exists at 65c1771b78ab972295d4bea91c93970e5bb65e74:

- TourChatPanel.tsx SHA-256: b9e61ca2f0c5db8259474cdd5247a0f336a87551f528758f0d4172eb6e78e274
- TourChatPanel.test.tsx SHA-256: 6a9debe96a2f40e6bfd048218921250ad03b2b4b9abe0b0e771f64d5e36a30d9

This is not a Runtime/Composition contract issue. It is an ordinary React composition dependency required by the new BrowserTourEditor. The exact upstream panel also imports ./NewChatMenu; that source and test are likewise absent from the candidate and are the necessary transitive dependency to account for:

- NewChatMenu.tsx SHA-256: 624f4ebab8757ef7d6a5f80043d4415d81c7cde902f338536aeb5c01223c1635
- NewChatMenu.test.tsx SHA-256: 246d2271fe7d017e97af41a753d25430980fcfb54e26dcec988d80d14a977576

The exact upstream components/tests should be restored in the scoped follow-up; no replacement or new product authoring is warranted.

## Production caller and contract audit

The actual production chain is present and unchanged:

- useTimelineCommit.ts rows edits call materializeData/rowsToConfig; config edits call serializeResolvedConfigForSave.
- useTimelineSave.ts:269-271 wires scheduleSave to useTimelinePersistence.
- useTimelinePersistence.ts:385-419 sends through localDocumentSave.flush() when the local document path is active.
- useTimelineSave.ts:186-231 creates createLocalSaveSession with the existing commitTimeline provider and outbox.
- localSaveSession.ts:152-179 rebuilds the persisted intent into the full C0 v2 request with api_version, project/timeline identity, both base pins, commands or doc.patch, label, steps/patch/read metadata, merge, source and dry_run, then sends the canonical /commit route with the persisted idempotency key.
- dataProvider.ts:750-766 requires the verified revision/publication pair and consumes the accepted/merged/rebased response closure and receipt. Generated DTOs retain preview, merged/rebased, conflict/refused/invalid code/path/hint/current/suggested-command shapes.

No old route, alternate writer, body/service/seed, or settings path was introduced by this candidate.

## Parents, scope and markers

- Candidate parents are exactly:
  - first: e2e75b38e29ef0f5f628d0fdab988d701205b758
  - second: 65c1771b78ab972295d4bea91c93970e5bb65e74
- git merge-base --is-ancestor succeeds for both parents.
- The common-ancestor-to-upstream delta has 84 paths; the first-parent-to-candidate delta also has exactly 84 paths, with no upstream-only or candidate-only paths. The 84-path set is the intended upstream refresh scope.
- The candidate's overlap with retained R4 paths is expected from the divergent merge bases; the two source-resolution paths are useTimelineCommit.ts and timeline-mutation-engine.ts.
- Changed-source conflict-marker scan is clean. git diff --check is clean. Worktree was clean before this review.

## Frozen artifacts

Diffs from the first parent to the candidate are empty for the frozen runtime.lock.json, package.json, package-lock.json, vendor, generated Runtime DTOs, timeline commit types, commitOutbox.ts, useTimelineSave.ts, and localSaveSession.ts.

The retained Composition artifact is present and hashes to 819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234. No schema/DTO regeneration or pin change is in this candidate.

## Test status and next obligations

Tests are N/A for this independent review; I did not rerun the retained failing cohort, full cohort, browser, localhost/live-socket, body, preflight, service, seed, bench or typecheck suites.

After the two scoped source obligations are resolved, the owner should rerun the two affected behavior tests, the changed onboarding/tour tests, App/Node/root typechecks and the specified P1=2/P3=1/P2=8 discovery list. Keep P1/P2/P3 and freeze on HOLD until those results qualify. No expected-failure annotation, policy relaxation, or test weakening is justified by this review.

