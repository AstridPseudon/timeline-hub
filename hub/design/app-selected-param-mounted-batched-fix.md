**Complete — mounted forwarding and coalesced PARAM acceptance fixed. D01 / production activation remains OPEN.**

Read PLAN.md and app-selected-param-field-fix-review.md before editing. Worktree: `/home/user/work/wt/app-m2-selected-param-mounted-batched-fix`; base `fb85a3a38ebdcaaeedac28a2498e23047ee12cd9`, tree `8e6df9a1be13e4a1ad1846aa3a19d7a8632cbe56`. No settled decision changed or contradicted; no execution blocker.

**Source and scope**

Four product files changed, +32/-12; one new direct test file, +342. Existing test files are unchanged. Exact patch including the new file: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-mounted-batched-fix/notes/candidate.diff`, SHA256 `2c90485ee26a39bf9b92ca4846c8884c8670e9390334cba64afe2a0d0c908802`. Per-file SHA256 values: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-mounted-batched-fix/notes/source.json`. HEAD stays at the assigned base because the harness owns commits.

- `src/tools/video-editor/hooks/useTimelineCommandSession.ts:177` forwards the read-only submitted-input accessor through the real mounted wrapper. A disposed/replaced session returns no input. Existing capture, legacy-clean, async read-generation, data/head, scope, abort and submission guards remain in place.
- `src/tools/video-editor/commands/commitSession.ts:103,237,421` gives each observed outstanding PARAM input a shared one-way acceptance flag keyed by its existing local/durable intent identity. Only that exact outbox acceptance changes the flag. The returned input and args/basis are frozen; `accepted` is a read-only getter for that input's known outcome. Accepted/cancelled observations leave the pending map; rejected-resolution/disposal clears it. Accepted flags survive only in input objects retained by their UI consumers. No accepted-history collection, durable field, journal, new submission/read path, event system or validator was added.
- `src/tools/video-editor/components/PropertiesPanel/SelectedElementParamFields.tsx:36` retains that submitted input object and checks its exact outcome after a batched render. Field text and edit generations still protect newer typing, including typing back to the same text. Ordinary Saved, equal values/head, unrelated PARAMs, ordinary ACKs and inverse results cannot mark an unaccepted input accepted.
- `src/sdk/video/timeline/timelineOps.ts:32` documents the existing read-only acceptance member; no API member or global binding was added.
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted-batched.test.tsx` promotes all seven review cases as ordinary positive assertions and adds three controls. The mounted helper renders the actual hooks and optionally the form together. All original review case names and expectation lines remain present. The original three promoted files containing all 17 prior cases are byte-identical to base, verified directly against `git show`.

**Counterexample mapping**

| Review case | Result and coverage |
|---|---|
| PARAM ACK + ordinary ACK in one act | PASS: accepted8, Apply disabled; exact outcome survives replacement of the outbox's last acceptance. |
| Real mounted hook drops accessor | PASS: actual hook ops returns refused16 with the original pin. |
| Real form remount loses refused16 | PASS: input16 beside accepted4; original durable basis/guards, pin, request and read count unchanged by rendering/accessor reads. |
| Accepted Seed8 resent after accepted Seed9 on Text edit | PASS: next command contains only `values:{text:'new'}`; Seed8 is retired. |
| PARAM ACK + inverse in one render batch | PASS: input4 beside accepted4. |
| Equal-head observation control | PASS: unsubmitted16 remains dirty; zero sends/reads. |
| Repeated read/disposal control | PASS: frozen input/pin, unchanged durable bytes/read count/send count. |
| Added multiple-PARAM/cancel control | PASS: two same-value PARAM submissions have distinct outcomes, the unsent same-value PARAM stays unaccepted after cancel and later PARAM + ordinary ACKs. |
| Added raw16 cancellation control | PASS: canceled raw16 remains dirty through an unrelated Text PARAM and ordinary ACK in one batch. |
| Added real mounted batching control | PASS: actual mounted hooks + form retire accepted8 across a coalesced ordinary suffix; no legacy writes. |

The unchanged neighbours also protect bare/unselected controls; own empty/prototype/constructor keys, null and absence; original pinned recovery; new typing; cancellation; project/scope/read fences; and accepted-only after-state. The existing provider remains the sole schema validator. No UI activation, root/pin/viewer change, guard refresh, client request field or accepted-basis rule changed.

**Exact verification**

CWD was the assigned worktree. Vitest 4.1.5, private Composition 0.0.12 artifact extraction/alias, runner loader, no cache, private cacheDir, max one worker and no file parallelism. Shared dependencies/caches were read-only.

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-mounted-batched-fix/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.shader.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.sequence.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.astridCatalog.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.lifecycle.test.tsx src/tools/video-editor/commands/commitSession.selectedParams.recovery-counterexamples.test.ts src/tools/video-editor/commands/commitSession.selectedParams.recovery-probes.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted-batched.test.tsx
```

PASS, exit0: **23 files / 428 tests**, 63.80s. This is the unchanged 418-test neighbour set plus ten new normal tests. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-mounted-batched-fix/notes/targeted.log`; exact command: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-mounted-batched-fix/notes/targeted-command.txt`.

```bash
node node_modules/eslint/bin/eslint.js --no-cache src/sdk/video/timeline/timelineOps.ts src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/components/PropertiesPanel/SelectedElementParamFields.tsx src/tools/video-editor/hooks/useTimelineCommandSession.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted-batched.test.tsx
git diff --check
```

Both PASS, exit0; ESLint had no output (log `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-mounted-batched-fix/notes/lint.log`). The source verification script compared the three prior promoted files byte-for-byte to base and checked all review case titles/expectation lines are retained: PASS. Exact hashes in source.json.

Earlier focused runs used the identical Vitest command prefix through `--no-file-parallelism`, with these file arguments:

- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted-batched.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.lifecycle.test.tsx`: exit0, 2 files / 20 tests, 7.31s (`focused.log`).
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted-batched.test.tsx`: exit0, 1 file / 9 tests, 5.00s (`multiple.log`), then exit0, 1 file / 10 tests, 5.34s (`mounted.log`). The final 428-test run includes the last additional read-only mounted assertions.

No test was skipped, disabled, deleted, weakened or marked expected-to-fail. No full suite, central-service request, build, browser, socket/localhost suite, tsc, install, native Runtime/Agent process, git mutation or shared dependency/cache write was performed. Private extraction/cache removed; retained private config and prepare-test-env.py recreate the extraction. No build output or temp files remain in the worktree; no KEEP marker.

**Decisions and remaining gate**

The small UI outcome latch was chosen because a single last-ACK slot cannot convey exact PARAM acceptance after React coalesces renders. It uses existing intent identities and the existing durable dispatch acceptance boundary, with only pending UI observations retained. Rehydration copies original submitted args/basis and cannot submit or recapture. There is no durable draft authority or guard recapture.

Actual Runtime **V1 max10 acceptance8/refusal16** across V2 hints/removal/restart and browser qualification remain OPEN. These are synthetic normal-port transport/read fixtures, not native schema-validation or browser-concurrency qualification. Native retained storage/build/custody, lost-ACK exact retry across Runtime process restart, native guarded inverse/undo/redo/reload, matching republished 0.2.9 tuple, zero-legacy browser traffic and refreshed-main integration remain unverified. Recommended next step: orchestrator reviews/lands this narrow change, then completes that separately owned real Runtime/browser activation gate.
