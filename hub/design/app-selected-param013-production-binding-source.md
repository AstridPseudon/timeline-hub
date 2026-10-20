# Selected PARAM on normal Runtime 0.2.13: source port complete, production binding blocked

Base **171a259acbeb3ced855ca8f72fed0943a2f5a5cb**, branch `tl/app-m2-selected-param013-production-binding-source`. Read PLAN, INBOX08:36, refreshed source-port report and mounted-final-review first. **Stopped at the task's explicit missing-authority/read-surface condition. No production binding or activation is claimed.**

## Source and diff

Applied only `git diff --binary 0ea988bdd2907c876b82fd2620820e3fb6d6ea84 783ee80478092b01f080fd627ffc7ddbca1e2966` using `git apply`; `git apply --check` passed first. No old ancestry or whole-tree copy. Exact patch retained in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/approved-param.patch`.

**20 paths, +2748/-30 (net +2718)**. Product: 11 paths +606/-25; tests/support: 9 paths +2142/-5. Every resulting allowed file is byte-identical to approved `783ee804`. All **5818 other tracked paths** are byte-identical to assigned `171a259`, including generated normal **0.2.13**, schema digest `sha256:8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`, CORS, current root/public Composition12, MAIN parity harness, preview/render and fallback writers. Source preservation is verified; this is not a fresh browser/parity qualification.

Exact allowlist:

- `src/integrations/runtime/retainedParamInputs.test.ts`
- `src/integrations/runtime/retainedParamInputs.ts`
- `src/sdk/video/timeline/timelineOps.ts`
- `src/tools/video-editor/commands/__tests__/commitSessionEnvironment.ts`
- `src/tools/video-editor/commands/clipParamsCapture.ts`
- `src/tools/video-editor/commands/clipParamsGesture.ts`
- `src/tools/video-editor/commands/commitSession.selectedParams.recovery-counterexamples.test.ts`
- `src/tools/video-editor/commands/commitSession.selectedParams.recovery-probes.test.ts`
- `src/tools/video-editor/commands/commitSession.selectedParams.test.ts`
- `src/tools/video-editor/commands/commitSession.ts`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.lifecycle.test.tsx`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted-batched.test.tsx`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx`
- `src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx`
- `src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx`
- `src/tools/video-editor/components/PropertiesPanel/SelectedElementParamFields.tsx`
- `src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx`
- `src/tools/video-editor/hooks/useTimelineCommandSession.ts`
- `src/tools/video-editor/hooks/useTimelineOps.ts`
- `src/tools/video-editor/hooks/useTimelineState.ts`

No additional product glue or repository tests were added after finding the blocker. Existing approved cancel/reopen/recovery/coalesced ACK/original-guard tests remain exact. No test was skipped, disabled, weakened or changed to expect lost behavior.

## Concrete blocker

- `src/tools/video-editor/hooks/useTimelineSave.ts:99-102` supplies the provider to the real session but cannot supply `paramReadClient` from any public provider capability. `DataProvider` has no exact retained-document/object read capability.
- `src/integrations/runtime/dataProvider.ts:330-331` keeps project and `AstridRuntimeClient` private. The facade's generated `WorkspaceClient` getter (`client.ts:287`) and authenticated `withSession` (`:506`) are private too. **Neither facade nor provider publicly forwards `getProjectVerifiedDocument` / `getProjectVerifiedDocumentObject`.** The two generated methods exist at `generated.ts:182-183`; generated existence alone is not an authenticated host binding. Accessing private members via casts or constructing another client would violate the brief.
- `PropertiesPanel.tsx:519-559` supplies none of the staged `retainedDocumentPin`/`timelineOps`/`commandState` props to `ClipPanel`. The body declares them at `ClipPanelBody.tsx:48-52`, but the original-pin accessor does not exist. Raw canonical closures retain a **set** of `dependency_manifest.documents`; this is not a target-specific pin accessor and may be empty for a selected clip. Display descriptors/admission revision hashes are not DocumentPins.
- The existing provider can successfully load a canonical selected-element clip with empty `documents`, as the executable reproduction demonstrates. Even giving an explicit external specimen pin (also present in the accepted manifest in the second case) does not cure the missing authenticated read capability.

