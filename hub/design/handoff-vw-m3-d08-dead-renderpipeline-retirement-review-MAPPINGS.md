# `renderPipeline` deletion review

Candidate: `77ad1f26afcba2df339e92441a86981ee32866ef`
Parent reviewed against: `e02a12c05`
Decision: **APPROVE**

## Caller/public-surface proof

- `src/tools/video-editor/render/renderPipeline.ts` was test-only: its only
  import in the parent tree was the private middleware block in
  `src/tools/video-editor/lib/renderRouter.test.tsx`.
- A repository-wide current-tree search finds no import, dynamic import, export,
  or executable reference to `executeRenderPipeline`, `RenderPipelineEvent`,
  `RenderPipelineMiddleware`, `ExecuteRenderPipelineOptions`, or
  `ExecuteRenderPipelineResult`.
- The only current-tree `renderPipeline` hit is the string in
  `src/sdk/__tests__/sdk-boundary.test.ts:1364`, an intentional forbidden SDK
  export name, not a caller or export.
- The host public entrypoint `src/tools/video-editor/index.ts` exports types,
  config/domain helpers, and command APIs; it never exported this helper.
- The live hook dispatches directly: browser routes call `useClientRender` at
  `src/tools/video-editor/hooks/useRenderState.ts:1214`; Runtime routes call
  `buildRenderTimelinePayload` and `enqueueAstridRuntimeRenderTimeline` at
  `:916` and `:934`. No live path passes through the deleted helper.

## Removed private tests/assertions, one-to-one disposition

The parent removed six tests (all in the private `Sprint 8 render pipeline
middleware` block). Every assertion is accounted for below.

1. **`renders supported local fixture timelines in the browser path with the
   local runtime type` (parent lines 1716–1770).**
   - Browser route decision and live client dispatch are retained by
     `renderRouter.test.tsx:99` (`routes a pure-media timeline to the client
     renderer`) and `useRenderState.test.tsx:511` (`invokes the client renderer
     only for client-route timelines`).
   - `result.status === 'done'` / `providerId === 'browser-remotion'` and the
     injected `startBrowserRender` call are private executor-result details;
     they disappear with the uncalled helper. The active surface now owns
     client-render status directly; no public `providerId` result exists.
   - The `beforeRender`, `assetMaterialized(assetCount: 1)`, and `afterRender`
     middleware event sequence is private-only behavior of the deleted module;
     no production consumer or public contract reads those events.

2. **`does not block browser export on an enforced seam with an active opaque
   effect` (parent lines 1772–1807).**
   - The route/client invocation half is covered by the same active pair:
     `renderRouter.test.tsx:99` and `useRenderState.test.tsx:511`.
   - The `executeRenderPipeline` result/provider and injected browser call are
     private-only executor details. The helper performed no seam analysis; its
     removal removes an uncalled test adapter, not a live seam decision.

3. **`emits beforeRender, assetMaterialized, and afterRender through one shared
   middleware path` (parent lines 1809–1843).**
   - Route selection and live browser dispatch are retained by
     `renderRouter.test.tsx:99` and `useRenderState.test.tsx:511`.
   - The three-event ordering and the helper's `providerId`/result assertions
     are private-only middleware semantics. There is no active middleware
     registration or consumer, so this behavior is intentionally gone with the
     private module.

4. **`emits renderFailed for preview-only routes without falling back to the
   browser renderer` (parent lines 1845–1869).**
   - Preview route selection is retained by
     `renderRouter.test.tsx:268` (`blocks remotion_module clips with missing,
     empty, or non-string artifact ids`).
   - Active error/no-browser-fallback behavior is retained by
     `useRenderState.test.tsx:681` (`blocks malformed remotion_module metadata
     without invoking the client renderer`) and its no-extension equivalent at
     `:2046` (`preserves preview-only routing with no extension runtime`).
   - `providerId === 'preview-only'` is the deleted helper's private result
     field; the live surface exposes the route reason through the render log,
     not a pipeline result object.
   - The `beforeRender`, `assetMaterialized`, `renderFailed` event sequence is
     private-only middleware behavior and is intentionally gone.

5. **`queues worker-capable routes through Astrid R1 without falling back to
   the browser renderer` (parent lines 1871–1942).**
   - Worker route selection and route-to-enqueue integration are retained by
     `renderRouter.test.tsx:113` (`routes a themed-only timeline to
     banodoco_render_timeline`) and `:1649` (`themed timeline decision drives a
     banodoco-pool enqueue`).
   - Queued status, task id, correlation id, capability lookup, and the
     canonical request body are retained by
     `renderRouter.test.tsx:1240` (`lists capabilities and admits the task...`)
     and `:1403` (`POSTs the canonical rendering.render envelope...`).
   - The live hook's scoped admission, task identity, polling, and no-browser
     fallback are retained by `useRenderState.test.tsx:777` (`admits a scoped
     render, polls on the declared 2s cadence, and exposes the R9 media URL`).
   - The deleted helper's `providerId` field and middleware event sequence are
     private-only result/telemetry details; active callers use the Runtime task
     result and hook state instead.

6. **`emits renderFailed when Astrid rejects render admission` (parent lines
   1944–1980).**
   - Admission rejection and message propagation are retained by
     `renderRouter.test.tsx:1476` (`surfaces a rejected Astrid admission as an
     error result`) and `:1489` (`surfaces a network failure as an error result`).
   - Active no-client-fallback behavior for a worker route is retained by
     `useRenderState.test.tsx:706` (`surfaces worker-unavailable state for valid
     remotion_module routes without client fallback`).
   - The exact private fixture text `Remotion is not installed`, the helper's
     `providerId === 'worker-astrid-runtime'`, and its three middleware events
     are not public behavior. The active route reports the admission error via
     the hook's render log and keeps the client renderer untouched.

The removed middleware assertions therefore either map to named active route,
admission, and hook tests above, or explicitly describe behavior that belonged
only to the deleted private executor. No active/public behavior is left covered
only by the removed tests.

