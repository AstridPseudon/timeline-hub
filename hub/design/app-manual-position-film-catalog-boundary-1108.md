# App M2 manual position: film/catalog boundary

## Classification

**Accepted-film change proven. This is not catalog-only. The fullM2 blocker remains.**

The gallery action is *intended* to act on a generation shown as unpositioned, but
the exact operation `usePositionExistingGenerationInShot -> placeGeneration` does
not only change an unplaced project-shot/catalog membership. It publishes a new
Runtime parent-composition revision containing a new authored media clip and a
shot-group pin. That changes accepted film placement and timing, and adds an
accepted media selection. It does not change the immutable child shot/internal
timeline revisions or their parent occurrence pins; that distinction does not
make the parent film edit catalog-only.

No code or tests were changed for this classification.

## Exact producer and caller

The exact hook is `src/shared/hooks/shots/useShotGenerationMutations.ts:341-370`.
Its comment says the generation has `NULL timeline_frame`, but the mutation
variables are only `{shot_id, generation_id, project_id}` at lines 348-356. The
hook resolves project scope and calls `placeGeneration` at lines 357-368 with no
`timelineFrame`, owner, head, time, occurrence, or revision pin. In the placement
API, omitted `timelineFrame` means auto-position, not pooled/unpositioned:
`src/shared/lib/placement/placementService.ts:160-192`.

There are exactly two production UI callers:

- `src/features/gallery/hooks/useGalleryPageState.ts:140-169` chooses this branch
  when `selectedShotFilter === resolvedTargetShotId && excludePositioned` (lines
  150-150), then forwards only the same three IDs (lines 156-161).
- `src/tools/image-generation/hooks/useImageGenActions.ts:60-93` makes the same
  `selectedShotFilter`/`excludePositioned` choice (lines 75-85) and forwards only
  `shot_id`, `generation_id`, and `project_id`.

Neither caller reads the authoritative placement document to prove that the
generation is still pooled, and neither carries an explicit owner or time. The
filter is UI intent, not an accepted-film basis.

The sibling add path makes the semantic split explicit:
`src/shared/hooks/shots/addImageToShotHelpers.ts:23-55` documents
`timelineFrame: null` as pooled/no clip, `undefined` as auto-position, and a
number as an explicit frame. The exact manual-position hook takes the second
case, not the catalog-only first case.

## Mutation and publish evidence

`src/shared/lib/placement/documentPlacement.ts` defines the authority and effect:

- Lines 4-9 say the timeline document is the only placement authority; a placed
  generation is a media clip in `config.clips` plus membership in a
  `PinnedShotGroup`, while a pooled member has no clip.
- Lines 223-239 merge the generation registry asset, ensure the shot group, and
  remove any prior expression. Since the hook omitted `timelineFrame`, lines
  242-263 append a real `TimelineClip` with `at`, `track`, `hold`, `asset`, and
  `source_uuid`, then add its clip ID to `group.clipIds`.
- Lines 95-134 read placed entries from group clip IDs and the registry, deriving
  their frame from `clip.at`; pooled entries are a separate `poolGenerationIds`
  branch at lines 116-125.

The service sends this document mutation through the Runtime parent head:

- `src/shared/lib/placement/placementService.ts:119-153` loads the default
  timeline reference and runs a bounded load/mutate/CAS cycle. Its load path is
  `RuntimeDataProvider.loadTimeline` plus `loadAssetRegistry` at lines 78-89.
- `src/shared/lib/placement/placementService.ts:172-192` resolves the
  generation's primary media through the existing R13 gallery detail authority,
  then mutates the document with the resulting registry entry and media URL.
  `src/tools/video-editor/data/generationAssetResolver.ts:79-99` selects the
  primary variant (or the first variant fallback), and lines 277-291 put that
  selected variant identity into the registry entry.
- On `origin/main` (`860d43b331fb4422b16bc0dbd7b08666a0c766a0`),
  `src/integrations/runtime/dataProvider.ts:727-740` requires the scoped
  project/timeline/head and `:774-811` builds the next parent composition with
  the changed config clips and registry. Lines `844-857` publish it with
  `expected_head` through `publishParentComposition`.
- The current integration provider has the same path at
  `src/integrations/runtime/dataProvider.ts:1014-1028`,
  `:1061-1144`; current code additionally tracks publication identity, but the
  placement helper still uses this direct parent-composition save path.

