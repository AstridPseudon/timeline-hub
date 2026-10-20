# Bootstrap project scope causal repair

Fixed a test observation race, with the original strict project/timeline equality preserved. Source is ready for independent custody review; the real bootstrap journey is **UNVERIFIED**. No browser, socket, build, request-test, full suite, or unchanged26944 rerun was performed.

## Exact cause

26944 did execute f487's intended test: source hash `df2b88dcebca08a9a1a5970108774b1289579209963da7a8611309fc58c15631`, list1, hosted build PASS. Its failure compares a **previously captured local projectId variable** with createScope. It does not measure the final URL's project ID at the failing line.

The f487 code releases init, awaits `creating` (Playwright click delivery), accepts **any** `/tools/video-editor?project=...` URL, and immediately saves its project ID. Only **after that snapshot** does it await the new project name, editor, and timeline URL. `CreateProjectModal.handleCreateProject` awaits `addNewProject`; `useProjectCRUD.addNewProject` awaits `ensureProjectHasTimeline` and its create/init/metadata work before the modal navigates to the created project's URL. A completed click cannot await that React async handler. Releasing the route hold similarly does not await the server ACK or the handler's navigation. Therefore the old project URL satisfies the broad wait while the initializer finishes, and the later timeline read belongs to the newly created project. This is mixed-time test observation, not evidence of a product adopting another project's timeline.

Retained failure values:

| Observation | Value |
| --- | --- |
| create request project (createScope) | `4dcb2321f23d451091785dec01757b74` |
| earlier URL snapshot's projectId variable | `36498405a10c4b2ab9a5412eaf22a9a5` |
| subsequently selected timeline | `d0022034-8d26-5584-8a06-ff87ba3b3d6b` |

Recomputing f487's `stableUuid('astrid-first-timeline:' + projectId)` gives exactly `d0022034-8d26-5584-8a06-ff87ba3b3d6b` for `4dcb…`; `3649…` instead gives `cc267826-f71e-5ae8-9b9b-915885e344bf`. The selected timeline is consistent with the observed create request. No stale-generation/bootstrap-owner production change is justified by this failure.

**Retention limit:** 26944's wrapper deleted `/tmp/timeline-normal014-app.fghg4t`, including its trace/browser output; the harness deletes its Runtime database/audit at stop. The central log remains, but does not retain the normal project-create response, final browser URL, or project/timeline lists. No such old evidence is invented here. Thus the source race and deterministic ID agreement are proven, while the complete historical HTTP/navigation sequence is not recoverable. The prior report's phrase “URL selected3649” overstates what its assertion measured. The252da failure has the same early snapshot before the awaited name check; its additional early list read likewise precedes timeline readiness.

## Source patch and scope

Base `812a609ee7ee02a6abe2fbf96513408e706c830d` lacked the approved bootstrap prerequisite. Applied exactly f487's16-path patch with `git apply`, preserving current surrounding source. Thirteen prerequisite paths, including all production/bootstrap/outbox/provider/client changes, are byte-identical to f487. The **new repair beyond those approved prerequisites changes only** the bootstrap test, timeline-scope helper/test, and App2 wrapper. No new shared session/Provider behavior, settings, shotSet, harness, package/pin/schema, other worktree, or shared dependency change was made. Current ordinary and conflict cases were compared and preserved.

The gate now observes the existing normal `POST /v1/projects` response whose request name equals the submitted name, checks status/id/name and normal GET project read, and asserts the native timeline-create request belongs to that response's exact project. `waitForCreatedProjectUrl` waits for that exact project identity before sampling the URL. The original `expect({ realmId: harness.realmId, projectId, timelineId: selectedTimelineId }).toEqual(createScope)` remains unchanged, with an additional final URL project check. All original pending-owner/create/init/history/retry/restart/undo/list/non-shot/zero-legacy assertions remain. No intercepted request is suppressed or scope adopted from a different project.

