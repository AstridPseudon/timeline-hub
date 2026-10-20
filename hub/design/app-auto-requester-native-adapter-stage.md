# Native automatic placement requester adapter — source stage

Completed on App base `ca51f422597adea38e5f5bd981b7f12fab38fff4`. **Activation OPEN.** The original-closure/native read-and-capture stage is connected to the SAME existing requester callback. The callback deliberately retains a visible refusal rather than returning an unfenced commit payload: the inspected producer contract cannot guard this media-only placement. This is the brief's permitted concrete capture-gap outcome, not completed automatic placement or Runtime acceptance.

## Scope and size

Only these worktree paths changed:

| Path under `src/tools/video-editor/commands/` | Authored change |
| --- | --- |
| `nativePlacementCapture.ts` | New, 76 lines / 4,863 bytes. Original read port, checked read/capture stage and inactive requester callback. |
| `nativePlacementCapture.test.ts` | New, 279 lines / 22,320 bytes, including one immutable native input/command/record golden. |
| `placementRequester.ts` | +13/-2 lines. Optional generated verified-media method and explicitly opted-in callback context, supplied from the existing effect's client/authorization/claim closures. Existing callbacks retain exactly two arguments. |

**Net product +87 lines; tests +279; total +366.** No outbox/storage, UI, task POST producer, root, pins, dependencies, browser/server/client implementation, generated file or old cohort was changed. No second journal, hydrator, recorder, wire type, operation, provenance field or worker write authority was added.

`readNativePlacementCapture` snapshots the original continuation and scope. It requires the existing `policy` slot to contain the explicit native approval, matching the separately persisted auto-approval, owner, raw anchor, preferred lane, saved fallback and sole reserved birth ID. Unsupported opaque policies remain refused; there is no retrospective approval/legacy-policy inference. The approved `output`, prepared admission bytes/key and locator remain owned by the unchanged requester. This local policy convention has no production producer/decoder yet.

`OriginalPlacementRead` is an explicit host injection consuming the ORIGINAL continuation/readClosure. It must return its original head pair and savedCanonicalDocument, using an inline saved document or the existing pinned raw-read callback. The adapter checks head/publication, project/timeline and raw parent revision, then uses the EXISTING `authoringBundleFromDocument`; it never calls head-resolving `loadTimelineCommandBasis`. It does not invent an accepted base for dirty/unknown predecessors. There is no production implementation of this injected read in this unit; the tests label it as trusted fixture data, not authenticated Runtime evidence. The injection must preserve original read parameters through any internal reads and run against the known host.

Verified intrinsic metadata comes only from the optional existing generated `getProjectVerifiedMedia(projectId, selection)` method on the exact requester client object. It receives the saved five-field media pin. The requester supplies live identity/claim checks, and the adapter invokes them before and after every await inside the capture effect, including rejected reads and the existing opener. Native capture checks verified pin equality and intrinsic facts. No object-ID-only trust, client hashing, metadata guess, latest head or second client is used. Registry create-or-require, native guard claims and strict-ABA machinery are unchanged.

## Contract references and concrete gap

- Native capture: Agent `80f5149631bb2b08c0569a2a53192e14442991e7`, as approved in `app-auto-native-capture-corrected-port.md` and `app-auto-native-port-independent-review.md`. The new golden uses one unchanged input from that worker's retained `vectors.json` (`ad0a0d423d513cf22d201d450ebb9aaeb5402f7a2a397b5613a832271bb7f8ae`) and checks COMPLETE native command and record hashes. The twelve existing native parity cases and neighboring guard probes remain unchanged.
- Frozen producer: Agent `0a0ac7baaa74e15485b10bcbaa80eda1afe48c00`, `astrid/sdk/timeline/producer.py::{build_producer_batch,capture_producer}` and schema `$defs/ProducerAttemptPin`. The exact pin contains task/attempt/executor/fence/runtime_epoch/admitted_target/proposal_digest. `producer.guard` must be first, followed by the ORIGINAL proposal commands, not arbitrary new births.
- Runtime inspected immutably at `8609333456b9537339ee1a5dfc7ffd9609242de8`: `runtime_protocol/timeline_commit_producer.py::_current_attempt` and `ProducerReads.capture` (lines 126, 223–274), plus `timeline_commit_port.py::RequestCommitPort.validate` (387), `MediaReads._output_selection_binding` (653), `_selected_project_media` (709), `selected` (803). Producer capture requires an admitted `authoring_proposal` output and exact stored proposal commands/rationale. A completed image/video publication has no such proposal pin. Prepending a guessed producer guard would be invalid.
- Existing media acceptance DOES re-read the five-field selection and verifies completed state, current attempt ID, settled output and association provenance. It is not absent task protection. However, the inspected media binding compares provenance with the attempt row; it does not compare the current task row's executor/lease_fence/runtime_epoch with that attempt as producer `_current_attempt` does. Same-attempt epoch/fence invalidation is therefore an unresolved source-level gap here, not a demonstrated accepted race. No Runtime race test was run by this App source task. Ordinary source reads cannot establish that a settled media-only placement has the full requested fence.
- App's generated base metadata remains 0.2.8. Read-only `git show` comparison against published Runtime `94114269d1ce23ab3224d7eca5a85138ce2b5fed` / 0.2.9 confirms BOTH generated selection/verified-media method implementations are byte-identical after trimming indentation. The method accepts `(projectId: string, selection: MediaSelection): Promise<VerifiedMedia>` and calls `GET /v1/projects/{id}/media-selection/verified` with the five selection fields. No DTO copy or adoption is needed to describe this seam. `AstridRuntimeClient` at this App base forwards selection through `withSession` (`client.ts:632`) but has no verified-media forwarding method; a production same-host binding is still needed. The approved browser-host branch and its proxy work were not copied or activated here.

