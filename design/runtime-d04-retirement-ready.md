# Runtime D04 retirement-ready map

Status: preparation only. This is the minimum later cut for the last live
`publishParentComposition` consumer; it is not permission to remove the route
now. The source basis is Runtime `a5a4f6b11a92ac8f01fbc7941db8a1470337ba9d`
(the requested `tl/integration` refresh), Agent current tree
`c10a301d`, and App current tree `7bb885b6` / tree `065b...`. The current
Runtime route is still live at `runtime_protocol/server.py:573-575`.

## Sequence and ownership

The cut is gated by both sides of the remaining consumer migration:

| Gate | Owner | Required evidence before the Runtime cut |
|---|---|---|
| App D01 | App/Reigh | `dataProvider` whole-parent saves, shot-graph/popup add and swap, and bootstrap use the existing `commitTimeline`/native command path; current-browser journeys pass, including reload/retry and zero legacy POST traffic. D01 rows remain open in `app-writers.md`. |
| Agent whole candidate | Agent/Astrid | `AuthoringCandidateWriter` promotion/publication uses the existing Runtime commit provider path, with CLI/SDK retry, reload, inverse, and rebase coverage. Do not invent an Agent operation name. |
| Agent `clip.set-element` | Agent/Astrid | The existing schema operation (`astrid/core/timeline/schema/edit-command.schema.json:903`) and recipe (`tests/editing_conformance/fixtures/recipe_m2_clip_set_element.json`) are accepted through the normal commit path and exercised by the SDK/CLI journey. |
| Runtime final gate | Runtime | Only after the two product migrations are qualified: remove the POST mutation surface and publish-only implementation; retain reads, restore, closure, bootstrap, F1 occupancy, and F2 non-empty-headless guards. |

Agent's current status still describes the frozen S1 full schema as 48
definitions / 22 operations, with the S2 successor and normal release under
construction. App's current status likewise leaves D01 and the broad Gate 5/6
journey open. Those status facts are why this document names the current
operation/fixture surfaces but does not treat either product as qualified.

The old Runtime consumer map's 16 already-retired operations are deliberately
not re-counted here. This map inventories only the still-live publication
writer and its actual current callers/fixtures. `composition-revisions` is a
mixed route: GET list, GET revision, and POST restore remain valid reads/control
operations; only POST collection publication is the D04 mutation target.

## Actual remaining callers and ports

