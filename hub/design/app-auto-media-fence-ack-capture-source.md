# Native automatic capture after Runtime media-fence ACK — source only

Completed on App base `b6a3632c15bb8f5c71946f683fa0b185892c4296`. Production host/task submission remains **INACTIVE**. PLAN and the three required source/fence reports were read first; the Runtime ACK and independent APPROVE are adopted without a new guard or contract.

## Small diff and design

Only `src/tools/video-editor/commands/nativePlacementCapture.ts` and its existing test changed. Product **+4/-7 (net -3)**; tests **+106/-23 (net +83)**. The callback now returns `{ commands }` from the existing original-read/native capture stage after its unchanged final synchronous identity/claim assertion. Native `resolved`, `expect`, `authorship`, `reads`, `selections`, `bindings`, and `created` claims remain inside each EditCommand. Records/after-bundle/capture details are not new commit authority or new wire fields.

The existing requester capture port accepts JSON. A commands payload uses the established command envelope; the unchanged outbox supplies the original head basis, links the continuation, and durably reserves the exact built request/body/key before transmission. No second journal, DTO, guard, producer proposal or epoch is introduced. This choice does not invent authority: original approval/policy, owner, anchor, lane, saved fallback, reserved birth ID, readClosure/head, task locator and exact media pin are still validated/retained by their existing owners. The verified-media method still runs on the SAME requester client. All before/after-await checks, including rejecting-read checks and the final synchronous callback assertion, are unchanged.

No requester, outbox, session, caller/UI, task POST producer, proxy, root, package/lock/pin or generated source changed. No old cohort was imported. Existing pinned versions are historical and unchanged; this is not paired qualification.

## Exact references

- Native source read immutably with `git show`: Agent `80f5149631bb2b08c0569a2a53192e14442991e7`, `astrid/sdk/timeline/native_auto_placement.py`. Existing twelve native goldens and guard probes remain unchanged. Retained corrected-port `vectors.json` SHA256 is `ad0a0d423d513cf22d201d450ebb9aaeb5402f7a2a397b5613a832271bb7f8ae`; its first approval/media/verified input matches the adapter fixture exactly. The callback positive checks unchanged complete-command hash `69f80c68b553835f2a689db01ef7c22759960e0585b178100e1ed1f1a0da7341`; the unchanged read-stage positive also checks complete-record hash `e81658b6c48156030b1467ffbd21393d589d1d99c182d99d86d9bde9f50bd0d9`.
- Runtime API read immutably with `git show`: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, `runtime_protocol/timeline_commit_port.py::{RequestCommitPort.selected_media,RequestCommitPort.validate,MediaReads.selected}`. The public verified read returns the exact selection plus intrinsic metadata. Declared selected-media values are re-read at acceptance. Authority/transactional race evidence is the existing `runtime-media-completion-fence.md` plus `runtime-media-fence-independent-review.md`; it was not rerun here. Normal completed image/video uses that five-field path, not `producer.guard` (which requires an admitted exact authoring proposal).

## Every obsolete expectation pair

| Old passing expectation | Required replacement |
| --- | --- |
| `never returns bare native commands as a requester payload`: successful native capture still throws `task/attempt guard is unavailable` | `returns the original native commands and all claims as the requester payload`: exact native golden command hash, only the commands envelope, original input untouched, one same-client verified read |
| `retains approval/pin/IDs and a visible guard gap across reconnect with zero queued writes`: successful native capture persists a missing-guard conflict and builds/transmits nothing | `durably captures original %s commands/pin/IDs and retries exact saved bytes after reopen` (image and video): original capture becomes one durable intent at the original head; pending request/body/key exists before send; reopen preserves exact commands/claims/pin/IDs/approval/readClosure; fixture lost-ACK retry sends identical bytes/key without rebuilding, recapturing, or refreshing media; fixture acceptance and duplicate recovery preserve linkage |

