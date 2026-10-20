# Selected PARAM field lifecycle fix

Fixed all three findings against base `3add7415e4eeb802776466fbd259b8cf012bd201` in `/home/user/work/wt/app-m2-selected-param-field-lifecycle-fix`. No activation or writer-retirement claim. No implementation blocker or evidence contradicting the settled plan.

## Exact diff

Eight paths: five product files **+72/-12 (net +60)**; three new test files **+705**. The complete binary-safe diff, including untracked new tests, is [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-field-lifecycle-fix/notes/change.diff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-field-lifecycle-fix/notes/change.diff).

| Path | Change |
|---|---|
| `src/sdk/video/timeline/timelineOps.ts` | +10/-0: optional read-only submitted-input accessor/type for the existing selected session binding. |
| `src/tools/video-editor/commands/clipParamsGesture.ts` | +2/-0: optional accessor on the existing capture port. |
| `src/tools/video-editor/commands/commitSession.ts` | +23/-1: read existing queued/durable command args, original basis, and exact acceptance identity; defensive cloned/frozen snapshots. Reuse the existing local-to-durable ID mapping, mint no identity. |
| `src/tools/video-editor/hooks/useTimelineOps.ts` | +7/-1: forward that read through the existing session port. |
| `src/tools/video-editor/components/PropertiesPanel/SelectedElementParamFields.tsx` | +30/-10: hydrate submitted input, retire fields only for their command ACK, preserve newer field edits, and read accepted params by own key. |
| `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.lifecycle.test.tsx` | +359: original ten external mounted/SDK cases unchanged, plus three focused checks. |
| `src/tools/video-editor/commands/commitSession.selectedParams.recovery-counterexamples.test.ts` | +163: original four external recovery/cancellation cases unchanged. |
| `src/tools/video-editor/commands/commitSession.selectedParams.recovery-probes.test.ts` | +183: original three external probes unchanged. |

All three external files were verified byte-for-byte as unchanged prefixes of the promoted files (16,094 / 9,923 / 11,624 original bytes). All existing tracked tests remain untouched. No skips, expected-failure markers, or inverted assertions were introduced.

## Reproduction mapping

| Review finding / boundary | Regression and result |
|---|---|
| P1: ordinary A ACK + permanently unsent selected B(raw16), then `session.undo(B)` | Original `keeps raw16 in the form after explicitly cancelling its unsent original-basis command`: passes unchanged. Only the move is sent; accepted4 stays4; outbox tail is gone; raw16 remains visible and the saved-session form still reports its dirty draft. |
| P2: refused durable16 after explicit owner recovery/remount showed4 | Original `restores the submitted raw16 field along with the existing durable refusal state`: passes unchanged. The input comes from the same outbox command; error/accepted4 remain visible. |
| P2: absent own-schema `__proto__` rendered inherited object | Original `shows absent prototype-looking parameters as absent rather than inherited object properties`: passes unchanged; input blank and output absent. |
| New typing before ACK, including typing back to the same text | Added `preserves newer typing even when it returns to the submitted text before ACK`: passes; per-field edit counters preserve that new draft across later accepted-value changes. Counters are component-local only. |
| PARAM ACK followed by unrelated queued move | Added `retires only the accepted PARAM fields across an unrelated queued move`: passes; a later Text edit sends no stale Seed value. |
| Recovery own-key semantics and immutability | Added `rehydrates own empty/prototype/constructor values, null and clears without changing the durable input or request`: passes; empty key/string, own `__proto__` object, own `constructor:null`, and blank clear survive; original basis/pin, command payloads, request bytes and retry identity remain unchanged; no retained re-read or second journal entry. A changed supplied V2 pin refuses Apply while preserving the recovered V1 input. |

The accessor reads the existing session/outbox only; it does not capture, prefetch, submit, persist, or reinterpret schema semantics. Recovery uses serialized native JSON values/clears; arbitrary pre-submit whitespace is not separately persisted. Cancellation preserves mounted raw input; unsubmitted typing and cancelled input still have component-local lifetime. Acknowledgement matching uses the existing command intent ID and accepted receipt rather than global session `saved` or param-value equality. Only matching, unedited submitted fields are retired.

