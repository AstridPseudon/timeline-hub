**Verdict: APPROVE for the selected-parameter mounted/batched source fix. Real Runtime / production activation remain OPEN.**

Reviewed `tl/app-m2-selected-param-mounted-batched-fix` at **`2952e801329e430cbf864b698b93df7055e76159`**, tree **`06ff158e27e67f53a2cf55e989a5c6ab39ff53a9`**, against **`fb85a3a38ebdcaaeedac28a2498e23047ee12cd9`**. Read PLAN.md and the prior HOLD report. No remaining blocking finding in this bounded diff. Five paths change: four product files +32/-12 and one new 342-line test file. No pre-existing test changes.

The assigned review worktree remains at `7bb885b638838588a0dff81b64b7c34960ac07f3`; execution used a private archive of the exact candidate. Post-test verification confirms **5,827 tracked blobs match**, including symlink target text. Product, repository tests/config, shared dependencies and shared caches were unchanged. The source branch still resolves to the reviewed SHA.

**Line proof (all product references at the candidate SHA)**

- **Actual wrapper forwarding fixed:** `src/tools/video-editor/hooks/useTimelineCommandSession.ts:176-180` forwards `submittedInput` and refuses access through a disposed/replaced session. `src/tools/video-editor/hooks/useTimelineOps.ts:165-168` consumes it. The unchanged prior mounted-wrapper accessor and form assertions now pass: refused input16 remains distinct from accepted4. Fresh actual-hook recovery repeats this across unmount, lock release, explicit owner recovery and form remount without new retained reads, recapture or commit traffic.
- **Specific acceptance survives later ACKs:** `src/tools/video-editor/commands/commitSession.ts:103-105,420-426` creates one shared outcome cell for an observed pending input, keyed by its existing local/durable intent identity. `:237-241` updates only the exact acknowledged identity and removes its map entry. The frozen returned input has cloned args/basis and a read-only acceptance getter. `src/tools/video-editor/components/PropertiesPanel/SelectedElementParamFields.tsx:36-46,65-71` retains that input and retires only matching submitted fields whose edit counters have not advanced. An ordinary ACK or inverse cannot revoke its acceptance or accept a cancelled input. This uses no global Saved/equal-value inference and adds no persisted fields, queue or accepted-history authority.
- **Bounded lifetime:** the map stores only observed outstanding inputs; acceptance deletes its entry (`commitSession.ts:241`), tail cancellation deletes only that ID (`:679-680`), explicit rejected-prefix resolution clears it (`:567-569`), and disposal clears it (`:716-718`). A mounted field retains its own outcome only until retirement/unmount. Detaching a form does not cancel a durable submitted command. The unchanged field cleanup aborts a still-loading request (`SelectedElementParamFields.tsx:32-34`), and the unchanged SDK abort check before submission prevents creating a PARAM after detachment (`useTimelineOps.ts:171-187`). No accepted-history map was added; the existing intent-ID mapping was reused.
- **Original authority preserved:** the capture/prefetch/finish/submit implementation is unchanged (`commitSession.ts:433-536`), including accepted-original-basis refusal, exact pin, generation/head/projection fences, retained bytes, command guards and no local PARAM after-state. `useTimelineOps.ts:171-187` still captures before awaiting and submits cloned original arguments. `SelectedElementParamFields.tsx:58-63,83-87` preserves the original pin, parses literal JSON/blank clears, and uses own-key checks/definitions. `commitOutbox.ts`, server validator, generated contract, normalizer and transport are untouched.

**Executable evidence**

Vitest **4.1.5**, private extracted Composition **0.0.12** alias, runner config loader, `--no-cache`, private `cacheDir`, maximum one worker and no file parallelism. No install, build, full-suite request, browser, localhost/socket or project tsc. The source fixtures use the normal RuntimeDataProvider transport with synthetic responses and fake IndexedDB; they do not validate native Runtime acceptance.

The prior seven ordinary counterexamples were copied **byte-for-byte unchanged** from the prior review (`sha256:3ff3f24e0848ecadbc273265783a52fc79044afb0cb1a72a7160b79bc5010b74`). All **7 pass**, replacing the prior **2 pass / 5 fail**. That includes exact mounted accessor/form integration, batched PARAM+ordinary retirement, accepted Seed9 followed by Text-only submission (no stale Seed8 resend), and PARAM+inverse in one React batch.

The complete requested targeted set passes **428 tests / 23 files**, including the unchanged earlier lifecycle, recovery, cancellation, identity, prototype-key and generation-fence controls.

Eight additional ordinary tests in `workers/app-m2-selected-param-mounted-final-review/notes/fresh-counterexamples.test.tsx` pass through **useTimelineCommandSession + useTimelineCommit + useTimelineOps + AstridElementParams**:

