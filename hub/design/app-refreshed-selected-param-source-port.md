# Refreshed selected-PARAM source port

Completed the approved bounded source port onto **`0ea988bdd2907c876b82fd2620820e3fb6d6ea84`**, branch `tl/app-m2-refreshed-selected-param-source-port`. Source: **`2952e801329e430cbf864b698b93df7055e76159` minus `080a5743a4e38847e0cc84dd07ccada67adb27f1`**. Read PLAN.md and final mounted approval first. **Production binding and real current-pair Runtime/browser qualification remain OPEN.** No KEEP marker or activation claim.

## Exact scope and preservation

Exactly **20 paths, +2,748/−30, net +2,718**. Product: **11 paths, +606/−25, net +581**. Tests/support: **9 paths, +2,142/−5**. Eleven files are added; nine existing files change. This is the cumulative selected-PARAM delta, not just its final five-file batching fix.

`notes/audit-source.py` verifies each path's complete added/removed line sequence is identical to the approved source delta. All **5,818 other tracked paths** are byte-identical to the coherent base, including symlink target text. Exactly the approved allowlist is changed:

| Path | Lines |
| --- | --- |
| `src/integrations/runtime/retainedParamInputs.test.ts` | +266/−0 |
| `src/integrations/runtime/retainedParamInputs.ts` | +86/−0 |
| `src/sdk/video/timeline/timelineOps.ts` | +19/−0 |
| `src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts` | +7/−3 |
| `src/tools/video-editor/commands/clipParamsCapture.ts` | +26/−0 |
| `src/tools/video-editor/commands/clipParamsGesture.ts` | +38/−0 |
| `src/tools/video-editor/commands/commitSession.selectedParams.recovery-counterexamples.test.ts` | +163/−0 |
| `src/tools/video-editor/commands/commitSession.selectedParams.recovery-probes.test.ts` | +183/−0 |
| `src/tools/video-editor/commands/commitSession.selectedParams.test.ts` | +459/−0 |
| `src/tools/video-editor/commands/commitSession.ts` | +250/−17 |
| `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.lifecycle.test.tsx` | +359/−0 |
| `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted-batched.test.tsx` | +342/−0 |
| `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx` | +310/−0 |
| `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx` | +23/−6 |
| `src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx` | +5/−0 |
| `src/tools/video-editor/components/PropertiesPanel/SelectedElementParamFields.tsx` | +99/−0 |
| `src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx` | +53/−2 |
| `src/tools/video-editor/hooks/useTimelineCommandSession.ts` | +31/−1 |
| `src/tools/video-editor/hooks/useTimelineOps.ts` | +28/−1 |
| `src/tools/video-editor/hooks/useTimelineState.ts` | +1/−0 |

Three overlapping files were reconciled narrowly:

- `commitSession.ts`: retain the coherent base's `pump(retryPending = true)`, pending-outcome gate, and append-triggered `pump(false)`. Appending B cannot retry unknown A. The approved PARAM logic is layered around these unchanged guards.
- `commitSessionEnvironment.ts`: preserve existing preview application, recorded body bytes, and reusable project callback; add only the approved optional synthetic PARAM responder.
- `ClipPanelBody.tsx`: add only the approved optional source-stage props/import; preserve MAIN duration/media cap, mobile actions, touch controls, text handling and inspector changes.

No old Root, render/download, boot, pin, package/generated cohort or harness is imported. `useTimelineState.ts` gains only the approved clipParamsPort forwarding. TrackLabel/TrackListRenderer/TimelineCanvas and their owner-approved desktop/touch supersession assertions are unchanged, as are explicit dirty-intent handling, initial accepted projection fences, MAIN opacity/duration clamping and the held raw-render work. Public12/package locks, 6ff parity harness, CORS, boot/provider/auth and render cohorts remain exactly at the assigned base. No existing behavior expectation was deleted, weakened, skipped or newly marked expected-to-fail.

## Server authority and submitted-input outcome

