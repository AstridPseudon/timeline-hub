# Runtime API surface census (rt-m2-api-surface-census)

Basis: Runtime `tl/integration` at `1f3e64d` (tree `6ef5bb9`), read-only. Sibling callers were grepped in the integration worktrees `/home/user/work/agent`, `/home/user/work/app`, `/home/user/work/composition` (composition has no references to any retired operation). No code, tests or generated files were changed. Nothing was run; every fact below is from reading code and grep.

## Summary

- **26 operations answer 410 on integration** (service-level refusal, mapped in `runtime_protocol/server.py`). Three more document routes refuse only canonical `timeline:` document ids (partial, not counted).
- **Verdicts: 9 REMOVABLE NOW, 17 WAITS.** REMOVABLE means no production caller in any sibling and no non-retirement test caller; see decision D-a for what "removable" should mean, because gate 6 requires legacy-endpoint rejection.
- **Top finding: integration is inconsistent with the 2026-10-20 sequencing decision.** `POST .../composition-revisions` (publishParentComposition) and `POST .../replace-parent-media` are refused 410, but App `createDefaultTimeline.ts:50` and `dataProvider.ts:282,1008`, and Agent `core/timeline/authoring_bundle.py:1572,1607` still call the publish route. The restore commit `da5f44e` exists on a branch but is not an ancestor of `tl/integration`.
- **Second finding:** the UTF-8 text first-use capability is recorded as KEPT in the ledger, but `set_project_shot_text_binding` and `rebind_project_shot_text_binding` refuse unconditionally (`service.py:2783-2789`). It is not live on integration.
- **Verified-read family (part 2):** four read operations, already one dispatch block in `server.py:518-569`. Consolidate internally (one service helper, one route table, one shared error contract). Do not merge the wire operations. The contract declares only 200 and 404 for these reads, but the code can return 409 and 400.
- **Frozen fixtures (part 3):** 4,458 JSON lines in four files plus a 23-line `sources.json`. Every file is read by a test or by `generators/generate.py`. None can be deleted without deleting an oracle.

---

## 1. Retired operations (answer 410 on integration)

Route and enforcement are from the runtime code. `Callers` lists production code in the sibling integration worktrees first, then non-retirement tests, then wrappers. Generated clients (`packages/python`, `packages/typescript`, and the vendored copies `agent/astrid_runtime_client/generated.py` and `app/src/integrations/runtime/generated.ts`) contain every operation, because they are generated from the OpenAPI document; they are not listed as callers.

Retirement sites: `_require_timeline_command` is at `service.py:1604-1611`. Direct shot writers raise `RetiredRouteError("direct shot writes are retired; use timeline commands")`.

