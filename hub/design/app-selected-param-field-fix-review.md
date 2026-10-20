**Verdict: HOLD — two lifecycle issues remain. D01 / production activation stays OPEN.**

Reviewed `tl/app-m2-selected-param-field-lifecycle-fix` at **`fb85a3a38ebdcaaeedac28a2498e23047ee12cd9`**, tree `8e6df9a1be13e4a1ad1846aa3a19d7a8632cbe56`, against **`3add7415e4eeb802776466fbd259b8cf012bd201`**. Read PLAN.md and the exact prior ingress findings. Eight paths changed: five product files +72/-12, three new test files +705. All existing tests are unchanged. The original three external files are unchanged prefixes of the promoted files (16,094 / 9,923 / 11,624 bytes); all 17 original external cases are preserved.

The assigned review worktree is at `7bb885b638838588a0dff81b64b7c34960ac07f3`, so testing used a private archive of the exact candidate. All **5,826 tracked blobs**, including symlink contents, match that candidate after testing. No product, test, config, or other repository file was changed. Source line references below are at the candidate SHA.

**Findings**

1. **P1 — the mounted command-session wrapper drops the new submitted-input seam.** `src/tools/video-editor/hooks/useTimelineOps.ts:165-168` reads only `clipParamsPort.submittedInput`, but `src/tools/video-editor/hooks/useTimelineCommandSession.ts:176-194` replaces the session port with an explicit object containing capture/prefetch/finish/submit/invalidate only. It never forwards `submittedInput`. As a result the actual mounted hook's `getSubmittedClipParams('x')` returns undefined with a durable refused16 command present. Remounting the actual `AstridElementParams` with that hook's ops/state displays input4 / accepted4 instead of submitted16 / accepted4. The new lifecycle suite binds directly to `createTimelineCommandSession().clipParamsPort`, bypassing this wrapper. Acceptance-based field retirement also cannot work through that wrapper, because neither initialization nor post-Apply can obtain an input identity. Forward the read-only seam through the existing guarded wrapper, preserving the existing scope/async fences, and add mounted-hook/form coverage. External normal assertions: `notes/counterexamples.test.tsx:154-177` (both fail).

2. **P1 — acceptance can disappear before the form renders, retaining accepted input as a stale dirty edit.** `src/tools/video-editor/commands/commitSession.ts:417-420` exposes only `record.accepted`, which contains the most recent acknowledged prefix. `SelectedElementParamFields.tsx:40-45` clears a submitted field only if a render observes that exact PARAM ID. If PARAM A and an ordinary suffix B finish within one React batch, B overwrites the only exposed acceptance before the form reads it. Deterministic repro: type/apply8, queue an ordinary move while A is held, then release and flush both within one async `act`. Accepted8 appears, but Apply stays enabled and Seed8 remains a dirty field. After a remote accepted change to Seed9, editing only Text sends **`values:{seed:8,text:'new'}`**, rather than only Text, and the synthetic accepted result overwrites9. A separate PARAM-ACK→inverse in one render batch displays input8 beside accepted4. No newer field typing occurs in these repros. The existing added queued-move test waits for the second commit outside `act`, allowing the form an intermediate render and missing this case. Ensure exact PARAM acceptance remains observable to its field lifecycle across render batching and subsequent ACKs, using the existing session/outbox path; do not clear on global Saved, equal values, unrelated ACKs, or inverse. External normal assertions: `notes/counterexamples.test.tsx:142-151,181-207` (three fail).

These are two separate causes: the batching failures use the direct session port, so forwarding the wrapper alone cannot fix them. The stale resubmission is observed through the normal App transport fixture; this is not a claim of native Runtime validation or a browser concurrency qualification.

**What the candidate does prove**

- All three original findings pass unchanged on the direct session binding: ordinary ACK followed by cancellation leaves raw16 visibly dirty; reopening/recovering a durable refused16 restores input16 beside accepted4; an absent own-schema `__proto__` parameter stays absent.
- The entire original 398-test set, all 17 promoted external cases (including the seven prior recovery/cancellation controls), and three new worker tests pass: **418 / 22 files**. New typing, including typing back to identical text before ACK, survives. Own empty/prototype/constructor values, null, blank clears, opaque fields, and no prototype pollution remain covered.
- The new accessor reads existing pending appends, outbox intents, and the last acceptance, returns cloned/frozen snapshots, and reuses local/durable intent IDs. It adds no persisted draft authority, recapture, retained read, schema validator, wire field, client, or command submission. Read-only remount/recovery assertions preserve the original basis, pin, durable command, pending request, and read counts. An additional external positive control proves repeated reads and disposal do not alter the durable refused input or send/read again.
- `setClipParams`' existing capture-before-await, native argument cloning, original schema pin, and abort-before-submit logic remain unchanged. Source inspection covered the unchanged capture/prefetch generations, false `acceptedBasisAvailable` refusal, cancellation of only the selected tail, one-operation inverse, owner recovery, disposal, and project-switch/read-generation fences. Their existing targeted controls pass; the wrapper omission above is the new seam's integration failure. An additional positive control keeps raw16 on equal-head observation without reads or sends.
- Source-stage optional pin/state props still do not install a production caller or retained-read binding. No activation, writer retirement, matching package tuple, or refreshed-main integration claim follows from these tests.

