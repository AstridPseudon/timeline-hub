# AP2-M2 ordinary zero-POST causal diagnosis

## Result

**First causal defect proven: the production extension retains an obsolete TimelineOps adapter whose apply callback has no generic command port.** It falls through to whole-document publication. The Runtime correctly refuses that publication with `409 timeline_commit_required`. Native command capture is never reached; neither another hold-shape conversion nor weakening capture checks can fix this first failure.

The defect is in App-owned shared core (`hooks/useTimelineOps.ts`), so the requested ownership rule was followed: publish an exact minimal patch and peer request, do not compete with its owner by editing shared source. The patch has two fail-to-pass regressions and passes targeted validation in the single private App copy. **No production fix has been integrated or browser-qualified.** The conditional diagnosis/patch handoff is complete; the corrected-source integration gate awaits the shared-core owner.

## Source and served-UI provenance

- Worker base/final App HEAD: `17655a570f92229635092013f28d2c5025f31ef0`, tree `02fbeadf4792077e3145ec4622708e0a90e9a263`.
- Run 22464's reported App `2b70346ec399b1fb5015ab60ca3d0b45f2445940` is a central test snapshot with **that same tree**. It was not a different App source. Its retained log establishes the line-1222 zero-POST failure; its referenced trace/error-context files were deleted by the runner's EXIT cleanup. The original trace could not be recovered. Predecessor 15359 has the same first assertion failure per retained evidence.
- Authorized diagnostic run: `ap2-m2-ordinary-zero-post-causal-diagnosis-e2e-m2-ordinary-integration-1020202058-11433`. Service-created clean committed snapshot `e748df0717429f65890be37ec2706967f985934d`, tree `59741a7043c487a75b37818a6c79017d4662969f`. Only temporary runner/test diagnostics differ from the base; product source is identical.
- Agent commit/tree: `8130a401bf44a518d5a40ae274d398b8c560be55` / `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime commit/tree: `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Existing repo-native runner `scripts/testing/run-central-m2-ordinary.sh` built its own snapshot's hosted dist with its pinned effective Composition 0.0.13 graph. No package/pin/schema/API/dependency change. No separate environment qualification rerun.
- Build-time source SHA-256 matched final unchanged source: extension `477ec52f4da4b5944033959b1a18035972b9c4fbcf58770eb01abcd08f74f087`; generic capture `fc1d25b4c58120485bfc1155c69d8abf7afb4277532d95b30530fafb4ebea506`.
- The fetched entry script `/assets/index-CV5eqmYe.js` matched local dist bytes exactly. All 22 JavaScript asset requests in the trace returned 200 and named assets emitted by that build. The entry is a bootstrap chunk (it does not itself contain the marker button literal); trace static-script bodies were not retained, so no byte-level claim is made for each dynamic chunk.
- `dev/localExtensions.ts` imports the App's `./scene-phase-markers/extension`, not an Agent copy. Its real panel was mounted and clicked. The resulting publication contains the intended parent positions 1/6 and holds 5/3 and retains the incoming crossfade. The intended compiled extension action therefore ran.

## Observed first error and causal chain

The retained diagnostic trace contains one timeline publication:

```text
POST /api/runtime/v1/projects/6cba18db6ba8463296efc99464b01683/timelines/61fe7ca0-bccb-4b46-9c93-a1660f778915/composition-revisions
409
{"code":"conflict","details":{"reason":"timeline_commit_required","status":"refused"},"message":"tracked timeline publication requires a timeline command",...}
```

The UI then says: `The timeline could not be saved because the payload is incompatible with the server schema.` The outbox has an owner but `intents: []`, with no pending command. There are zero ordinary `/commit` POSTs. Console shows the 409 resource failure; no page exception or native `GenericPatchRefusal` occurred. Repeated preview/inspect availability errors occur later and are not the first save refusal.

Source trace:

1. `useTimelineCommandSession` exposes `sessionRef.current?.genericPatchPort` after asynchronous initialization.
2. `useTimelineOps.apply` captures that optional port. Changing it recreates the apply callback and the returned useMemo object.
3. `editorRuntimeAssembly` supplies a TimelineOps object at extension activation; `createExtensionTimelineOps` retains that object. `extensionLifecycle.synchronize` keeps the same activation for an unchanged manifest.
4. The marker panel's retained apply therefore sees the pre-startup absent port, despite a ready session now existing. It takes `compileTimelinePatch` -> `commitData(..., { save: true, semantic: true })` -> the legacy publisher. The trace proves that publisher was reached.
5. The new regression retains the pre-port object, rerenders with an available port, and calls the retained apply. Old source fails by not capturing/submitting through that port. The current-authority regression separately demonstrates the same stale callback problem for a changed permission object.