| # | operationId | Method and route | Retirement site | Callers | Verdict |
|---|---|---|---|---|---|
| 1 | createTimelineDocument | POST `/v1/projects/{p}/timeline-documents` | `server.py:570-575` (unconditional 410) | Agent `astrid/sdk/workspace_client.py:481` (wrapper); Agent test `tests/packs/video_editing/test_runtime_publication_chain.py:71,225` calls `service.create_timeline_document` | WAITS: publication-chain test moves to publish/commit (D01 Agent side) |
| 2 | publishParentComposition | POST `/v1/projects/{p}/timelines/{t}/composition-revisions` | `service.py:2598-2600`; `server.py:578` | App `createDefaultTimeline.ts:50`, `dataProvider.ts:282,1008`, `client.ts:639`; Agent `core/timeline/authoring_bundle.py:1572,1607`, `sdk/timeline/store.py:301`, `sdk/remote.py:409,1456`, `sdk/timeline_elements.py:60`, `sdk/authoring_remote.py:303`, `core/dev/reference_realm.py:99` | WAITS: App D01 migration to commitTimeline, then the route re-lands (restore `da5f44e`). Broken on integration today. |
| 3 | replaceParentCompositionMedia | POST `.../timelines/{t}/replace-parent-media` | `service.py:2594-2596`; `server.py:593` | Agent `workspace_client.py:451`; CLI verb `timelines replace-parent-media` (`packs/timeline/cli.py:3944`, `core/gateway/help.py:109`, `packs/rendering/docs/SKILL.md:624`) | WAITS: Agent swap bundle (commit replacement) or CLI removal (D-b) |
| 4 | updateTimeline | PATCH `/v1/timelines/{t}` | `service.py:1613-1615`; `server.py:632` | none | REMOVABLE NOW |
| 5 | replaceTimelineClip | POST `/v1/timelines/{t}/replace-clip` | `service.py:1617-1619`; `server.py:635` | Agent `workspace_client.py:569` (wrapper); `sdk/remote.py:1276` already refuses locally; Agent test `tests/test_timeline_clip_replacement.py` (fake transport, behaviour expectations) | WAITS: Agent popup swap / occurrence media swap bundle (10 Runtime xfails) |
| 6 | archiveTimeline | POST `/v1/timelines/{t}/archive` | `service.py:2904-2906`; `server.py:648` | Agent `sdk/remote.py:1608` (`timelines archive`, `help.py:109`) | WAITS: no replacement is named; decision D-b |
| 7 | recoverTimeline | POST `/v1/timelines/{t}/recover` | `service.py:2908-2910`; `server.py:649` | Agent `sdk/remote.py:1615` (`timelines recover`) | WAITS: decision D-b |
| 8 | createShot (timeline-scoped) | POST `/v1/timelines/{t}/shots` | `service.py:2912-2914`; `server.py:630` | none (App `createShot` hooks are Reigh UI, not the Runtime) | REMOVABLE NOW |
| 9 | createReference (timeline-scoped) | POST `/v1/timelines/{t}/references` | `service.py:2921-2923`; `server.py:630` | none | REMOVABLE NOW |
| 10 | updateShot | PATCH `/v1/shots/{s}` | `service.py:3479-3484` (`_update_shot_state`); `server.py:653` | Agent `sdk/remote.py:2342` returns `unsupported_operation` before calling | REMOVABLE NOW |
| 11 | archiveShot | POST `/v1/shots/{s}/archive` | same; `server.py:659` | Agent `sdk/remote.py:2349` (unsupported before calling) | REMOVABLE NOW |
| 12 | recoverShot | POST `/v1/shots/{s}/recover` | same; `server.py:659` | Agent `sdk/remote.py:2356` (unsupported before calling) | REMOVABLE NOW |
| 13 | updateReference (timeline-scoped) | PATCH `/v1/references/{r}` | `service.py:3486-3492` (`_update_reference_state`, `_require_timeline_command`); `server.py:663` | Agent `sdk/remote.py:2257` (unsupported before calling) | REMOVABLE NOW |
| 14 | archiveReference | POST `/v1/references/{r}/archive` | same; `server.py:669` | Agent `sdk/remote.py:2266` (unsupported) | REMOVABLE NOW |
| 15 | recoverReference | POST `/v1/references/{r}/recover` | same; `server.py:669` | Agent `sdk/remote.py:2275` (unsupported) | REMOVABLE NOW |
| 16 | createProjectShot | POST `/v1/projects/{p}/shots` | `service.py:2617-2619`; `server.py:839` | Agent `workspace_client.py:625`; `sdk/remote.py:2335` (`shots create`; CLI `packs/shots/cli.py` exposes create) | WAITS: Agent shots move to shot-group/occurrence EditCommands (M2 group contract) |
| 17 | updateProjectShot | PATCH `/v1/projects/{p}/shots/{s}` | `service.py:2662-2664`; `server.py:800` | Agent `sdk/remote.py:2346` (`shots.update`); Agent `tests/stage1/test_runtime_client_cutover.py:465,758-761,1223-1225` (live expectations) | WAITS: Agent shots migration; those tests will fail on integration until then |
| 18 | archiveProjectShot | POST `.../shots/{s}/archive` | `service.py:2662-2664`; `server.py:805` | Agent `sdk/remote.py:2353`; `test_runtime_client_cutover.py:467,762,1227` | WAITS (as 17) |
| 19 | recoverProjectShot | POST `.../shots/{s}/recover` | `service.py:2662-2664`; `server.py:805` | Agent `sdk/remote.py:2360`; `test_runtime_client_cutover.py:469,763,1228` | WAITS (as 17) |
| 20 | addShotItem | POST `.../shots/{s}/items` | `service.py:2666-2668`; `server.py:812` | Agent `packs/shots/cli.py:181` (`shots add`); `sdk/remote.py:2366` | WAITS: occurrence/shot-group EditCommands |
| 21 | removeShotItem | DELETE `.../shots/{s}/items/{i}` | `service.py:2670-2672`; `server.py:820` | Agent `packs/shots/cli.py:194` (`shots remove`); `sdk/remote.py:2373` | WAITS (as 20) |
| 22 | reorderShotItems | POST `.../shots/{s}/reorder` | `service.py:2674-2676`; `server.py:824` | Agent `packs/shots/cli.py:207` (`shots reorder`); `sdk/remote.py:2411` | WAITS (as 20) |
| 23 | promoteProjectShotCandidate | POST `.../shots/{s}/promote-candidate` | `service.py:2678-2680`; `server.py:816`; store `store.py:1506` | Agent `sdk/remote.py:2375-2396` (`shots.promote_candidate`); tests `tests/stage1/test_runtime_client_cutover.py:955-987`, `tests/stage1/test_generated_client_cutover_regressions.py:116` | WAITS: recorded-command candidate promotion (no D01 step names it) |
| 24 | setProjectShotTextBinding | POST `/v1/projects/{p}/shot-text-bindings` | `service.py:2783-2785`; `server.py:779` | Agent `packs/shots/cli.py:135` (text set); `sdk/timeline/publish.py:180` (voiceover text on the publish path); `packs/rendering/docs/scripts/timeline_document.py:179`; `sdk/remote.py:2452`; test `tests/sdk/test_shot_text_bindings.py` | WAITS: text-source seam. The KEPT first-use capability is refused today. |
| 25 | setProjectShotTextBindingById | POST `.../shot-text-bindings/{b}` | `service.py:2783-2785`; `server.py:786` | Agent `sdk/remote.py:2452-2453` | WAITS (as 24) |
| 26 | rebindProjectShotTextBinding | POST `.../shot-text-bindings/{b}/rebind` | `service.py:2787-2789`; `server.py:790` | Agent `sdk/remote.py:2458`; text rebind verb in `packs/shots/cli.py` | WAITS (as 24) |