| Current caller | Owner / row | Replacement and first use | Fixture port | Acceptance |
|---|---|---|---|---|
| App `src/integrations/runtime/dataProvider.ts:282-287` (`publish`) and `:1008-1021` (`saveTimelineAtHead`/`saveTimelineInOrder`); handwritten client wrapper `src/integrations/runtime/client.ts:639-651` | App D01 whole-parent plus shot-graph adapter | Existing `commitTimeline` command session and the existing native command used by the graph adapter. First use is ordinary whole-editor save, then head/in-order save after a reload. The wrapper disappears with the generated operation; it is not a new compatibility writer. | Port `src/integrations/runtime/dataProvider.test.ts`, `dataProvider.parity.test.ts`, `opaqueRootWriters.test.tsx`, and recorded 409 responses to commit responses while preserving positive save/reload assertions. | Current browser whole-parent journey: create/edit/save, lost ACK exact retry, restart/reload, undo/inverse, and a captured request assertion that no POST collection publication occurs. |
| App `src/tools/travel-between-images/components/shotTimelineDataProvider.ts:435-590`, especially `:452+` and `:539-546` | App D01 shot graph / popup add and swap | Existing `enqueueCanonicalShotPublish` becomes the command-session enqueue already used by the adapter. First use is popup add, then popup swap; each must be an accepted native command, not a refusal-only port. | Port `shotCompositionRuntime.test.ts`, `opaqueRootWriters.test.tsx`, popup fixtures, and any `publish_conflict_409.json` response fixture to accepted command responses. | Current browser popup add and popup swap each survive reload and retry, with the accepted closure visible to the next client and no legacy publication POST. |
| App `src/integrations/runtime/createDefaultTimeline.ts:51-81` (`publishEmptyTimeline` calls `:60-80`); ingress callers are recorded in `app-writers.md:43-54` | App D01 bootstrap, distinct from ordinary App save | Existing Runtime `createTimeline` plus constrained `commits.bootstrap` / `commits.adopt_empty_shell` (`runtime_protocol/service.py:1655-1721`). First use is new-timeline creation; it must remain the empty bootstrap seam, not a whole-candidate publish. | Port `createDefaultTimeline.test.ts`, fake workspace runtime tests, and `tests/v10/test_timelines_create.py` bootstrap fixtures to the existing create/bootstrap response. | Current browser create-new-timeline, restart, and exact retry; empty bootstrap succeeds, non-empty overwrite remains guarded, and no collection publication POST is emitted. |
| Agent `astrid/core/timeline/authoring_bundle.py:43-53,1604-1655`; SDK `astrid/sdk/timeline/store.py:298-307` and `astrid/authoring_remote.py:297-324` | Agent whole candidate, including candidate promotion/publication | Existing Runtime `commitTimeline` provider and the Agent's current authoring-candidate abstraction. First use is the normal approved-candidate publication/promotion journey. Keep the candidate model; replace only its legacy transport writer. | Port `tests/timeline/test_authoring_bundle.py`, `test_authoring_media.py`, `test_authoring_feedback.py`, `test_shot_composition_migration.py`, `tests/sdk/test_timeline_publish_connection.py`, and their writer doubles to the existing commit provider. | Agent CLI/SDK whole-candidate journey on current Runtime: publish/promote, lost ACK retry, restart/reload, undo/inverse, and rebase/concurrent disjoint edit. The positive journey must remain positive; a 410 test alone is insufficient. |
| Agent one-time migration `astrid/core/timeline/shot_composition_migration.py:151,1030-1041`; typed surface `astrid/sdk/workspace_client.py:248,434-444` | Agent shot-composition migration, not the ordinary authoring bundle | Existing commit provider with the migration's durable marker/reload/idempotency seam. First use is the explicit legacy-shot/group migration command; do not confuse it with App D01 or invent a new Agent op. | Port `tests/timeline/test_shot_composition_migration.py` and any migration receipt fixtures to accepted command receipts while retaining source-fingerprint, replay, and reload assertions. | CLI migration run plus exact replay, source-change rejection, restart/reload, and zero legacy publication POST. |
| Agent `astrid/sdk/timeline_elements.py:57-71`; typed transport path `astrid/sdk/remote.py:327-409` | Agent `clip.set-element`, separate from whole-candidate publication | Existing schema operation `clip.set-element`; use the current command envelope and commit provider, not a guessed operation name. First use is the element-edit gesture that calls the typed writer. | Port `tests/editing_conformance/fixtures/recipe_m2_clip_set_element.json`, `test_commit_runtime_first_clip.py`, `test_commit_runtime_m1.py`, and the element/SDK response fixtures to accepted command receipts. | CLI/SDK element-edit whole journey: accepted `clip.set-element`, reload/readback, lost ACK exact retry, inverse, and no legacy publication POST. |
| Agent bootstrap/reference fixtures `astrid/sdk/remote.py:480-545` (`create_empty`) and `astrid/core/dev/reference_realm.py:98-99` | Agent bootstrap fixture, not Agent whole-candidate migration | Existing `createTimeline` followed by Runtime empty bootstrap/adoption. First use is `create_empty`; do not route it through candidate publication. | Port bootstrap setup in `tests/v10/test_timelines_create.py` and reference-realm fixtures to the retained bootstrap seam. | SDK bootstrap creates one empty shell, is restart/retry safe, and never depends on the removed POST collection writer. |
| Runtime conformance fixture `conformance/fake-second-product.ts:80,85` and related response fixtures | Runtime conformance owner; fixture-only caller | Existing `commitTimeline` fixture transport. First use is the second-product command conformance run. | Port the fake product's publication response fixture to commit acceptance; retain its read/list/restore fixtures. | Gate 6 raw route test plus positive second-product command/readback run. |

The source inventory also finds direct `service.publish_parent_composition`
seeds in Runtime and Agent tests (`tests/test_shot_composition_runtime.py:284`,
`tests/test_timeline_raw_payload_contract.py:95`, the `tests/editing_conformance`
seed files, and authoring-bundle fixtures). They are fixture/positive-behavior
ports, not evidence of an additional production owner. Preserve their positive
expectations by seeding through the existing command/bootstrap path. Do not
delete them or turn them into expected failures.

For completeness, the remaining direct fixture/transport inventory is:

- Runtime publication/seed or route fixtures: `tests/test_render_historical_admission.py`,
  `test_shot_composition_runtime.py`, `test_spec_reference.py`,
  `test_timeline_legacy_authority.py`, `test_timeline_legacy_occupancy.py`,
  `test_timeline_headless_overwrite_refused.py`, `test_timeline_null_speed_retained.py`,
  `test_timeline_ordinary_http.py`, `test_timeline_commit_port.py`,
  `tests/test_door_routes.py`, and `tests/test_client_parity.py`. The same
  `composition-revisions` strings in history-boundary, commit-route, and
  restore tests are retained GET/restore controls, not live publication
  consumers. `conformance/fake-second-product.ts:80,85` and the Runtime
  generated/template files are covered by the final contract regeneration.