The source wrapper now checks the candidate's13 approved files against f487 and pins all3 repaired source hashes, instead of overwriting the repair with the frozen donor test. The unique bootstrap selector, private normal014 tuple, locked public13 graph, and private caches are unchanged. EXIT cleanup preserves status. A later approved run writes only sanitized normal project list, exact create response/read identity, before/after timeline lists, and URL scope snapshots to `bootstrap-scope.json`; the wrapper copies that file to this worker's `scope-evidence/` before deleting its run root. No credentials, headers, raw bodies, arbitrary metadata, or Runtime database are retained.

## Causal regression

The socket-free helper regression uses26944's two project IDs and timeline ID. It starts on the previous project's URL after click completion, proves that URL matches the original broad assertion, holds navigation, and requires the helper to stay pending until the exact created project's URL arrives. It also refuses another project's URL even with the right timeline and a different route with the right project.

Mutation control: substituting the original broad URL match into the helper caused **2 pass /1 fail**, specifically premature settlement (`true !== false`). Restoring the exact project predicate caused **3 pass /0 fail**. Both commands were `node --import tsx tests/e2e/local/support/timeline-scope.test.ts`; retained outputs are `scope-regression-before.log` and `scope-regression-after.log` in this worker folder. The helper was restored in `finally` before other checks.

## Exact verification

All commands ran in `/home/user/work/wt/ap2-m2-bootstrap-project-scope-causal-repair`:

```sh
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/bootstrapInitialization.test.ts src/integrations/runtime/createDefaultTimeline.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.test.ts
```

PASS:4 files,128 tests.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-fixed-pair-gate/sources/agent-4296:$PWD" /home/user/work/venv-app2-native/bin/python -m pytest -q -p no:cacheprovider src/tools/video-editor/commands/fixtures/bootstrap_parity.py
```

PASS:12 tests; one existing unknown `integration` mark warning. The frozen Agent source is used read-only; this proves native semantics, not Runtime admission.

```sh
node --import tsx --test tests/e2e/local/support/timeline-scope.test.ts
node --import tsx tests/e2e/local/support/timeline-scope.test.ts
```

PASS: scope file; direct output confirms3 named tests.

```sh
node node_modules/eslint/bin/eslint.js src/integrations/runtime/bootstrapInitialization.test.ts src/integrations/runtime/bootstrapInitialization.ts src/integrations/runtime/client.ts src/integrations/runtime/createDefaultTimeline.test.ts src/integrations/runtime/createDefaultTimeline.ts src/integrations/runtime/dataProvider.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/bootstrapCapture.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitOutbox.ts tests/e2e/local/support/app.ts tests/e2e/local/support/timeline-scope.test.ts tests/e2e/local/support/timeline-scope.ts tests/e2e/local/three-products.spec.ts --report-unused-disable-directives --max-warnings 0
npm run typecheck:strict-islands
node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit
node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep 'M2 real gate 5 bootstrap actual consumer' --list tests/e2e/local/three-products.spec.ts
sh -n tests/e2e/local/support/bootstrap-wrapper-selector-source-fix.sh
git diff --check
```

All PASS; Playwright only listed1 test in1 file, no browser launched. Additional source checks confirmed13 approved files byte-equal to f487,3 wrapper hash pins match, original strict equality exists, and current neighboring ordinary/conflict test bodies remain unchanged. No generated/build/temp output remains in the worktree.

## Next action / limits

Independent custody review must APPROVE this exact repaired candidate and wrapper before any real gate/browser/socket/request-test. Then the orchestrator can authorize one narrowed bootstrap integration gate against this candidate (not the frozen f487 test), with sanitized `bootstrap-scope.json` retained. Do not reuse26944's result as qualification. Real create/init ACK ordering, normal HTTP/navigation sequence, restart/retry and guarded undo on this repaired candidate remain unverified. No peer-owned production seam is needed for the source-proven observation race; a future normal-create/read mismatch must fail the new early equality and be investigated from its retained snapshots.