Reproduction: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/binding-blocker.test.tsx`, **2/2 diagnostic tests PASS**, using real `RuntimeDataProvider` with synthetic HTTP transport, real `useTimelineSave`, its real session wrapper and real `useTimelineOps`. For manifest absent/present, start from accepted seed4 and submit literal seed16 with a test-owned exact pin. Both reject exactly **“Selected clip parameter input reads are unavailable; draft preserved”** at `commitSession.ts:488`; accepted4 remains displayed, **zero retained reads and zero commits** occur. These external assertions document the blocker, not a desired replacement behavior or native acceptance. No fake successful panel callback is used. This is deliberately smaller than inventing a Props binding with fabricated authority.

## Smallest proposed follow-up (manager decision)

1. Authorize the small existing-client bridge outside this task's allowlist: `DataProvider.ts`, `integrations/runtime/dataProvider.ts`, `integrations/runtime/client.ts`. Add only the read capability needed to forward the two existing generated retained reads through the **existing** authenticated client/session and provider project scope. No new client, endpoint, DTO, browser validator or cache.
2. Add an accessor in the existing command session/port for the selected raw clip's original retained pin at the accepted basis. Resolve only exact pins retained in that canonical closure against the existing verified read helper; retain the original selection/basis across awaits. Missing or ambiguous retained authority must remain a visible draft-preserving refusal. An initially empty closure needs an explicitly supplied authoritative original pin from its owning admission path; latest document/pack metadata cannot supply it by inference. The manager should identify that source before extending implementation.
3. Then wire `useTimelineSave` to `paramReadClient` and pass that accessor's pin plus the existing store ops/session state through `PropertiesPanel` → `ClipPanel`. Add the requested actual Props→panel→op pending/accepted/refused tests, including raw16 and original guards. Current native/browser activation remains the separately owned gate.

This is evidence that the brief's assumption of an existing public authenticated read/pin surface does not hold on `171a259`; it does not contradict or change the settled single-server-validator decision. No source outside the approved20 was changed to work around it.

## Commands and results

CWD `/home/user/work/wt/app-m2-selected-param013-production-binding-source`. Node22.22.0 / Vitest4.1.5 / private read-only Composition0.0.12 dependency view. All test commands used private TMPDIR/cacheDir, runner loader, no cache, maximum one worker, no file parallelism. The 23-file command is the approved lifecycle set; the save controls are direct neighbors of the session boundary.

```bash
env TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/tmp node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.selectedParams.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/tools/video-editor/commands/semanticGestures.test.ts src/tools/video-editor/commands/trackLabelGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/video-editor/hooks/useTimelineCommandSession.projection.test.tsx src/integrations/runtime/retainedParamInputs.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.selected.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/hooks/useTimelineOps.trackLabel.test.ts src/tools/video-editor/hooks/useTimelineOps.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.shader.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.transition.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanel.sequence.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.test.tsx src/tools/video-editor/components/PropertiesPanel/SequenceParamEditor.astridCatalog.test.tsx src/tools/video-editor/components/PropertiesPanel/ClipEffectsTab.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.lifecycle.test.tsx src/tools/video-editor/commands/commitSession.selectedParams.recovery-counterexamples.test.ts src/tools/video-editor/commands/commitSession.selectedParams.recovery-probes.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted-batched.test.tsx
```

```bash
env TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/tmp node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/vitest.repro.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism
```

```bash
env TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/tmp node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/hooks/useTimelineCommit.test.tsx src/tools/video-editor/hooks/useTimelineSave.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.test.tsx src/tools/video-editor/hooks/useTimelineSave.recovery.persistence.test.tsx
```

- Targeted: **23 files / 432 PASS**, exit0, 63.88s (`notes/targeted.log`). Includes mounted PARAM input/outcome/form tests, recovery, original guard, retained-read validation and ordinary control neighbors.
- Blocker reproduction: **1 file / 2 PASS**, exit0, 5.02s (`notes/repro.log`). Diagnosis only; no production ingress success.
- Save/recovery preservation: **4 files / 34 PASS**, exit0, 9.58s (`notes/preservation.log`).

Other exact commands (all exit0):

```bash
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/audit-source.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/source-audit.json
git diff --check
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/audit-deps.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/deps-before.json # before tests
python3 -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/audit-deps.py > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/deps-after.json  # after all tests
cmp /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/deps-before.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-selected-param013-production-binding-source/notes/deps-after.json
```

The source audit verifies exact20 files and every other tracked blob, including symlinks. The dependency audit compares all77 Composition package file hashes, React/Remotion peer package metadata and observed shared `.vite`/`.vite-temp`/`.cache` trees. Those observations match before/after. No shared dependency, runtime, venv or cache was mutated by this worker. Only the worker-local node_modules link was temporarily redirected, then restored. Private notes dependency link/cache/tmp removed; `notes/prepare-test-env.py` recreates the test setup.

## Unrun and handoff

**Not run:** full suites, build, install, project tsc, browsers, localhost/sockets, native Runtime/provider acceptance, actual full PropertiesPanel ingress success, or the prior review's external7+fresh8 standalone probes. The corresponding checked-in approved mounted/lifecycle tests ran as part of432. Runtime V1 max10 accept8/refuse16 after V2/removal/restart, lost ACK/restart retry, native inverse/reload, current browser zero-legacy traffic and production activation remain OPEN. Synthetic tests do not close these gates.

No new semantic validator/preview engine, proxy, auto/None path, writer deletion, bootstrap, generated edit, commit/merge/rebase/checkout/push or ref operation. Source port is ready for review; real binding is **BLOCKED** pending the bounded capability/original-pin handoff above. Wrote worker report, commit-msg, BLOCKED and KEEP. **No DONE marker**, because the production binding could not be completed honestly.
