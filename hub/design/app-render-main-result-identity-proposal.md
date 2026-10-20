# App render main-result identity proposal

Status: source-only proposal for Viewing-owner review. No App files are changed or activated by this worker.

## Problem

`useRenderState` currently stores the number returned by `flushPendingSave()` in `renderRevisionRef` and `TimelineRenderControls` labels a completed managed result as `Timeline version N`. That number is the App's local display/config counter. It is not the Runtime document version: a local counter of 7 can be admitted by Runtime as `config_version` 12.

The existing Runtime response already carries the needed authority. After the existing neutral mutation validation and `runtimeTaskToAdmittedTask` projection, the admitted task is read at:

```text
task.spec.spec.inputs.timeline_authority
```

The inspected Runtime authority contains `project_id`, `timeline_id`, numeric `config_version`, and, for canonical parent composition renders, `parent_revision_id` (plus existing immutable hashes/input details and the existing seam report). The current App adapter retained only the seam report, so the smallest App seam is to retain that existing authority object in the existing task projection and consume only its identity/scope fields.

## Proposed behavior

- Keep the durable save barrier and its valid-ack check. Its returned value remains a pre-admission readiness fence, never result identity.
- On admission, copy Runtime `config_version` to the existing `RenderResultInfo.revision`; copy `parent_revision_id` to an optional `parentRevisionId` pin when present.
- If Runtime omits the authority, publish `revision: null` and `parentRevisionId: null`; never fall back to the local save counter.
- Validate the admitted task's existing `project_id`, and any returned authority project/timeline fields, against the requested project/timeline. Refuse a mismatched admission.
- Apply the same task-id/project/timeline checks to detail polling. Existing poll-generation checks continue to discard a late read from an older task; an old ACK cannot relabel the current result.
- Keep all existing MAIN behavior: `/api/astrid` capability/admission, operation-scoped v3 idempotency, command flush ordering, seam report/advisory UI, streaming save picker, blob fallback, compact controls, native video download/context-menu suppression, cancellation, and error handling.

No new head read, wire field, endpoint, DTO/schema generation, requester/provenance protocol, or renderer dependency is introduced. The only new object is an internal projection of fields already present in the admitted task read model.

## Exact patch

Apply [app-render-main-result-identity-proposal.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-render-main-result-identity-proposal.patch) at the current App HEAD. It changes only:

- `src/integrations/astrid/runtimeReadModels.ts`: retain the existing Runtime `timeline_authority` object instead of projecting only `visual_seam_report`.
- `src/tools/video-editor/lib/renderRouter.ts`: extract the existing authority, return its identity with the admitted task, and refuse project/timeline scope mismatches.
- `src/tools/video-editor/hooks/useRenderState.ts`: replace the local revision ref with admitted Runtime identity and fence task reads.
- The two neighboring test files: add authority-vs-local-counter, missing-authority, scope-refusal, and late-old-task-read coverage; existing test bodies remain intact.

The patch deliberately does not edit `TimelineRenderControls`: it already renders the existing `revision` field and therefore displays Runtime version 12 after the hook supplies it.

## Regression matrix

The added normal tests should remain in the existing Vitest lanes and assert:

1. Admission authority `{config_version: 12, parent_revision_id: "parent-revision-12"}` with save-barrier value 7 yields result revision 12 and the canonical pin.
2. Missing authority yields unknown identity, not revision 7.
3. Wrong admitted project refuses before polling; wrong timeline authority refuses likewise.
4. A detail read for an older task that resolves after a newer render generation is ignored and cannot replace the newer result identity.
5. Existing seam-report/admission, picker/blob, compact/native suppression, cancellation, and operation-key assertions remain unchanged.

Suggested targeted command after owner application (private cache, no shared dependency writes):

```sh
VITEST_CACHE_DIR="$PWD/.vitest-render-identity" npm exec vitest run --no-cache \
  src/tools/video-editor/lib/renderRouter.test.tsx \
  src/tools/video-editor/hooks/useRenderState.test.tsx
```

This worker did not run Vitest, build, browser, socket, full-suite, install, or TypeScript checks, and makes no activation or qualification claim.

## Review decision requested

Approve or revise the internal `parentRevisionId` name/display policy. The source evidence supports retaining the exact Runtime field as an optional result pin while preserving the current user-facing `Timeline version N` label. 
