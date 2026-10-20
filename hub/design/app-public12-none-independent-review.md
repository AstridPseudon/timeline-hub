# Bounded public12 native None review: APPROVE source unit

**APPROVE** the bounded source unit at App **`ccd0fad325511d4830c5c3279f9c86884035ddcd`**, compared only with **`080a5743a4e38847e0cc84dd07ccada67adb27f1`**. No blocking capture, atomicity, preservation or scope regression found. This is a source approval, not automatic integration, activation or qualification. Pending paired proof is not a reason to reject this source.

Read PLAN first, the source worker report, the older independent 209-test review, and the `1be0efdde` transition-preservation contract. Product worktree stayed clean throughout. No product/test/pin/root changes, refs, commits, installs, full/build/browser/tsc/socket requests or KEEP request.

## Closure and minimality

The diff is exactly **26 paths**: 17 product paths (+726/−10, **+716 net**), eight test/support paths (+1266/−15), one 6317-line native golden. Total +8309/−25. No historical ordinary/popup/renderer cohort was imported. The four reused product modules total **509 lines** and are byte-identical to `90f39e080`; the integration is +207 net product lines.

| Changed paths | Why this unit needs them |
| --- | --- |
| `commands/clipScalarCapture.ts`, `clipScalarGesture.ts` | Native raw capture/record validation and exact single/batch clear handoff. Uses existing AuthoredState/MoveRecording, not a second document writer. |
| `commands/commitSession.ts` | Resolve real raw ownership, finish all commands on one original basis, prepare once and enqueue once into existing outbox. |
| `lib/clip-scalar-preview.ts`, `lib/timeline-patch.ts`, `src/sdk/video/timeline/patch.ts` | Explicit local removal metadata avoids lossy row serialization and distinguishes removal from null. The special compiler returns no publication mutation. |
| `hooks/useClipScalarControl.ts`, `useTimelineCommandSession.ts`, `useTimelineState.ts`, `useTimelineState.types.ts`, `contexts/VideoEditorProvider.tsx` | Expose the same session port through both editor hosts and preserve earlier-save fences at capture, finish and submit. |
| `PropertiesPanel/{PropertiesPanel,PropertiesPanelBody,ClipPanelBody,ClipEffectsTab,ClipTransitionSection,BulkClipPanelBody}.tsx` | Carry capture from both production hosts to None/Remove, full selected IDs for bulk, read-only refusal and visible capture errors. SET/duration/reset keep their existing callbacks. |
| Eight test/support paths and native golden | Exercise captures, native session, mounted controls, recovery, exact preview, and existing native command/record/output parity. |

This is minimal at the reused-module boundary, **not literally line-minimal**: `clipScalarCapture.ts:22–147` and `:213–272` retain hold/timing helpers unused by transition-only clear. They are reviewed built-in scalar semantics, with the unchanged full golden/tests; removing them here would specialize the native executor and discard its exact parity. This is an acceptable reuse tradeoff, not an ordinary batch UI or general writer framework. Only transition clears are accepted by `finishBatch` (`commitSession.ts:370`); no hold/asset UI migration or params/trim/track-create/popup work was added. Optional later module splitting is not an approval condition.

## Native semantics and atomicity

