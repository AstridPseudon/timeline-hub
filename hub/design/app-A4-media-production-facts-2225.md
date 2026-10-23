## A4/A3 source handoff

No product files were changed. Commit message and `DONE` marker were written as required.

### Production after-anchor facts

Current reachable App path:

`AstridTimelineEditor.tsx:524-533` and `useAddVariantAsGeneration.ts:87-97` call:

```ts
commands.addClip({
  preparedAsset,
  afterClipId: clipId,
})
```

This routes through [`useTimelineCommandsService.ts:457-509`](/home/user/work/wt/app-A4-media-production-facts-2225/src/tools/video-editor/hooks/useTimelineCommandsService.ts:457), then [`media.ts:560-705`](/home/user/work/wt/app-A4-media-production-facts-2225/src/tools/video-editor/commands/media.ts:560), which uses [`duplicate-clip.ts:32-103`](/home/user/work/wt/app-A4-media-production-facts-2225/src/tools/video-editor/lib/duplicate-clip.ts:32).

Actual App semantics:

- Clones normalized `TimelineData` action/meta, not authored raw parent rows.
- Duplicate starts at source `end`.
- Duration is `max(0.05, source.end - source.start)`.
- Later actions on the same row shift by that duration.
- Other rows/tracks are unchanged.
- `clipOrder` inserts the new ID immediately after the source.
- Metadata is cloned, including `transition`, then asset/track are replaced.
- No raw `hold`, missing-vs-null distinction, `from/to`, or raw `at_ms` birth semantics are preserved.

The Runtime-backed save boundary explicitly rejects this prepared after-anchor shape. [`timelineLocalSaveHandoff.ts:246-279`](/home/user/work/wt/app-A4-media-production-facts-2225/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:246) requires an ordinary image add and refuses `afterClipId`, replacement/removal, forced tracks, and non-image media. Therefore the current after-anchor UI path is preview/local-state reachable, but not a valid prepared-media Runtime semantic commit.

The raw after-anchor implementation in [`parentAfterAnchorCapture.ts:58-145`](/home/user/work/wt/app-A4-media-production-facts-2225/src/tools/video-editor/commands/parentAfterAnchorCapture.ts:58) is dormant helper/test behavior, not a current production caller or registered provider. Its semantics are:

- Duration: authored `hold` when numeric, otherwise `to - from`, divided by speed.
- Placement: anchor start plus `max(0.05, duration)`.
- Clone preserves the source row’s raw fields, including missing/null `hold` and `transition`; it changes reserved ID and selected media asset.
- `at_ms` is preserved/recomputed when authored.
- Ripple shifts later same-track siblings in `collection.clips.after`; other tracks/siblings remain unchanged.
- It validates source track, raw asset identity, selection, and clone equality.

Those four old positive raw cases are therefore not reachable from the current UI/provider path. They must not be relabeled as production acceptance evidence.

Agent-side production has a related limitation:

- [`native_parent_media_commands.py:25-52`](/home/user/work/agent/astrid/sdk/timeline/native_parent_media_commands.py:25) can create a parent after-anchor through `ctx.create(..., after=...)`, but uses `raw_window=False`, requiring a complete positive hold and rejecting non-null transition.
- [`native_occurrence_media_commands.py:220-263`](/home/user/work/agent/astrid/sdk/timeline/native_occurrence_media_commands.py:220) and `:284-290` show `clip.swap-media` using `raw_window=True`. Swap preserves raw timing/transition/hold distinctions, including missing/null hold and incoming transition, but it replaces an existing clip and does not birth a new one.

Smallest migration need: extend the existing parent birth path to use the raw-window semantics required for after-anchor birth. No new operation, generic patch path, waiver, or provider abstraction is justified by the evidence.

### Current image witness seam

Current real image path:

