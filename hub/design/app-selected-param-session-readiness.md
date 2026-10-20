# Selected PARAM session input staging

Status: **BLOCKED for the whole requested native-capture connection; bounded prefetch/session staging is complete and tested.** No activation or writer-readiness claim.

Base: App `55e7e217b` / `tl/app-m2-ordinary028-current-safety-compose`, ROOT10; shared dependencies `/home/user/work/app/node_modules`. This worktree is a delta source for future composition, **never merge its whole tree**. The base lacks the later corpus/history tests called out in the brief.

## What changed

- Reused the reviewed `feacb6405` retained-input adapter and its tests verbatim from `tl/app-m2-retained-param-input-adapter`, plus the reviewed `c5a773924` authenticated-client forwarder/test delta from `tl/app-m2-verified-read-session-adapters`. Those are prerequisites copied into this base, not newly qualified native capture implementations. Future composition should deduplicate these existing adapter deltas.
- Added optional source-only `paramReadClient` injection to the existing command session/hook and `clipParamsPort.prefetch(originalBasis, originalPin)` / `invalidatePrefetch()`. No production caller supplies the injection; no UI producer or provider/registry writer was changed.
- Prefetch requires an unchanged session-issued capture, uses its exact raw parent/occurrence target and native `elementRef`/`element_ref` precedence, and freezes a detached full `{document_id, version, content_digest}` before asynchronous reads. It returns that same original basis plus the frozen existing native `schema_source`, `schema_inputs=[(VerifiedDocument, objects)]`, and `realm_id` facts. No command/basis is recaptured from live display after the reads.
- Read exactly one uniquely selected admission object via normal verified document/object methods. No latest read, descriptor schema, caller hash, cache, queue, backend, package/pin/root/wire/DTO change, or inferred defaults. With no cache, every read carries the entire original project/realm/pin scope; there is no cross-pin or cross-scope cache alias.
- Reject late results after another selection capture (including failed capture), explicit selection cancellation, another prefetch, local generation change, observed head/bundle/projection change, disposal, hook display/head/read-generation change, or an earlier legacy save. A future selection consumer must call `capture` or `invalidatePrefetch` when selection changes; this stage installs no input into a global/current selection and creates no selection UI wiring.
- Kept original `clipParamsCapture.ts`, its unsupported-selected-input refusals, existing command guards, finish/submit, durable outbox, request IDs/idempotency keys, retry, recovery and inverse paths intact. Prefetch returns detached input facts only; it never treats read-port bytes as a validated element schema. Pending reads/refusals do not submit or modify the draft/outbox.

## Concrete blocker / contract evidence

The brief's `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-clip-params-contract.md` does not exist. Actual names were checked in the retained-read reviews and immutable Agent `027bd16d96010544331c953c0e1014e161786e71:astrid/sdk/timeline/_scalar_commands.py` via `git show`.

Agent's native capture accepts `capture_clip_set_params(bundle, select, values=..., clear=..., schema_source=pin, schema_inputs=[(verified, objects)], realm_id=...)`; its pure native selected resolver validates document/portable bytes/resources/build/descriptor identity and records `params.schema`, `params.snapshot`, `params.element` and retained documents. The current App base's `clipParamsCapture.ts` only accepts `values`/`clear`; `validateValues` explicitly refuses changed selected-pack values and there is no callable browser selected-schema capture implementation or native capture process/port in this base. Both reviewed adapters only read inputs. Official client 0.2.8 supplies the reads, not that native capture implementation.

Consequently the staged tuple cannot yet be fed into the existing TypeScript capture without adding a native selected-schema consumer. Passing it as `schema_source` currently refuses. Implementing an App hydrator/guessed schema, blessing a descriptor/read response, inventing a backend/native process or enabling unsupported wire would violate this task's constraints. The original refusal is preserved and explicitly tested even after a successful prefetch. This is evidence that the stated base does not contain the assumed consuming capture seam, not a change to the settled retained-read decision.

## Executed checks (final source)

```sh
node node_modules/vitest/vitest.mjs run src/integrations/runtime/client.test.ts src/integrations/runtime/retainedParamInputs.test.ts src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.params.test.ts src/tools/video-editor/commands/clipParamsCapture.test.ts src/tools/video-editor/commands/clipParamsGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx --maxWorkers=1 --no-file-parallelism
```

Exit 0: **8 files / 374 tests passed**, 24.85s. New session cases cover detached/frozen original inputs, selected-only I/O, mutable caller-pin/UI isolation, A/B selection and local/head/close/cancel/new-read races, forged captures, unavailable reads, read failures, unchanged selected capture refusal, and simulated retained V1 reads after V2/removal/reopen. Mounted hook cases cover late display/head/legacy-save/disposal changes. Retained-read fixtures are explicitly transport specimens with no valid portable build; they are never presented as native acceptance goldens.

```sh
node node_modules/eslint/bin/eslint.js src/integrations/runtime/client.ts src/integrations/runtime/client.test.ts src/integrations/runtime/retainedParamInputs.ts src/integrations/runtime/retainedParamInputs.test.ts src/tools/video-editor/commands/clipParamsGesture.ts src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx --max-warnings 0

git diff --check
```

Both exit 0. During development, the first new test run had four incorrect assertions that an idle session has no outbox row; corrected the new tests to compare the full before/after outbox instead. An initial lint run found the new read-client effect dependency; added it. The final commands above passed after those corrections.

## Limits / next steps

**UNRUN / unproven:** native selected capture golden equality from this App seam; V1 max10 4→8 acceptance and raw16 refusal under V2 max20/removal/restart; actual Runtime public reads/acceptance/reload/exact retry/inverse/redo with a final matching published tuple; browser journeys. No full suite/test-service request, build, tsc, install, socket, Runtime service or native execution was run. The simulated V1 read tests prove retained input selection, not actual retained storage or native validation. Existing retry/inverse neighboring tests passing does not qualify selected PARAM acceptance.

Recommended owner step: identify/provide the reviewed native selected-PARAM consumer for this source base (or authorize a separately scoped native capture port), then connect this exact detached tuple to that consumer using the original basis and validate the full native command/record goldens and original guards. Follow with the matching published Agent/Runtime tuple's real V1/V2/removal/restart/retry/inverse/browser qualification. Do not retire the selected writer/refusal or activate the injection before that work is qualified.

`KEEP`, `commit-msg`, this report, `ORCHnotes`, and `BLOCKED` written. `DONE` intentionally absent because the whole task is blocked. No commits, merges, checkouts, pushes, integration worktree changes, installs, build output or temporary worktree files.
