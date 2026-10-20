# Viewing architecture and M4 current state

Status: M4 cleanup is in progress. Composition 0.0.13 is current; D10, the
dead App `renderPipeline`, and the dead inspector are deleted. D08, D09, audio proof,
physical proof, and delivery are still open. Gate 6 has no current Scene,
MP4, or frame/audio parity success claim.

## Architecture

There is one timing compiler and one evaluator. Agent's timeline compiler under
`astrid/sdk/timeline/` (including `_timing_evaluators.py`) is the authority for
derived timing. Composition's existing transition-admission seam consumes and
validates the selected compiled representation; it is not a second authoring
or timing authority. The one public Composition evaluator is
`@banodoco/timeline-composition`: its public `evaluation` entry point exports
the pure scene preparation/query functions, and `TimelineComposition.tsx`
renders the same prepared scene. The evaluator answers what the supplied scene
means; it does not load Runtime data, save, accept history, or certify source
authority.

Composition source is the M4 integration at `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`
(release metadata commit `73bd62b1e1b710a730545c862bd2da76e324ca46`). The
0.0.13 change is the existing `encodedEnvelopeSource`/
`EncodedEnvelopeSource` export in `typescript/src/evaluation.ts`; the package
surface is assembled by `typescript/src/index.ts` and `package.json`. The
immutable artifact is:

```text
@banodoco/timeline-composition@0.0.13
banodoco-timeline-composition-0.0.13.tgz
SHA-256 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
58,477 bytes, 77 regular members
```

Agent consumes that installed package through its normal pin in
`astrid/core/rendering/remotion_runtime.py` and `remotion/package.json` /
`remotion/package-lock.json`. Its existing `remotion/src/Root.tsx` supplies
the host registries and imports the public Composition surface; D10 removed
the nine duplicate Agent wrapper implementations and resource declarations.
App consumes the same immutable bytes through
`vendor/artifacts/banodoco-timeline-composition-0.0.13.tgz`, pinned by its
`package.json` and `package-lock.json`; its composition/audio consumers use
the public package exports (for example
`src/tools/video-editor/compositions/AudioTrack.tsx` uses the public
`evaluation` APIs). Neither consumer has a second vendored Composition source
copy. App's public13 identity control is
`config/vite/timelineCompositionPackage.test.mjs`.

The normal Agent route obtains the accepted or candidate timeline and asset
closure through `inherited_source(timeline_path, assets_path)`. The existing
`_prepared_remotion_root` materializes that source and keeps the source,
compiled tracks, assets, theme, registries, canvas, and rational fps together
for the normal Root lifetime. Root rendering and the advisory Scene query use
that same prepared input. No new source factory, authority field, universal
renderer DTO, or snapshot rewrite is part of this architecture.

Scene checks are advisory. The existing private `scene_only` request may write
`scene-answers.json` under the existing `filmstrip_bundle`; it does not render
PNGs or add a route. Before and after the query, the source-bound label, full
frame extent, and compiled clip map must validate. Missing, stale, forged, or
malformed source is unavailable, not an empty successful scene, and never
blocks save or rewrites authored data.

The Composition scene seam is exercised by
`typescript/tests/scene-evaluation.test.ts` and
`typescript/tests/scene-diagnostics.test.ts`. The source/Root lifetime and
label rules are covered by Agent
`tests/packs/rendering/test_live_source_label_native.py::test_cas_and_unclaimed_inputs_stay_uncertified`
and
`::test_retained_source_reaches_exact_final_root_inside_normal_lifetime`.

Saving is renderer-free. Commit, reload, retry, rebase, undo, and history
acceptance depend on Runtime admission and the immutable accepted closure, not
Composition, Node, Root, or the renderer. Preview and Scene availability are
separate reports.

## Revision labels and provenance

The label describes the bytes actually displayed or admitted; a newer head,
receipt, acknowledgement, or save status cannot relabel older output.

| Display fact | Existing carrier and label |
| --- | --- |
| Accepted App projection | `TimelineData.editProjection` with `kind: 'accepted'`, carrying the exact `head.revisionId` and `head.publicationId`. |
| Local App projection | The same carrier with `kind: 'local'`, carrying its `base` pair and local `generation`; a local suffix remains local until the matching accepted basis is installed. |
| Committed managed snapshot | `snapshot_label.status: 'committed'`, label `committed revision <actual>`, and `actual_revision_id`; the identity comes from the admitted canonical/capture authority, not requested or current-head hints. |
| Candidate managed snapshot | `snapshot_label.status: 'candidate'`, label `unsaved candidate based on committed revision <base>` (or `unsaved candidate (committed base unavailable)`), with no `actual_revision_id`. |
| Uncertified/unavailable output | `snapshot_label.status: 'unavailable'`, label `revision unavailable` (or `candidate revision unavailable` for contradictory candidate bases), with no actual revision. Native input-only/CAS output keeps any claimed/base hint as uncertified and does not present it as an accepted revision. |

The existing provenance carriers are the Runtime accepted closure and
DocumentPin/read basis, Agent's `RenderRequest.verified_source` and
`inherited_source` validation, the `_prepared_remotion_root` lifetime, the
source-bound `snapshot_label`/canonical or capture authority, and App's
`editProjection` callback/generation/race guards. These are facts about the
selected source and display; they are not a second authority or a new save
protocol.

## Current qualification boundary

- Composition 0.0.13 release/package admission is qualified: build, registry
  generation, public ESM/SSR/admission checks, the scoped consumer declaration
  check, archive safety, and the central registry-child rerun passed. The
  repository's current package run is recorded as 76 passing tests.
- D10 is deleted. Agent's nine duplicate wrappers and matching implementation
  resources are gone; App's nine vendored builtin copies and normal provenance
  refresh are gone. The App dead `renderPipeline` path and six mapped private
  middleware tests are gone. The unreachable inspector and its dead resources
  are gone. Existing render-router, admission, polling, error, no-fallback,
  navigation, and filmstrip tests remain the behavior evidence.
- The deletion evidence includes Agent
  `RemotionElementGenerationTest.test_public_membership_uses_composition_registry_api`
  and `test_committed_catalog_is_fresh_for_the_in_repo_packs`, plus App
  `renderRouter.test.tsx`, `renderRouter.attach.test.ts`,
  `timelineOutputProjection.test.ts`, and `useRenderState.test.tsx`.
- D08 (private visual/timing/audio evaluation), D09 (private visualize/Scene
  evaluation and geometry/crop retirement), and the continuous-PCM/audio
  deletion remain open. Retained pixel checks and timing evaluators are not
  themselves the parity gate.
- The latest normal export has no current MP4. The saved Scene attempt failed
  before the required positive/stale/candidate/save-without-Node proof, and
  physical Player/export frame and audio parity has not been qualified. The
  owner-film and ZIP delivery gates are also open.

Historical evidence remains historical: the immutable 0.0.12 archive
(`0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`) and
prior private pixel/Scene runs are retained for comparison, but they do not
qualify the current 0.0.13 consumers or relabel the current open gates.
