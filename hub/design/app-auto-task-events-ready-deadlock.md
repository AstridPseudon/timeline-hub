# App automatic-placement readiness deadlock

## Result

Fixed the App-owned event-readiness lifetime/setup defect on the worker branch
`tl/app-m2-auto-task-events-ready-deadlock`, based on App parent
`29ca79958` (`test(timeline): qualify automatic placement real proxy gate`).

The fix keeps the automatic-placement readiness cursor on the already negotiated
editor Runtime operation. It does not add a wire field, header, endpoint, or
fallback. It also retains the existing operation identity fence before and
after admission and the durable reservation of the original placement request
before any task admission.

## Diagnosis

The placement path in `src/tools/video-editor/commands/editorImagePlacement.ts`
awaits `host.taskEventsReady()` before validating/capturing the placement and
before calling the task client. The Provider installed that callback through
`readyRuntimeTaskEvents(taskQueries, projectId)`. The event poller was keyed by
`(QueryClient, projectId)` but constructed its client as a fresh ambient
`AstridRuntimeClient`, independent of the operation acquired by
`RuntimeOperationHost` and exposed by `createEditorImagePlacementHost`.

The predecessor central run
`app-m2-auto-proxy-harness-api-executor-e2e-auto-current-root3599-tree-final-agent8130-runtime2c4-public12-e2e-integration-1020172107-6504`
showed the exact symptom: operation acquisition, operation health/handshake/
realm and `/api/runtime/v1/events` requests returned 200, but
`createEditorImagePlacement.prepare()` never crossed `taskEventsReady`; no
capability lookup or `POST /v1/tasks` was emitted. The repeated event requests
used the ambient `/api/runtime` path and a cursor outside the placement
operation lifetime, so 200 transport responses did not prove that the
operation-bound readiness fence had resolved.

## Change

- `RuntimeOperation` now exposes its existing `listEvents` read through the
  same operation transport and retirement fence as `getTask` and admission.
- `useRuntimeTaskEvents`/`readyRuntimeTaskEvents` accept an optional event
  client. The Provider passes `bound.operation` both when retaining the poller
  for the editor lifetime and when awaiting readiness.
- If the task pane created an ambient poller before operation negotiation, the
  existing `(QueryClient, projectId)` poller is replaced in place by the
  operation-bound poller while retaining its consumer reference count. This
  preserves one cursor/poller lifetime and prevents readiness from returning
  from the wrong client.
- A focused test proves the readiness cursor calls the supplied operation and
  does not call the ambient client.

No task admission or commit payload changed. No authority was guessed, and no
timeout-to-success, bypass, or fallback was introduced.

## Frozen source tuple

This worker is based on the older App/public12 source tuple required by the
brief. The central gate remains the named current-root public12 gate with Agent
`8130a401bf44a518d5a40ae274d398b8c560be55` and Runtime
`2c4ac180c2220bdad966bc01e95ad230e99ce26a2`; no current-root port or
requalification is claimed until that gate reports.