The actual mounted wrapper forwards `submittedInput`, refuses stale/disposed owner access, and passes it to the SDK accessor. Only observed outstanding PARAM inputs have transient outcome cells keyed through the existing intent identity. Exact ACK acceptance is monotonic for the retained handle across later PARAM, ordinary and inverse ACKs. Acceptance/cancellation/rejected-prefix resolution/disposal remove map entries; no accepted-history journal or persisted outcome field was introduced.

Capture occurs synchronously before async retained DocumentRead. The original literal arguments, exact DocumentPin, accepted-basis flag, generation/head/projection fences and original guards are preserved. A false accepted-original-basis flag is never freshened after predecessor acceptance. PARAM has no browser-computed after-state: the display keeps the last accepted value until the provider ACK supplies its closure. Schema display hints do not clamp raw16 or authorize it. Cancellation retains dirty16; recovery/refusal shows submitted16 beside accepted4; null/blank clear and own empty/prototype/constructor keys preserve absence semantics. Coalesced Seed8→Seed9 plus ordinary ACK cannot cause a later Text-only submission to resend stale8. Plain unselected controls remain covered and unchanged in behavior. No new browser validator, guard refresh, durable history, outbox format or wire format.

## Runtime 0.2.13 compatibility comparison

The worktree keeps its assigned **DEVELOPMENT 0.2.9 generated cohort** unchanged; it is not relabeled as a safe published pin. The separate normal13 worker owns package adoption. Read-only comparison used committed published producer **`2c4ac180c2220bdad966bc01e95ad230e99ce26a`** in `/home/user/work/wt/app-m3-runtime013-producer-source` (HEAD asserted; working type bytes equal committed bytes), contract **0.2.13**, schema digest `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`.

Exact declaration equality holds for the entire selected DTO dependency closure: `ClipSetParamsArgs`, both variants, `DocumentPin`, `ID`, `Digest`, `JSON`, `VerifiedDocument`, `VerifiedDocumentObject`, and `Document`. The complete generated `getProjectVerifiedDocument` and `getProjectVerifiedDocumentObject` method lines also equal published013. This establishes source compatibility for this port; it does not qualify the future matching tuple. No generated/schema/wire edits or manual Args were needed.

## Exact commands and results

CWD for all commands: `/home/user/work/wt/app-m2-refreshed-selected-param-source-port`. Node v22.22.0 / Vitest4.1.5 / public Composition0.0.12. The worker-local ignored node_modules link was temporarily pointed at read-only `/tmp/app-coherent-deps12/node_modules`; the original link is restored after testing. The notes config imports the unchanged repository config and only overrides cacheDir. Runner preload supplies `__dirname`. To reproduce after cleanup, temporarily repoint only this worktree’s node_modules symlink to `/tmp/app-coherent-deps12/node_modules`, recreate `notes/tmp` and the notes-local node_modules symlink to the same read-only dependency directory, then run the retained command scripts. All Vitest invocations use runner loader, no cache, one worker and no file parallelism; TMPDIR is worker-private. No install, full, build, project tsc, browser, localhost/socket or native Runtime run/request.

```bash
env TMPDIR="/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/tmp" node --require "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.shader.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.sequence.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.astridCatalog.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.lifecycle.test.tsx src/tools/video-editor/commands/commitSession.selectedParams.recovery-counterexamples.test.ts src/tools/video-editor/commands/commitSession.selectedParams.recovery-probes.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted-batched.test.tsx > "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/targeted.log" 2>&1
```

```bash
env TMPDIR="/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/tmp" node --require "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/vitest.external.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism > "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/external.log" 2>&1
```

```bash
env TMPDIR="/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/tmp" node --require "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/vitest.config.ts" --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/components/TimelineEditor/TrackListRenderer.test.tsx src/tools/video-editor/components/TimelineEditor/TimelineCanvas.test.tsx src/tools/video-editor/hooks/useTimelineTrackManagement.test.ts src/tools/video-editor/hooks/useTimelineCommit.test.tsx src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx src/integrations/runtime/opaqueRootWriters.test.tsx src/tools/video-editor/data/shotCompositionProjection.test.ts src/tools/video-editor/compositions/playerEvaluation.test.ts src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.initialRead.test.tsx > "/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/preservation.log" 2>&1
```