`createNativePlacementCapture` exercises the read/capture stage, then throws an explicit missing-normal-media-completion-task/attempt-guard error. Existing storage retains the ORIGINAL approval/request/read closure/IDs/locator and selected pin with a visible `placement_capture_failed` conflict; it queues zero intents and builds/transmits zero commits. The transient native result is NOT persisted or claimed accepted. Reconnect retains that refusal without recapture or rearming. Identity/claim interruption instead escapes the surrounding outbox lifecycle check and retains a retryable continuation without a semantic conflict. No settled policy was changed; the permitted source stage is complete with the guard/binding limitation exposed.

## Exact commands and results

All App commands ran from `/home/user/work/wt/app-m2-auto-requester-native-adapter-stage`. These abbreviations expand to the exact absolute paths used:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-requester-native-adapter-stage
D=/tmp/app-coherent-deps12/node_modules
```

```sh
node --require $W/runner.cjs $D/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/nativePlacementCapture.test.ts src/tools/video-editor/commands/autoCapture.test.ts src/tools/video-editor/commands/authoringBundle.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/placementRequester.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.test.ts
```

**PASS: 9 files / 635 tests, exit 0, 19.49 s** (`$W/vitest-final.log`). This run included 36 new adapter tests. Four additional adapter tests, a test-only fixture extent correction, a test type assertion and an error-message wording change followed; final affected-file validation:

```sh
node --require $W/runner.cjs $D/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/nativePlacementCapture.test.ts src/tools/video-editor/commands/placementRequester.test.ts
```

**PASS: 2 files / 133 tests, exit 0, 2.97 s** (`$W/vitest-adapter-final.log`): 40 new adapter tests plus all **93 unchanged requester tests**, preserving the original requester/synchronous identity probes. Native golden/record parity, exact original pin/IDs after read retry, explicit saved fallback/shared defaults, mismatched policy/base/scope/pin refusal, missing host method, before/after-await identity/claim interruption and same-client real-requester outbox retention/reconnect are covered. The managed/verified transport responses are trusted fixtures, not Runtime acceptance. No passing behavior expectation was rewritten, skipped or weakened.

An initial neighboring run caught the existing exact-two-argument callback expectation; the opt-in context fixed it without editing the original test. An initial new shared fixture used the narrower completion extent; it was corrected to the native shared vectors' wider original extent while keeping the positive placement expectation.

```sh
$D/.bin/eslint src/tools/video-editor/commands/nativePlacementCapture.ts src/tools/video-editor/commands/nativePlacementCapture.test.ts src/tools/video-editor/commands/placementRequester.ts --no-cache
node $W/check-types.cjs
git diff --check
```

**All PASS, exit 0.** Scoped compiler-API check: **0 diagnostics**, strict/noEmit, three adapter/requester files and their import closure, existing JS fake IndexedDB fixture included with allowJs/checkJs=false; no project tsc. The fixture is explicitly cast to the browser IDBFactory port in the test. Private runner establishes config `__dirname`; cache-free runner loading and one worker throughout. No shared dependencies, runtimes, venvs or their caches were written. No install, full, build, browser, localhost/socket, commit, merge, checkout, force, push or integration-worktree mutation was performed. No build/temp output remains in the worktree.

## Activation OPEN / recommended next work

1. Runtime/Agent owners must supply or qualify the normal media-only completion fence using the existing public authority path. Do not fabricate producer proposal pins, epoch fields or hashes in App. Source inspection above is a concrete gap report, not permission to widen the contract here.
2. Bind the original saved document/pinned raw read and this explicit approval codec to the existing authorized requester ingress, plus same-host session/lifecycle verified-media forwarding. No new hydrator or head refresh. Unsupported originals remain visible and retained.
3. Await the final safe normal 22-op Agent/schema/Runtime/client release, then take the coordinated pin and qualify original successful placement, task cancellation/supersession/epoch races, lost ACK/restart/retry, same-pin/same-ID command retention, actual conflict/refusal/draft preservation, accepted canonical reload, undo/redo/strict ABA and zero legacy traffic. UI/task-producer activation and writer retirement remain separate and OPEN. Pool promotion/parent births/extent growth and owner short-video/style requirements remain inherited open items.

DONE denotes this bounded source/read-capture task plus explicit permitted gap report only. It does not denote a commit-capable adapter or production activation.
