# Runtime legacy consumer map

Scope: composed Runtime `tl/rt-m2-authority-compose` (`2b7be58`), with live
non-generated source in Agent/App/Composition integration trees. This is a
census, not an authorization to retain compatibility routes.

Retired Runtime methods: `update_timeline`, `replace_timeline_clip`,
`create_timeline_document`, `replace_parent_composition_media`,
`publish_parent_composition`; timeline archive/recover; direct `create_*`,
`update_*`, archive/recover, item add/remove/reorder/promote, reference link/
associate/primary, and shot text-binding mutations; `publish_timeline_render`.
Canonical `create_document`/`update_document` also refuse `timeline:*` and
`timeline.composition`; internal `promote_shot_items` has no product caller.

## Live consumer families

- **App parent/canonical film writer (exclusive):** `src/integrations/runtime/dataProvider.ts:282-287,1008-1022` calls `publishParentComposition`; the `RuntimeDataProvider`/commit-session port is the owner. Replace every ordinary edit with Agent `commitTimeline` EditCommands. No full-document fallback or settled command exists for the remaining label/delete/add/trim/split/track cases.
- **App popup add/swap (exclusive):** `shotTimelineDataProvider.ts:452-546` queues `enqueueCanonicalShotPublish` and calls `shotCompositionAdapter.publish`; this reaches the same retired parent publication. Replacement read is Runtime `getProjectMediaSelection` plus the immutable canonical head/closure; exact add and replacement/clear commands are still an Agent dependency. Do not invent `add-media`/`swap` wire names.
- **App shared placement (shared helper):** `shared/lib/placement/placementService.ts:104-106,119-239` mutates a loaded document then calls `saveTimelineAtHead`, which ends at the same retired parent publication. Placement/unplacement/frame edits need Agent commands or deletion; the CAS loop is not migration proof.
- **App bootstrap/setup only:** `createDefaultTimeline.ts:50-76` publishes an empty parent to create/repair a shell. It is not an ordinary product edit, but it still hits the retired route; hand off to constrained `createTimeline`/explicit empty bootstrap, then `commitTimeline` for edits. Its setup tests must follow that seam.
- **Agent authoring writer:** `astrid/core/timeline/authoring_bundle.py:43-53,1577-1617`, reached by SDK authoring/remote/store adapters, still emits a whole compiled publication. Agent owns conversion to the command provider; Runtime must not resurrect a publication alias. `sdk/workspace_client.py` and `sdk/remote.py` retain broad retired wrappers, but no additional product caller was found.
- **Agent/Viewing render settlement:** `astrid/core/execution/generic_host.py:8401-~8520,9631-9639` and `packs/rendering/shared/runtime_stitch.py:104-158` call `publish_timeline_render` after `rendering.assemble_timeline`. Replace with Agent command commit of the authoring proposal, then Runtime `admitTask` for revision-pinned `rendering.render`; settle output through the existing task/output path. This is a coupled Agent/Viewing handoff; Runtime retirement waits for retry/restart proof.
- **Composition/App viewing:** Composition has no Runtime calls. App `renderRouter.ts` already admits `rendering.render` tasks and does not call `publish_timeline_render`; it is a read/render consumer, not a retired writer.
- **Unconsumed retired surface:** No live non-generated product caller was found for `replace_parent_composition_media`, timeline-document creation/update, or direct shot/reference/item/text-binding Runtime methods beyond Agent API wrappers and setup/tests. App Supabase shot/generation/placement RPCs and edge append routes are catalog/relational or legacy canonical writers, not replacements for Runtime commands; purge/convert the canonical ones per `app-writers.md`.

## Existing tests that cannot migrate yet

- Agent positive whole-publication fixtures: `tests/editing_conformance/test_commit_runtime_m1.py`, `tests/sdk/test_timeline_script.py`, `tests/timeline/test_authoring_{bundle,media,feedback,shot_composition_migration}.py`; keep their semantic assertions, migrate only after Agent publishes command schemas/provider fixtures.
- App positive publication fixtures: `src/integrations/runtime/{dataProvider.test.ts,dataProvider.parity.test.ts,shotCompositionRuntime.test.ts,createDefaultTimeline.test.ts}` and `src/test/fakeWorkspaceRuntime.ts`; they currently model `composition-revisions`, so cannot become commit-door tests until each producer has command coverage.
- Render chain: `tests/packs/video_editing/test_runtime_publication_chain.py` positively stubs/calls `publish_timeline_render`; retain it until assemble→command→render admission and exact retry/restart are proven. Runtime authority/refusal tests remain valid and should not be weakened.

## Exact handoff

Runtime manager: use this map to reject/retire the routes only after the named
consumers are migrated; no compatibility writer or new DTO. Agent manager owns
the missing ordinary, popup, authoring, shot/occurrence/reference, and render-
settlement command schemas/captures. App manager owns producer conversion,
bootstrap setup, zero-traffic tests, and deletion of fallback/edge canonical
writers. Viewing manager coordinates assemble/render settlement and proves
revision-pinned frame/audio parity. Catalog metadata remains catalog metadata;
canonical film writes go only through `commitTimeline`.
