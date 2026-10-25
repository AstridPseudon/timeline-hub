# App16 corrected classification

Verdict: `PASS_CORRECTED_CLASSIFICATION`.

The immutable tuple is base `3881e9440688f774878e18806da2dc5c993a9b00`, ours `d5a1d1ab6550187e377fd7387d300102b8b82ece`, and upstream `213318f1ec6ea5c324787bbd1c30a73072d1151a`. The read-only `git merge-tree --trivial-merge` preview is 769,114 bytes with SHA-256 `6c7cf7073a554a81ddbfe9aca90da2a192e73bed90245e137e030998c4439535`.

The exact census is 16 files and 81 preview headers. Reconciliation against the actual preview gives:

- 67 clean, non-conflicting headers;
- 14 headers with conflict markers across five files;
- 13 semantic true conflicts;
- one mechanical textual import union;
- zero unclassified headers.

`hunk-map.json` is the complete ordered 81-header map. Every entry records its path, exact `@@` header, marker presence, decision, and the immutable base/ours/upstream blob triplet. `source-manifest.json` records all 48 blob IDs and source-byte SHA-256 values.

## The 14 marker-bearing hunks

1. `public/install-manifest.json` — `@@ -1,11 +1,22 @@`: semantic; App lead with Agent/Runtime release owners. Regenerate after final integrated Agent/Runtime choices, retain upstream vibecomfy/OMP additions, and publish computed hashes/digests only.
2. `src/tools/video-editor/components/AgentChat/AgentChat.test.tsx` — `@@ -6,7 +6,11 @@`: mechanical textual union; retain both independent imports.
3. `src/tools/video-editor/components/AgentChat/AgentChat.test.tsx` — `@@ -314,7 +329,219 @@`: semantic; App AgentChat owner.
4. `src/tools/video-editor/components/AgentChat/AgentChat.test.tsx` — `@@ -513,6 +740,12 @@`: semantic; App AgentChat owner.
5. `src/tools/video-editor/components/AgentChat/AgentChat.test.tsx` — `@@ -1365,7 +1598,11 @@`: semantic; App AgentChat owner.
6. `src/tools/video-editor/components/AgentChat/AgentChat.test.tsx` — `@@ -1374,8 +1611,16 @@`: semantic; App AgentChat owner.
7. `src/tools/video-editor/components/AgentChat/AgentChat.tsx` — `@@ -534,7 +548,17 @@`: semantic; App AgentChat owner with Timeline lead.
8. `src/tools/video-editor/components/AgentChat/AgentChat.tsx` — `@@ -1038,10 +1130,17 @@`: semantic; App AgentChat owner with Timeline lead.
9. `src/tools/video-editor/components/AgentChat/AgentChat.tsx` — `@@ -1057,7 +1156,36 @@`: semantic; App AgentChat owner with Timeline lead.
10. `src/tools/video-editor/components/AgentChat/AgentChat.tsx` — `@@ -1396,6 +1554,7 @@`: semantic; App AgentChat owner with Timeline lead.
11. `src/tools/video-editor/components/AgentChat/AgentChatMenu.tsx` — `@@ -1,3 +1,4 @@`: semantic; App AgentChat owner.
12. `src/tools/video-editor/components/AgentChat/AgentChatMenu.tsx` — `@@ -84,9 +95,14 @@`: semantic; App AgentChat owner.
13. `src/tools/video-editor/components/AgentChat/AgentChatMenu.tsx` — `@@ -299,6 +315,7 @@`: semantic; App AgentChat owner.
14. `src/tools/video-editor/components/AgentChat/TourChatPanel.tsx` — `@@ -152,8 +152,18 @@`: semantic; App tour owner.

## The 13 semantic choices

The existing reviewer proposals are retained verbatim in `findings.json` and `conflict-classes.json`; no new approval flow is introduced because these are the finite PLAN-covered choices for the App cut owner.

- Manifest: preserve upstream additions and compute final hashes from selected integrated sources.
- `AgentChat.test.tsx` (four seams): preserve both upstream setup/catalog/terminal-nudge tests and ours voice/session/queue tests, with exact mocks and refusal predicates.
- `AgentChat.tsx` (four seams): integrate upstream setup/error/terminal behavior with the timeline-session availability gate, voice behavior, and unified menu; the mounted App outbox → Runtime `commitTimeline` caller remains authoritative.
- `AgentChatMenu.tsx` (three seams): reconcile unified menu API with upstream setup/terminal actions while preserving focus handoff, agent/model selection, and source-owned callbacks.
- `TourChatPanel.tsx` (one seam): preserve static no-session behavior and unified menu; add only the upstream coarse-pointer styling after anchors and scripted predicates remain intact.

All choices preserve the complete C0 v2 request/reply shape, authority and guards, privacy, live inputs/predicates, and both test families. No semantic patch, normal merge, source edit, pin, kit change, ZIP, or build was performed.

## Mechanical import union

`trivial-resolutions.patch` is an evidence-only artifact for the precise import seam. Base has the shared import boundary; ours adds `CHAT_VOICE_ENABLED`; upstream adds the type-only `LocalAgentChoice` import. Both symbols are used by the preserved test families. The artifact was not applied.

## Mounted production path

The real mounted path is `useTimelineSave.ts:319-323` → `commands/localSaveSession.ts:168-196` → `dataProvider.ts:751-767` → registered `client.ts:735-742`. The outbox preserves original commands, operands, steps, reads, IDs, and idempotency key; the provider checks project/timeline and revision/publication guards before Runtime transport. The ordinary supported D66 diagnostic path is the explicit opt-in `__timelineSaveDiagnosticsEnabled` hook in `lib/timeline-diagnostics.ts:10-14,147-201`; it is observational/redacted and cannot change result classification.
