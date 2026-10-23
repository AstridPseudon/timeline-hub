# P1 / A2 first-draft chain proof

Result: **P1 full-chain NO-GO on the first actual A2 draft.** The real draft is healthy for its isolated local-save unit scope, but it does not mount that session into the App and does not expose the v2 request/reply DTOs needed for a Runtime+Agent chain. No integrated three-products scenario was added and no browser/socket/heavy farm run was requested.

## Identity and scope

- App HEAD: `e739d880e711c3267cff5f72c172d85092fdbeee`
- Base: `hub/timeline/app/tl/app-A2-save-funnel`
- Worktree: clean; no tracked repository edits.
- R1 reference named by the brief: `draft8a66b1ac88b88ee437e42ba4b7d14ad67930d360`; this proof did not fabricate a cross-repo launcher or execute a real farm journey against it.
- Source under audit:
  - `src/tools/video-editor/commands/localSaveSession.ts`
  - `src/tools/video-editor/commands/localSaveSession.test.ts`
  - mounted path: `useTimelineState.ts:622` → `useTimelineSave.ts:64` → `useTimelinePersistence.ts:399-403`

## Exact checks

Logs are retained at the following absolute paths:

```text
/tmp/ap2-p1-a2-chain-draft-proof-vitest.log
/tmp/ap2-p1-a2-chain-draft-proof-vitest-list.log
/tmp/ap2-p1-a2-chain-draft-proof-tsc.log
/tmp/ap2-p1-a2-chain-draft-proof-eslint.log
/tmp/ap2-p1-a2-chain-draft-proof-diffcheck.log
```

| Command | Result |
|---|---|
| `node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/commands/localSaveSession.test.ts` | PASS — 1 file, 13 tests |
| `node node_modules/vitest/vitest.mjs list --config config/testing/vitest.config.ts src/tools/video-editor/commands/localSaveSession.test.ts` | PASS — positive nonzero list of 13 tests |
| `node node_modules/typescript/bin/tsc --noEmit` | PASS, exit 0 |
| `node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/localSaveSession.ts src/tools/video-editor/commands/localSaveSession.test.ts --max-warnings 0` | PASS, exit 0 |
| `git diff --check` | PASS, exit 0 |

No full suite, browser, localhost/socket, or heavy run was performed.

## Chain-leg evidence

| Promised leg | Status | Exact boundary and limitation |
|---|---|---|
| Split captures a created right clip ID | **PASS partial / FAIL real App** | Unit test `localSaveSession.test.ts:73-104` persists `clip.split`, `args.right_id: "right"`, and `created: ["parent/clip:right"]`. This is authored fixture data; `createLocalSaveSession` has no production import/caller (the only repository reference outside its own source is the test). |
| Dependent trim targets the newly created ID | **PASS partial / FAIL real App** | The same test persists the second intent with `basis: { after: predecessor }`; `trimCommands` targets `parent/clip:right`. No mounted App gesture submits this session intent. |
| Accepted reply and canonical suffix adoption | **PASS mock only** | `localSaveSession.test.ts:73-104` uses `vi.fn` transport and synthetic `result(...)`; this is not Runtime acceptance. |
| Intervening Agent edit | **UNEXECUTED** | `localSaveSession.test.ts:132-149` adds an in-memory `agent: "preserved"` field to a mocked canonical result. It does not call Astrid/Agent or Runtime. |
| Merged reply | **PASS mock only; FAIL v2 contract** | `localSaveSession.test.ts:132-149,183-207` sets `response.data.status = "rebased"` in a fixture. It never receives v2 `merged`. The generated validator at `src/integrations/runtime/generated.ts:170-177` accepts only `accepted`/`rebased`. |
| Refused predecessor and dependent revalidation/rollback | **UNEXECUTED real refusal** | `localSaveSession.test.ts:231-275` covers synthetic 422 validation and a synthetic 409 with `details.status: "conflict"`; no Runtime `refused` envelope is exercised and no dependent revalidation against a real new head is proven. |
| Lost ACK and restart | **PASS mock-only partial** | `localSaveSession.test.ts:151-181` and `:183-207` replay exact mocked request/key after fake IndexedDB owner recovery. This proves outbox mechanics only, not Runtime durable commit/replay. |
| Runtime/Agent created-ID map | **UNEXECUTED** | The fixture declares `created`, but no Runtime response supplies or verifies `id_map`; the synthetic result leaves the graph empty. |
| App-mounted new session | **FAIL** | `rg` shows `createLocalSaveSession` referenced only by `localSaveSession.test.ts`. The mounted editor instead calls `useTimelinePersistence`, whose save mutation invokes `attemptProvider.saveTimelineAtHead(...) ` at `:399-403`. |
| Real App+Runtime+Agent three-product chain | **UNEXECUTED** | `tests/e2e/local/three-products.p1-commit-v2.spec.ts` is absent. Existing `three-products.spec.ts` has real products, but its current App save assertions use the existing whole-document route and cannot prove this A2 session chain. |

## Concrete missing boundaries and owners

1. **App A2 owner:** wire the exported `createLocalSaveSession` (or an equivalent A2 session) into the mounted `useTimelineSave` path. Provide a real gesture capture/submit caller for split, carry Runtime-created `right_id/id_map` into the dependent trim, and preserve the outbox owner/recovery identity.
2. **App A2/U4p owner:** replace the current whole-document save call for this path with a `commitTimeline` request carrying the v2 controls `label`, `steps`, `merge`, and declared reads, while retaining exact idempotency key/body replay.
3. **Schema/Runtime integration owner:** regenerate and adopt DTOs before farm execution. Current `CommitRequest` at `src/integrations/runtime/timeline-commit-types.ts:68` has no `steps` or `merge`; `CommitAccepted.status` at `:86` has no `merged`; `CommitFailureDetails.status` at `:91` has only `conflict|refused`; `invalid` is absent. The current generated response parser would reject a v2 `merged` reply.
4. **Runtime/Agent owners:** expose a callable real service path that accepts the named R1 provider and returns canonical document, `id_map`, accepted/merged/refused (or approved compatibility forms), and structured error fields. Do not use the unit `vi.fn` transport as substitute evidence.

## Farm handoff

No farm command/selector was issued: the required App caller and v2 DTO boundary are absent, so a browser journey would be fabricated or fail before the promised chain. Once owners land those boundaries, the existing three-products harness is the appropriate dependency; add exactly one real `tests/e2e/local/three-products.p1-commit-v2.spec.ts` case, retain all existing success/refusal assertions, and list it positively before farm execution.

P1 remains **NO-GO**, while the 13 passing local-save tests remain valid partial outbox/recovery evidence.

