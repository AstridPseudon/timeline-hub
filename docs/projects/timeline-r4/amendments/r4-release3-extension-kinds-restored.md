# Release 3: the five extension kinds are back in scope

**For:** the r4 manager already working on the plan.
**Decided by:** the user, 15 Oct 2026.
**Applies to:** project J (Extensions), plus two dependency lines in A and G.

## What changed and why

An earlier rework cut Release 3's extension platform down to one proven kind (an operation) plus declarable curves and transitions. The user disagreed: the cut saved only a few days, all in Release 3, and it dropped a promised capability. **All five extension kinds are back in scope:** operation, view, component, check and generator.

**How they're built, unchanged from the lean approach:** each kind is built together with its first real extension. No adapter or generic machinery gets built ahead of a real user. The CLI, SDK, App and view support for each kind is built in the card that delivers that kind's first extension.

**Still out of scope, not restored:** advisory presence in the App, meaning "who else is in this timeline". REVIEW stays review-before-accept only.

## The cards (project J, Release 3)

| Card | Status | Size | What it proves |
|---|---|---|---|
| EXT-ONE | unchanged, scope note updated | 2.5 d, xhard | the **operation** kind plus the extension mechanism; a fresh agent builds `fit_to_beats` from the recipe |
| EXT-VIEW | **new** | 2 d, xhard | the **view** kind; a fresh agent builds `story_overview`, which appears in `show`, `visualize` and the App |
| EXT-COMPONENT | **new** | 2.5 d, xhard | the **component** kind; the modifier contract is written first; a fresh agent builds `vignette`, which renders identically in the App and in exports |
| EXT-CHECK-GEN | **new** | 1.5 d, normal | the **check** and **generator** kinds; an existing check (DAMAGED-ART) and an existing generator (`chiptune.compose`) become declarations |
| EXT-CURVES | **widened** | 1.5 d, normal | curves and transitions as before, **plus** music actions and command macros, each by one declaration |

Project J goes from 4 days to about 10. Releases 1 and 2 are unchanged.

## Dependency and milestone changes
- **EXT-CURVES** now produces `J#curves`. `J#proofs` is produced by **EXT-CHECK-GEN**.
- **FINAL-R3** (A) depends on `A#r1-accepted, I#*, C#schema-warn, D#script, D#retention, F#repairs, E#review, G#full-parity, J#curves, J#ext-view, J#ext-component, J#proofs`.
- **FULL-AUDIO-EXT** (G) depends on `G#render-parity, I#audio, J#curves, J#ext-component`: full parity includes contributed components and transitions.
- **EXT-VIEW** needs `J#ext-one, G#views, I#story`. **EXT-COMPONENT** needs `J#ext-one, G#render-parity, I#motion-contract`. **EXT-CHECK-GEN** needs `J#ext-one, J#curves, G#checks`.

## Release contract, Release 3 (replacing the narrowed text)
- Five contributor-facing extension kinds, each admitted through one extension mechanism and each with real runtime support:
  - operation `fit_to_beats` (`J#ext-one`);
  - view `story_overview` (`J#ext-view`);
  - component `vignette` (`J#ext-component`);
  - an existing check and generator converted (`J#proofs`).
- Curves, transitions, music actions and command macros, each added by one declaration (`J#curves`).
- Review-before-accept of an agent's proposal (`E#review`). **No presence.**
- The full parity matrix, every supported row passing, including contributed components and transitions (`G#full-parity`).

## The card texts (as they appear in cards.md)

### EXT-ONE: one real contribution, end to end
`J · R3 · 2.5 d · xhard · produces J#ext-one` · replaces M9 (core) + SK-2
**Goal:** One contributed operation is admitted, invoked and identified through one extension mechanism, and a fresh agent can repeat it from a recipe.
**Done when:**
1. The mechanism is chosen while proving the operation in item 2, preferring the route production already uses: pack v3's manifest `extensions` (`permissions.py`, read by `core/pack/loader.py` and `core/rendering/registry.py`) over the restored `core/extensions/*` registry (89 tests, no production consumer). The choice and its reason are in the card result. The other mechanism is frozen (no new callers), not deleted, until its callers and compatibility obligations are known.
2. An operation that returns commands runs through discovery, schema and invocation using that mechanism, and passes the harness extension path. A same-name neighbour file cannot replace it (point-qualified identity); the implementation digest changes when the code changes.
3. A pack-builder recipe (one skill) is written, and a fresh agent follows it to build `fit_to_beats` (an operation); build time and stumbles are recorded.
4. Unsupported surfaces report "unsupported" explicitly.
**Start from:** `A/astrid/core/extensions/` (`registry.py`, `model.py`, `sidecar.py`, `scopes.py`; tests `A/tests/core/extensions/`); `A/astrid/core/pack/permissions.py` (lines 123-284: manifest `extensions`); `A/astrid/packs/rendering/pack.yaml` (V3 declarations); `A/tests/editing_conformance/runner.py` (the harness).
**Not in scope:** the view, component, check and generator kinds (EXT-VIEW, EXT-COMPONENT, EXT-CHECK-GEN build each with its first user); deleting the other mechanism; a bespoke App panel.
**Depends on:** D#commands, G#evaluator-film.
**Why xhard:** chooses the platform's extension mechanism, an open design decision, and a contribution's identity (point-qualified, digest over its code) is a load-bearing invariant.
**Design detail:** `fleet/m4-music-clock.out.md` section 3.

