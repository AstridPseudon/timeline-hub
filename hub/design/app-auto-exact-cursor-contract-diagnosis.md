# Automatic placement: the recorded failure precedes readiness

## Finding

The surviving final-run evidence contradicts the premise that `prepare()` is
stalled at `taskEventsReady()`. The real gate submits the default **By reference**
form without a reference image. `buildSubmissionTaskParams()` returns `null`,
and `queuePromptGenerationTask()` returns before invoking `onGenerate`.
Consequently `ImageGenerationModal.handleGenerate()`, placement `prepare()`, and
the direct operation readiness read are never reached for that submission.

This is an invalid gate stimulus, not evidence of a Runtime cursor defect. No
product fix or readiness delay is justified by that evidence. The original
approval, command owner, lane, anchor, closure, IDs, admission request, and
retirement guards are unchanged. All original tests and browser assertions are
unchanged; three focused regression tests were added.

## Exact sources and limits

- Assigned App parent: `693dc753ff2bd5e4032570e2a34309e10fb1e2de`, tree
  `ec57f1f4c794ec239d8aec5cfa9c74fea48d9f30`.
- Original central run `1020175019-31635` actually snapshotted tree
  `fac2f569ce659b7c4f466a14ebc3c09f55a5137a`. Its only difference from the
  committed parent is a `console.error('[timeline task events readiness]', …)`
  inside the direct readiness response callback. That message is absent from
  its surviving diagnostics. Its absence alone is not proof, since the
  diagnostics retain only the last 40 entries.
- Frozen Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`.
- Frozen Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`. The previous design and the
  registered suite's `TIMELINE_BUNDLE_RUNTIME_HEAD` contain an extra trailing
  `2`; that string is not a real SHA. The actual Runtime checkout named by
  `ASTRID_RUNTIME_CHECKOUT` resolves to the correct 40-character SHA above.
- Public Composition **0.0.12**, the archive the unchanged browser gate
  explicitly extracts: SHA-256
  `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
- This is the older App/public12 cohort, not current production or a current-root
  qualification. No port or independent-review claim is made.

The original central result directory retains `log.txt`, `snap`, `request`, and
`summary`, but **not** its referenced `trace.zip` or response resources. The
central `bin/test-run` removes the snapshot immediately after the command exits.
The referenced snapshot is gone, and no automatic-placement trace remains under
`/home` or `/tmp`. Therefore the original HTTP response bodies cannot honestly be
called captured or inspected. This report distinguishes the surviving request
evidence, the frozen implementation's output, and a new unchanged-gate capture.

## Surviving original evidence

Source: absolute
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/app-m2-auto-task-events-ready-deadlock-e2e-auto-current-root3599-tree-final-agent8130-runtime2c4-public12-e2e-integration-1020175019-31635/log.txt`.

1. The reported page shows **Upload your first reference image** and the
   By reference / Just text controls. The gate selects **Managed** prompts,
   enters the prompt, and clicks Generate; it never selects Just text or uploads
   a reference. `useGenerationSource.ts` initializes to `by-reference`.
2. The operation performs one acquire/health/handshake/realm sequence and then
   continues event polling. There is no operation DELETE/rebind in the complete
   operation request list. This is evidence of a continuing operation, not a
   claim to have inspected its private handle or authenticated response identity.
3. Subsequent requests include this actual cursor:

   ```text
   GET /runtime-config/v1/operation/runtime/v1/events?limit=50&cursor=eyJrIjpbIjAiXSwibnVtZXJpYyI6dHJ1ZSwicyI6ImV2ZW50czoqIiwidiI6MX0
   HTTP 200
   ```

   Decoded opaque cursor payload (diagnosis only):
   `{"k":["0"],"numeric":true,"s":"events:*","v":1}`.
   Unlike HTTP 200 alone, the outgoing cursor is evidence the poller already
   consumed a response, passed the generated page decoder, validated
   `next_cursor`, and assigned its cursor. The poller calls `markReady()` in
   that same synchronous continuation before another request can be issued.