## Minimal peer patch

Directory: `workers/ap2-m2-ordinary-zero-post-causal-diagnosis/` beside this report's parent.

- `peer-fix.patch`: production diff plus two behavior tests.
- `production.patch`, `regression.patch`: split forms.
- `peer-request.md`: exact owner request and subsequent gate instructions.
- `peer-fix.patch` SHA-256: `97fb1c46827199b89f68e81cd912d72f3a6cce9bbe19fcf85d6a3a7bbc743149`.

The patch retains one TimelineOps identity and dispatches its seven existing operations through a ref to current callbacks. It changes neither command meanings nor producer shapes. Current authority and local-version checks execute before capture; exact document/head checks, generation validation, guarded source/opaque/transition semantics and atomic native refusal remain in the existing code. A capture refusal is propagated and never falls back to snapshot saving. Tests assert both refusal and changed authority through the retained adapter.

## Exact validation

The one private copy was `.causal-overlay` inside the assigned worktree, produced from `git archive HEAD`. Its node_modules symlink was read-only; Vitest used `--no-cache --configLoader=runner`. `validate-peer.sh` has EXIT cleanup, which removed the copy. No /tmp App copy, shared-install mutation, socket, browser, full suite, or dependency installation was performed locally.

Commands (cwd was `.causal-overlay`):

```sh
npm exec vitest run --no-cache --configLoader=runner src/tools/video-editor/hooks/useTimelineOps.test.ts -t 'retained adapter|extension-retained'
```

Before production patch: **exit 1, 43 passed / 2 failed**. npm consumed `-t` as an option (warning in log), so the entire 45-test file ran. Both new tests fail on the intended stale-dispatch/authority assertions; all pre-existing tests pass.

```sh
patch -p1 < "$WORKER/production.patch"
npm exec vitest run --no-cache --configLoader=runner src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts src/tools/video-editor/commands/ordinaryMoveMember.test.ts src/tools/video-editor/commands/ordinaryScalarMember.test.ts src/tools/video-editor/dev/scene-phase-markers/__tests__/patch-building.test.ts
npm exec eslint -- --max-warnings 0 src/tools/video-editor/hooks/useTimelineOps.ts src/tools/video-editor/hooks/useTimelineOps.test.ts
```

After patch: **5 files / 114 tests passed; ESLint exit 0**. The adapter regression uses an observed command port to isolate dispatch; the existing generic/ordinary suites cover real capture. This is not proof of corrected browser/Runtime acceptance.

Central diagnostic:

```sh
$ORCH/bin/request-test ap2-m2-ordinary-zero-post-causal-diagnosis e2e-m2-ordinary-integration
$ORCH/bin/wait-test ap2-m2-ordinary-zero-post-causal-diagnosis-e2e-m2-ordinary-integration-1020202058-11433 1
```

**FAIL, exit 1, 181s, one failed test at the unchanged first zero-POST expectation** (line 1235 after temporary diagnostics). The first wait returned 124 while running; the later wait returned the final result. This was the one completed diagnostic browser run. An earlier request `...1020202034-7950` was accidentally submitted after the instrumentation edit failed; it was explicitly canceled, marked `cancelled`, and supplies no qualification evidence.

Final `git diff --check`: PASS. Final worktree: clean and still at the requested base; all temporary runner/test edits reverted. No final branch commit is expected because this handoff is patch-only.

## Remaining issues / next step

The Runtime's refusal is correct. App shared-core owner should apply/commit the peer patch, return the exact hash/tree, then request the named central ordinary integration gate once against the resulting source. A post-fix or postcommit gate was not requested against unchanged/unpatched source, and no gate pass is claimed.

A distinct next obstacle is already visible in captured data: `moveExistingShotsToMarkers` selects **all five visual clips**, while the journey expects four commands for only two parent clips. The legacy publication includes the three occurrence-child display clips as well. Do not filter unsupported members, weaken assertions, or change producer scope without owner resolution. The first child's original 12-second duration moving to 6 seconds may also hit the native occurrence boundary during the move-before-hold sequence; this is a source-based prediction, not an observed capture refusal. Follow the first restored native failure rather than guessing at another producer fix.

Lost-ACK retry, restart, Agent label rebase and undo remain unverified in this ordinary journey. No full suite was requested or run. The PLAN2/3/6 critical path remains unqualified until the owner source and real gate pass.

Retained evidence: `diagnostic-browser-output/**/trace.zip` (SHA-256 `92e1ebbb8f8bb9033b0467f37cd1a08826b4f6299f9d038c53dbfee9413293a3`), UI error-context, `trace-findings.json`, central log, `regression-before.log`, `regression-after.log`, and `peer-eslint.log`, all in the worker folder or central result folder, never design/ archives.