Count: REMOVABLE NOW = 9 (rows 4, 8-15). WAITS = 17 (rows 1-3, 5-7, 16-26).

### Partial retirement (not counted)

- `createDocument` (POST `/v1/projects/{p}/documents`), `getDocument` and `updateDocument` refuse only canonical ids and kinds: `timeline:` ids and kind `timeline.composition` (`service.py:3131-3137`, `server.py:700-717`). Generic documents stay live; App `dataProvider.ts:383-451` uses them. KEEP.
- Dead wrappers that only reach these refusals: Agent `workspace_client.py:484` (`update_timeline_document`) and App `client.ts:683` (`updateTimelineDocument`). No callers found. Remove with their generated counterparts.

### Checked and NOT retired (so nobody mistakes them for retired)

`restoreProjectParentCompositionRevision` (commit path, `server.py:597-617`); `listProjectParentCompositionRevisions` and `getProjectParentCompositionRevision` (reads); `getProjectShotRevision` and `getProjectTimelineRevision`; `getShot` and `getReference` (reads of timeline-scoped rows); `renameTimeline` (`service.py:1630`); `createTimeline`; `listTimelineCommits`; `commitTimeline`. The catalog writes `createProjectReference`, `updateProjectReference`, `associateReference`, `linkReferences`, `setPrimaryReference` and their archive/recover are KEPT (RK01). Shot and text-binding GETs and lists are live.

### Decisions this census needs from the orchestrator

- **D-a. What "removable" means.** Gate 6 includes direct legacy-endpoint rejection, and the ledger's refusal tests assert 410 (`test_timeline_legacy_authority.py`, `test_timeline_shot_authority.py`). Removing a route entirely would turn those assertions into 404, which is a rewrite of expectations and is not allowed. Proposal: for the 9 REMOVABLE rows, drop the OpenAPI path and generated client methods (Runtime, plus the vendored Agent and App copies on regen), and keep one generic 410 handler for the legacy family. Needs a yes or no.
- **D-b. archiveTimeline and recoverTimeline** (`timelines archive` and `timelines recover`). No replacement is named in the plan. Remove the CLI verbs, or give them a commit path?
- **D-c. Publish route on integration.** Either merge the narrow restore `da5f44e` now, or accept that App `createDefaultTimeline` and Agent authoring publish are refused until D01. The 2026-10-20 decision says this is a sequencing error that gets restored narrowly.
- **D-d. Text first-use.** Ledger says KEPT; code refuses. Either restore the first-use write narrowly, or record it as lost behaviour with a strict xfail that names the seam.

---

## 2. The verified-read family

### Current operations

