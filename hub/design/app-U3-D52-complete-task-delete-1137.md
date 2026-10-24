Implemented U3/A4/D52: deleted exactly 48 tracked files under `supabase/functions/complete_task/**`, including its exclusive tests. No config, routes, dependencies, or neighboring functions changed.

Deleted inventory:

```text
authContext.test.ts
authContext.ts
billing.test.ts
billing.ts
cleanupMaterializedInputs.test.ts
cleanupMaterializedInputs.ts
completionHelpers.test.ts
completionHelpers.ts
constants.test.ts
constants.ts
deno.json
errors.test.ts
errors.ts
generation-child-diagnostics.test.ts
generation-child-diagnostics.ts
generation-child.test.ts
generation-child.ts
generation-core.test.ts
generation-core.ts
generation-handlers.test.ts
generation-handlers.ts
generation-parent.test.ts
generation-parent.ts
generation.test.ts
generation.ts
handler.placement.test.ts
handler.test.ts
handler.ts
index.ts
orchestrator.gate.test.ts
orchestrator.test.ts
orchestrator.ts
orchestratorCore.ts
orchestratorPolicy.test.ts
orchestratorPolicy.ts
params.test.ts
params.ts
paramsGeneration.test.ts
paramsGeneration.ts
request.test.ts
request.ts
shotValidation.test.ts
shotValidation.ts
storage.test.ts
storage.ts
taskParamNormalizer.test.ts
taskParamNormalizer.ts
types.ts
```

Source proof:

- Project: `e8a593e1d38d9e84207de1f97806b535ec1a1a8f`, tree `c94c46704d0265c0a1d2217e84992a6532420ef5`
- Upstream: `2a288e629c47d3020cd1fd83558ac949eec3d6cf`, tree `d7136487c1dad394e0dbd27d0daee3f1c551de84`
- Post-change `git diff origin/main -- supabase/functions/complete_task` is empty.
- No production imports/callers found across App, Agent, or Runtime. Retained flow is App `createTask` → Runtime task admission/routes; settlement remains Runtime/Worker-owned.
- External deployed-service probing was not performed per task scope.

Tests and checks:

- Supabase neighbor Vitest: 1 file, 1 test passed.
- Root Vitest (`createTask`, `taskRoutes`): 2 files, 20 tests passed.
- `tsc -p tsconfig.json --noEmit`: passed.
- `tsc -p tsconfig.app.json --noEmit`: passed.
- `tsc -p tsconfig.node.json --noEmit`: passed.
- `git diff --check`: passed.
- Scoped lint: not applicable; deletion-only change.
- Full/browser/backend/service/network suites: not run as instructed.

Commit message written and `DONE` marker created. Worker ledger row:

`| U3/A4/D52 | Delete retired complete_task closure and exclusive tests | e8a593e1 | 48 deletions | targeted Vitest + 3 tsc configs pass; lint N/A |`