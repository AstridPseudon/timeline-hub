# AP2-M2 project-create response predicate/source repair

## Result

Fixed the TEST-LOCAL bootstrap project-create observation path on current
`hub/tl/integration`. The production project-create source was not changed.

## Root cause

The retained `bootstrap-scope.json` contains only `beforeCreate`, so the
timed-out gate produced no project-create response evidence. Current App
source shows the normal flow clearly:

- `AstridLocalProjectRoutes.create()` sends `POST /v1/projects` with JSON
  `{ name, slug, metadata }` and validates a strict mutation envelope
  `{ data, receipt }` (`src/integrations/astrid/projectRoutes.ts:53-71`,
  `src/tools/video-editor/data/bridgeContract.ts:109-113,409-418`).
- `useProjectCRUD.addNewProject()` uses the trimmed submitted name, takes the
  project ID from `created.data.project_id`, then awaits native timeline
  bootstrap before returning the created project (`src/shared/hooks/projects/useProjectCRUD.ts:129-162`).
- Native bootstrap is a separate timeline create/init flow keyed by that
  returned project ID (`src/integrations/runtime/createDefaultTimeline.ts:55-84`).

The previous real gate with the broad URL wait reached the later strict scope
assertion with the pre-create project ID. That proves the click/create flow
does occur; the failing observation boundary was `page.waitForResponse`, which
does not see this service-worker-routed bridge response in the locked harness.
The pure route/body matcher was not the product gap.

## Old -> new guard map

| Old | New |
| --- | --- |
| `page.waitForResponse(...)` observed the named project response and timed out before `projectCreate` evidence. | `BrowserContext` response observation sees service-worker-routed responses. |
| Inline predicate accepted the route/body shape only at the page event boundary. | `isCreatedProjectResponse()` requires HTTP 201, normalized `/v1/projects`, POST, and exact parsed request `name`. Malformed bodies fail closed. |
| Broad URL wait could settle on the pre-create project. | Existing custody-approved `waitForCreatedProjectUrl()` requires `/tools/video-editor` and the exact response `project_id`. |
| Project/timeline scope could be mixed across observations. | Existing strict `{ realmId, projectId, timelineId }` equality remains; response project ID is checked against Runtime readback and native timeline-create route. Exact selected timeline list lookup and lifecycle/retry/undo/zero-legacy assertions remain. |

The offline regression uses the retained project name `Direct Journey 927865`,
the real request JSON fields, the real `/api/runtime/v1/projects` URL shape,
HTTP 201, and the real `{data, receipt}` response envelope. Its fake browser
surface exposes only `context.waitForEvent('response')`; the old page-level
waiter therefore fails this regression rather than silently passing a page
that cannot observe the response.

## Checks

- `node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts` — PASS.
- `npx eslint tests/e2e/local/support/timeline-scope.ts tests/e2e/local/support/timeline-scope.test.ts tests/e2e/local/three-products.spec.ts` — PASS.
- `node_modules/.bin/tsc -p tsconfig.node.json --noEmit` — PASS.
- `npx playwright test --config playwright.three-products.config.ts --list tests/e2e/local/three-products.spec.ts` — PASS; 12 tests listed, including exactly one bootstrap consumer test.
- `git diff --check` — PASS.

Not run: browser, local sockets, Runtime Door, full suite, `request-test`, or
any blind retry. No shared provider/session/API/pin/schema/product source was
changed; no build output was created.

## Review / next step

The candidate is ready for independent custody review. That review must verify
the old/new guard map, the unchanged original scope/lifecycle controls, and
the context-only offline regression before any new authorized central gate.
The real post-change browser qualification remains unverified.
