# Independent review: dead `renderPipeline` retirement

## Verdict

**APPROVE candidate `77ad1f26afcba2df339e92441a86981ee32866ef` for App owner
review/merge.** The exact deletion against `e02a12c05` is safe and bounded:
`src/tools/video-editor/render/renderPipeline.ts` and its six private middleware
tests are dead; the live router and hook paths remain.

## Reviewed diff

- Modified `src/tools/video-editor/lib/renderRouter.test.tsx`: removed only the
  private `executeRenderPipeline` import and six middleware tests.
- Modified `src/tools/video-editor/lib/renderRouter.ts`: removed two stale
  references to the deleted helper from comments.
- Deleted `src/tools/video-editor/render/renderPipeline.ts` (177 lines).
- Candidate patch: `candidate-e02a12c05-to-77ad1f26.patch`.

## Independent findings

The parent tree's only executable import of the helper was the removed private
test block. Current source has no import, dynamic import, export, or executable
reference to the helper or its types. The remaining `renderPipeline` text is
only an SDK-boundary forbidden-name assertion. Current production dispatch is
direct from `useRenderState`: browser routes end in `useClientRender`; scoped
routes call the router payload builder and Runtime task admission.
The host public entrypoint `src/tools/video-editor/index.ts` does not export the
helper.

The complete assertion-level disposition is in `mappings.md`. In short, route
selection, browser dispatch, preview blocking, worker admission/body/error
handling, task polling, and client-fallback refusal each have named retained
active-surface tests. Middleware event ordering and the helper's internal
`providerId` result fields were private-only behavior and correctly disappear
with the private module.

## Evidence

- Reused base candidate evidence: `renderRouter.test.tsx`,
  `renderRouter.attach.test.ts`, and `timelineOutputProjection.test.ts` — **76
  tests passed**; ESLint passed; `git diff --check` passed. Exact commands are
  recorded in `COMMAND` and the base worker report.
- Independent targeted proof on this exact candidate:
  `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader bundle --no-cache src/tools/video-editor/hooks/useRenderState.test.tsx`
  — **1 file, 67 tests passed**.
- Static caller audit found no helper import/export/executable reference; the
  sole `renderPipeline` hit is the SDK forbidden-name test.
- Patch identity: `git rev-parse HEAD` =
  `77ad1f26afcba2df339e92441a86981ee32866ef`.

No full suite, browser journey, live socket, build, install, or typecheck was
run, per the task boundary. No product edits were made by this review.

## Owner action

App owner review/merge is requested through the accompanying durable peer note
and App hub inbox entry. No manager ledger entry was edited; the owner/manager
should record the deletion only after merge.

