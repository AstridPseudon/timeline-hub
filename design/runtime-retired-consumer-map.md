# Runtime retired-consumer map

Status: design-only census at Runtime `tl/integration` `642eef7` (2026-10-20).
This is the follow-up to finding 2 in `runtime-review-contract-clients.md`. It
does not remove an operation, change a route, alter a client, or change a test.

## Scope and reading rules

The 16 operations below are already unconditional Runtime refusals (`410
retired_route`) but are still advertised by the Runtime OpenAPI contract and
generated clients. The existing RT05 nine-operation removal is separate and is
left unchanged. A generated method, operation metadata entry, server refusal
branch, or refusal test is not by itself a product consumer.

The classifications used here are:

- **Live production consumer:** an Agent product path can still invoke the
  named Runtime operation (directly or through its SDK family), or a retained
  generated wrapper remains callable by product code.
- **Adapter/fixture only:** the named spelling is present in a high-level
  adapter, test, route-policy table, generated surface, or documentation, but
  the production adapter does not dispatch that Runtime operation.
- **None:** `rg` found no in-tree consumer beyond Runtime’s own compatibility
  refusal/contract surface.

The search covered production and tests in `/home/user/work/agent`,
`/home/user/work/app`, and this Runtime worktree with `rg`, excluding shared
dependency/build directories. Generated clients and the Runtime contract are
listed as surfaces to remove only after the named consumers below qualify.

## Current consumer map

