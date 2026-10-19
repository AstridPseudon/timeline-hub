# Runtime legacy consumer map

Scope: Runtime base `9f9b25c`, with live non-generated source in the Agent,
App, and Composition integration trees. This is a census and handoff, not an
authorization to retain compatibility routes.

## Disposition

M2 rejects direct timeline/shot/reference/document writers. In particular,
project shot create/update/archive/recover, item add/remove/promote/reorder,
shot text-binding set/rebind, project reference create/update/archive/recover,
reference associate/primary/link, and `publish_timeline_render` must not write
canonical state. `create_timeline` is only the constrained empty bootstrap.
Project shot/reference GET/list/show remain catalog reads; catalog-shaped
mutations are still canonical semantic writes and are not retained by default.

## Live consumer families

- **App parent/canonical film writer:** `src/integrations/runtime/dataProvider.ts:282-287,1008-1022` calls `publishParentComposition`. App owns conversion to Agent `commitTimeline` commands; no settled command exists for the remaining label/delete/add/trim/split/track cases.
- **App popup add/swap:** `shotTimelineDataProvider.ts:452-546` queues `enqueueCanonicalShotPublish` and `shotCompositionAdapter.publish` into the same retired publication. App owns producer conversion; prerequisite is Runtime immutable media selection plus exact add/replace/clear command schemas.
- **App shared placement:** `shared/lib/placement/placementService.ts:104-106,119-239` mutates a loaded document then calls `saveTimelineAtHead`. App owns command conversion or deletion; the CAS loop is not migration proof.
- **App bootstrap:** `createDefaultTimeline.ts:50-76` publishes an empty parent for shell setup. App/Runtime own the constrained empty bootstrap; subsequent edits use commands.
- **Agent authoring writer:** `astrid/core/timeline/authoring_bundle.py:43-53,1577-1617` and its SDK/remote/store adapters still emit whole publication. Agent owns command-provider conversion; Runtime must not add a publication alias.
- **Agent catalog/reference and shot CLI (previously omitted):** `astrid/packs/references/cli.py:129,142,154,163,187,199,211` calls `client.references.{create,update,archive,recover,associate,link,set_primary}`; `astrid/packs/shots/cli.py:171,181,194` calls `client.shots.{create,add_item,remove_item}`. Agent owns command schemas/captures for reference metadata/associations and shot/occurrence/item semantics, with exact media pins as prerequisites.
- **Typed transport trace:** `astrid/sdk/remote.py:2305-2398,2401-2548` routes these families through `_typed` (`:323-440`) to `WorkspaceClient` generated calls (`astrid/sdk/workspace_client.py:661-752`); these are real typed Runtime calls, not dead wrapper names.
- **Agent promotions and text bindings:** `RemoteShots.promote_candidate` (`astrid/sdk/remote.py:2465-2494`) reaches `promote_project_shot_candidate` but has no non-wrapper product caller in the source scan. Text writes have callers in `astrid/packs/shots/cli.py:115-138`, `astrid/sdk/timeline/publish.py:60-78`, and `astrid/packs/rendering/docs/scripts/timeline_document.py:201-220`; reads include `astrid/sdk/render_shot_snapshot.py:32`. Agent owns command-based source/speech binding with retained exact inputs; `rebind_text_binding` is wrapper-only.
- **Agent media-handle lineage:** `astrid/sdk/media_handles.py:431-490` is called by `astrid/sdk/invocation.py:3385-3387`; it reads references at `:469` and calls `client.references.associate` at `:454` for `used_as_input`/`depicts`. This is catalog lineage, but the direct association writer is still rejected; Agent owns the command or explicitly approved producer-artifact seam, preserving task/run idempotency and media authority.
- **Agent/Viewing render settlement:** `astrid/core/execution/generic_host.py:8401-~8520,9631-9639` and `astrid/packs/rendering/shared/runtime_stitch.py:104-158` call `publish_timeline_render`. Agent/Viewing own assemble-to-command conversion; Runtime migration waits for revision-pinned `rendering.render` retry/restart proof.
- **Composition/App viewing:** Composition has no Runtime calls. App `renderRouter.ts` admits `rendering.render` and does not call the retired publication route.
- **No other product callers:** no non-generated Agent/App caller was found for direct project shot/reference mutations beyond the paths above; generated clients, wrappers, and tests remain consumers until replacements are proven.

## Existing tests and handoff

Keep positive semantics in `tests/editing_conformance/test_commit_runtime_m1.py`,
`tests/sdk/test_timeline_script.py`, `tests/timeline/test_authoring_{bundle,media,feedback,shot_composition_migration}.py`,
`tests/packs/video_editing/test_runtime_publication_chain.py`, and the App
provider fixtures. Migrate them only with command coverage; do not weaken them.

Agent owns the missing ordinary, popup, authoring, shot/occurrence/reference,
text-binding, media-lineage, and render-settlement command schemas/captures.
App owns producer conversion, bootstrap setup, zero-traffic tests, and fallback
writer deletion. Runtime retains catalog/immutable reads and rejection guards;
Viewing coordinates render settlement and parity. No compatibility writer or
new DTO is implied.