Results, all exit0:

- **23 files / 432 tests PASS**, 62.28s (`notes/targeted.log`). The approved 428-test selection now includes four preserved coherent-base cases; no assertion was changed to obtain this increase.
- **2 files / 15 tests PASS**, 7.74s (`notes/external.log`): byte-for-byte original seven counterexamples plus byte-for-byte final-review eight actual-hook cases. Preserves all 7+8 approved assertions against refreshed code, including mounted accessor, double-PARAM/ordinary batching, exact recovery, cancellation, retained-read detachment and owner transition.
- **12 files / 315 tests PASS**, 31.57s (`notes/preservation.log`): desktop clean-focus/explicit dirty labels, owner-approved phone/tablet no-capture behavior, canvas forwarding, mounted command/save/recovery, opaque roots, initial preview reads, source projection and public evaluation/clamping.

**762 Vitest tests passed across 37 files**, zero failures. Additional focused source/package checks:

```bash
node config/vite/timelineCompositionPackage.test.mjs
node scripts/quality/check-known-failures.mjs
git diff --check
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/audit-source.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/source-audit.json
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/audit-deps.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/deps-before.json # before tests
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/audit-deps.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/deps-after.json  # after tests
cmp /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/deps-before.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-refreshed-selected-param-source-port/notes/deps-after.json
```

Package/source guard: **9 tests PASS**, includes all supported configs, embed and Node SSR public subpaths. Failure-marker guard: **PASS**, exactly three existing authorized drag markers, zero forbidden markers. Whitespace check, source allowlist/exact edit-line audit and DTO/source comparison: **PASS**. Dependency/cache snapshots are byte-equal: all77 Composition files, six peer manifests, and shared/private `.vite`, `.vite-temp`, `.cache` metadata. No shared dependency/cache/venv was written.

Exploration accounting: `git apply --check` identified the three expected context overlaps before any patch application. All other files applied directly; those three were reconciled as described above. The audit treats absent pre-port files as empty blobs (Git prints expected absent-path diagnostics); audit exited0. No failing behavior test or changed test expectation, installer, package change or alternative schema was introduced.

## Actual missing production caller / remaining gates

**No bounded source blocker. Production activation is still OPEN.** Two real caller gaps remain:

1. `hooks/useTimelineSave.ts:99` constructs `useTimelineCommandSession` without `paramReadClient`. The production owner must supply the existing authenticated project/realm-scoped retained DocumentRead client through this caller. Its methods already exist; this port creates no endpoint or provider ownership assumption.
2. `components/PropertiesPanel/PropertiesPanel.tsx:522` mounts `<ClipPanel>` without `retainedDocumentPin`, `timelineOps`, or `commandState`. `ClipPanel.tsx:31` spreads props into AstridElementParams, but the production caller does not install them. The existing admission/selection authority must provide the original exact retained pin alongside the current session ops/state. Descriptor hints or a live replacement pack are not pin authority. No original owner/pin was invented here.

Without that explicitly owned binding the selected source-stage UI is not activated by production; unselected plain controls still operate. The orchestrator must assign this caller wiring before claiming D01 activation.

Actual same-pair Runtime V1 max10 accept8/refuse16 after V2 hints/removal/restart/reload, retained custody/storage, lost-ACK exact retry across Runtime restart, native guarded inverse/undo/redo, browser zero-legacy traffic, matching Agent/Runtime013/public12/App pair qualification and held rendering activation all remain **OPEN**. Synthetic transport/fake IndexedDB and source equality do not close them. The next step is to compose this source with the separately owned normal13 pin and matching Agent source, assign the real production binding, then run the orchestrator-authorized composed typecheck and native/browser gates. No settled PLAN decision changed or contradictory evidence was found.

No Git commit/merge/rebase/checkout/push/ref deletion or integration worktree mutation. No build/temp output remains in this worktree. Test logs/configs/source comparisons are retained only in this worker's notes; private caches/TMPDIR and notes dependency link are cleaned after tests. The shared private12 overlay is left untouched. Conventional commit message and DONE are provided for the harness; no KEEP marker.