| operation and route | exact current consumers | replacement / capability debt and owner | removal readiness |
|---|---|---|---|
| `createProjectShot` — `POST /v1/projects/{project_id}/shots` | **Live Agent:** `astrid/sdk/remote.py:2335` (`RemoteShots.create`), `astrid/packs/shots/cli.py:170-177`; wrapper `astrid/sdk/workspace_client.py:625`. **Runtime fixture:** `conformance/fake-second-product.ts:57`; positive shot tests are strict-xfail fixtures. **App:** no direct caller; only generated method. | Canonical shot ownership/occurrence EditCommand, including stable IDs and recorded creation. Agent owns the command/provider migration; Runtime owns contract/client removal; App owns any future generated-client refresh. | **Held.** Qualify CLI and `RemoteShots.create` through `/commit`; preserve creation, idempotent replay, project isolation, and the positive conformance scenarios before removing the route/client/`ProjectShotCreate` DTO. |
| `updateProjectShot` — `PATCH /v1/projects/{project_id}/shots/{shot_id}` | **Live Agent:** `astrid/sdk/remote.py:2346`, wrapper `astrid/sdk/workspace_client.py:631`; no current CLI verb. **Runtime fixture:** `tests/test_runtime_p1_blockers.py:230-238` strict-xfail and `tests/test_runtime_e2e.py` shot CRUD xfail. **App:** no direct caller; generated method only. | Canonical shot/occurrence metadata EditCommand with expected-head guards; exact command name is not registered in the current Agent registry. Agent owns the replacement. | **Held.** The original update positive and stale/idempotency behavior must pass through the command path; do not count the current 410 or xfail as migration. Remove `ProjectShotUpdate` only after that proof. |
| `archiveProjectShot` — `POST /v1/projects/{project_id}/shots/{shot_id}/archive` | **Live Agent:** `astrid/sdk/remote.py:2353`, wrapper `astrid/sdk/workspace_client.py:634`; no current CLI verb. **Runtime fixture:** shot CRUD xfail in `tests/test_runtime_e2e.py`. **App:** generated method only. | Shot lifecycle archive EditCommand, if the kept lifecycle capability remains; no named replacement is present. Agent owns the capability decision/command, Runtime owns retirement. | **Held / capability debt.** Preserve archived visibility, idempotency, and recovery semantics in a positive command test before deleting the client method and `ExpectedVersion` use for this route. |
| `recoverProjectShot` — `POST /v1/projects/{project_id}/shots/{shot_id}/recover` | **Live Agent:** `astrid/sdk/remote.py:2360`, wrapper `astrid/sdk/workspace_client.py:637`; no current CLI verb. **Runtime fixture:** shot CRUD xfail in `tests/test_runtime_e2e.py`. **App:** generated method only. | Shot lifecycle recover EditCommand paired with archive; no named replacement is present. Agent owns the capability. | **Held / capability debt.** Require a positive archive→recover command journey and exact replay before removing the operation and its generated method. |
| `addShotItem` — `POST /v1/projects/{project_id}/shots/{shot_id}/items` | **Live Agent:** `astrid/sdk/remote.py:2366`, `astrid/packs/shots/cli.py:180-190`; wrapper `astrid/sdk/workspace_client.py:640`. **Runtime fixtures:** `tests/test_shot_candidate_promotion.py:30-36`, `tests/test_timeline_shot_authority.py` refusal matrix, and shot CRUD xfail. **App:** generated method only. | Recorded shot-item/occurrence insertion command with same-project media selection, stable item ID, and order recording. Agent owns the command/provider migration. | **Held.** Migrate `timelines shots add`; retain the original item/order/media-positive assertions and candidate-promotion setup. Remove `ShotItemCreate` only after all live callers and positive fixtures use commands. |
| `removeShotItem` — `DELETE /v1/projects/{project_id}/shots/{shot_id}/items/{item_id}` | **Live Agent:** `astrid/sdk/remote.py:2373`, `astrid/packs/shots/cli.py:193-200`; wrapper `astrid/sdk/workspace_client.py:663`. **Runtime fixture:** `tests/test_timeline_shot_authority.py` refusal matrix and shot CRUD xfail. **App:** generated method only. | Guarded shot-item removal EditCommand; it must record the selected item/order and preserve media bytes. Agent owns it. | **Held.** Qualify `timelines shots remove` plus undo/replay/order behavior; do not delete positive behavior tests or infer readiness from 410. |
| `reorderShotItems` — `POST /v1/projects/{project_id}/shots/{shot_id}/reorder` | **Live Agent:** `astrid/sdk/remote.py:2411`, `astrid/packs/shots/cli.py:203-212`; wrapper `astrid/sdk/workspace_client.py:666`. **Runtime fixture:** `tests/test_timeline_shot_authority.py` refusal matrix and shot CRUD xfail. **App:** generated method only. | Guarded whole-shot item-order EditCommand with selected membership/order recording. Agent owns it. | **Held.** Qualify the CLI permutation and concurrent/rebase semantics; retain omission/duplicate/extra refusal positives. Remove `ShotReorder` only after the command path owns order. |
| `promoteProjectShotCandidate` — `POST /v1/projects/{project_id}/shots/{shot_id}/promote-candidate` | **Live Agent:** `astrid/sdk/remote.py:2396` (`RemoteShots.promote_candidate`), wrapper `astrid/sdk/workspace_client.py:643-660`; no current CLI caller. **Runtime positive fixtures:** `tests/test_shot_candidate_promotion.py:16,59` strict-xfail tests, plus `tests/stage1/test_generated_client_cutover_regressions.py:116` and `tests/stage1/test_vendored_workspace_client_parity_luna.py:143`. **App:** generated method only. | **Candidate-promotion capability debt.** Replacement must be a recorded command/proposal preserving primary supersession, dependency invalidation, provenance validation, expected-head behavior, receipt replay, and stable IDs. Agent owns the replacement; Runtime preserves the positive tests until it exists. | **Held.** The two original positive tests must pass against the replacement. The existing 410/refusal tests are not completion evidence. Remove `ShotCandidatePromotion` and the generated operation only after the positive replacement is qualified. |
| `setProjectShotTextBinding` — `POST /v1/projects/{project_id}/shot-text-bindings` | **Live Agent:** `astrid/sdk/remote.py:2452-2454`, `astrid/packs/shots/cli.py:126-138`, `astrid/sdk/timeline/publish.py:180`, wrapper `astrid/sdk/workspace_client.py:672-673`. **Runtime fixtures:** `tests/test_shot_text_bindings.py` four strict-xfail positives and `tests/test_timeline_shot_authority.py` refusal matrix. **App:** generated method only. | **Text first-use capability debt.** A text-source EditCommand must store exact UTF-8 bytes/digest, binding identity, expected head, and clear semantics. Agent owns the text-source seam; Runtime keeps the read/list DTOs and refusal coverage. | **Held.** Qualify first-use, non-ASCII bytes, size/UTF-8 refusal, replay, and explicit clear. Never mark complete from the current 410 or from transformed refusal tests. |
| `setProjectShotTextBindingById` — `POST /v1/projects/{project_id}/shot-text-bindings/{binding_id}` | **Live Agent:** `RemoteShots.set_text_binding` selects this operation when `binding_id` is supplied at `astrid/sdk/remote.py:2450-2454`; wrapper `astrid/sdk/workspace_client.py:678-679`. **Runtime fixture:** `tests/test_shot_text_bindings.py` update/replay positive xfail. **App:** generated method only. | Same text-source EditCommand as first-use, with an existing binding identity and expected-head guard. Agent owns it; it cannot be removed merely because the create form is retired. | **Held.** Qualify update-by-ID, exact replay, stale-head conflict, and clear behavior through the text seam before removing `ShotTextBindingSetById`. |
| `rebindProjectShotTextBinding` — `POST /v1/projects/{project_id}/shot-text-bindings/{binding_id}/rebind` | **Live Agent:** `astrid/sdk/remote.py:2456-2458`, wrapper `astrid/sdk/workspace_client.py:681-682`; no current App or CLI direct caller. **Runtime fixture:** `tests/test_shot_text_bindings.py` rebind positive xfail. **App:** generated method only. | Text-source/media-binding EditCommand retaining the binding ID, selected media identity, expected head, and exact source bytes/metadata. Agent owns it. | **Held.** Qualify rebind event/order, expected-head conflict, and byte identity. Keep the positive test until this capability exists; current refusal is not completion. |
| `replaceTimelineClip` — `POST /v1/timelines/{timeline_id}/replace-clip` | **No current direct product dispatch:** `astrid/sdk/remote.py:1276` locally returns `_retired_document_route`; wrapper `astrid/sdk/workspace_client.py:569-580` and generated clients remain callable. **Runtime fixtures:** `tests/test_timeline_clip_replacement.py` strict-xfail positive behavior and `tests/test_timeline_legacy_authority.py` refusal matrix. **App:** generated method only; no call site found. | Recorded media replacement command for popup/occurrence swaps, with exact media selection, timing preservation, dependency closure, undo, and retry. Agent owns the command; Runtime’s direct handler remains a refusal boundary. | **Held.** Translate the original clip-replacement positives to the command path and qualify both popup and occurrence media swap. Only then remove the public operation, `timeline-clip-replacement.json` surface, and wrappers. |
| `replaceParentCompositionMedia` — `POST /v1/projects/{project_id}/timelines/{timeline_id}/replace-parent-media` | **Adapter, not exact dispatch:** `astrid/packs/timeline/cli.py:1286-1295,3954-3957` calls `RemoteTimelines.replace_parent_media`; that adapter reads the pinned closure and publishes through live `publish_parent_composition` rather than calling the named Runtime operation (`astrid/sdk/remote.py:1278-1355`). The exact operation remains in `astrid/sdk/workspace_client.py:451-473`. **App:** generated method plus route-policy fixture `src/integrations/paired/pairedRoutePolicy.test.ts:445`; no production caller found. **Runtime:** refusal matrix in `tests/test_timeline_legacy_authority.py`. | The existing high-level closure replacement is the candidate replacement, but its command-path successor still needs the approved media add/swap EditCommand and M2 qualification. Agent owns the adapter/command; Runtime owns contract removal. | **Held.** Prove exact closure reads, occurrence isolation, publish/retry, undo, and no legacy-document access on the high-level path. Do not call the adapter’s passing `publish_parent_composition` test proof that the generated operation can already be removed. |
| `archiveTimeline` — `POST /v1/timelines/{timeline_id}/archive` | **Live Agent:** `astrid/sdk/remote.py:1602-1608`, `astrid/packs/timeline/cli.py:3959-3963` via `client.timelines.archive`; wrapper `astrid/sdk/workspace_client.py:594-597`. **Runtime positives retained as strict-xfail:** `tests/test_stage1_runtime_contract_completion.py:54-67`, `tests/test_runtime_domains.py:364-379`; refusal coverage in `tests/test_timeline_legacy_authority.py`. **App:** generated method only. | **Archive capability debt.** No approved EditCommand replacement is named for timeline lifecycle archive in current Agent/Runtime docs. Agent owns the capability decision and command; Runtime preserves refusal tests. | **Held.** Do not remove the CLI/SDK operation until an explicit guarded lifecycle command preserves event/history, idempotency, visibility, and recovery semantics. A 410 is not a completed archive migration. |
| `recoverTimeline` — `POST /v1/timelines/{timeline_id}/recover` | **Live Agent:** `astrid/sdk/remote.py:1609-1615`, `astrid/packs/timeline/cli.py:3964-3967` via `client.timelines.recover`; wrapper `astrid/sdk/workspace_client.py:599-613`. **Runtime positives retained as strict-xfail:** `tests/test_stage1_runtime_contract_completion.py:54-67`, `tests/test_runtime_domains.py:364-379`; refusal coverage in `tests/test_timeline_legacy_authority.py`. **App:** generated method only. | **Recover capability debt.** No approved EditCommand replacement is named; it must pair with archive and retain the old head/history semantics through a guarded command. Agent owns the capability. | **Held.** Qualify archive→recover, exact replay, stale head, and history preservation before removing the operation/client method. |
| `createTimelineDocument` — `POST /v1/projects/{project_id}/timeline-documents` | **No live Agent production caller found:** wrapper `astrid/sdk/workspace_client.py:481-482` is still exposed, but current production bootstrap uses `createTimeline`; direct calls are test setup. **Runtime fixtures/refusal:** `tests/test_runtime_domains.py:247-282`, `tests/test_timeline_clip_replacement.py:69`, `tests/test_timeline_legacy_authority.py:84-165`, `tests/test_timeline_render_publication.py`; Agent publication-chain setup `tests/packs/video_editing/test_runtime_publication_chain.py:71,225`. **App docs only:** `docs/extensions/astrid-acp-local-bridge.md:174-176`; generated method/metadata only. | Empty `createTimeline` bootstrap followed by canonical EditCommands/commit; no public whole-document create. Agent owns migration of fixture/setup and docs; Runtime owns operation/schema removal. | **Candidate for removal after fixture qualification, not now.** Convert production-facing examples and positive publication-chain setup to bootstrap+command, retain direct service calls needed to test the intentional 410, and keep the original behavior assertions. Remove `CreateTimelineDocument` only after generated-client parity is updated. |

