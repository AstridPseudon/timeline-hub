# Releases 2 and 3: card-owned work on the same timeline

**Authority:** [North Star](northstar.md), [architecture](architecture.md), [current cards](cards.md), the restored [Release 3 scope](amendments/r4-release3-extension-kinds-restored.md), and the [Astra23 many-hands ruling](amendments/20261015-many-hands-elegance.md). Each card's dependencies and acceptance criteria remain in cards.md and [dependency-graph.json](dependency-graph.json); this overview adds none.

## Release 2

Release 2 extends the same command path, timing compiler, and shared evaluation. Work starts when the card's actual dependencies and first consumer are available; the release label does not impose a separate implementation waterfall.

- Timing repairs and music segments remain owned by [TIMING-FIXES](cards.md#timing-fixes-timing-binds-to-the-words-and-steps-it-meant) and [MUSIC-SEGMENTS](cards.md#music-segments-rebuild-the-music-bed-on-every-compile).
- Story ranges, motion, transitions, and audio remain owned by [STORY](cards.md#story-chapters-keep-their-target-kind), [MOTION-CONTRACT](cards.md#motion-contract-the-clock-trim-and-keyframe-origin), [MOTION](cards.md#motion-easing-loop-phase-fit-curves-modifiers), [TRANSITIONS](cards.md#transitions-one-ownership-rule), and the existing audio cards.
- Schema findings, replays, and lint keep their current owners and dependencies in the card set. They use the same authored projection and edit semantics; this overview does not add a new evaluator, package, or compatibility rule.

## Release 3: five contributor-facing kinds

The five kinds are proven one at a time through existing hosts and their first consumers. They are contributor contracts over existing mechanisms, not a universal plugin runtime.

| Kind | Existing host and first consumer | Current example |
|---|---|---|
| Operation | EXT-ONE; returns ordinary commands through the runner | **fit_to_beats** |
| View | EXT-VIEW; reads addressed data and existing projections, without mutation | **story_overview** |
| Component | EXT-COMPONENT; uses the renderer/catalog and declares bounds or reports unknown | **vignette** |
| Check | EXT-CHECK-GEN; returns addressed findings; a fix is an ordinary command | **DAMAGED-ART** |
| Generator | EXT-CHECK-GEN; uses an existing action and project asset handles; placement is an ordinary edit | **chiptune.compose** |

See [EXT-ONE](cards.md#ext-one-one-real-contribution-end-to-end), [EXT-VIEW](cards.md#ext-view-the-view-kind-proven-by-a-fresh-agent), [EXT-COMPONENT](cards.md#ext-component-the-component-kind-proven-by-a-fresh-agent), and [EXT-CHECK-GEN](cards.md#ext-check-gen-the-check-and-generator-kinds-each-with-a-real-first-user). [EXT-CURVES](cards.md#ext-curves-curves-transitions-music-actions-and-command-macros-as-declared-contributions) owns declared curves, transitions, music actions, and macros; a macro remains one transaction and one undoable step.

EXT-ONE prefers the production pack-v3 route while proving its real operation. The compatibility bridge stays private and is frozen for new consumers until its callers and obligations are known; remove duplicate consumer behavior only where the current source shows the replacement is complete. F/G's renderer bridge follows the same rule: keep the narrow bridge private, extend the shared evaluator from real renderer consumers, and retire duplicate semantics under [RETIRE-EVAL](cards.md#retire-eval-delete-the-duplicate-evaluators).

## Existing demonstrations and pending evidence

Keep the named [IP3–IP8 demonstrations](testing.md#3-integration-points-the-merge-manager-through-the-lease) and their current card examples:

- **IP3–IP4 and X0:** a 9-frame anchored App drag survives an intervening agent retime; a held save response plus a newer local edit resolves to the canonical accepted state plus the preserved suffix. Retry, disjoint survival, named overlap conflict, and failed-suffix recovery remain part of the existing demonstrations. The [main editor](cards.md#x0-editor-record-the-main-editors-save-paths) and [shot popup](cards.md#x0-popup-record-the-shot-popups-save-paths) carry the same meaning.
- **IP5–IP6:** the App and two agents share accepted provenance and exact revisions; preview, render, and audio agree through the shared evaluation. Existing undo, revert, and restore examples remain attached to their cards.
- **IP7:** story, motion, audio, and timing examples use the current Release 2 cards and their existing film fixtures.
- **IP8:** the first-consumer examples above use the existing hosts and extension proofs; no second preview engine, alternate publication path, or private timing engine is added.

These are the established proof locations, not claims that the points have passed. X0 observations and named historical film proof remain pending in [status](status.md). Synthetic fixtures do not become historical proof through documentation edits.

## Historical proposals retained as history

Earlier wording proposed M5/SK-1 as a separate grammar experiment, K2 as a published contract package with TimelinePatch aliases, an extra cursor publication feed, and per-feature requires bumps. These are not active architecture: the shared vocabulary and generated registry are current; [architecture](architecture.md) names the existing commit and command contracts, and the Runtime's existing revision history remains the history source. Storage compatibility uses the single **app.astrid.v** property. Keep these old labels as historical context only; the current cards and DAG govern implementation and acceptance.