4. No capability lookup or task admission follows the Generate click. That is
   consistent with the earlier form guard; it does not establish a readiness
   await. The last-60 response list cannot establish every earlier request URL.

## Frozen Runtime contract and precise await chain

Frozen `runtime_protocol/server.py:1093` forwards `/v1/events` query `from` to
`RuntimeService.events_page(from_=…)`. Frozen `service.py:7973` distinguishes:

| Request | Empty-store response |
| --- | --- |
| `/v1/events?limit=50&from=latest` | `{"items":[],"next_cursor":"eyJrIjpbIjAiXSwibnVtZXJpYyI6dHJ1ZSwicyI6ImV2ZW50czoqIiwidiI6MX0"}` |
| `/v1/events?limit=50&cursor=<that cursor>` | Same body; the numeric cursor remains valid at the idle tail |
| `/v1/events?limit=50` | `{"items":[],"next_cursor":null}` (ordinary finite paging) |

These bodies were independently reproduced with the frozen service method and
an in-memory empty SQLite events table, without HTTP, servers, or Runtime edits.
That reproduction is not substituted for an original browser capture.

The frozen Runtime TypeScript generator output and App `generated.ts` agree:
`listEvents(cursor, limit, aggregateId, from)` includes `from=latest` when
requested; the page decoder requires `items` to be an array and `next_cursor`
to be null or a string. The handwritten client maps `listEvents(undefined,
true)` to that `from=latest` request. No new header, DTO, cursor format, or
fallback is necessary.

Had placement preparation been invoked, its chain would be:

```text
ImageGenerationModal.handleGenerate
  -> imageGeneration.prepare
  -> assertCurrent(box)
  -> await host.taskEventsReady()
     -> readyRuntimeTaskEvents(queryClient, projectId, exact bound.operation)
     -> await operation.listEvents(undefined, true)
        -> operation run: active() before / after
        -> handwritten withSession
        -> generated GET /v1/events?limit=50&from=latest
        -> operation transport: active() after fetch and after body read
        -> generated page decoder
     -> require truthy next_cursor
  -> assertCurrent(box) again
  -> validate and capture original target/basis
  -> reserve exact request and original approval/IDs durably
  -> admit task
```

The actual earlier branch is:

```text
Generate button
  -> useSubmitHandler -> submitManaged
  -> queuePromptGenerationTask -> getTaskParams
  -> buildSubmissionTaskParams
     generationSource == by-reference && !styleReferenceImageGeneration
     -> toast.error("Please upload a style reference image for by-reference mode.")
     -> return null
  -> return without onGenerate, prepare, or taskEventsReady
```

## Changes and focused evidence

Only two existing test files changed:

- `operationHost.test.ts`: accept the observed numeric cursor through the real
  handwritten/generated operation clients, retain the same operation handle,
  and reject a successful late event body after reconnect retires its owner.
- `useFormSubmission.test.ts`: reproduce the empty-reference managed form and
  assert its existing validation error, no placeholder, and no `onGenerate`.

Exact successful focused command (85 passed, 5 files):

```sh
env -u ASTRID_CHECKOUT -u ASTRID_PUBLIC_CHECKOUT NODE_OPTIONS=--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs NODE_COMPILE_CACHE=/tmp/app-m2-auto-exact-cursor-contract-diagnosis-node-cache node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/operationHost.test.ts src/features/tasks/components/TasksPane/hooks/useRuntimeTaskEvents.test.tsx src/shared/components/ImageGenerationForm/hooks/useFormSubmission.test.ts src/shared/components/ImageGenerationForm/hooks/formSubmission/submissionTaskPlan.test.ts src/tools/video-editor/commands/commitSession.placement.test.ts
```