## Shared Runtime surfaces that must remain

Removing the 16 operations does not mean removing every similarly named DTO.
These schemas are still used by live operations or live read projections:

- `CommittedMutation` is used by current project/timeline creation, rename,
  commit, restore, catalog mutations, object/media mutations, and task/output
  operations.
- `ExpectedVersion` is shared by live project-reference archive/recover and
  other live lifecycle/control operations. Its use by retired shot/timeline
  archive routes is not enough to delete it.
- `ProjectShot`, `ProjectShotPage`, and `ShotItem` remain required by live
  `listProjectShots`, `getProjectShot`, revision reads, and the canonical
  read projections. Deleting shot mutation DTOs must not delete these reads.
- `ShotTextBinding`, `ShotTextBindingPage`, and the list/get binding operations
  remain live. Only `ShotTextBindingSet`, `ShotTextBindingSetById`, and
  `ShotTextBindingRebind` are retired-operation request DTOs.
- `Timeline`, `TimelinePage`, `TimelineRevisionPage`, `ImmutableRevision`,
  `ParentCompositionRevision`, and `ParentCompositionRevisionPage` remain
  live for list/get/history/revision reads and restore/publication inspection.
- `ParentCompositionPublication` remains live for the constrained publication
  boundary. `ParentCompositionMediaReplacement` is retired-operation-only.
