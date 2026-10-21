# App transition SET proposal source review

## Verdict

**No SOURCE ACK for the exact existing App carrier yet.** The proposed raw
values.transition shape and incoming TO/adjacency behavior match the App/Main
source where the existing selected reference is present, but the current
dormant App producer has concrete incompatibilities with the proposal's paired
clear, selected-source carrier, and legacy callback cases below. This is a
source review only: no App, schema, generated artifact, pin, caller, release,
or writer activation was changed.

## Matching source

- Main writes the incoming transition and selected elementRef to the TO clip
  in one image, stores authored seconds, and preserves an existing transition
  envelope on update:
  src/tools/video-editor/runtime/element-adapter.ts:355-415.
- Main requires same-track adjacency (< 0.001) and shortest-neighbor frame fit:
  src/tools/video-editor/runtime/element-adapter.ts:175-189,231-243,360-367.
- The dormant App clip.set recorder has the same TO-oriented stable parent /
  occurrence target, predecessor selection, endpoint tolerance, FPS window,
  and shorter-neighbor check:
  src/tools/video-editor/commands/clipScalarCapture.ts:149-170,243-288.
- Its transition validator accepts type, positive finite seconds, optional
  non-empty revision, object params, and literal finite-JSON opaque top-level
  keys while refusing compiled-only fields:
  src/tools/video-editor/commands/clipScalarCapture.ts:224-235.
- The existing transition-only clear is correct: the panel emits
  values:{}, clear:['transition'] at
  src/tools/video-editor/components/PropertiesPanel/ClipTransitionSection.tsx:111-120,
  and the recorder clears only that property at
  src/tools/video-editor/commands/clipScalarCapture.ts:385-389. Focused tests
  verify ABSENT-after-clear and preservation of unrelated fields/ref data at
  src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx:191-210.

## Concrete incompatibilities

1. **The proposed paired clear is not representable by the dormant App scalar
   carrier.** The proposal requires
   clear:['transition','elementRef'] for associated removal and rejects a lone
   elementRef clear (runtime-transition-set-owner-proposal-20261021T0920.md:121-131).
   App's ClipScalarArgs and ScalarClear admit only hold, asset, and transition
   (src/tools/video-editor/commands/clipScalarGesture.ts:7-15;
   src/tools/video-editor/commands/clipScalarCapture.ts:18-20), and the
   recorder rejects any other clear key at
   src/tools/video-editor/commands/clipScalarCapture.ts:202-204.
   captureClipClear also exposes only the three-key union at
   src/tools/video-editor/commands/clipScalarCapture.ts:465-471. Therefore
   the existing App helper can produce the already-native transition-only
   RESET, but cannot produce the proposal's explicit associated transition
   removal.

2. **Optional elementRef wording conflicts with the ca9 semantic guard and
   App's legacy no-ref shape.** The proposal describes elementRef as present
   only when a transition element is selected
   (runtime-transition-set-owner-proposal-20261021T0920.md:53-57), while the
   ca9 Agent source requires a matching ref for every transition SET and
   compares its id/revision
   (/home/user/work/agent/astrid/sdk/timeline/_clip_scalar_commands.py:98-104).
   App's authored model explicitly permits legacy clips without a ref
   (src/tools/video-editor/types/index.ts:396-398), and its scalar SET path
   accepts a transition with no supplied or existing ref: it reads the ref if
   available, but only validates it when defined
   (src/tools/video-editor/commands/clipScalarCapture.ts:363-376). The
   existing scalar fixture contains an incoming transition with no elementRef
   (src/tools/video-editor/commands/fixtures/recipe_m2_app_clip_scalar_fields.json:24-31).
   Either the proposal must explicitly refuse legacy/no-ref transition SETs,
   or ca9's required-ref guard and the proposal's optional wording need
   reconciliation; the current App source cannot ACK both interpretations.

3. **Selected-pack schema_source / retained P1 authority is not carried by the
   dormant App scalar path.** The proposal adds the existing DocumentPin
   carrier for selected project-pack transitions and requires retained source
   authority (runtime-transition-set-owner-proposal-20261021T0920.md:45-57,98-105).
   App's scalar command shape requires exactly values and clear, rejecting any
   third argument at src/tools/video-editor/commands/clipScalarCapture.ts:189-192;
   captureClipSet constructs only those two args at
   src/tools/video-editor/commands/clipScalarCapture.ts:445-460, and the
   session invokes it directly at src/tools/video-editor/commands/commitSession.ts:862-879.
   The existing selected-element capture explicitly says project-pack
   authoritative capture is unavailable at
   src/tools/video-editor/commands/elementCapture.ts:69-75. This is not a
   request for a new authority; it is an exact missing handoff of the existing
   retained authority into this carrier.

4. **The current type-selector callback is not a complete opaque transition
   SET.** Selecting a type builds only type, duration, and params and drops the
   old transition's revision/unknown members and any matching elementRef:
   src/tools/video-editor/components/PropertiesPanel/ClipTransitionSection.tsx:147-163.
   The current mounted callback test records that replacement at
   src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx:237-245.
   Duration, parameter, and reset callbacks do remain SETs and spread the
   existing envelope (ClipTransitionSection.tsx:258-275,293-335); reset
   remains a SET as required. But the type callback cannot be mapped to the
   proposal's complete raw envelope plus matching ref without a later caller
   change.

5. **params:null is accepted by the current legacy duration callback but is
   refused by the proposed SET validator.** The current duration callback
   spreads the transition, retaining absent or null params
   (ClipTransitionSection.tsx:269-275), and existing tests cover both cases
   (src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx:273-297).
   The dormant native validator requires params to be an object when present
   (src/tools/video-editor/commands/clipScalarCapture.ts:224-229), so a raw
   duration SET over params:null refuses. Reset intentionally materializes an
   object and remains a SET (ClipTransitionSection.tsx:300-309; tests
   TransitionPreservation.test.tsx:299-307). The proposal must preserve the
   intended null/absence distinction or explicitly make the refusal visible;
   silent normalization is not source-compatible.

## Evidence

Command run against the unchanged App worktree (shared node_modules resolved
to /home/user/work/app/node_modules; Vitest cache disabled):

    node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-parent-trim029-source-slice/notes/vitest-runner.cjs ./node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipScalarCapture.test.ts src/tools/video-editor/commands/clipScalarGesture.test.ts src/tools/video-editor/components/PropertiesPanel/ClipPanel.nativeNone.test.tsx src/tools/video-editor/components/PropertiesPanel/TransitionPreservation.test.tsx

Result: **4 files passed, 74 tests passed**. No browser, actual/live, full,
build, TypeScript, install, graph, schema generation, pin, or release run.

## Recommended next step

HOME should reconcile the five exact points above against the settled proposal
before recording an App source ACK. Keep the existing clip.set carrier and
transition-only clear; any repair should remain within that carrier, preserve
the existing retained P1 proof, and leave SET/type/reset as SET operations.