The first invocation without the existing snapshot preload exited 1 at config
load (`__dirname is not defined`), before executing any tests. Adding that
existing preload resolved the config-loader issue; no repo config was edited.

Other exact checks:

```sh
node node_modules/eslint/bin/eslint.js --no-cache src/integrations/runtime/operationHost.test.ts src/shared/components/ImageGenerationForm/hooks/useFormSubmission.test.ts
git diff --check
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/app-m3-runtime013-producer-source /home/user/work/venv-runtime/bin/python -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-exact-cursor-contract-diagnosis/runtime-cursor-counterexample.py
```

All exited 0. No full suite, project typecheck, install, local browser, Runtime
edit, shared dependency write, or cache write inside a shared install occurred.

## One central unchanged gate

Requested exactly once with:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m2-auto-exact-cursor-contract-diagnosis e2e-auto-current-root3599-tree-final-agent8130-runtime2c4-public12-e2e-integration
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-m2-auto-exact-cursor-contract-diagnosis-e2e-auto-current-root3599-tree-final-agent8130-runtime2c4-public12-e2e-integration-1020180834-11796
```

Run `1020180834-11796`, source tree
`5d7f7588b7018fc0e817e067329dfbc7dc01b4c3`, has exactly the three added unit
tests above. All product code, browser inputs, and strict browser assertions are
unchanged from the assigned parent. Result and credential-free recaptured
response evidence:

- **FAIL, exit 1, one failed test**, at the original `taskPost` wait. Central
  elapsed time 199 seconds, including waiting for the shared browser lock.
- The complete trace was read before central snapshot cleanup. Only event
  response bodies, request URLs/methods/timestamps, UI actions, and the relevant
  validation message were retained. No credential headers, operation handles,
  discovery/config responses, or raw trace archive were saved.
- Absolute retained artifact:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-exact-cursor-contract-diagnosis/central-response-evidence.json`.
- **63 captured HTTP event responses** all have this exact parsed JSON body:

  ```json
  {"items":[],"next_cursor":"eyJrIjpbIjAiXSwibnVtZXJpYyI6dHJ1ZSwicyI6ImV2ZW50czoqIiwidiI6MX0"}
  ```

- The exact operation startup request is
  `GET http://127.0.0.1:37563/runtime-config/v1/operation/runtime/v1/events?limit=50&from=latest`.
  There is exactly **one** such operation `from=latest` request, at startup.
  Subsequent operation requests poll that same numeric cursor. There is no
  second readiness read, capability lookup, composer request, task POST,
  operation DELETE, or successor acquisition in the captured request sequence.
- Trace action `call@54` clicks **Generate 1 New Image** at monotonic
  `43832.222` ms. The frame snapshot at `43951.963` ms contains exactly:
  **Please upload a style reference image for by-reference mode.**
  The trace's ten click/check/fill actions include Managed and the raw
  owner/lane/anchor/prompt inputs; none selects Just text or supplies a reference.

This newly captured real response exactly matches the focused client's fixture
and the frozen Runtime reproduction. The body, subsequent numeric cursor use,
single startup read, and immediate form error together establish the actual
failed branch. There is **no failing response await or operation identity to
repair in this submission**: its existing form validation prevents entry into
the readiness chain. The unchanged gate did not exercise task admission,
reconnect/retry/reload/undo, or zero-legacy acceptance after admission, so none
of those end-to-end outcomes is claimed as newly qualified.

## Peer action

The App gate owner should explicitly provide a valid text-image stimulus using
the existing UI: Just text, a registered model and resolution, one prompt/image,
and no unsupported reference/LoRA controls. Keep every original task,
reconnect, exact retry, reload, guarded undo, and zero-legacy assertion. Do not
weaken form validation, infer authority from the event feed, or add readiness
delays to make that invalid submission proceed. This is a stimulus correction
for the orchestrator to authorize; this worker leaves the requested unchanged
gate intact. No Runtime defect or Runtime change request is supported.
