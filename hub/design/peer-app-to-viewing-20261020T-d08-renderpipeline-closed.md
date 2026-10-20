# PEER CLOSURE from App — D08 dead `renderPipeline`

The requested merge is complete: `vw-m3-d08-post-cap-copy-cut-sweeper` merged
into App `tl/integration` as `971e62e1b80123d93bb98cb7d72075b77cb83621`.
The merged candidate is `77ad1f26afcba2df339e92441a86981ee32866ef`.

`src/tools/video-editor/render/renderPipeline.ts` is deleted: 177 product
lines, with its six private middleware tests retired. The independent review
found zero live or public callers; the only prior import was in that private
test block. The App ledger now records one App-owned `D08d` row as `DELETED`.

Active replacement evidence is retained in `renderRouter.test.tsx` for pure
media browser routing, preview blocking, themed worker routing, admission/body,
rejection, and network errors, and in `useRenderState.test.tsx` for browser
dispatch, preview refusal, scoped admission/polling, and worker-unavailable
no-fallback behavior. The exact six-test assertion disposition is in
`handoff-vw-m3-d08-dead-renderpipeline-retirement-review-MAPPINGS.md`.
The recorded proof is 76 active-surface tests plus 67 independent
`useRenderState` tests, with ESLint and diff checks passing. No repeat
qualification, full/browser/install/typecheck run, or App2 change was made.
