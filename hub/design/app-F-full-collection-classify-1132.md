## Result

Classified all six failures as a shared legacy `complete_task` scope issue, not a live Runtime/App defect.

| File | Project blob | Result / classification | Smallest owner |
|---|---|---|---|
| `billing.test.ts` | `091fab77…` | 0 tests; Node rejects transitive `https://esm.sh/@supabase/supabase-js@2.49.4`; dead-scope/deletion candidate | U3 integration; A4 deletion |
| `handler.placement.test.ts` | `8cd97e2f…` | Same; `handler.ts` transitively loads billing/request/orchestrator | U3/A4 |
| `orchestrator.gate.test.ts` | `1ea86e28…` | Same via `orchestrator.ts` → `orchestratorCore.ts` | U3/A4 |
| `orchestrator.test.ts` | `57c78481…` | Same via `orchestratorCore.ts` | U3/A4 |
| `params.test.ts` | `672510fb…` | Same via `params.ts` → `paramsGeneration.ts` | U3/A4 |
| `request.test.ts` | `33803a80…` | Same via `request.ts` | U3/A4 |

Baseline: `2a288e629c47d3020cd1fd83558ac949eec3d6cf`, tree `d7136487…`; all six files and the complete_task production closure are absent.

Project: `e8a593e1d38d9e84207de1f97806b535ec1a1a8f`, tree `c94c4670…`; the six suites and legacy Supabase scope were reintroduced. The root App Vitest config lacks the existing edge alias for the remote Supabase type import.

Commands/results:

- Baseline targeted Vitest: exit 1, `No test files found`.
- Project root Vitest, Node `20.20.0`, Vitest `4.1.5`: exit 1, `6 failed`, `0 tests`, exact error `Only URLs with a scheme in: file, data, and node are supported ... Received protocol 'https:'`.
- Existing `supabase/functions/vitest.unit.config.ts`: exit 0, `6 passed`, `33 passed`.

Static call-graph evidence supports D52: current production flow is App `createTask` → Runtime `/v1/projects/:slug/tasks` admission → Worker/Runtime settlement. No App, Agent, or Runtime production caller references `complete_task`; current docs explicitly mark the Supabase task lifecycle historical. External deployed Supabase callers were not live-probed, so deletion is a strong candidate, not externally proven.

No source, test, config, or worktree files were changed. Commit message and `DONE` marker were written.