1. [`ShotTimelineMediaControls.tsx:186-240`](/home/user/work/wt/app-A4-media-production-facts-2225/src/tools/travel-between-images/components/ShotTimelineMediaControls.tsx:186) uploads the file and calls `prepareGenerationAsset`.
2. [`useAssetManagement.ts:366-396`](/home/user/work/wt/app-A4-media-production-facts-2225/src/tools/video-editor/hooks/useAssetManagement.ts:366) calls Runtime `prepareMediaImport`.
3. [`dataProvider.ts:1722-1739`](/home/user/work/wt/app-A4-media-production-facts-2225/src/integrations/runtime/dataProvider.ts:1722) retrieves and validates the exact Runtime selection:
   `asset`, `generation_id`, `variant_id`, `object_id`, `catalog_digest`.
4. [`useAssetManagement.ts:240-248`](/home/user/work/wt/app-A4-media-production-facts-2225/src/tools/video-editor/hooks/useAssetManagement.ts:240) carries that selection into the prepared asset.
5. [`timelineLocalSaveHandoff.ts:246-279`](/home/user/work/wt/app-A4-media-production-facts-2225/src/tools/video-editor/hooks/timelineLocalSaveHandoff.ts:246) emits the native command:

```json
{
  "schema_version": 1,
  "op": "clip.add-media",
  "version": "1",
  "select": "parent",
  "args": {
    "row": "...canonical authored row...",
    "media": {
      "asset": "...",
      "generation_id": "...",
      "variant_id": "...",
      "object_id": "sha256:...",
      "catalog_digest": "sha256:..."
    }
  },
  "intent": {"ownership": "parent"}
}
```

The full V2 request retains the required API/project/timeline/base revision/publication, command, label, step, merge, reads, idempotency, dry-run, source, rationale, and group metadata. Replies retain accepted/merged/historical-rebased, canonical document, digest, identity map, records, dependencies, effects, steps/history/undo steps, preview/required/would-status, and structured conflict/invalid fields.

Existing mounted E2E evidence is in [`three-products.p2-elements-assets.spec.ts:467-505`](/home/user/work/wt/app-A4-media-production-facts-2225/tests/e2e/local/three-products.p2-elements-assets.spec.ts:467). It uses a real harness-managed object, observes the real import and selection responses, and asserts that emitted `command.args.media` exactly equals the Runtime selection. It also verifies the canonical row shape and registry fields.

The existing Agent fixture is the smallest authority-bearing source:

- [`test_commit_runtime_parent_media.py:150-159`](/home/user/work/agent/tests/editing_conformance/test_commit_runtime_parent_media.py:150) obtains `editing.pins['new']` through `RuntimeService.get_project_media_selection`.
- The resulting selection has exactly the five fields above.
- [`test_commit_runtime_parent_media.py:69-70`](/home/user/work/agent/tests/editing_conformance/test_commit_runtime_parent_media.py:69) uses that selection in `clip.add-media`.
- [`timeline_commit_port.py:350-357`](/home/user/work/runtime/runtime_protocol/timeline_commit_port.py:350) resolves the selection through Runtime media reads.
- [`commit.py:964-968`](/home/user/work/agent/astrid/sdk/timeline/commit.py:964) declares/reads media for `clip.add-media` and `clip.swap-media`.

The bridge should bind `editing.pins['new']` directly as `PreparedMediaImport.mediaSelection`, then let the existing App carrier flow deliver it through `prepareGenerationAsset` and the semantic outbox. Do not use the retained `33934817...` packet or synthetic `sha256:` placeholders as authority: that packet contains four synthetic `doc.patch` requests and is not Runtime-authority-complete.

There is no existing in-repo adapter that runs the App React/outbox path against the exact live Python `media_realm()` instance. The existing App E2E has live Runtime authority; the Agent fixture has real managed selections but fixture-generated media bytes. The next bounded worker must compose those existing seams. No new API, emitter, helper, manifest, or authority fabrication is needed.

### Verification

Not run, per the READONLY/source-only brief. No tests, types, lint, browser, Runtime, or full suites were invoked.