All four are `projects:read`, all four go through `_timeline_authorize(..., mutation=False)` under `store._mutex`, and all four detach their input before validating it. Server dispatch is one block (`server.py:518-569`) with a `forms` table; the four public routes differ only in the form and in the function they call.

| operationId | Route | Query (exact) | 200 response | Service method (`service.py`) | Production consumers |
|---|---|---|---|---|---|
| getProjectMediaSelection (resolve) | GET `/v1/projects/{p}/media-selection` | either {asset, generation_id, variant_id} or {association_id, object_id, version (int >= 1)} | MediaSelection {asset, generation_id, variant_id, object_id, catalog_digest} | `get_project_media_selection` (2484) to `MediaReads.selection` | App `client.ts:632` (wrapper); `pairedRoutePolicy.test.ts:394` lists it as a local-door-only op |
| getProjectVerifiedMedia (recheck) | GET `/v1/projects/{p}/media-selection/verified` | all five: asset, generation_id, variant_id, object_id (sha256), catalog_digest (sha256) | VerifiedMedia {selection (5 fields), media_type, size (required), duration_seconds?, width?, height?} | `get_project_verified_media` (2495) to `MediaReads.selected` | none outside generated clients |
| getProjectVerifiedDocument (document by DocumentPin) | GET `/v1/projects/{p}/document-inputs/verified` | document_id, version (int >= 1), content_digest (sha256) | VerifiedDocument {pin {document_id, version, content_digest}, document (Document)} | `get_project_verified_document` (2515) to `read_project_source_document` | none outside generated clients |
| getProjectVerifiedDocumentObject | GET `/v1/projects/{p}/document-objects/verified` | document_id, version, content_digest, object_id (sha256) | VerifiedDocumentObject {object_id, digest, size >= 1, media_type = application/json, bytes_base64} | `get_project_verified_document_object` (2503) to `read_project_pack_object` | none outside generated clients |

Kind rules: the source-document read accepts `*.config` or the project-pack kind (`timeline_commit_port.py:437-453`). The object read accepts only the project-pack kind (`read_project_pack_object`, 493-509). The pin must be in the authorized closure, which is every pin linked by an accepted timeline record in the project, or the live exact version. Failures are `refused(...)` (HTTP 409 `conflict`, `timeline_commit_port.py:90-94`) or `ConflictError` (409, changed digest, `MediaReads.selected`).

The commit path uses the same internals in-process (`timeline_commit_port.py:269-307`: `MediaReads.selected`, `capture_document_input`, `read_pack_snapshot_object`). So the public routes are thin views over the commit port's own readers.

Consumers: no Agent production code calls any of the four (only `astrid_runtime_client/generated.py`). App calls only the resolver, through `client.ts:632`. Nothing outside tests calls the recheck or the two document reads, so changing the internal shape is low risk. The wire shapes are the constraint.

### Problems found

1. **Contract under-declares errors.** Each of the four operations in `contract/openapi/workspace-v1.yaml` (lines 287-332) declares only `200` and `404`. The code can return 409 (`refused`, changed digest, changed pin) and 400 (`ValidationError`, malformed pin or object id). Additive fix: add the shared 400 and 409 responses to all four.
2. **`object_id` means two things.** On the media routes it is the output object digest; on the document-object route it is a pack-object digest. Both are sha256 digests of bytes, so it is harmless. Document it, do not rename it.
3. **Path names are uneven.** `document-inputs` (operation `getProjectVerifiedDocument`) and `document-objects` (operation `getProjectVerifiedDocumentObject`) do not match their operationIds, and `media-selection` (resolver) has no `/verified` sibling in its path. Do not rename; the generated clients pin these names.

### Proposal: one family, compatible

**Merge (internal, no wire change):**

- One service helper, `verified_read(project_id, form, selector, *, authorize, expect)`. It replaces the four near-identical methods at `service.py:2484-2525`. Each caller keeps its own `expect` (`media`, `document`, `object`), and only the verified three map `CommitRejected` through `public_failure`. The resolver's behaviour is unchanged.
- One route table in `server.py`: a single dict from path suffix to `(form, function, verified)` replaces the `forms` branches in the block at `server.py:518-569`.
- One contract section, "verified reads": a shared rule (read-only, `projects:read`, closure-authorized, never refreshes, refuses on any change) and shared 400 and 409 responses. Additive.

**Keep separate (wire operations unchanged):**