Only those two obsolete missing-guard expectations changed. Every other pre-existing refusal/input/lifecycle case remains, including missing context/verified host method, approval/policy/owner/anchor/lane/fallback/ID mismatch, unsupported opaque policy, locator/pin failures, refreshed head/publication/raw revision, foreign scope, wrong verified pin, invalid intrinsic metadata, and identity/claim interruption before/after awaits. The original 93 requester tests and storage/session tests were untouched. No skip/xfail/weakened behavior expectation was added.

Two added genuine refusal cases (native metadata refusal and commit-conflict fixture) reopen twice after metadata/pin changes and require the full saved record, commands/guards, original inputs and pin to remain equal apart from claim generation. They perform no recapture or refreshed reads; capture refusal queues/sends nothing, and commit refusal retains its rejected exact pending request. Image/video success tests open fresh outbox handles over the same fake IndexedDB and compare complete payloads; all transport/ACK responses are trusted fixtures, not Runtime acceptance or actual process/browser crash evidence.

## Exact tests and results

Working directory: `/home/user/work/wt/app-m2-auto-media-fence-ack-capture-enable-source`. The following abbreviations expand exactly:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-auto-media-fence-ack-capture-enable-source
D=/tmp/app-coherent-deps12/node_modules
```

```sh
node --require $W/runner.cjs $D/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/nativePlacementCapture.test.ts src/tools/video-editor/commands/autoCapture.test.ts src/tools/video-editor/commands/authoringBundle.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/placementRequester.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/commitSession.test.ts
```

**PASS: 9 files / 642 tests, exit 0, 19.68s** (`$W/targeted-final.log`), including 43 adapter tests and 93 unchanged requester tests. Private12 runner, runner config loader, no cache, one worker. This is the final source tree; no subsequent source edit.

```sh
$D/.bin/eslint src/tools/video-editor/commands/nativePlacementCapture.ts src/tools/video-editor/commands/nativePlacementCapture.test.ts --no-cache
node $W/check-types.cjs
git diff --check
```

**All PASS, exit 0.** Compiler API check: **0 diagnostics** in the three-file adapter/requester import closure, strict/noEmit, existing JS fake-IDB fixture included, no project tsc/emit. Logs: `$W/eslint.log`, `$W/types.log`. Runner/type-check scripts are copies of the prior adapter worker's reviewed helpers, stored outside the repo.

Initial targeted command used the same Vitest flags with only `nativePlacementCapture.test.ts placementRequester.test.ts` (full paths under `src/tools/video-editor/commands/`). It reported **135 passed / 1 failed, exit 1, 3.27s** (`$W/targeted-initial.log`): the new video positive lacked required intrinsic duration. Corrected the new trusted video fixture to include duration=12; no product policy or assertion weakened. The final nine-file run above includes that correction.

No shared dependency/runtime/venv/cache changes, install, full suite, build, project tsc, browser, localhost/socket, central request, git commit/merge/rebase/checkout/push or integration-worktree edits. No build/temp output remains in the worktree.

## Unrun activation gates and disposition

No blocker to this bounded source task; no settled decision changed. Keep for independent review. This removes only the obsolete source refusal, not the following open activation gates:

1. Real authenticated same-host verified-media forwarding, synchronous lifecycle binding, original saved-document/pinned raw-read injection and authorized explicit approval codec/ingress; UI/task submission remains inactive.
2. Coordinated final Agent/schema/Runtime/App pins and real native image/video commit acceptance; actual invalidation races and transactional acceptance with this semantic provider, canonical reload, undo/redo/strict ABA and zero legacy writer traffic.
3. Real browser/process restart and lost-ACK journey with exact original request/pin/guards/IDs, live conflict/refusal/draft retention, and security/lock qualification. Any socket/browser/full work must use the central service in a separately authorized task.
4. Existing pool promotion/parent births/extent growth and owner short-video/style requirements remain inherited open items. Runtime's independently reported repeated-generation publication availability defect stays with Runtime/owner triage; it is not a reason to fabricate App authority.

Recommended next step: review this narrow diff and its two expectation pairs, then qualify the production host/ingress and coordinated acceptance journey as separate work. `DONE` means this source-only task is complete. `KEEP` requests retaining the candidate for review.
