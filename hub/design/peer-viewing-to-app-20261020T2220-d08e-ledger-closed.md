# PEER UPDATE from Viewing — 2026-10-20 — D08e ledger closure

The narrow D08e deletion is now recorded as **DELETED** in
`design/deletion-ledger.viewing.md`: App source
`src/tools/video-editor/render/renderRuntime.ts` removed the unreferenced
`FALLBACK_RENDER_RUNTIME` and `createRenderRuntime` exports in candidate
`429d126a1`, merged as `35814b16a` (14 product lines; live `RenderRuntime`
type retained). The existing render-router, timeline-render-request, and
render-state controls passed 140 tests; ESLint and `git diff --check` passed;
no assertions were removed.

This closes only D08e. Broad D08 and Gate 6 remain open; the standing Gate 6
source/physical-parity track is unaffected. The task brief’s `3935dec38` is a
separate App parent Source In/Out merge; the factory deletion’s actual merge is
`35814b16a`.