Read-only source comparison proved all pre-existing `commitSession.ts` implementation bytes unchanged after removing the added accessor/import, and the entire existing `useTimelineOps.setClipParams` callback byte-identical. In particular capture guards, false `acceptedBasisAvailable`, permanent unsent basis, native args, original pin, retained bytes, dispatch/retry/undo/recovery logic, wire body, and server validation are unchanged. No new persisted schema, durable draft store, protocol field, command identity, root/pin/render adapter, or activation binding. `AstridElementParams`/`ClipPanelBody` and their missing-explicit-pin/state behavior remain unchanged.

## Exact checks

CWD for all checks: `/home/user/work/wt/app-m2-selected-param-field-lifecycle-fix`. Vitest 4.1.5, private extracted Composition 0.0.12, `--configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism`; private `cacheDir` in the worker notes. Shared node_modules, runtime packages, venvs and their caches were only read.

```bash
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-field-lifecycle-fix/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.shader.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.sequence.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.astridCatalog.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.lifecycle.test.tsx src/tools/video-editor/commands/commitSession.selectedParams.recovery-counterexamples.test.ts src/tools/video-editor/commands/commitSession.selectedParams.recovery-probes.test.ts > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-field-lifecycle-fix/notes/targeted.log 2>&1
```

**PASS, exit 0 — 22 files / 418 tests, 58.39s**: the original **398**, all **17** promoted external cases including the original three failing positive assertions, plus **3** added checks. Log: [/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-field-lifecycle-fix/notes/targeted.log](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-field-lifecycle-fix/notes/targeted.log). Exact command also retained in `notes/targeted-command.txt`.

```bash
node node_modules/eslint/bin/eslint.js src/sdk/video/timeline/timelineOps.ts src/tools/video-editor/commands/clipParamsGesture.ts src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/components/PropertiesPanel/SelectedElementParamFields.tsx src/tools/video-editor/hooks/useTimelineOps.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.lifecycle.test.tsx src/tools/video-editor/commands/commitSession.selectedParams.recovery-counterexamples.test.ts src/tools/video-editor/commands/commitSession.selectedParams.recovery-probes.test.ts > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-field-lifecycle-fix/notes/lint.log 2>&1
git diff --check
```

**PASS, exit 0** for targeted ESLint and whitespace check. No ESLint cache option was enabled.

Earlier focused run: the original 17 external cases plus the existing 17 selected-form cases passed (4 files / 34 tests, 10.22s). An added immutability test initially compared the entire recovered outbox record and failed because explicit recovery advances its generation; it was corrected to compare the immutable intents and pending request/outcome, with all original promoted assertions untouched. The final 418-test pass includes the corrected test and all final source changes.

No full suite/test-service request, build, browser, socket/localhost service, project tsc, install, native Agent process or native Runtime process was run. No Git commit/merge/rebase/checkout/push was performed. Private Composition extraction and caches were removed after checks; `notes/prepare-test-env.py` plus the retained private config recreate this environment. No KEEP marker.

## Remaining gate / next steps

D01 / production activation remains **OPEN**. Synthetic normal-port transport and in-memory fake IndexedDB reopening do not prove native provider validation, a Runtime process restart, or browser traffic. The separately owned matching republished Runtime/package 0.2.9 tuple, retained storage/build/custody, native V1 max10 acceptance8/refusal16 across V2 hints/removal/restart, lost-ACK exact retry, native guarded inverse/undo/redo/reload, browser zero-legacy proof, and refreshed-main integration qualification remain unverified. Land this narrow source fix through the harness, then run that native pair/activation gate before retiring writers.

Local decisions: use a read-only accessor on the existing port rather than another draft authority; use exact existing intent acceptance rather than global saved; retain the submitted original pin on recovery; track local field edits so equal-text retyping also survives ACK. No orchestrator decision was changed.