1. Two PARAM ACKs (Seed8 then Seed9) plus an ordinary ACK before any React render; a render counter verifies no intermediate render. Both exact outcome handles accept; the form follows9 and a subsequent Text edit sends only Text (`:155`).
2. Newer post-submit raw16 survives the same double-PARAM/ordinary batch, beside accepted8 (`:187`).
3. A pending form remount attaches to the existing input and retires it across PARAM+ordinary ACK; remount after acceptance stays clean (`:208`).
4. Actual-hook remount and explicit owner recovery restore durable refused16 beside accepted4, with identical original intents/request and no additional reads/sends (`:229`). Recovery increments the existing owner-fence generation exactly once.
5. Detaching during a held retained read aborts the form request; after read release there is no PARAM or submitted input (`:260`).
6. Provider/actor-owner change fences the old accessor, shows the new owner's clean accepted4 after form detachment, leaves the original owner's durable record unchanged, and restores refused16 only after returning and explicitly recovering it (`:277`).
7. Cancelling unsent raw16 leaves its handle unaccepted and the field dirty through two later PARAMs and an ordinary ACK (`:308`).
8. Refusal preserves newer mounted typing17 while accepted4 stays visible; remount recovers the exact submitted16, own empty/prototype/constructor values, null and blank clear, without changing command bytes or rereading (`:336`).

Exact commands (N = `ORCH/workers/app-m2-selected-param-mounted-final-review/notes`):

```bash
# CWD N/source; expands the exact 23-file command below
bash ../targeted-command.txt
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-mounted-final-review/notes/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.shader.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.sequence.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.astridCatalog.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.lifecycle.test.tsx src/tools/video-editor/commands/commitSession.selectedParams.recovery-counterexamples.test.ts src/tools/video-editor/commands/commitSession.selectedParams.recovery-probes.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted-batched.test.tsx > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-mounted-final-review/notes/targeted.log 2>&1
```

**PASS, exit0 — 23 files / 428 tests, 62.95s.** Log: `N/targeted.log`.

```bash
# CWD N/source
node node_modules/vitest/vitest.mjs run --config ../vitest.external.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism > ../external-unchanged.log 2>&1
# CWD N
node node_modules/vitest/vitest.mjs run --config vitest.fresh.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism > fresh-final.log 2>&1
```

**PASS, exit0 — unchanged 7/7, 5.42s; fresh 8/8, 5.02s.** Logs and executable tests/configs are retained under N.

```bash
# CWD assigned review worktree
git diff --check fb85a3a38ebdcaaeedac28a2498e23047ee12cd9 2952e801329e430cbf864b698b93df7055e76159
python /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param-mounted-final-review/notes/verify-source.py
git status --short
```

**PASS, exit0 — whitespace clean; all candidate blobs match, prior seven cases byte-identical, no existing tests changed; assigned worktree clean.** Details: `N/source-verification.json`.

Exploration accounting: the first six fresh cases had one harness-expectation failure because explicit recovery renews the existing outbox claim generation. Corrected the private assertion to require generation+1 and exact intents/pending request, then eight cases passed. A subsequent added owner-transition assertion assumed the form stayed attached; inspection showed the harness deliberately detaches it while the session port is unavailable. The corrected test checks clean new-owner display and exact original-owner recovery without manually remounting on the outward switch. Its final eight cases pass. These exploration logs remain (`fresh.log`, `fresh-owner-exploration.log`). No product code, prior passing requirement, or original seven-case assertion was rewritten, skipped, disabled or marked expected-to-fail. The 428-test and unchanged-seven source runs were not repeated after private-test-only changes.

**Decisions, limits, next steps**

No settled design decision changed; no evidence contradicts PLAN.md. Local decisions: archive/test the exact final SHA, preserve all seven prior assertions, use actual mounted hooks plus a render counter for fresh batching probes, and leave product implementation untouched. No execution blocker.

Real Runtime **V1 max10 accept8/refuse16** across V2 hints/removal/restart remains **OPEN**, as do native retained storage/custody, lost-ACK exact retry across Runtime restart, native guarded inverse/undo/redo/reload, production binding, matching republished package tuple, zero-legacy browser traffic and refreshed-main qualification. The checked-in `src/integrations/runtime/generated-contract-metadata.ts:3` still declares **0.2.8**; this is **not** 0.2.9 qualification. Fake IndexedDB and synthetic transport do not close those gates. D01 / production activation remains OPEN.

Recommended next step: the orchestrator may accept this bounded source fix, then complete the separately owned real Runtime/browser/package activation gates. Private source/Composition extractions, dependency symlinks and any private caches were removed after verification; `N/prepare-test-env.py` recreates the test environment. No KEEP marker, integration worktree mutation, shared dependency/cache mutation, commit/merge/rebase/checkout/push or ref deletion.