- Agent publication writers/transport fixtures: `astrid/core/timeline/authoring_bundle.py`,
  `astrid/core/timeline/shot_composition_migration.py`,
  `astrid/sdk/authoring_remote.py`, `astrid/sdk/remote.py`,
  `astrid/sdk/timeline/store.py`, `astrid/sdk/timeline_elements.py`,
  `astrid/sdk/workspace_client.py`; `tests/editing_conformance/test_commit_runtime_m1.py`,
  `test_commit_runtime_first_clip.py`, `test_commit_runtime_numeric_move.py`,
  `test_commit_runtime_media_manifest_inverse.py`,
  `test_commit_runtime_occurrence_media.py`, `test_commit_runtime_clip_scalar_fields.py`,
  `test_commit_runtime_opaque_items.py`, and `test_commit_runtime_shared_inverse.py`,
  `tests/timeline/test_authoring_bundle.py`, `test_authoring_media.py`,
  `test_authoring_feedback.py`,
  `tests/timeline/test_shot_composition_migration.py`,
  `tests/sdk/test_runtime_response_conformance.py`,
  `test_timeline_publish_connection.py`, `test_timeline_script.py`,
  `test_capture_source_runtime.py`,
  `tests/integrations/test_c06_public_timeline_visualizer.py`,
  `tests/v10/test_timelines_create.py`,
  `tests/v10/test_domain_cli_projects_timelines.py`,
  `tests/test_timeline_clip_replacement.py`, and the Agent
  `tests/fixtures/runtime-responses/publish_conflict_409.json`. The direct
  `tests/sdk/test_timeline_commit_provider_add_delete_runtime.py`/first-clip monkeypatches
  are retained guard fixtures; they must be updated only when the public
  writer is actually removed.
- App publication/transport fixtures: production/generated surfaces are
  `src/integrations/runtime/dataProvider.ts:282-287,1008-1021`,
  `client.ts:639-651`, `createDefaultTimeline.ts:60-80`,
  `generated.ts:160-167`, and `generated-contract-metadata.ts:7`; indirect
  popup traffic originates in
  `src/tools/travel-between-images/components/shotTimelineDataProvider.ts:435-590`.
  Fixture callers are `dataProvider.test.ts`, `dataProvider.parity.test.ts`,
  `createDefaultTimeline.test.ts`, `opaqueRootWriters.test.tsx`,
  `shotCompositionRuntime.test.ts`, `recordedResponses.test.ts`,
  `fakeWorkspaceRuntime.ts` and its tests, `tests/e2e/local/support/harness.ts`,
  and `tests/e2e/local/direct-journey.spec.ts`. Their positive assertions must
  be ported; route-policy tests and GET/restore reads remain separate controls.

## Minimum Runtime cut when all gates are green

The later implementation should be one deletion/contract regeneration change,
not a new endpoint, compatibility writer, or canonical store:

1. In `runtime_protocol/server.py`, remove the collection `POST` dispatch at
   `:573-575`; keep collection `GET` at `:576-581`, revision `GET` at
   `:591`, and restore at `:594-614`. Update any refusal detail that still
   advertises the removed publication route (including `:705`) to name the
   existing commit path. In `runtime_protocol/door.py:162`, change the route
   token from `GET,POST` to `GET`.
2. In `runtime_protocol/service.py`, remove the live
   `publish_parent_composition` body (`:2725-3106`) and only its publish-only
   helpers: `_validate_published_shot_payload`,
   `_validate_published_text_bindings`, `_apply_published_shot_projection`,
   `_shot_projection_matches_revision`, `_verify_shot_head_projection`,
   `_revision_payload`, `_complete_internal_timeline_payload`,
   `_validate_timeline_track_roles`, `_complete_shot_payload`,
   `_complete_parent_payload`, `_normalize_occurrence`,
   `_validate_media_dependencies`, and `_collect_digest_media`. Verify
   `_revision_digest` has no retained caller before removing it. Keep
   `_revision_id`, `_legacy_timeline_payload`,
   `_record_legacy_timeline_revision`, and `_record_internal_revision`: the
   constrained empty `create_timeline` bootstrap still uses them.
