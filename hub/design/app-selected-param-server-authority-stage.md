# Selected-PARAM server-authority stage

Implemented on App base `080a5743a` (`tl/app-m3-release12-current-safety-compose080a5743`). **D01-app-selected-param stays OPEN.** This is staged source, not production UI activation or paired Runtime/browser qualification.

## What changed

- Added a selected-only gesture/capture port using official `ClipSetParamsArgs` and `EditCommand`. Structural JSON/target/pin/clear checks only; literal expressions and raw 16 pass through unchanged. No Ajv import, schema validator, Agent browser export, local PARAM execution, new DTO, endpoint, command body field, client hash or guard.
- Reused only the retained document/object read adapter and tests from `c660894ff`; did not import its old capture/cohort. Prefetch uses existing generated read ports and retains exact verified document/object bytes. It never reads latest. Successful prefetch is optional: the existing provider resolves the exact pin through its own read ports, so an unavailable browser read does not become a schema-semantic refusal.
- Session persists the original bundle, command values/clear/schema_source, display basis, retained inputs and realm in its existing outbox payload. Selected after-state is `null`, with a visible `pending` state/message. Inputs and realm remain local; the normal commit body is unchanged.
- Only an original accepted bundle authorizes submission at its captured head. A selected draft authored over unacknowledged work is retained unsent, including after its predecessor ACK/reload. The stored accepted-basis flag never changes, and the branch does not recapture at HA.
- Uses the normal durable request reservation, exact body/key retry, typed refusal/conflict handling and inverse command. Acceptance projects the provider closure atomically with newer ordinary previews. Refusal keeps the exact draft and dependent suffix. Existing move/label behavior remains covered.
- Hook exposes the staged port, fences retained reads against display/session changes, and keeps existing legacy-save/history guards. No property panel activation or package/pin changes.

Product delta: approximately **312 net lines** across existing session/hook plus three small source files; 9 total source/test files changed/added. Outbox storage/transport implementation is unchanged.

## Existing provider trace and executable evidence

Frozen Agent source: `931d7ec56dadffc2efdc893fec80b4c4aadf8a8e`. `astrid/sdk/timeline/commit.py::RuntimeCommitService.commit` loads the exact base revision and validates its publication. `_hydrate` reads the request's exact `schema_source`; `_schema_resolver` uses existing `config_source`/`document_object` ports. It executes original commands at the original base before server replay on a newer head. `commands.execute` verifies supplied recorder claims only when present; it creates authoritative records when they are absent. `_scalar_commands.clip_set_params` runs the single native Draft202012 validator.

The socket-free probe uses this actual provider and its existing `DetachedRealm`/`DetachedPort` test fixtures, mocking only the two Runtime ABI exceptions/metadata as the main Agent tests do. Its portable build receipt is explicitly **synthetic**. It proves: absent browser claims, V1 maximum 10 accepts 4→8, exact schema dependency is recorded, V1 raw16 refuses after live V2/removal and JSON reopening the in-memory state, and inverse/redo recover 4/8. The actual provider refusal is currently **409 / status=refused / invalid_edit_command**, not 422. App transport fixtures independently cover typed 422, refused 409 and real-conflict 409. No owner correction/blocker was found for this accepted-base route.

Artifacts: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-server-authority-stage/notes/native-provider-oracle.py` and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-server-authority-stage/notes/native-provider-result.json`. The App acceptance fixtures are deliberately synthetic normal-port transports, not native provider implementations or custody/build qualification. JSON reopening is not a Runtime process restart or durable idempotency proof.

## Exact validation commands and results

Working directory: `/home/user/work/wt/app-m2-selected-param-server-authority-stage`.

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-server-authority-stage/notes/vitest.config.mjs --configLoader=runner --no-cache src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts --maxWorkers=1 > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-server-authority-stage/notes/targeted.log 2>&1
```

**PASS: 8 files, 232 tests, 26.82 s (Vitest 4.1.5).** Includes selected pending/no optimistic after, literal clear/input preservation, raw16 refusal with suffix retained, reload byte/key equality after V2/removal, inverse, a new selected capture after ordinary ACK, ordinary capture after selected ACK, permanently unsent original unacknowledged basis, late-read/pin fences, own `__proto__`/`constructor` keys, and mounted accepted projection with an ordinary move suffix and no legacy writes. Existing tests were not skipped, weakened, deleted or marked expected-to-fail.

```bash
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/clipParamsCapture.ts src/tools/video-editor/commands/clipParamsGesture.ts src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.ts src/integrations/runtime/retainedParamInputs.test.ts --max-warnings 0 > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-server-authority-stage/notes/lint.log 2>&1
git diff --check
```

**PASS: scoped ESLint, zero warnings; diff whitespace check.**

```bash
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-server-authority-stage/notes/native-provider-oracle.py
```

**PASS: actual provider original-base acceptance, retained-only native refusal, JSON reopen, inverse/redo (status 409).** Shared venv used read-only; frozen source archived temporarily inside this worker's notes and removed on exit.

Earlier test iterations: runner config initially hit existing `__dirname` assumptions twice before collecting tests; the private config mirrors the repository config with absolute paths and a private `__dirname` shim/cacheDir. One new test initially used stale fixture display state after ACK; its fixture now projects accepted display state. Subsequent 77-test and 97-test batches passed before the final 232-test pass. No shared dependency/cache repair or mutation was performed.

## Decisions, limitations and next step

**SUPERSEDED 08:36:** the prior request in `workers/app-m2-selected-param-native-capture-port/notes/agent-browser-pure-export-request.md` for a browser-pure Agent validator/export is retired by the orchestrator's 08:36 decision. No such export or second validator is required or requested here. This note records the supersession without editing another worker's directory.

No task blocker. No full suite, central service request, install, build, tsc, browser, localhost, live socket, integration worktree modification, git mutation or pin update was run. Shared dependencies remained read-only; all test config/cache/temp paths were private. The source base's normal contract pin remains unchanged; 0.2.9 composition belongs to the separate pin unit.

Next: manager composes this bounded delta with the official paired Agent/Runtime 0.2.9 source and separate normal App pin, then requests the actual Runtime/browser selected journey. D01 remains OPEN until real V1 8 acceptance, raw16 refusal after V2/removal/restart, lost-ACK exact retry, inverse, reload and zero legacy traffic are proven. The unsent unacknowledged-basis case deliberately remains pending; no automatic conversion into an accepted basis is implemented.