- `ClipTransitionSection.tsx:111` sends exactly `clip.set` v1 with `{values:{},clear:['transition']}`. `BulkClipPanelBody.tsx:207` captures the entire selection before `submitClipTransitionClears`; that helper (`clipScalarGesture.ts:49`) verifies one port, command count/order/select/version/args before one `submitBatch`. Empty/mixed/unsupported captures refuse; a native capture error never invokes the detached callback fallback.
- `commitSession.ts:318` resolves ownership from raw parent authority or a complete projector occurrence binding: actual occurrence/raw ID, project/parent, shot/internal revisions and stable output identity. `:352` checks displayed revision/publication and unique identity. No new wire guards, display-ID ownership inference or authority fields were invented. Parent opaque `app.canonical` stays authored data.
- `commitSession.ts:378` checks distinct targets, local generation, identical original bundles and predecessor/head basis. It finishes sequentially on the original transaction basis, then executes the original claims against current bytes. A late ACK cannot refresh those claims. Only after every execution succeeds does it install a prepared batch; only one enqueue changes authored state, previews, or outbox (`:404`). A failed second member cannot submit/preview the first member.
- `clipScalarCapture.ts:149,173,274` records owner/source/type/media dependencies and explicit ABSENT writes. Existing `clipMovePrimitives.ts:211` deletes the own leaf; `:281` mirrors raw parent clips into config. No null/sentinel conversion, timing normalization, reordering, opaque-key filtering or whole-document publication was introduced.
- `timeline-patch.ts:1050` dispatches only patches carrying explicit local `clear` metadata to the scalar preview; ordinary patches retain the prior compiler. `clip-scalar-preview.ts:10` rejects compound non-scalar operations before exposing its cloned result. Existing compound/missing-target tests retain the dirty draft and outbox atomically.
- Official Runtime **0.2.9** source was checked read-only at **`53dae2ff693b1b27a80d39c1112e908fdb35b18c`**: `packages/typescript/src/contract-metadata.ts:3` identifies 0.2.9; `contract/schemas/edit-command.json:1215` already defines the values/clear union and incoming transition removal. No new operation is needed. This App source deliberately still has its separate 0.2.8 pin placeholder; the normal pin/pair adoption is another unit.

## Preservation, recovery, evidence limits

`notes/source-audit.json` independently verifies:

- The entire original 21-case TransitionPreservation describe block is byte-identical to base; its rawClip fixture and authored/published assertion helper bodies are identical too. Base's complete transition file equals `1be0efdde`. All eight files of the original **268-test** lane ran here; the seven new native cases increase that lane to 275. The original positive None callbacks, revision/opaque/reset/null/absence/own-key/order/per-clip duration and full outgoing serializer assertions remain.
- Both original None publication expectations are ordinary positive tests (`TransitionPreservation.test.tsx:332`) on the same raw fixtures and exact removal result, through the named native boundary. They assert accepted `parent.clips` and `parent.config.clips`, including JSON order, and zero snapshot callbacks. The old legacy serializer is not relabelled fixed.
- Scalar capture, gesture, session tests and native golden are byte-identical to reviewed source. Golden SHA256 **`8bb75e23c10c9677635d85f33f219b7f1b2d89baf481e3b7ed21f425b76f0c06`** equals frozen Agent `027bd16d96010544331c953c0e1014e161786e71`'s fixture. App's exact full commands/records/after-bundle parity passed (`clipScalarCapture.test.ts:28`).

The previous independent review's concrete defect is repaired: `TransitionPreservation.test.tsx:202` replays recovered previews; `:415` now checks both displayed planes remain cleared and both accepted raw mirrors remain unchanged on rejection. Exact stored intent/request and no retransmission after definitive rejection remain asserted.

The successful lost-ACK batch + newer move test (`:434`) preserves exact body/key, original suffix commands and accepted predecessor identity, **but does not remount**. Scalar unit cases (`commitSession.clipScalar.test.ts:271,349,387`) cover explicit recover, identical original claims and ACK handling. These are in-process unit transports. They are not actual Runtime, browser/process death or accepted transition-batch restart proof.

Recovered source/fact labelling remains driven by actual basis and preview presence: `commitSession.ts:479` uses persisted displayBasis/original closure and accepted receipt data; `useTimelineCommandSession.ts:74–111` projects the actual supplied canonical basis and labels replayed previews local, preview-free projections accepted. This code is unchanged from base. Existing label/projection tests passed; this review did not fabricate an accepted basis or replace these paths with label mocks.