### EXT-VIEW: the view kind, proven by a fresh agent
`J · R3 · 2 d · xhard · produces J#ext-view` · new (restores the view kind of the five)
**Goal:** A contributed read-only view, declared once, appears in `show`, in `visualize` and in the App's views, and a fresh agent can build one from the recipe.
**Done when:**
1. A view declaration (id, schema, the read model it consumes, label/help) is admitted through the EXT-ONE mechanism; `timelines show --as <view>` and `visualize --view <view>` list and render it without per-view code.
2. The App lists the declared view in its views from the declaration (generic panel from the schema; no bespoke UI) via its extension surface.
3. A fresh agent follows the recipe to build `story_overview` (chapters and story beats at a glance); build time and stumbles are recorded.
4. A view never mutates: a test asserts zero journal entries and an unchanged document after rendering every declared view. An unsupported host reports "unsupported".
**Start from:** `A/astrid/sdk/timeline_views.py`; `A/astrid/packs/rendering/actions/timeline_visualize/layers/` (`builtin.py`, `base.py`); `P/src/tools/video-editor/runtime/extensionSurface.ts`, `useExtensionLoaderWiring.ts`; `reviews/astra-high-extensions.md` (view contract).
**Not in scope:** views that edit; a bespoke App panel per view.
**Depends on:** J#ext-one, G#views, I#story.
**Why xhard:** crosses Astrid and the App, and fixes the view contract every later contributed view relies on.

### EXT-COMPONENT: the component kind, proven by a fresh agent
`J · R3 · 2.5 d · xhard · produces J#ext-component` · new (restores the component kind of the five)
**Goal:** A contributed visual element, declared once, renders identically in the App Player and in exports, and a fresh agent can build one from the recipe.
**Done when:**
1. The modifier contract (how a component modifies the frame beneath it: inputs, bounds declaration, time origin) is written first and reviewed by the orchestrator before the build.
2. A component declaration (element id, params schema, bounds, render implementation) is admitted through the EXT-ONE mechanism; it is addable with `edit --add` and the App's add menu without per-element code; the shared evaluation reports its bounds (or "unknown").
3. A fresh agent follows the recipe to build `vignette` (darkened edges); Player and export agree on it at event-centred frames (the RENDER-PARITY harness; planted 1 px change fails).
4. A component without declared bounds gives coverage "unknown" with a named finding; an unsupported host refuses explicitly.
**Start from:** `A/astrid/packs/rendering/elements/` (`catalog.ts`), `A/astrid/core/rendering/registry.py`; the shared evaluation from EVAL; `P/src/tools/video-editor/clip-types/`, `effects/`, `runtime/extensionSurface.ts`; `reviews/astra-high-extensions.md` (component and modifier contracts).
**Not in scope:** new built-in elements; motion modifiers beyond what `vignette` needs.
**Depends on:** J#ext-one, G#render-parity, I#motion-contract.
**Why xhard:** the component contract crosses Astrid, the composition package and the App, and a mismatch silently changes how contributed elements look.

### EXT-CHECK-GEN: the check and generator kinds, each with a real first user
`J · R3 · 1.5 d · normal · produces J#proofs` · new (restores the check and generator kinds of the five)
**Goal:** A check and a generator are each declared once and appear where users meet them, proven by converting an existing one of each.
**Done when:**
1. Check kind: one existing check (e.g. DAMAGED-ART) becomes a declaration (finding codes, severity, what it reads) admitted through the EXT-ONE mechanism; `check` and `lint` run it unchanged (its existing tests pass unmodified) and list its codes in `lint --list-checks`.
2. Generator kind: one existing generator (e.g. `chiptune.compose`) becomes a declaration (inputs, the assets it produces) admitted the same way; its output lands as project media with the handle printed; the App's action form for it comes from the declaration.
3. The five kinds (operation, view, component, check, generator) are listed in the pack-builder recipe, each with its proof card and one example.
4. An unsupported host gets an explicit refusal.
**Start from:** `A/astrid/packs/rendering/actions/timeline_visualize/layers/builtin_checks.py`, `A/astrid/sdk/timeline/check.py`; `A/astrid/packs/chiptune/actions/compose/`; `P/src/tools/video-editor/capabilityManifest.ts`; the EXT-ONE mechanism.
**Not in scope:** new checks or generators beyond the two conversions.
**Depends on:** J#ext-one, J#curves, G#checks.

### EXT-CURVES: curves, transitions, music actions and command macros as declared contributions
`J · R3 · 1.5 d · normal · produces J#curves` · replaces M9 (remainder)
**Goal:** A new audio curve, transition, music action or command macro is added by one declaration, with no per-kind dispatch edit.
**Done when:**
1. A new curve entry appears in the Python and TypeScript consumers without editing dispatch (generated tables agree; endpoint and legacy-linear identity tests).
2. A contributed transition appears in the App registry and passes Player/render parity.
3. The music pack's actions (`music.align/level/beats`) are admitted as declared contributions through the EXT-ONE mechanism and appear in the CLI and SDK without per-action code; a command macro (an operation built from existing commands) is one declaration and journals as one undoable step.
4. An unsupported host gets an explicit refusal.
**Start from:** `A/astrid/core/timeline/audio_curves.json`, `A/scripts/gen_audio_curves.py`; `P/src/tools/video-editor/transitions/registry/`; `A/astrid/packs/music/`; the EXT-ONE mechanism.
**Not in scope:** new curve or transition designs beyond one each for the proof.
**Depends on:** J#ext-one, I#audio, I#transitions, G#render-parity.

## Where this already lives
- **The r4 plan:** `${HISTORICAL_CONTROL_RUN_ROOT}`, branch `rework-20261015`, commits f7ac3f9 (restore) and 64534ae (presence kept out). There, `cards.md`, `release-contract.md` and `architecture.md` §3 already say this, and `projects/generate.py` regenerates the J tasklist and gates. It passes its checks: 95 cards, about 137 human-days.
- **The zip:** `timeline-r4-portfolio-20261015.zip` contains the same version.