- **Resolve vs recheck** (`media-selection` vs `media-selection/verified`). The resolver takes two selector forms and returns the current selection. The recheck takes exactly five fields and refuses on any change. Merging them with a `verified=true` flag flips the refresh semantics, which is breaking. The recheck's input is the resolver's output, so keep them as a pair in the contract description.
- **Media vs document.** Different identity domains (asset, generation, variant, digest versus document pin) and different payloads (VerifiedMedia metadata versus Document content).
- **Document vs object.** Different payloads (JSON Document versus bytes) and different kind rules (`config` or pack versus pack only). Merging them into one route with an optional `object_id` would give one path two response schemas (`oneOf`), change generated client signatures, and is not recommended now. It is additive for old callers, but not worth the risk when no production caller exists.

**Tests that pin these shapes (must stay green):** `test_timeline_verified_media.py`, `test_timeline_verified_media_http.py`, `test_timeline_media_selection.py`, `test_timeline_pack_document_read.py`, `test_timeline_pack_param_retained_read.py`, `test_timeline_commit_contract.py` (`test_verified_document_object_public_contract_and_generated_python_adapter`, `test_verified_document_public_contract_and_generated_python_adapter`), `test_timeline_commit_port.py`.

---

## 3. Frozen schema fixtures

Directory: `tests/fixtures/published-command-schemas/`. Totals: 4,458 JSON lines across the four snapshots plus 23 lines of `sources.json`, 4,481 in all.

| File | Lines | Role | Read by | Deletable? |
|---|---|---|---|---|
| `runtime-0.2.3.json` | 1,330 | The live compatibility floor (`sources.json` points here) | `generators/generate.py:104-116` (gate on every generate run); `tests/test_command_schema_compatibility.py` (default baseline, `test_frozen_fixture_digests`, `test_actual_d13_guard...` and others) | No. It is the floor. Policy: advance only after an authorized publication. |
| `runtime-0.2.2.json` | 729 | Historical snapshot | `test_command_schema_compatibility.py:33-35` (exact-unchanged), `:165-172` (digest), `:185-188` (`test_historical_regex_rewrites_are_not_claimed_as_proven_widenings` expects exactly 5 review-required errors) | No, unless that regex-review test is retired. That is a decision, not cleanup. |
| `withdrawn-10c.json` | 889 | Negative oracle: an Agent schema withdrawn, never a floor | `test_command_schema_compatibility.py:38-48` (lost definitions and operations), `:168` (digest), `:233` (copied into a tmp tree) | No. It is the only proof the gate catches withdrawn shapes. |
| `producer-guard-1bffd.json` | 1,510 | Positive oracle: the Agent D13 guard schema (superset of the floor) | `test_command_schema_compatibility.py:175-182` | No, while the D13 guard test exists. It is the largest file and the only copy of that schema here. |
| `sources.json` | 23 | Provenance index (repo, commit, path, sha256) | `baseline()` in the test; `generate.py:106` | No |

Findings:

- **Nothing is unused.** Every JSON file is read by a test or by the generator. `runtime-0.2.2.json` is read only by tests (and the generator reads only `0.2.3`).
- **Not in the artifact manifest.** `contract/manifest.json` and `contract/artifacts.json` do not reference any of these files. They are gated only by the test and the generator. If the owner wants them audited with the other artifacts, that is a manifest change.
- **Proposal: delete nothing.** Each file is an oracle or the floor, and the rules say snapshots stay immutable. The cheapest real reduction is a policy decision: stop carrying `runtime-0.2.2.json` if the historical regex-review test is retired. That would lose coverage, so it needs an owner decision.

---

## Method and caveats

- Retirement sites were read from `runtime_protocol/service.py` and `server.py`. The OpenAPI document was read for operationIds, methods and paths, not for retirement, because it does not mark retired operations.
- Caller grep covered `astrid/`, `tests/`, `docs/` and `packs/` in Agent; `src/`, `tests/` and `config/` in App; and the Runtime. Composition has no references. The grep is textual, so a dynamic call built from a string could be missed. The Agent `astrid/sdk/remote.py` dispatch table (`remote.py:340-430`) was taken as the full list of dynamic callers.
- The verdict column is a judgment built on the rule in D-a. Rows 1 and 5 have only test or wrapper callers, but those tests encode positive behaviour, so they are WAITS, not REMOVABLE.
- No tests were run for this census. The ledger's run numbers (1020054712) are for tree `0b3be24`, which is older than the current integration tree `6ef5bb9`.