The golden contains commands, records and after state, **not inverse output**. Frozen Agent conformance `test_recipe_clip_scalar_fields.py:79–95` explicitly verifies inverse/redo/replay before matching that golden; it was read, not run here. Unchanged App `commitSession.test.ts:198` and `commitSession.ts:561` cover exact publication-addressed inverse requests. The unit environment (`__tests__/commitSessionEnvironment.ts:125`) restores a saved prior document for inverse; it cannot prove real guarded inverse or concurrent-author safety. No new inverse-parity claim is made.

## Exact checks performed

From `/home/user/work/wt/app-m2-public12-none-independent-review`. All substantive focused runs use runner/no-cache/maxWorkers=1. Private runner/config live only under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-none-independent-review/notes`. The final config imports the unmodified repo config, aliases all Composition export entrypoints to read-only `/tmp/app-coherent-deps12/node_modules/@banodoco/timeline-composition` (0.0.12), keeps the base's single React/Remotion runtime, and points cacheDir to this worker's notes. No shared dependencies/runtimes/venvs/caches were edited.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-none-independent-review/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-none-independent-review/notes/vitest.public12.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/clipScalarGesture.test.ts src/tools/video-editor/commands/commitSession.clipScalar.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/lib/clip-scalar-preview.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx
```

**PASS: 8 files / 208 tests**, exit 0, 29.93s. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-none-independent-review/notes/focused-public12-coherent.log`.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-none-independent-review/notes/snapshot-vitest-runner.cjs node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-none-independent-review/notes/vitest.public12.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.test.tsx src/tools/video-editor/components/SchemaForm/SchemaForm.test.tsx src/tools/video-editor/transitions/catalog.test.ts src/tools/video-editor/transitions/validation.test.ts src/tools/video-editor/lib/timeline-domain.transition.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx src/tools/video-editor/lib/serialize.test.ts src/tools/video-editor/lib/timeline-patch.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts src/tools/video-editor/commands/authoringBundle.moveOpaque.test.ts src/tools/video-editor/commands/authoringBundle.sharedOpaqueRemap.test.ts
```

**PASS: 15 files / 813 tests**, exit 0, 39.47s. Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-public12-none-independent-review/notes/neighbors-public12.log`. Final distinct source coverage: **23 files / 1021 passed**, no failed/skipped/todo. This reproduces the source worker's selection, not a full suite.

Other executed checks:

```sh
node scripts/quality/check-known-failures.mjs
git diff --check 080a5743 HEAD
git status --porcelain
```

All exit 0: exactly three original authorized group-drag markers, zero forbidden; diff clean; product worktree clean. The read-only Python/Git assertions are recorded in `notes/source-audit.json`.

Environment attempts are retained transparently: the initial same eight-file command with `--config config/testing/vitest.config.ts` passed 208/208 in 30.74s, but resolved Composition 0.0.10 through the existing worktree symlink (`focused.log`), so it is not the public12 evidence. A first public12 private config also redirected React/Remotion while external testing-library still used the base React: **51 failed / 157 passed**, exit 1, Invalid hook call (`focused-public12.log`). The corrected configuration leaves those runtime aliases unchanged and imports public12 through the repo's existing inline-dependency rule; all 1021 pass above. No test or product change was made to obtain that pass.

No independent ordinary-edit counterexample was necessary: no product finding arose. Existing ordinary patch/serializer/move/label/opaque and compound-refusal neighbors passed. No full, build, browser, tsc, install or socket was run/requested; active full 21209 was not disturbed.

## Required follow-up and blockers

**No blocker to approving this source unit.** Compose only this delta with separately owned official pin and after-ACK work; freeze the actual Agent/Runtime/App/public12 tuple. Then centrally prove installed-host single/bulk None and Remove, exact raw immutable reload in both mirrors, shared-occurrence isolation, whole-batch guard failure with zero partial acceptance, accepted reload + guarded undo preserving another author's work, lost ACK + newer suffix + process restart + exact retry/body/key, changed-body/key refusal, publication identity/revision reuse, and **zero legacy POST/snapshot traffic**. Do not retire the old writer based on these unit mocks or historic pair results. Do not request a full merely for this review.
