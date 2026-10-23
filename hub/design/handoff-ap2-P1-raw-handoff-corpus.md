# P1 raw handoff corpus — app2 handoff

- Worktree: `/home/user/work/wt/ap2-P1-raw-handoff-corpus`
- Base commit: `02a161cae3dc3f42c792430a157acd6fe26cfc45`
- Base tree: `c689d1ab56ea730d0917d67dbffc710c9b6f9c2b`
- Changed file: `src/tools/video-editor/hooks/p1RawHandoffCorpus.test.ts`

The proof slice exercises real App parent documents through `createTimelineLocalSaveHandoff` → real `LocalSaveSession` → durable outbox → `documentPatchIntent`. The track-label case passes with an exact absent-to-label set and preserves the untouched closure. The trim case preserves the original authored expected removals as a failing regression: current `timelineLocalSaveHandoff.ts` does not emit omitted `app.astrid.for` / `until` clears, although the original fixture after-document removes them. No product code was changed.

The original trim closure includes dependent shots/occurrences, so the test uses a parent-only projection in memory; no child IDs or Runtime identities are fabricated. Move lacks a compatible canonical parent registry/after document in its original fixture. Split→trim and accepted/merged/refused/lost-ACK transport remain explicit H3 gaps. No GO claim.

Production path inventory: `useTimelineState.ts` → `useTimelineSave.ts` stages `readTimelineOriginalSaveBasis`; `useTimelinePersistence.ts` has optional `localDocumentSave` capture, but current state wiring does not construct/pass the handoff session. Full v2 transport activation is pending.

Verification:

- New test: 2 passed, 1 failing trim regression.
- Required targeted command: 23 passed, 2 failed: the trim regression and an unchanged corpus provenance SHA mismatch (`harness.ts`, expected `2ba2164b…`, actual `b243b340…`).
- TypeScript: pass.
- ESLint targeted: pass.
- `git diff --check`: pass.
- No install/browser/socket/full/heavy run.
