# Independent producer review — APPROVE

Verdict: APPROVE the exact current-only two-file patch from
`vw-m3-queued-seek-existing-callback-producer-0935`.

## Scope and exact source

- Reviewed only the new Viewing-owned `RemotionPreview` producer, direct mailbox tests, and the approved callback type seam.
- Base HEAD: `4db86a76acd505dd1c7dc798695e2b7a9c932170`; base tree: `461fa0cddd67f4eb574563b38407733bd50afa7c`.
- Changed paths, and only changed paths:
  - `src/tools/video-editor/components/PreviewPanel/RemotionPreview.tsx`
  - `src/tools/video-editor/components/PreviewPanel/RemotionPreview.mailbox.test.tsx`
- Producer blob: `df6bf5740412f92b6f00e2f81841fb3236c799c2`.
- Direct-test blob: `ca5238598ccde30b5a786fc9124e40949ac69a5a`.
- Producer SHA-256: `3cb8f65809bf45560dbea2971783b7b4047bc0978d43c6605f4b8a1c2e5f3a02`.
- Direct-test SHA-256: `b13cbab8a5f2c75ffaa2b696f71e96d0b2b98e5cf791fa8a10473e98f89c6806`.
- Current-only binary diff SHA-256: `426efc6110a4b9fca75c703f1b6fc989bfd2e914822d389ffb890b0ddc92ad9f`.
- Pre-edit producer comparison was byte-identical for HOME `33b4a86cfdc2ac2ee63b069c225ae465d1f35656`, pending `ab938b4beacc02419de7293dfa09190956b9d0ba`, and current pre-edit source: `3bd5cddce54f10e0b75c28aab7ddcea9b4f1c860508ad24bec4b7c0679a5a902`.

## Contract/assertion map

- Existing callback only: `onTimeUpdate(time, seekComplete?)`; no second callback, public Player API, clock, counter, store, DTO, or consumer activation.
- `true` is emitted only for the active latest surviving mailbox target: frame feedback matches `activeSeekFrameRef` while `pendingSeekRef` is null; the active target is retained across the mailbox RAF.
- Same-frame/clamped no-op completion is explicit from the existing `getCurrentFrame()` path, preserving the ordinary frame/fps value.
- A-effect-before-B-dispatch witness is direct and scheduler-backed: `seek:15 -> frameupdate:15 -> seek:30 -> frameupdate:30`; A is ordinary, B is `30 / (30000/1001)` with `true`, and later frame 45 is ordinary.
- Narrow direct neighbors cover same-frame/no-op, latest-target coalescence, config-deferred matching delivery, and unmount cancellation.
- Existing authored time, source window, fps, tolerances, playback resume, final release, drag RAF/newer final click, config coalescence, and unmount behavior remain in the source; original mailbox and `RemotionPreview.test.tsx` assertions were retained, with callback metadata added one-to-one only in new producer assertions.

## Live callers (unchanged; consumer remains App-owned)

- `src/pages/Home/PublicAstridEditorParts.tsx:67`
- `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewSurface.tsx:156`
- `src/tools/travel-between-images/components/ShotTimelinePreview.tsx:285`
- `src/tools/video-editor/components/CompactPreview.tsx:83`

No live caller changed. App owns the later `useTimelineSync`/`useTimelinePlayback` consumer and the one original mounted split proof; neither was activated or run here.

## Evidence

- 0935 targeted Vitest: 47 passed across `RemotionPreview.test.tsx`, `RemotionPreview.mailbox.test.tsx`, and `RemotionPreview.audioFailure.test.tsx`.
- 0935 scoped ESLint: passed.
- 0935 `git diff --check`: passed.
- Review checks: changed-path set exactly two files; no source worktree edits made here.
- Not run by scope: consumer, browser, mounted split, physical/native, Runtime, helper/socket, install, full, central, or public-graph qualification.

## Decisions and blockers

- APPROVE exact SHA/hunks above; no scheduler counterexample or assertion-preservation defect found.
- No product edit was made in this review worktree. No blocker.
- Next step: App may review the paired consumer against this exact producer and then perform its separately owned activation/original mounted split proof.