This is an accepted parent-film write even though the publication sends empty
`internal_timeline_revisions` and `shot_revisions`: the provider deliberately
preserves existing child authority from the parent occurrences. The current
provider says this directly at `src/integrations/runtime/dataProvider.ts:1137-1144`.

## Readback authority and the pin boundary

The authoritative readback is the Runtime parent head and its immutable closure,
not relational `timeline_frame`/`end_frame` values and not a display projection.

1. `src/integrations/runtime/dataProvider.ts:1395-1446` (current integration;
   `origin/main` is `:1094-1137`) inspects the canonical head, reads the
   immutable parent-composition revision for that head, and returns its `config`
   and `registry`. `canonicalParentClips` at lines 1962-1973 rejects conflicting
   top-level/config clip authorities rather than guessing.
2. For the accepted film closure,
   `src/integrations/runtime/dataProvider.ts:870-942` requires a history head
   containing both revision and publication, reads that exact parent revision,
   and validates the dependency manifest's immutable shot and internal-timeline
   pins. `:658-726` resolves each parent occurrence's pinned shot revision and
   that shot's pinned internal timeline revision. `runtimeGraphToContract` at
   `:2213-2304` carries parent occurrences and those exact child revisions into
   the graph; it does not substitute projected placement rows.
3. The placement/gallery read model is only a compatibility projection:
   `src/shared/lib/placement/placementService.ts:254-264` reads the parent
   document, and `src/shared/lib/placement/placementImageRows.ts:4-15` and
   `:86-103` merge `readPlacements` with gallery rows into the old
   `GenerationRow` shape. Its `timeline_frame` is derived from `clip.at` and is
   not the authority. The same is true of the task connection check at
   `src/features/tasks/components/TasksPane/utils/task-utils.ts:121-133`.

Therefore the immutable child revision pins remain unchanged, but the parent
revision's `config.clips`, `config.pinnedShotGroups`, and registry are accepted
film state. The classification does not infer a film edit from a relational or
display row; it follows the actual parent publish and exact-head readback.

## Frozen R4 precedent

The frozen qualified App reference
`origin/codex/handover-timeline-r4-20261019-candidate-app-qualified` has the same
document-native semantics: its placement service says there is no relational
placement route (`src/shared/lib/placement/placementService.ts:1-15`), and its
`placeGeneration` path calls the document mutation with omitted frame
(`:123-155`). Its document primitive explicitly says placed means a `config.clips`
media clip plus `PinnedShotGroup` membership
(`src/shared/lib/placement/documentPlacement.ts:1-13`, `:218-263`). Current
`origin/main` preserves that meaning while changing the publish transport to the
Runtime parent-composition route.

## Owner/time carrier result

**Concrete NO-CARRIER for this exact original UI path.** The gallery handlers are
the only production callers of this hook, and neither supplies both an explicit
film owner and an explicit time. The existing editor command session is a real
owner/head carrier—`src/tools/video-editor/hooks/useTimelineCommandSession.ts:19-35`
requires the provider, timeline ID, head refs and editor store, while
`:85-105` loads the verified identity/basis and projects the accepted parent
config—but the gallery path is not wired to that session or its capture ports.

There is an unrelated existing explicit-frame carrier,
`useUpdateShotImageOrder` at `src/shared/hooks/shots/useShotGenerationMutations.ts:263-291`,
used by the travel-between-images ShotEditor. It carries numeric frame updates
for already identified placement entries; it is not an owner-bearing carrier for
the manual-position gallery action and cannot be substituted by inference.

Accordingly, this operation cannot be admitted as an EditCommand producer on the
evidence available here. Do not delete the existing project operation, invent an
owner/time field, infer first occurrence or first frame, add a new UI/API/store
authority, or close the fullM2 blocker from this source classification. The
remaining work is a separately authorized producer/capture path with an existing
explicit owner and time carrier, or an explicit product decision to keep this
legacy direct parent writer out of film history.

## Verification

Read-only source inspection only. No tests, browser, localhost/live socket,
full suite, build, install, graph run, or unchanged9 rerun was performed, as
required by the task. Relevant App producer/placement files are identical
between the working tree and `origin/main`; the provider has the documented
current-integration delta noted above.