3. Regenerate the normal Runtime contract/client tuple after removing only
   `publishParentComposition` and `ParentCompositionPublication` from
   `contract/openapi/workspace-v1.yaml` (the operation is at `:344-348`, the
   schema at `:1486-1499`). The Runtime generated surfaces to update are
   `packages/python/astrid_runtime_client/generated.py`,
   `packages/python/astrid_runtime_client/contract_metadata.py`,
   `packages/typescript/src/generated.ts`,
   `packages/typescript/src/contract-metadata.ts`,
   `conformance/typescript/generated.ts`,
   `conformance/typescript/contract-metadata.ts`, and
   `runtime_protocol/contract_metadata.py`; the corresponding generated
   operation methods and metadata in Agent and App must be regenerated by
   their own normal release flow. Retain
   `listProjectParentCompositionRevisions`,
   `getProjectParentCompositionRevision`, restore, their response types, and
   the read-side `parent_composition_revisions`/head data. The separate
   `replaceParentCompositionMedia` operation is in the already-retired 16-op
   cohort; it is not a second live D04 writer.
4. Change the stale integrity diagnostic at
   `runtime_protocol/store.py:1982` from `publishParentComposition` to the
   existing `commitTimeline` replacement. Keep `_require_timeline_command`
   and all existing refusal handlers for the other retired direct writers.

The current line-span census is approximately 382 lines for the publication
body, about 390 lines for the listed publication-only validation/projection,
normalization, and payload helpers, and a handful of route/door lines: roughly
775 authored Runtime lines before formatter movement. Generated clients remove
one mutation method plus its operation/schema metadata per normal client; their
exact count is generator-dependent. This is an estimate for review sizing, not
a license to remove shared helpers whose callers have not been re-checked.

Retain all of the following: `RuntimeService` revision list/get/restore;
`TimelineCommitStore` closure validation, persistence, publication, install,
`bootstrap`, and `adopt_empty_shell`; closure/media readers and revision/head
tables; `create_timeline` empty bootstrap; `_require_timeline_command`; F1
tracked-timeline occupancy protection; and F2 non-empty headless overwrite
protection. F1/F2 stay until every consumer is qualified and the route cut is
made in the same gated step.

## Gate 6 evidence and exact commands

The final gate needs both refusal and positive replacement evidence. Raw 410
coverage must include the removed collection POST in
`tests/test_door_routes.py`, `tests/test_timeline_legacy_authority.py`,
`tests/test_timeline_legacy_occupancy.py`,
`tests/test_timeline_headless_overwrite_refused.py`,
`tests/test_timeline_ordinary_http.py`, and the generated-client parity
assertions in `tests/test_client_parity.py`. Keep the current tracked-timeline
F1 tests and non-empty-headless F2 tests; do not replace them with weaker
refusal-only tests. The direct publish positive in
`tests/test_shot_composition_runtime.py` and all conformance/authoring seeds
must be ported to positive command tests.

Required post-D01 checks (not run by this documentation worker):

```sh
# Runtime route/refusal plus command positives, from the Runtime worktree.
/home/user/work/venv-runtime/bin/python -m pytest -q \
  tests/test_door_routes.py tests/test_client_parity.py \
  tests/test_timeline_legacy_authority.py \
  tests/test_timeline_legacy_occupancy.py \
  tests/test_timeline_headless_overwrite_refused.py \
  tests/test_timeline_ordinary_http.py \
  tests/test_timeline_commit_integration.py \
  tests/test_timeline_commit_port.py \
  tests/test_timeline_commit_crash.py \
  tests/test_shot_composition_runtime.py

# Agent whole-candidate/element positive integration, through the central service.
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:agent commit-integration) && \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:agent conformance) && \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"

# App current-browser D01 journey; central service owns browser/live-socket runs.
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:app e2e-harness) && \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:app full-e2e-timeline) && \
  /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

The named suites and `integration:<repo>` target syntax are the repository's
current `suites.conf` entries. The first Runtime command is
the direct targeted command for the later code change; this worker did not run
it because no product code was changed. The browser journey is required for
the current App, and the Agent CLI/SDK journey is required for whole-candidate
and `clip.set-element`; neither can be replaced by a Runtime unit refusal.

## Capability debt that remains OPEN

The following retained capabilities are not deletion proof and must not be
silently folded into D04: text-binding first-use/clear/rebind positive
replacement, candidate promotion, and archive/recover. Existing strict xfails
and open status rows name these gaps (including
`tests/test_shot_text_bindings.py`,
`tests/test_timeline_text_selection.py::test_clear_removes_the_live_binding`,
`tests/test_shot_candidate_promotion.py`, and the open Runtime-domain/e2e
cases). Keep their positive expectations and port them when their named
replacement is decided. This document deliberately names no new Agent op for
those capabilities. A 410/refusal for any of them is not evidence that D04 is
complete.