**Exact tests and checks**

CWD: `WORKER/notes/source`, where `WORKER` is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-field-fix-review`.

Vitest **4.1.5**, private Composition **0.0.12** extraction/alias, runner config loader, no cache, maximum one worker, no file parallelism; config `cacheDir` points inside this worker's notes. Shared dependencies and caches were read-only throughout.

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-field-fix-review/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.shader.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.sequence.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.astridCatalog.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.lifecycle.test.tsx src/tools/video-editor/commands/commitSession.selectedParams.recovery-counterexamples.test.ts src/tools/video-editor/commands/commitSession.selectedParams.recovery-probes.test.ts > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-field-fix-review/notes/targeted.log 2>&1
```

**PASS — exit0, 22 files / 418 tests, 59.71s.** Exact command also retained in `notes/targeted-command.txt`; log `notes/targeted.log`.

```bash
node node_modules/vitest/vitest.mjs run --config ../vitest.external.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism > ../external-final.log 2>&1
```

**Review RED — exit1, 1 file / 7 ordinary tests: 2 pass / 5 fail, 4.89s.** The five failures are the two findings' independent mounted-hook/form and batching assertions above; the two controls pass. All executable cases and log are in this worker's notes. No implementation or passing requirement was rewritten, skipped, weakened, or marked expected-to-fail.

Earlier exploration: a three-case external run exposed the batching failure and two harness errors because the reused context mock omitted the real Context export. Corrected only the private harness to partially mock that module. The next seven-case run produced the same 2pass/5fail; the final run adds an intervening accepted Seed9 before the stale-resubmission assertion. No candidate file changed. Only external tests were rerun after external harness/case changes; the unchanged 418-test source run was not repeated.

From the assigned review worktree:

```bash
git diff --check 3add7415e4eeb802776466fbd259b8cf012bd201 fb85a3a38ebdcaaeedac28a2498e23047ee12cd9
python WORKER/notes/verify-source.py
git status --short
```

**PASS — whitespace check exit0; source verification exit0, 5,826 matching blobs, all three original external prefixes identical, no pre-existing tests changed; worktree clean.** Verification details are `notes/source-verification.json`. The first ad hoc hash check followed the tracked `CLAUDE.md` symlink and reported a comparison mismatch; the retained verifier correctly hashes the symlink target text as Git does. There was no source mismatch.

**Decisions, limits, and next steps**

No settled design decision was changed or contradicted. Local review decisions: test the exact archive; exercise the existing mounted wrapper; use normal positive behavior assertions to test coalesced renders; leave fixes to the owning worker. No blocker prevented completion of this review; HOLD is the code-review verdict, not an execution blocker.

Actual Runtime **V1 max10 acceptance8/refusal16** across V2 hints/removal/restart and **browser qualification remain OPEN**. Native retained storage/build/custody, lost-ACK exact retry across a Runtime process restart, native guarded inverse/undo/redo/reload, matching republished 0.2.9 tuple, zero-legacy browser traffic, and refreshed-main integration remain unverified. Fake IndexedDB reopening and synthetic normal-port transport are not those gates.

No full suite/test-service request, build, browser, localhost/socket, project tsc, install, native Runtime/Agent process, or ESLint rerun was performed. No commit/merge/rebase/checkout/push or shared dependency/cache mutation was performed. Private source/Composition extractions, dependency symlinks and caches were removed after verification; `notes/prepare-test-env.py` recreates them. Reports/configs/executable counterexamples remain; no KEEP marker.

Recommended next step: forward the accessor through the actual hook and fix exact acceptance delivery across batched ACKs without another persisted authority, promote these ordinary assertions into the existing suite, and rerun affected targeted tests. Then complete the separately owned native Runtime/browser activation gate.
