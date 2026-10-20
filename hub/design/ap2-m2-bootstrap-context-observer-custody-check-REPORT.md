# AP2 M2 bootstrap context-observer custody review

Verdict: **HOLD** for `tl/ap2-m2-bootstrap-create-response-predicate-source` (`fca9317a0f099c1886971f559861a1a6c53d0919`).

## Evidence

- The production creator is `src/shared/hooks/projects/useProjectCRUD.ts:140-154`. It calls `AstridLocalClient.projects.create()` with the exact trimmed modal name, derived slug, and aspect-ratio metadata, then uses `created.data.project_id` to perform native timeline bootstrap.
- `src/integrations/astrid/projectRoutes.ts:59-70` sends `POST /v1/projects` through `AstridBridgeTransport` and validates `runtimeMutationSchema(runtimeProjectResourceSchema)`, i.e. the existing `{data, receipt}` envelope.
- `src/integrations/runtime/connection.ts:88-90` defines the bridge base as `/api/astrid` (or `${VITE_RUNTIME_ORIGIN}/api/astrid`), while `/api/runtime` is the separate Runtime client base.
- Runtime’s actual route in `/home/user/work/runtime/runtime_protocol/server.py:667-679` accepts `POST /v1/projects` and returns strict HTTP **201** with `{data: resource, receipt: committed_receipt(...)}`. `src/tools/video-editor/data/bridgeContract.ts:97-113` supplies the strict receipt/data envelope schema.
- The candidate predicate in `tests/e2e/local/support/timeline-scope.ts:30-36` strips only `/api/runtime` and then requires `/v1/projects`. Its fixture in `tests/e2e/local/support/timeline-scope.test.ts:35` likewise uses `https://astrid.test/api/runtime/v1/projects`.
- The direct hosted build compiles `VITE_RUNTIME_ORIGIN` to `http://127.0.0.1:17340` (`scripts/build-hosted.mjs` and `scripts/hosted-build-origin.mjs`), so the normal project-create response is from `http://127.0.0.1:17340/api/astrid/v1/projects` in this journey. Therefore the candidate predicate cannot match the real response and the new waiter will time out. This is a concrete route/source mismatch, not a causal inference from the fake regression.
- The context-level `response` channel is the right observation surface and the waiter is created before the Create Project click. The exact POST/name/strict-201 checks and malformed JSON refusal are present in the helper. The exact project ID response readback, native timeline reservation, selected project/timeline equality, realm equality, and exact URL wait are also scoped correctly; the prior URL alone cannot satisfy the new wait.
- The diff leaves the existing reservation, ACK-loss, retry, restart, inverse, opaque-data, ordering, and zero-legacy-save assertions unchanged. The existing context-only scope tests remain, and the added list/readback evidence does not select an arbitrary latest/list project.

## Smallest required correction before approval

Make the predicate match the actual bridge source (`/api/astrid`, including the configured gateway-origin form) and add an explicit source/origin guard appropriate to the hosted journey. Keep the exact `/v1/projects`, POST, submitted-name, and 201 guards. Re-run the support unit lane and the named bootstrap journey after that correction; do not broaden matching to arbitrary response status, latest project, or list contents.

The candidate has no wrapper/hash changes to approve. No source files were edited by this review.

## Checks

- `git diff --check hub/tl/integration...tl/ap2-m2-bootstrap-create-response-predicate-source` — passed (no output).
- Browser, socket, `request-test`, full, and repeat-old-gate runs — not run, per the task’s explicit review restrictions.