- `CreateTimelineDocument`, `RecoverTimeline`, `ProjectShotCreate`,
  `ProjectShotUpdate`, `ShotItemCreate`, `ShotCandidatePromotion`,
  `ShotReorder`, `ShotTextBindingSet`, `ShotTextBindingSetById`,
  `ShotTextBindingRebind`, and the `timeline-clip-replacement.json` request
  shape are operation-specific candidates for removal after the consumer gates
  above pass.

The generated Python/TypeScript clients, operation metadata, OpenAPI paths,
and the Runtime generator template are contract surfaces, not evidence of a
live downstream call. They may be regenerated only as one qualified tuple with
the Agent vendored client and App generated client. Runtime `server.py` and
`service.py` refusal handlers plus their 410 tests stay for the direct legacy
endpoint rejection gate.

## Qualification gate for a future deletion

For each operation, Runtime may remove the advertised path/client/helper only
when all applicable named consumers in the table are gone or emit the one
canonical `/v1/projects/{project_id}/timelines/{timeline_id}/commit` command
path, and the original positive behavior remains proven. The minimum evidence
is:

1. `rg` over Agent/App production trees finds no call to the exact generated
   operation or retired route. High-level adapters must be shown to use
   `commitTimeline`/the approved command path, not merely to return a local
   410.
2. Agent command conformance covers stable references, exact selected media or
   text bytes, explicit clears, expected-head/rebase behavior, idempotent
   retry, undo, and created-ID preservation for the relevant capability.
3. The preserved Runtime positives pass through the replacement. This includes
   shot CRUD/item ordering, candidate supersession/invalidation/provenance,
   text first-use/update/rebind/clear, clip media replacement, and archive /
   recover lifecycle behavior. Existing refusal tests remain separate and are
   not deleted or weakened.
4. Runtime OpenAPI, Python/TypeScript generated clients, operation metadata,
   and artifact hashes regenerate together; Agent’s vendored client and App’s
   generated client/metadata are refreshed to the same tuple. App’s paired
   route-policy test is updated only for the generated inventory change.
5. The operation-specific request DTO is removed only after the shared DTO
   audit above passes. Keep the shared read/projection DTOs and `ExpectedVersion`
   where live operations still use them.

No operation in this map meets all gates on `642eef7`. In particular, text
first-use, candidate promotion, and archive/recover remain missing replacement
capabilities. The current Runtime 410s are intentional safety behavior, not
completion evidence.

## Separate backlog: wrong-project publication status

The pre-existing composition-publication mismatch where a timeline owned by
project A can produce `409` rather than the established project-scoped `404`
for project B is not part of this consumer removal. It is recorded as a
Runtime backlog row in the dedicated ledger; no implementation or test change
is proposed here.

