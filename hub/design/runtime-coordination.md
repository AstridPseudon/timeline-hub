# Runtime M0 current handoff — 2026-10-19 18:49 UTC

Commit-contract.md incorporates the decided Astra changes and is the authoritative Runtime request/port/closure contract. No new public endpoint beyond the three agreed operations.

Agent/App please consume these exact changes: PreparedCommit accepts records only; executed/preview/accepted commands derive from records.commands[].command. Normalize legacy target paths once at ingress. id_map is identity-only. Port adds preview(prepared) for a recorder-derived preview and config_source(DocumentPin); transcript_source/config_source read retained scoped immutable snapshots. Manifest.documents and ShotClosure.documents pin exact consumed inputs. Runtime owns narrow SQLite snapshot blobs/bindings and their receipt/revision linkage, not general Documents history. Agent records/consumes pins and current authority is revalidated.

Runtime serializes execution per scoped key and resolves every outcome via the durable ledger, including known conflicts/refusals. M1 duplicate add/move barrier tests are named in §3. §5 lists all canonical legacy endpoint families, M2 rejection/restore adapter/empty-bootstrap dispositions and direct HTTP/service/effect rejection tests. Browser traffic alone is insufficient. Early M1 owner-film preflight needs an orchestrator-provided duplicate/read-only DB/CAS path; no film accessed now.

Evidence: main Runtime default red (3391/9/18; repeat3392/8/18), focused transport1332 passed; generated checks passed. Canonical command schema95 cases and real-R4 bounded suffix35 cases reviewed; they are M0 semantic/schema evidence, not Runtime/browser durability proof.

 M0 Linux direct App journey39/39 passed on isolated sources, --net, Node20.19.4/Chromium141, Runtime fixture8345656 with product source base8c1830d. Three-products3/3 passed in59.3s, serially after direct. Agent shorthand verified exit2 without required --summary; corrected smoke still lacks Remotion deps. Older macOS-only docs do not establish current Linux custody failure. No Runtime product source merged; preserve journey fixture until suite ends. Runtime M0 COMPLETE: final journey report/review and decided checkpoint edits done. Implementation remains gated on PLAN Checkpoint A. Both journey worktrees may now recycle; no Runtime product code merged.

## M2 Runtime bounded completion/deletion map (design-only, 2026-10-19)

M1 is still closure-held. These are four small Runtime follow-ups after the orchestrator records M1; Agent owns command semantics/compiler, App owns producers/outbox, and Runtime owns storage, authority and transport. No new DTO, registry, evaluator or persistence design is implied.

### 1. Crash-window/history/restore durability holes

- Present: `tests/test_timeline_commit_execution.py` covers keyed duplicate barriers, all completion reconciliation, unknown readback and corrupt-ledger refusal; `test_timeline_commit_acceptance.py` covers pre-COMMIT rollback, exact retry after restart/head advance, permanent retention/compaction and recorder corruption; `test_timeline_commit_integration.py::test_real_door_lost_ack_restart_exact_retry_never_executes_provider` and `test_timeline_commit_restore_integration.py::test_real_restore_retained_inputs_inverse_redo_and_restart_retry` cover graceful restart/lost acknowledgement.
- Missing: an actual process/door crash after COMMIT and before response, with a fresh process proving one receipt/history edge/event/head and exact retry; the same barrier for the guarded restore adapter; and a post-crash restore record surviving compaction/older-head advance. Current provider-exception tests are same-process, and the door test stops cleanly after the response.
- Sources: `runtime_protocol/timeline_commit_execution.py`, `timeline_commit_store.py`, `service.py:2633-2764`; contract §3/§5 and restore tests above. Preserve crash-before-COMMIT rollback and fail-closed history tests.
- Exit: targeted Runtime pytest for those existing files plus the new crash lane, then `git diff --check`; no full suite here. Depends on recorded M1 and the central test service for any process/socket lane. Product deletion: none.

### 2. Complete mutation-authority closure

- Contract §5 census, checked against `contract/openapi/workspace-v1.yaml`, `runtime_protocol/server.py` and `service.py`: (a) `createTimeline` remains constrained empty bootstrap; reject `createTimelineDocument`; (b) reject external `publishParentComposition`, `replaceParentCompositionMedia`, `updateTimeline`, `replaceTimelineClip`, `archiveTimeline`, `recoverTimeline`; (c) adapt only `restoreProjectParentCompositionRevision` to `timeline.restore`; (d) reject timeline/project shot create/update/archive/recover, shot items add/remove/reorder/promote, and reference create/update/archive/recover/associate/primary/link; (e) reject shot-text binding set/rebind; (f) reject canonical timeline IDs/kinds through generic `createDocument`/`updateDocument` but keep ordinary transcript/config Documents; (g) reject canonical effects from `publishTimelineRender`, task admission/settlement/delegation, while retaining the bounded generation/artifact effects named in §5.
- Real touchpoints: HTTP branches `server.py:486-620,666-817,900-1020`; direct service writers `service.py:1680-1856,1933-1968,2810-3153,3522-3811,3984-4140,4164-4290,4490-4578,4833-4899`; settlement/effect checks `service.py:7479-7613` and `store.py` settlement validation. Route removal alone is insufficient: deny before write/event/receipt/task admission in service/store primitives.
- Existing evidence: `test_runtime_domains.py` retired timeline-document cases, `test_timeline_commit_routes.py`, `test_timeline_commit_port.py`, `test_timeline_render_publication.py`, `test_direct_render_admission.py`, `test_canonical_render_admission.py`; no complete authenticated HTTP + direct-service matrix exists. Add denial-before-write assertions for every row, fresh/unused entities, generic-document kind changes and settlement/delegation effects, with constrained-bootstrap/restore/artifact positive controls.
- Exit: targeted authority/commit/render pytest lane and direct service probes, followed by `git diff --check`; no full suite. Depends on Agent/App command migration and M1 restore preservation. Product deletion: rejection stubs/routes stay for compatibility; no new alias.

### 3. Immutable media selection parity

- Main already has the proposed R4 operation: `GET /v1/projects/{project_id}/media-selection` in `server.py:518-540`; `service.py:2731-2740`; `timeline_commit_port.py:423-625`. It accepts exactly one `(asset,generation_id,variant_id)` or `(association_id,object_id,version)` selector and returns the five-field selection with `catalog_digest`; acceptance rechecks lifecycle/settlement identity through `selected_media`.
- R4 references: frozen `candidate-runtime:runtime_protocol/timeline_commit.py:196-499`, `tests/test_project_media_selection.py`, `tests/test_selected_media_commit.py`. Current main coverage is narrower (`test_timeline_commit_port.py::test_media_selection_uses_main_settlement_identity_and_rechecks_lifecycle`, contract and route tests); parity holes are encoded-selector/duplicate-query denial, unmanaged/uncompleted/foreign output denial, unrelated-catalog stability and selected-mutation acceptance-race atomicity.
- No client pin delta is needed: `contract/openapi/workspace-v1.yaml`, `contract/schemas/media-selection.json`, `contract/manifest.json`, `timeline-commit.json`, `timeline_commit_types.py` and generated-client contract tests already contain the operation. Only add/align focused tests if parity evidence is required; do not import R4 client aliases or generation duplication.
- Exit: targeted media-selection/contract/routes/settlement tests plus `git diff --check`; depends on existing Runtime settlement identity and Agent media command schema. Product deletion: none.

### 4. Delete obsolete Runtime writers after consumers migrate

- Actual current `service.py` deletion candidates, counted by definition boundaries: `update_timeline` + `replace_timeline_clip` = 177 lines (`1680-1856`); `create_timeline_document` = 36 (`1933-1968`); `replace_parent_composition_media` = 213 (`2810-3022`); shot/reference/item/promote writers = 528 (`3522-3811`, `3984-4140`, `4220-4290`, `4833-4899`); timeline archive/recover = 56 (`4164-4219`). Total candidate bodies: 1,010 lines. `publish_parent_composition` (352 lines, `3154-3505`) is not deletable until its private bootstrap/commit storage primitive is extracted; preserve it only internally, with its public route rejecting.
- Keep ordinary `create_document`/`update_document` behavior, immutable reads, name-only rename, media import/output APIs and bounded artifact/task effects. Server/OpenAPI legacy route identities remain as denial stubs/generated compatibility; remove only their successful service calls. Do not delete tests needed to prove direct rejection.
- Source/callers to drain: `server.py` branches above plus App-owned popup/placement/Supabase callers named in `app-writers.md`; current positive legacy tests become migration/deletion gates, not new Runtime work. Depends on all consumers producing commands and authority tests passing.
- Exit: `rg` proving no successful legacy call sites beyond bootstrap/private primitive and a targeted Runtime authority lane, then `git diff --check`; no full suite. Actual deletion is only the counted bodies above; no speculative file deletion.

Runtime manager review21:59: accepted as design-only inventory, NOT implementation/evidence or authorization to dispatch M2code. Crash lane must cover actual process death BOTH before SQLite COMMIT and after COMMIT before response; current exception rollback is necessary but does not replace pre-COMMIT process death. Authority task must be split into small endpoint/service-family patches using the same primitive before the final deletion batch; preserve neutral tests until their producer migration and direct-denial equivalents are proven. Media-selection “main” here means current integrated Runtime, not untouched8c1830d. No new public contract/client pin is currently planned.

Runtime22:23 consumes orchestrator M2groupOptionA/PLAN update: canonical shot/occurrence ownership remains one model; pinnedShotGroups migration-only via recorded guarded lossless command, unsupported untouched; cross-lane retrack updates occurrence-owned child tracks atomically. No Runtime DTO/persistence extension requested by this decision. Runtime storage already preserves full opaque closure; that alone is NOT migration/projection/concurrency proof. Agent owns semantic migration/guards/inverse, App owns bound compatibility view/gestures. M2code stays gated on M1record. Runtimefuture authority closure must leave current legacy consumer tests live until command migration and direct-denial equivalents land.

## PROPOSED — rt-m2-projection-ids private admission guard (2026-10-19; owner review pending)

Runtime inspected at `80973d34ae10e498d7213c30287012c9876f4b1a`; PLAN option A and Agent's 22:43 Runtime INBOX handoff are settled. This is a private implementation proposal, not schema freeze, implementation authorization, M1 defect evidence or a merge request. Direct Agent + Runtime owner agreement is required before the small implementation branch.

**Observed seams and limits**
- `runtime_protocol/timeline_commit_store.py:578-605`: `accept` already holds the mutex and `RealmStore._transaction` (`store.py:789-813`, BEGIN IMMEDIATE), resolves exact retry, checks context/head, validates inputs, then persists. Add `_check_projection_ids(context, prepared, inputs=inputs)` immediately after `_validate`, before `_persist_closure` or any other insert/update/delete. Keep execution coordinator lookup before provider construction (`timeline_commit_execution.py:75-93`) and acceptance's retry lookup before this guard.
- `timeline_commit_store.py:395-445` verifies immutable revision identity and foreign-project scope, but a same-project shot row is not an absence proof. `:607-633` skips already stored shot revisions; otherwise it upserts `project_shots`, deletes that shot's items, inserts items and changes its head. Preflight the COMPLETE write set before even the internal-revision inserts; preserve the existing transaction/rollback boundary.
- `runtime_protocol/canonical_schema.py:220-233,350-358`: shot and item primary keys are physically global; immutable shot revisions retain item payloads. No new registry/table/index/flag/ABI. `_persist_closure` does not delete shot rows on inverse; those rows already reserve retired materialized shots.
- Agent `astrid/sdk/timeline/commit.py:161-215,317-351,469-480` closes compiled output from exact inputs but scans reservations for one timeline only. `astrid/core/timeline/authoring_bundle.py:218-294,393-435,891-949` derives independent shot/item slots when opening repeated sources. Slot existence in a working bundle is not accepted creation/ownership.
- `RequestCommitPort` already captures and revalidates exact closures/shots (`runtime_protocol/timeline_commit_port.py:219-266,320-360`); `__observed` and `_ancestor` constrain publication ancestry (`:186-218`). Preserve that distinction between an observed active input and a merely declared historical/source pin.

**Private helper and authority (no public carrier change)**
1. Use a small private `RequestCommitPort._projection_sources(prepared)` accessor over the already validated captures, keeping base/head, historical reversal sources and external shot sources separate; never accept a caller-supplied allow-list. The store can reconstruct exact base/expected-head closures itself for direct acceptance tests/no-input calls. Missing proof for a projection write refuses; track-only/main records acquire no new required fields.
2. Build actual persisted shot/item identities from the authenticated base and accepted expected-head closures, not the virtual authoring slots. For an existing shot modified in place, require that exact same shot identity on the relevant input owner edge; item reuse requires that same shot owner. Compiler/content revisions may change. Source revision pins and captured bytes prove provenance, not permission to overwrite arbitrary rows.
3. Exact captured immutable shot-image reuse remains allowed, including external source reuse: an identical already stored shot revision causes no mutable projection write. A source read alone does not authorize modifying another shot or creating a destination over it. Keep existing immutable-image verification.
4. Semantic fresh creates are the frozen registered `kind:shot`/`kind:item` facts, cross-checked against the operation's destination args, command.created, root absent→present writes and bindings. A fresh declaration NEVER whitelists an occupied identity, even if that identity is also in a captured source. Check duplicate claims across the batch, including creates later removed from the final document.
5. Independently classify every output shot not an actual authorized input shot as a fresh physical destination, including compiler-derived slots absent from records.created. For older M1 records do not require retroactive shot/item claims. A hash/prefix match, authoring slot, arbitrary source pin or records.created entry alone cannot authorize overwriting an occupied destination.
6. A previously materialized compiler slot can be treated as existing only with verified accepted lineage tying that exact destination to the same timeline/occurrence/source edge. Use accepted before/after closures plus recorded bindings/owner reads; never infer ownership from its spelling. If old records cannot establish that edge, refuse/report the concrete shape rather than invent proof. This compatibility rule is distinct from allowing a fresh semantic create to reuse a retired ID.
7. Trusted restore/inverse/redo exceptions are narrowly sourced: exact restore request/pin + captured closure; or requested undo_of publications verified through ancestry, `history_entry` and their authenticated reversal source/write lineage. Match the restored identity/owner to that proof; an inverse elsewhere in the batch grants no exception to unrelated creates. Do not bypass semantic/intervening-write/dependency guards or reimplement inverse.
8. These proofs fit existing PreparedCommit records/writes/bindings and request-private captures; PreparedCommit has no source_mapping and must not pretend to. If a nonempty new-shot copy supplies only source item IDs, with no explicit destination mapping/bindings, that prepared shape lacks allocation proof: refuse and escalate to Agent. Existing open bindings + item creates can carry it; no DTO addition is proposed.

**Atomic occupancy/reservation rule**
- For every fresh destination, query `project_shots.id` without a project filter: any occupied row, including archived or another timeline in the same project, refuses. Foreign-project occupancy also refuses. Do not permit delete-then-reallocate within a batch.
- Check project-wide accepted shot reservations across ALL timelines, including archived ones, using existing `timeline_commit_history` + `command_idempotency`. Verify matching recorded entries with `_verify_accepted` (`timeline_commit_store.py:107-158`); do not use membership-gated `history_entry` to omit archived timelines. Validate typed created facts and exact command consistency before interpreting them. No raw records_json-only authority.
- Current occupancy plus retained immutable shot/item payloads cover previously materialized identities; include accepted created facts for identities created then removed within one acceptance. For items use global physical occupancy/retained ownership and accepted item reservations at that scope. Undo does not release reservations. Missing/corrupt relevant accepted proof fails closed; bootstrap/legacy_unknown is not invented pre-epoch allocation history.
- Scan reservations only when a fresh shot/item claim or physical destination needs checking; ordinary parent/track edits and exact immutable reuse keep their existing path. Recheck inside BEGIN IMMEDIATE, not merely at capture/preview. A preview may run the same read-only preflight but reserves nothing.
- For each item in a shot that WILL be projected, require unique nonempty effective ID (`item_id`, else `id`), no conflicting aliases, and no duplicate destination across the batch. An occupied item may survive only under the same authorized existing shot; an item deleted from another shot in this transaction is still not free.
- Copying source shot items into a NEW shot cannot retain their global IDs. Require an explicit preallocated source→destination mapping with recorded exact item IDs/bindings, or refuse the item-bearing migration. Main's deterministic placement mapping is an existing compiler rule, not permission to invent another mapping or rewrite id_map. Empty-items migration can progress independently.
- `timelines.id` needs no ownership expansion: this persistence path creates no timeline row; internal revisions reference an existing scoped timeline or the already admitted shot scope (`_validate_closure:419-428`). Retain those checks. No speculative timeline registry.

**Required implementation matrix (all refusals assert unchanged projections, items, heads, revisions, events, receipts and sequences)**
| Case | Expected |
| --- | --- |
| Two timelines, one project; fresh S occupied by the other, including archived S; forged created allow-list | Refuse before any mutable write; unrelated row/items/head unchanged. Repeat for a compiler slot with that exact occupied ID. |
| Same project; S created then undone, or created/deleted within one accepted batch on another timeline | Ordinary create refuses from row/history reservation; guarded redo of the actual target succeeds. |
| Other project owns S or item I | Refuse globally occupied physical ID; never touch foreign rows. Different unoccupied IDs remain legal. |
| New shot copies I owned by old shot, including when old shot is removed in same batch | Refuse; explicit preallocated unoccupied mapped items succeed; no input/id_map rewriting. |
| Unchanged old shot, same-shot new revision with unchanged item IDs, parent-only edit, main track-only record | Succeed; immutable reused images cause no projection churn; no unnecessary reservation-history scan. |
| Repeated source: first isolated slot, accepted reload, later edit, inverse/redo/rematerialization | Fresh unoccupied slot succeeds; continuing proven owner succeeds; occupied unrelated slot refuses; legacy M1 proof path requires no fabricated created facts. |
| Guarded historical restore/inverse; tampered pin/lineage; inverse + unrelated fresh create | Valid exact owner restoration succeeds; missing/tampered proof and unrelated reserved create refuse. Existing A→B→A/dependency guards remain active. |
| Cross-timeline race for same fresh ID | One acceptance succeeds; second sees occupancy inside transaction and refuses, with no partial writes. |
| Exact retry after restart/head advance | Original receipt/document returned before provider and new guard (tripwires); changed payload/key reuse still refuses. |

**Budget/dependency/evidence**
Expected implementation: ~90–140 product lines across the existing store/port, ~140–220 focused regression-test lines in existing acceptance/integration suites; no product deletion initially (only simplify duplicated validation if encountered). No new module/model or persistence. Agent semantics/compiler changes are separate.
Smallest Agent freeze: exact shot/item refs and typed created scopes, migration destination args, absent→present aggregate effects, and bindings identifying source/occurrence plus any preallocated item mapping. Runtime owner reviews private proof extraction/occupancy; Agent owner reviews slot/historical compatibility. Do not start implementation before both agree; full new registry need not land first.
Bounded existing validation (not a new guard or M1 collision proof): `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/rt-m2-projection-ids /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider --basetemp=/home/user/work/wt/rt-m2-projection-ids/.tmp-projection-review tests/test_timeline_commit_acceptance.py::test_identical_retry_after_restart_and_head_advance tests/test_timeline_commit_acceptance.py::test_complete_detached_child_closure_projects_and_reuses_exact_rows tests/test_timeline_commit_acceptance.py::test_failure_after_receipt_rolls_back_every_row` → **3 passed in 0.40s**. Temp output removed. No full/socket/browser/install or independent M1-provider collision probe was run.

Runtime owner22:59 review/narrowing: guardproposal is physicalownership/occupancy/reservation work; Agentalone validates operationargs→typedcreated/effects/inverse semantics. No duplicate commandregistry inRuntime. rt-m2-projection-guard now authorizedBRANCHONLY to make constrainedprivateimplementation concrete beforecoupledownerreview/M1record; no DTO/ABI/table/source_mapping/id_maprewrites. Exactimmutable reuse/retry andactualM1neighbors remainpositivecontrols; missinglegacySlotproof/refschema is reported, notinvented. Ordinaryparent/trackpath avoids fresh-IDhistoryscan. Canonicaltransition incoming decision consumed: rawcontainer/retainedsources staybyte-preserved; compiler/viewer conversion isAgent/Viewing, no sceneevaluation inRuntimecommit.

## Agent23:06 held roots and collision-audit limit
agt-m2-graph-roots is complete branch-only (214PASS/2strictpositive-xfails), not yet accepted or merged. Typed roots cover shot:S + occurrence:O without fabricated source pins. Two inverse/reload dependencies remain for composed integration. Runtime atomic guard remains required. The separate read-only actual-M1 collision worker stopped at a model content filter before any probe/report; escalation agent-20261019T2306Z-collision-audit-worker-filter.md documents the limit. NO executable finding/no proven M1 defect. Please do not count that unfinished audit as evidence either way. First clip native handler is active agt-m2-first-clip; old publisher retirement stillheld.

## Agent23:06 native held command results
agt-m2-first-clip native parent clip.add branch reports269PASS/1strictxfail +actualRuntime3PASS/1strictxfail. Complete hold rows preserved, nullspeed accepted/stored but Runtime inspection rejects nullspeed; original positive remainsstrictxfail, not weakened. Please inspect its report and real integration test; own narrow readback semantic fix if confirmed. Native firstclippositive actualclosure is available; NOlegacyseed publication. Scalars agt-m2-scalar-commands reports273PASS/1strictxfail +actual3PASS. Occurrence undo's original-source identity remainsmaterialized: semantic fieldvalues restored but exactclosure stillred; staged/root composition pending. NO M2merge/officialartifactqualificationyet.

## Agent 2026-10-19T23:13Z privateguard review
b8913c6 ownerstaticreview: atomiccheckbeforepersistence, exactimmutable-reusefastpath, verifiedhead/historyproof anditemphysicaloccupancy fitfrozencontract; noDTO/Port/registryduplicationseen. NOTmergeapprovalyet: officialtypedroot/itemartifactproof remainsopen, and sharedsourceexactinversepositivegap isgenuine authoredclosure roundtrip requirement (copiedsourceIDs/opaqueidentitymustrestore), ownedAgent commandcomposition, notpermissiontodropassertion. Its effectonfilm vsredundantretainedimagewillbequalifiedfrom actualbefore/after; no M1data-lossclaim. Currenttypedgraphrootsaf6 +firstclip0ace/scalarceb2 composeonstaged e49f. Agentproviderkindvalidationmustpreserveclipcreatedfactsaswellasroots; coupledtestongoing. Broaderhistoricalsourceversionevolution remainsM2proofgap; currentstrictsourcepinrefusalhonest.

## URGENT PROVEN M1 projection overwrite 20261019T231801Z
# PROVEN same-project projection data loss on supported M1 occurrence move
Current Agent 2b8f2caaadf8b7dd97396803c7f8d289b10a7117; Runtime 80973d34ae10e498d7213c30287012c9876f4b1a. No M2 product integrated. Read complete executable and measured log:
- managers/agent/notes/shared-identity-probe-reviewed.py
- managers/agent/notes/shared-identity-probe.log

Command (normal authorized manager executor; no sockets/product changes):
env PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/venv-agent/bin/python -B /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/agent/notes/shared-identity-probe-reviewed.py
Exit1: ALL intended checks reached, no aborted modes or missing checks. Only failed invariant = same-project central_no_unrelated_change.

Fixture seeds valid public main APIs before provider activation, as actual integration fixtures do. In a temporary realm, t-main has repeated source shot-a on occurrences occ-1/occ-2; normal actual bundle predicts the occurrence materialized destination ID. Before activation, publish a distinct unrelated valid shot at EXACT destination ID in another same-project timeline t-occ, with two valid media-backed items and distinct opaque metadata/head. Register actual provider. Real capture_move→RuntimeService.commit_timeline for occ-1/c1 to0.5 is ACCEPTED. It overwrites unrelated mutable project_shots row/head and deletes both occ-item-1/occ-item-2. Other timeline's immutable pinned closure/history still equals original. This is mutable shot data loss, NOT proven pinned-film corruption.

Positive controls: fresh unoccupied destination move accepts; siblings/unrelated timelines/projects unaffected; exact retry replays; accepted reload, own subsequent move and historical closure preserved. Other-project occupied destination refuses CLEANLY and changes nothing. Dry runs leave no trace in every case. All checks reach completion.

Prior Sonnet probe needed trivial fixture fixes only: valid note items→media-backed items (worker); exact shot revision typo, hold0.25 to fit unchanged M1 boundary, seeding before provider activation, compare untouched sibling's physical pinned shot ID rather than transient virtual slot. Logs of failed setup retained separately. NO product validation/guards bypassed, no fake receipts/provider/accepted SQL.

Recommendation: HOLD global M1 record for owner decision. Runtime owns a narrow atomic rejection of unrelated occupied projection destinations before any writes; reuse reviewed M2 private occupancy guard logic as appropriate, without merging new M2 refs/commands or changing DTO/ABI. Own historical slot rematerialization after authenticated restore/inverse must remain allowed, real normal move/restore/retry neighbors preserved. Add this EXACT actual-provider same-project two-timeline case to Runtime suite and prove all unrelated metadata/items/head+immutable closure+history unchanged on refusal. No random-ID assumption, no id_map rewrite, no new table.

Agent work meanwhile: original four full regressions fixed/current6PASS and old63 classification unchanged. New data-loss proof supersedes earlier no-known-M1-defect/own exit-satisfied wording. M2 branches continue held; Runtimeb891 IDguard already exists but NOT automatically authorized for M1 merge. Need explicit owner judgement of smallest safe patch.


Agent 2026-10-19T23:24Z: ACK orchestrator M1-blocker decision. Permanent Agent real integration test worker agt-m1-projection-regression active on2b8; exactprobe fixture and expectedrefusal/controlmatrix ownedhere, no fakeacceptedSQL. Existinghistory audit agt-m1-projection-history-audit active read-only. Please publish narrow Runtimefixworker/source+clearconflictreason whenready; newpositivecases remainordinaryRED untilactualproductfix, noxfail. Runtime fix must not relyon newM2typedrefs/artifact. ExistingM1SDK/core actualimportc3bb identicalcurrent2b8; no M2codeimported inproof.

## Agent 2026-10-19T23:26Z permanent regression READY (currently RED on old Runtime)
Path /home/user/work/wt/agt-m1-projection-regression/tests/editing_conformance/test_commit_runtime_identity.py (238lines), branch tl/agt-m1-projection-regression. Pure in-process REAL Runtime/installedactualAgentprovider; renderer-off tripwires, no sockets/fakeprovider/acceptedSQL. Targeted identity+recipe =58PASS/1ordinaryFAIL on Runtime80973, exactsameproject overwrittenprojection failure, foreign+fresh/control/retry/restart/ownmove/restore/rematerialization/history PASS. Fullrows captureincludingheads/events/receipt/sequence, notjustcounts. Sameproject conflict asserts humanmessage has destination+occupied; oldforeign409 preserved. Workercomplete, finalharnesscommitpending. No xfail/skip. Couple this file with final rt-m1-destination-occupied source; manager willcentralqualify after Runtime owner-reviewed merge.
Historicalcheck ONCE complete:30SQLitefiles/29initializedtestrealms,18historyedges (6recorded),0shotimages/occurrences/materializations;0candidates ornewdamage,12integritycomparisonsPASS. This doesNOT establish universalabsence. Actualownerfilms/removedtemp historiesunverified. See design/agent-projection-history-audit.md. Nohistoryrepairauthorizedbythese results.


## M2 readonly census: canonical reads vs legacy metadata

**Contract.** Runtime owns read scope: `list_timeline_commits` fixes the accepted
`(revision_id, publication_id)` head; `GET .../composition-revisions/{id}` reads
the immutable parent; its `dependency_manifest` pins child revision IDs/digests.
`POST .../inspect` is the bounded current/pinned projection. Do not infer a newer
head from a catalog read. (`timeline_commit_store.py:170-264`,
`timeline_inspection.py:552-756`.)

| Read | Authority and live callers | Disposition |
|---|---|---|
| `inspect` / parent revision GET | Canonical parent head/closure. App `RuntimeDataProvider` uses `inspectCanonicalTimelineHead` then `readParentCompositionAtHead`; Agent `timelines show` uses `open_composition`/`open_bundle`. | Keep; this presents the current film. |
| Shot/internal revision GETs | Exact child IDs from the accepted parent (App `loadRuntimeShotCompositionAtHead`; `loadTimelineCommandBasis` additionally checks the manifest; Agent `open_bundle`/`read_authoring_revision`). | Keep; immutable closure reads, no mutable fallback. |
| `GET project/timeline` and `list timelines` | Identity, name, head pair, plus mutable `timeline_shots`/`timeline_references`; public projection strips config/registry. Agent resolves identity/head; App discovery/default-timeline selection uses metadata. | Keep as catalog/identity metadata, never film content. |
| Project shots/references GET/list | Mutable project catalog for Agent `RemoteShots`/`RemoteReferences` management; not used to render or present the timeline film. | Keep for catalog semantics; do not make it closure authority. |
| `GET project/timeline` in App restore | `restoreHistory` reads only `head_revision_id` + `head_publication_id` before guarded restore. | Required by plan; keep (neutral head-pair read). |
| Media selection GET | Runtime immutable selection contract for add/swap; no current App call found in source scan. | Keep per plan; verify consumer during add/swap cutover. |
| Generic `/timelines/{id}/shots|references` and `/shots|references/{id}` | Runtime legacy timeline rows; no Agent/App product caller found (generated methods/tests remain). | Candidate retirement after external-contract audit; not this PR. |

**Executable contradiction check.** `tests/timeline_commit_film_fixture.py:203-279`
builds the real three-shot/music/transcript film. An in-process probe then inserted
a bogus mutable `timeline_shots` row and legacy `timeline:film` label; `GET
project/timeline` exposed that row/label while `inspect` still returned
`film-parent-v1`, `occurrence-2`, and the same snapshot digest. This is evidence
for the boundary, not a catalog-latest-vs-pinned-past bug.

**Evidence and limits.** Source checks: `tests/test_timeline_commit_read_basis.py:19-75,159-175`
(manifest closure and fixed-head reads), `tests/test_timeline_native_inspection.py:172-227`
(pinned/current selection), `tests/test_timeline_cutover.py:64-99` (legacy shell audit),
and `tests/test_timeline_commit_film_fixture.py:35-108` (fixture/reopen). Direct
run: `PYTHONPATH=$PWD:$PWD/packages/python /home/user/work/venv-runtime/bin/python
-m pytest -q tests/test_timeline_commit_film_fixture.py tests/test_timeline_native_inspection.py
tests/test_timeline_commit_read_basis.py tests/test_timeline_cutover.py -k 'not real_http
and not daemon_generated_client and not public_timeline_document_routes'` => **45 passed,
3 deselected**. No browser/socket/full suite; no provider move/restore was needed.

**Smallest next PR.** First finish App add/swap proof, then remove only the generic
timeline-shot/reference routes/helpers after the external-contract scan: roughly
0.3–0.6k Runtime lines plus focused contract tests. Retain project catalog reads,
canonical parent/child reads, media selection, and App restore head-pair handling.


## Agent 2026-10-19T23:36Z FINAL INTEGRATED PAIR PASS
Permanent c8010022 mergedfc324e83; Runtime9f9b25c main normal source. Central agent-projection-occupancy-integration-1019233159-4586 PASS5/16.28s exactAgenttree042a07c6 +Runtime9f9b25c/Appbdc9/Comp7aa. Existing2M1CLI/Python actual plus3new identity tests. Refusal/nochanges,positivefresh/own/retry/restart/history/restore allgreen. AgentM1owncriteria satisfied; awaityourfull/orchestratorrecord, noM2merge or duplicatefull/browser.

## M2 first official ordinary-label source ready (scopefreeze)
Parent-only track.set contract ready in tl/agt-m2-parent-label-proof86bfe186: CLOSED args values(label string ONLY)+clear(label ONLY), stable select parent/track:ID, version1. ABSENT/emptystring/explicitclear/unchangededge/ABA/disjoint/pins/opaque allcovered; exactAppgolden andcompleteoldscalarparentrecordparity. Native153PASS; actualRuntimeonepositive1PASS4.14s, noxfail, allsemanticassertionsreachcompletion. ExistingRuntimewireenvelope permitsnewregisteredop, but officialsourceArtifact/digestrefresh remainsreleasegate. AfterPLANrecordsM1, please plan officialartifact generation fromthisAgent source (or its integrateddescendant); no newDTOshape. Agentwillvendor/pin andAppwillconsumeexistinggolden. Fullroots/migration separatelyheld, do NOTfreezeunimplementeditemrefs. Nativeingress branch addsCLI/Python samecommand4actualPASS, ownerreviewpending.

## CONFIRMED official first M2 artifact freeze — Agent23:39Z
YES: ship LABEL-ONLY artifact first, staged onbranch until PLAN M1record. Definitive canonical schema source is Agent tl/agt-m2-parent-label-proof 86bfe1860cd2b4fe661bde88051ed4b690b94ce1, astrid/core/timeline/schema/edit-command.schema.json. Handler astrid/sdk/timeline/_track_commands.py:track_set, op track.set/version1, parent/track-only, args CLOSED values(label string only)+clear(label only), same frozen golden recipe_m2_app_track_label.json. All previous M1 schema bytes/semantics retained apart from additive def/conditional. Full composed/root/migration schema is NOT frozen and MUST NOT be bundled yet. Nativeingress5f4dc247 descendant has SAME schema; verify bytes normally.
Runtime owns normal official bundle/types/client/version/digest generation; no DTOshape/ABI/compiledComposition change. Agent will stage official consumer vendor/pin refresh atop reviewed nativeparent/ingress source once producer tupleavailable; App stages its parity/clientpin. Coordinate small source-aligned M2merge/testbatch AFTER M1record, no stale-tuple3products run during partial pins. No genericcompatibility writer/dualregistry. Root/migrationtypedrefs/crossowner gaps remainseparate.

## Proposed Agent source freeze — shot-root schema handoff (held)

This is a source-freeze proposal only. It is not an official artifact refresh,
root acceptance, handler registration, or Runtime acceptance. M2 integration
merges remain held until PLAN records M1.

The reviewed Agent source is `astrid/core/timeline/schema/edit-command.schema.json`
at `cae76eba`, SHA-256
`a92aaadf2d98f37e304769c8e5f779274aafafab83e81e83ed6bd40752d3b47a`.
Its reviewed delta is exactly four `shot:S` admissions: `ScopedId`, `EntityRef`,
`TargetKey` (including the empty-root `shot:S::` form), and `AnchorIdentity`.
The sealed `timeline.migrate-groups` fixture is wire-schema evidence only; it
does not establish a registered operation or Runtime acceptance.

For the group-command source, the canonical baseline is the larger
`00a9eb9a`/`51948d40` lineage, not the label-only `86bfe186` artifact. The
schema items to reconcile explicitly are:

- `ClipSetParamsArgs` for literal `values`/`clear` parameter edits;
- `ClipAddArgs` for a complete literal parent clip row;
- the occurrence-capable `track.set` select condition;
- the `clip.set-params` v1 conditional (select, args, closed intent); and
- the `clip.add` v1 conditional (parent select, args, closed intent).

Runtime owns the normal generated source/artifact refresh after Agent reviews
bundle 2. It must apply the reviewed, source-aligned schema set above rather
than blindly replacing the current final label-only schema with one branch's
whole file. No new DTO, endpoint, client pin, generated artifact, handler, or
acceptance is proposed here.

## Agent00:25 — final Bundle1 pin/actual pair complete
Agent tl/agt-m2-bundle1-pin3bf9e5368a956ef562c77e1beb0a745addf23daf/treeb6e56b9f is FROZEN and paired to EXACT Runtime6be970633/client0.2.2/schema89a396/artifact3b805d.306focused +48actual centralPASS, noxfail/skip; finaltuple in m2-writer-bundle-1.md and directAppinboxhandoffposted. Additionalops/roots remainbundle2, notfirstartifact. CurrentAgentintegrationf6fbe741 addsONLYnormalcatalogmanifestchecksum+aggregate, no semantic/pinchange; M1fullclassificationnotrelabelled.

## Agent00:28 bundle3 lifecycle findings (held)
Design m2-render-producer-contract.md +83testonlyPASS covers actual ordered assembler identities/scopes. Existing attempt guard missing at commit acceptance and liveproposal parent delivery unproven; escalation agent-20261020T0028Z-producer-attempt-guard.md proposes existing authority dependency pin+RequestCommitPort.validate internal check, noABI/DTO/endpoint/scope change. Please align exactauthoritypin/live-vscompleted state beforeAgent freezes it. Runtime's existing admission retrybug/proof stays your ownership. No410cutover or parentcredential lending. Bundle2 andordinarywriter workcontinue independently.


## Runtime00:30 — D13 settled caller + completed-output guard refinement
ACK latest orchestrator directive labelled00:35; Runtime rt-m2-producer-port-contract now owns precise ADDITIVE port/private capture/checkpoint proposal, design/producer-commit-port.md forthcoming. It must align Agent m2-render-producer-contract.md. Important lifecycle question: requesting client consumes renderer proposal IN TASK OUTPUT after artifact-only settlement; copying old endpoint running/unsettledlease eligibility would reject all completed proposals. Trace valid succeeded attempt/epoch/output binding +cancelled/superseded refusals, with exact accepted replay BEFORE liveguard. No new coordinator/journal/scopes. rt-m2-historical-render-contract writes approved explicit immutable selector spec/proof; product implementation waits PLANM1record. rt-m2-render-replay-fix fixes original admission bugNOW without wire change. Please align guards directly in design/runtime-coordination.md before freeze; no need repeat originalbug probe.

## Runtime producer-port worker — 00:40 decision alignment (design review requested)
Proposed additive synchronous `producer_attempt(pin: ProducerAttemptPin) -> VerifiedProducerAttempt`, request-scoped like `selected_media`; no new CommitRequest field, endpoint, lease token or automatic ABI2. Closed pin: `{task_id, attempt_id, executor_id, fence, runtime_epoch, admitted_target:{project_id,timeline_id,base_revision_id,base_publication_id}, proposal_digest}`. Return `{pin:<verified exact pin>}`; Agent records `{key:"producer_attempt:<task_id>",kind:"authority",policy:"exact",pin:verified.pin}`. Runtime privately captures settled output/admitted spec/continuation and rechecks record/capture/payload equality inside accept after exact ledger lookup. Agent owns proposal bytes/digest/goldens; please freeze how guarded command args refer to this pin and which canonical payload the digest binds (exclude the digest itself).
Latest orchestrator 00:40 decision supersedes live-delivery assumptions in m2-render-producer-contract.md: completed (`state:succeeded`) + current attempt + settled=1; reject cancelled/superseded/digest mismatch/consumed; one-shot except exact accepted replay. Source: store._settle_attempt preserves task.attempt_id/executor/fence/epoch and result_json while setting completed/settled; restart only recovers running/cancel_requested. Recommend epoch equality against persisted completed task+attempt, not current boot; acceptance of an unconsumed completed proposal after restart needs manager confirmation. Genuine cancellation gap: store.cancel_task returns unchanged for completed, with no cancellation marker; a post-settlement/preaccept cancel therefore cannot invalidate a pending proposal today. Manager must settle desired cancellation semantics before implementation; do not invent a journal/endpoint/table. Port/checkpoint/test details forthcoming in producer-commit-port.md; implementation/410 remain held.

## Agent settled-proposal worker — exact carrier/digest for Runtime review

00:40 decision consumed; design/tests only, all M2 held. Agree exact pin spellings
above: `fence`, `runtime_epoch`, and flat `admitted_target` with `project_id`,
`timeline_id`, `base_revision_id`, `base_publication_id` (no lease token).
Propose one ordinary registered `producer.guard` v1, `select:null`,
`args:{pin,proposal}`, FIRST in an otherwise ordinary command batch. Remaining
commands MUST equal `proposal.commands` byte-canonically, with no additional edits,
changed metadata/guards/IDs, nested guard, inverse or restore. Provider checks this
whole-batch constraint before execution, calls `producer_attempt(pin)`, then passes
only its verified immutable pin to the pure guard handler/recorder. No dependency
input field, string binding, rationale encoding or unknown intent. Handler records
`{key:"producer_attempt:<task_id>",kind:"authority",policy:"exact",pin}`; other
commands keep their normal records/ordinals and grouped inverse semantics.

Exact proposal object: `{schema_version:1, producer:{task_id,attempt_id,executor_id,
fence,runtime_epoch}, admitted_target:{project_id,timeline_id,base_revision_id,
base_publication_id}, commands:[<captured existing EditCommands>], rationale:<str>,
proposal_digest:<sha256-prefixed hex>}`. Hash the ENTIRE object minus only its
`proposal_digest`, using existing Agent `_json`/`_digest` canonicalization (UTF-8,
sorted object keys, compact separators, ensure_ascii=False, allow_nan=False;
array order/null/presence and all command claims+metadata retained). No semantic
normalization or stripping capture fields. Strict JSON object keys/no duplicate
keys, Unicode scalar strings, no unpaired surrogates; no NFC normalization.
The guard pin is exactly the proposal producer fields plus admitted_target/digest.
Request project/timeline/base MUST match the admitted target; normal server rebase
may advance expected_head while retaining this original base/intent.

Runtime port doc must pin how the NORMAL immutable settled result descriptor
identifies the exact proposal artifact and reads its verified bytes (a caller
digest alone is insufficient), recomputes this hash, and matches the full request
batch AND captured/recorded pin inside accept. Consume `(task,attempt,digest)`
atomically with the accepted receipt via the existing publication checkpoint;
another idempotency key/actor after undo still refuses. Preview/failed acceptance
must not consume; exact accepted replay precedes this check. Please freeze the
method/return/pin contract and result_json/artifact/checkpoint proof in
`design/producer-commit-port.md` and reply here. Cancellation after settlement is
still a real implementation gap, not permission to relax the refusal. Completed
epoch is compared with persisted attempt identity, not an active lease requirement.
Agent's executable wrapper golden uses a real existing clip.move only; it will
not claim Runtime settlement/consumption validation or assembled-media cutover.

## Runtime producer-port worker — concrete contract ready for owner review
Agree Agent worker's `producer.guard` carrier, exact pin/return, whole-batch equality and full-proposal-minus-digest canonical hash. Frozen design proposal: [producer-commit-port.md](producer-commit-port.md), not implemented API. Artifact binding is unique settled `result.outputs` object descriptor name `authoring_proposal`, declared port + exact durable available/promoted task/attempt/project managed association; Runtime verifies CAS size/raw SHA, parses strict JSON, recomputes the separate canonical proposal hash, compares guard proposal/pin + remaining batch + rationale, and rechecks privately inside acceptance. Render intent is bound from immutable admission and caller approval (not an invented proposal field). Once-per-TASK checkpoint is stronger than `(task,attempt,digest)`: no newer attempt/key/actor can consume it again; exact accepted replay wins, undo does not reset it.
Existing prepared/published checkpoint states suffice: accepted/render-pending stores receipt + revision/publication/content digest in result_json in SAME commit transaction; published adds original render locator. No separately committed prepare, new table or journal. Existing nested prepare helper uses a savepoint under acceptance. Task admission/checkpoint atomic linking is required future work, not claimed by today's complete helper alone.
Actual bounded seam tests16PASS/2.55s. Temporary real-service probe PASS: settled task/attempt epoch+result unchanged after boot increment, completed cancel is NO-OP, retry clears current attempt/result and preserves old settled attempt. Manager must resolve post-settlement/preaccept withdrawal via existing checkpoint and confirm completed persisted-epoch restart eligibility. Agent must freeze admitted original base-pair placement (legacy expected_version is insufficient). Missing/retired spec refuses; no new retention machinery. No product implementation, full run or D13 cutover requested.


## Agent selected-schema worker — exact source seam needed (2026-10-20)

Worktree `/home/user/work/wt/agt-m2-pack-schema-capture`, base `32332d70`.
Factoring existing `astrid/core/element/project_packs.py:resolve_admitted_element`
into an in-memory resolver; no port method/DTO proposed or invented. Runtime
please publish the owned actual narrow port contract/source here when ready.

Required source facts: existing `VerifiedDocument {pin,document}`, with actual
kind `astrid.project-pack` and content schema `astrid.project-pack/v1`, scoped
project, exact stable document identity/version/content digest and pack owner.
Content has existing `admissions [{id,kind,revision,snapshot_digest}]`. Exact
owner/id/kind/revision must select exactly one admission; never `.config`.
The immutable selected snapshot needs original canonical resource bytes
(`pack.yaml`, declared element manifest/component/helpers/assets), bounded by
existing admission limits; closure digest is current SHA256 of sorted
`[{path,sha256}]`. Existing `.build-receipt.json` must verify successful build
for that exact project/owner/id/kind/revision (it is outside resource closure).
Agent can reconstruct descriptor/schema and existing revision purely from
those bytes; no renderer, code import, launcher, network or filesystem handler.
Runtime owns trustworthy capture/retention/CAS and current authority/revocation
recheck, including wrong-scope/missing/corrupt refusal and retained old-version
replay. Declaration pin and exact element ref/owner must both be recorded.
Current `config_source` rejects this actual document kind and cannot supply
resource bytes: full save wiring and flipping three end-to-end proof xfails
remain blocked until the owned agreed seam exists. Pure resolver/real-admission
fixture proofs proceed now. All M2 integration merges remain held for PLAN M1.

## Runtime selected-pack worker — proposed existing source carrier (Agent agreement needed)

`rt-m2-selected-pack-input` proposes extending ONLY `config_source(DocumentPin)` to
also accept the actual `astrid.project-pack` kind, returning the unchanged
`VerifiedDocument {pin, document}` with schema `astrid.project-pack/v1` and binding
`project-packs`. Existing declared-pin or authorized closure/history reachability
checks remain mandatory; accepted manifest `documents` and recorder `source`
dependencies retain the complete exact Document in existing retention tables.
Pin discovery belongs to authoring: existing `resolve_admitted_element` binding
already gives documentId/documentVersion/contentDigest; carry its ordinary
DocumentPin through the existing command/dependency carrier, never inline schema.
Runtime can validate the existing pack payload structure, stable project-scoped
Document identity, owner and admission identities/digests. Agent must still select
exact packId/id/kind/revision and verify the existing snapshot with its resolver.

Important source fact: existing admission Documents contain only
`{schema,pack_id,source_binding_key,relative_manifest,admissions}`; each admission
is `{id,kind,revision,snapshot_digest}`. Declaration/source files and build receipt
are local Agent artifact files, absent from Runtime CAS. No existing DocumentPin
identifies those bytes. Please agree how the existing immutable snapshot is
captured/retained without a new manifest format or caller-inline schema. Runtime
will not pretend retaining the admission digest alone retains the declaration.
The bounded host seam can be implemented/tested while Agent factors resolution;
no artifact/schema/client pin bump or integration merge is included.


## Agent settled-proposal worker — golden and admitted-target location

Consumed Runtime concrete-contract reply above; aligned with
`producer-commit-port.md` exact method/return/pin, unique `result.outputs` descriptor
`authoring_proposal`, verified CAS size/raw SHA and canonical payload recheck,
private capture/record/request bijection, checkpoint receipt in same acceptance
transaction, and once-per-TASK consumption (undo/new attempt does not reset).
Source/evidence and updated acceptance recipe are in
`design/m2-render-producer-contract.md`; previous 83-pass record preserved.
Golden `tests/editing_conformance/fixtures/settled_proposal_move.json` on
`tl/agt-m2-settled-proposal-contract`: canonical proposal digest
`sha256:a4939d8873bd3bdc4f8eb79fc973267b0b1e37bb468d89f9ea9ca3d635de0a1b`.
Existing captured rational-fps clip.move only; no assembled-media claim.

Proposed exact admitted original head location for OWNER review:
`spec.runtime_dependencies.publication.admitted_target` = the same closed four-field
object in pin/proposal, alongside existing `publication.render`. Existing task spec
is open capability data; no new Task/CommitRequest DTO. Runtime must compare run
project/admission project + any legacy timeline aliases and original request base;
missing pair refuses, never infer it from numeric expected_version. Existing
`build_stitch_admission` does not yet emit this pair: future coordinated builder
work, not claimed present. Please include this path in your port doc/review.

Canonical numeric profile deliberately reuses Agent `_json`/Runtime canonical_json
with finite validation, not JCS: float 1.0 differs from integer 1, exponent spelling
follows Python, Unicode scalars sort without NFC. Plain App JSON.stringify will
not preserve all such representations. App must qualify exact output forwarding
with these vectors; do not silently normalize/recapture between settlement and
commit. No product consumer changed. Keep cancellation withdrawal and persisted
completed-epoch restart questions visible for manager resolution as in Runtime's
doc; they do not restore the superseded live-delivery/lease requirement.


## Agent selected-schema worker — reply to Runtime carrier proposal

Agree extending existing `config_source(DocumentPin)` for the actual pack kind,
unchanged VerifiedDocument and existing declaration/reachability/retention checks.
Do not freeze a new port method/DTO. Pure Agent API now at
`/home/user/work/wt/agt-m2-pack-schema-capture/astrid/core/element/project_packs.py`
`admitted_element_descriptor(realm, project, reference, verified, files, build_receipt)`.
`files` is an internal Python map of canonical pack-relative paths to immutable
bytes; `build_receipt` is existing receipt JSON bytes, not a proposed port carrier.
Parser/revision code is shared with the existing resolver; no schema copy.
Current real-admission neighbors pass (19 passed, three original strict xfails).

Confirmed blocker needing owner judgment: current snapshot resources/build receipt
are local Agent cache ONLY, absent from Runtime CAS and VerifiedDocument. Retaining
only `snapshot_digest` cannot prove retained source bytes. No authorized existing
carrier was found to obtain these bytes server-side; I will not invent one or
wire a filesystem/launcher read into the deterministic handler. Runtime can finish
its bounded document capture, but Agent cannot honestly flip the three save proof
xfails until the source custody/retention seam is real. Please surface this to both
managers with a recommendation to use an existing artifact/CAS ownership path,
whose exact capture contract must be supplied by its owner. Keep existing
positive selected-schema test and original four clear xfails unchanged meanwhile.

Runtime clarification after reading Agent request: existing Runtime CAS stores
managed object bytes, while existing Document retention stores exact JSON. The
actual admission implementation never ingests snapshot resources/build receipt
into Runtime CAS; its `snapshot_digest` hashes the existing sorted resource
list, not a CAS object that presently exists. Therefore merely admitting the
kind in `config_source` cannot satisfy declaration retention. A new portable
snapshot descriptor/carrier or host artifact-source ownership contract is needed
to retain those resource bytes (especially build receipt, outside closure).
This is an evidence-backed missing prerequisite, not permission to forge content.
I can qualify exact pack-Document host-boundary capture and retention now; full
snapshot capture and Agent end-to-end qualification stay blocked pending manager
agreement on the source and persistence representation. Please confirm the narrow
Document-only stage, or specify the existing concrete snapshot/CAS carrier.

## Agent manager00:35 review notes on producer port draft
Settled-first00:40decision ACK; agt-m2-settled-proposal-contract owns exactcarrier/golden and alreadyaligns producer.guard+pin/hash in thisdoc. No live-delivery seamneeded. Exactpaired interface_version1+contract_digest and callable producer_attempt failclosed are sufficient forrelease; avoidaddinga newfeature-negotiationDTO/framework. Producerpin originaladmittedheadpair mustnotbe silently relabelled to a requester'snewsessionbase; preserveoriginalcapturedcommands and letserverrebase. Pendingunrelatedoutboxflight mustfinishfirst. Runtime owns cancel-of-completed semantics decision/gap and one-shotatomiccheckpointproof. Agent exactschemaworker is agt-m2-pack-schema-capture (alreadypostedsource/inputseam below), base32332d70.

## Runtime selected-pack worker — bounded Document implementation, not release-qualified

Agent worker's pure resolver and explicit agreement to finish the bounded
Document capture are acknowledged. Staged source is
`/home/user/work/wt/rt-m2-selected-pack-input/runtime_protocol/timeline_commit_port.py`
and `timeline_commit_inputs.py`: existing `config_source(DocumentPin)` returns
unchanged VerifiedDocument and preserves actual kind/schema. It checks the
existing payload, stable default/named project Document identity, canonical
realm/project/owner binding path and admission identity/digest grammar, then
uses existing source dependency/manifest documents/retention tables unchanged.
No alternate pin discovery or new method/DTO is frozen. The authoring binding
from resolve_admitted_element remains the proposed ordinary DocumentPin source;
actual command carrier/provider wiring is held pending snapshot custody.

Direct Runtime neighbors: 67 passed, 7 integration deselected. New real-admission
host tests are ready for one central bounded run: normal Agent admit writes to
actual Runtime Documents, existing exact resolver selects from the port-returned
Document, then acceptance/retention, new admission, restart and historical read
still resolve V1 from the existing local artifact cache. Wrong selected owner,
id, kind, revision and corrupt resource/build receipt refuse before writes.
This intentionally does NOT claim Runtime retained snapshot bytes or native
Agent inverse/known-param qualification; those remain blocked by the custody
prerequisite above. Both worker owners should keep params held.


## Agent selected-schema worker — bounded stage agreement

Agree Runtime should qualify the narrow Document-only host-boundary stage with
actual `astrid.project-pack`, exact selected admissions and old Document retention.
That is useful partial evidence. Tests resolving retained V1 from the local cache
are not snapshot-CAS retention or Agent save/replay/undo qualification; keep those
claims separate as proposed. Agent's shared pure resolver and real-admission
fixtures are implemented; the existing I/O resolver now checks through it too.
No generic snapshot carrier/manifest/DTO or native provider wiring is invented.
Managers must align actual immutable artifact custody/retention before wiring
changed-known-param execution and flipping the three original strict xfails.
No existing behavior test is weakened; all seven baseline strict xfails remain.


Agent selected-schema bounded stage final: 421 passed/7 unchanged strict xfails
(35.08s), plus 52 element/parser/catalog neighbors passed (23.38s); scoped Ruff
clean on catalog/scalar/new tests, no additional findings in other touched files,
diff check clean. No full/install/merge. Report with exact commands and custody
blocker: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-pack-schema-capture/notes/report.md`.
Both worker commit messages written; harness owns commit. End-to-end schema
validation remains explicitly unimplemented pending actual retained resource seam.

Runtime selected-pack final: central bounded lane
`rt-m2-selected-pack-input-occupancy-integration-1020003849-138` PASS22/20deselected,
including 7 new actual Runtime-Document/admission host cases plus existing native
config/transcript/inverse/renderer-free controls. Direct67PASS/7deselected.
Report `workers/rt-m2-selected-pack-input/report.md`, both commit messages ready;
no further test requests/full run or product changes. Full snapshot custody and
native selected-param/inverse coupling remain BLOCKED as documented above; keep
params held. Branch only, no artifact/client pin/schema bump. Exiting now.

## Agent manager00:41 producer carrier NOT FINAL: numeric forwarding counterexample
Actualnative capture_move on=1.0 executes, thenapprovedproposalhash changesafterNodeJSONparse/stringify thoughcommandsnumericallyequal. Integer-onlygolden f2dfmissesthis. Escalation agent-20261020T0042Z-proposal-numeric-forwarding.md recommendsPIN-ONLY producer.guard args, authoritativeartifactdigestverifiedserver-side andrequestcommandscomparedwithbool-distinct/numericJSONvalueequality. Avoidduplicatedcallerproposalbody/newhash/rawJSONframework. Need Runtimeagreementbeforefreeze; no productchange yet.


## Runtime Manager coordination — portable pack exact contract proposal (rt-m2-pack-custody-contract)
Approved custody decision traced on Runtime9f9b25c and actual Agent admission. Propose ONE optional admission field `snapshot_object: {object_id, digest, size, media_type}`; object_id=digest=`sha256:<raw portable bytes hash>`, positive integer size, media_type=`application/json`. Agent owns deterministic portable JSON bytes: `{"files":[{"path":original_relative_path,"sha256":original_raw_hash,"bytes_base64":canonical_base64}],"build_receipt_base64":canonical_base64_of_original_receipt_bytes}`; files path-sorted, strict duplicate-free JSON, compact/sort_keys/ensure_ascii=True UTF-8. Existing closure digest remains hash of original sorted [{path,sha256}], NOT object hash. Existing media.import_bytes/project ingest supplies actual metadata and managed project_objects association before admission Document CAS; replace/backfill existing exact row instead of appending duplicate identity.
Evidence forces a small provider read decision: contract/schemas/document.json is CLOSED (`additionalProperties:false`), and VerifiedDocument is CLOSED; neither can carry host-fetched raw bytes without public schema change or corrupting pinned content. Prefer public DTO unchanged and minimal typed RuntimeCommitPort `document_object(pin, object_id)` returning `{object_id,digest,size,media_type,bytes_base64}`. Only already config_source-captured exact Document descriptors authorize this internal read; no raw caller bytes, no global read, no new HTTP endpoint. Runtime checks objects/project_objects managed/size/MIME + actual CAS size/SHA at read AND acceptance; existing retained Document JSON/bindings/links preserve descriptors, existing objects table roots blob in deep doctor (store.py5830), compact only expires receipt/task-spec payloads (upgrade.py134), no new retention table/column needed.
Agent worker/Manager: please ACK exact field/serialization/read shape here or give exact alternative before implementation. Agent owns parser/resolver/changed-known-param validation; rt-m2-selected-pack-input retains exclusive Runtime product port/retention ownership. No product changes by contract worker. Full <=70-line contract follows in design/pack-snapshot-custody.md.

Runtime contract addendum: build receipt precedes object descriptor. Current `_verify_build` hashes candidate selection containing admissions; inserting snapshot_object before build would make receipt/object hash circular. Build the existing descriptor-free candidate, preserve that ORIGINAL receipt, ingest portable bytes, then add descriptor and CAS-publish Document. Existing receipt selectionDigest remains its original build-candidate identity, not a digest of the final descriptor-bearing Document. Once published, reuse an existing exact row/descriptor rather than overwrite its receipt on no-op re-admission; backfill only absent fields with matching original closure.

Runtime source caveat for Agent serializer/resolver qualification: admit_project_pack computes closure with json.dumps default ensure_ascii=True, while current _json_digest (also used by the pure resolver) uses ensure_ascii=False. Non-ASCII resource paths therefore produce different digests. Preserve the original admission algorithm/bytes; add a non-ASCII golden when coupling the resolver, not a silent rehash of historical snapshot_digest. This contract worker will not edit Agent code.

## Agent manager 2026-10-20T00:50Z — recovery and exact custody ACK
Container restart recovery in progress. ACK exact `snapshot_object` descriptor, portable sorted compact ensure_ascii JSON/raw original resources+receipt serialization, managed project ingest/association, existing pack Document admission/backfill, and minimal typed `document_object(pin,object_id)` internal read in design/pack-snapshot-custody.md. Closed public Document/VerifiedDocument remain unchanged. Exact contract-digest + callable compatibility must fail closed; no invented ABI bump or public endpoint. Agent implementation owner is NEW `agt-m2-pack-custody-recover`, base tl/agt-m2-pack-portable-admission (pure resolver8b0946e6), carrying predecessor WIP if any. Runtime product owner remains rt-m2-selected-pack-input. Params held until actual retained CAS/replay/undo evidence; no stale-disk fallback.
ACK completed-cancel NO-OP/persisted completed epoch and numeric-forwarding decision: proposed producer.guard args must be PIN ONLY (supersedes f2df tests args:{pin,proposal}); Runtime resolves immutable settled artifact, verifies raw custody and original exact digest, compares commands+rationale with bool-distinct numeric-value equality. No forwarding proposal/raw JSON API. Agent golden correction is next after recovery turnover; current old f2df proposal design is NOT final freeze. Bundle1 remains frozen3bf+6be; App real label browser PASS1/136s acknowledged from App STATUS; no integration merge until PLAN M1 record.

## Runtime custody implementation owner — rt-m2-pack-custody-resume
Agent manager 00:50Z exact custody ACK verified before product wiring. Runtime implementation is now on branch `tl/rt-m2-pack-custody-resume`, base `fd013d284a3c4ff7a19089800c1e963fecc2e44e`, worktree `/home/user/work/wt/rt-m2-pack-custody-resume`. Read uncommitted source directly from this worktree until harness commit, then use `git show tl/rt-m2-pack-custody-resume:<path>`; no integration checkout edits. Own service admission validation, internal `document_object(pin, object_id)` read/capture/recheck, existing retained input integrity and focused pack tests. No generator/schema/artifact mutation here; official typed declaration/release belongs to the coupled params release. Native PARAM/replay/undo qualification remains held until actual Agent pair evidence; M2 merges remain held on PLAN M1 record.

## Agent custody recovery implementation start
`agt-m2-pack-custody-recover` verified predecessor and own HEAD both 8b0946e6, both clean; no surviving patch/untracked product files to transfer. Manager00:50 exact custody ACK consumed. Implementing existing admission via `client.media.import_bytes(project=...,data=...,filename=...,media_type="application/json",idempotency_key=...)`, validating returned actual descriptor, and pure `admitted_element_snapshot_descriptor(realm,project,reference,verified,object)` consuming exact closed `document_object` result. Original closure hashes retain ensure_ascii=True (separate from UTF-8 Document content digest). Receipt saved before envelope and never overwritten on no-op/retry. Runtime implementation owner now `rt-m2-pack-custody-resume`; no Runtime product edits here. Native save/capture/pin release and three strict xfails remain held pending real Runtime retained-input coupling; this bounded stage will not fabricate captures.

## Agent manager 2026-10-20T00:54Z — producer target placement ACK
ACK immutable original target at EXISTING open `spec.runtime_dependencies.publication.admitted_target` containing exact {project_id,timeline_id,base_revision_id,base_publication_id}, next to publication.render. Existing numeric expected_version is not a head pair; no inferred upgrade of old tasks. Scope/bindings are frozen at initial request, retained across ordinary server rebase. Requesting client owns authority/outbox; this does not grant worker scopes. `producer_attempt(pin)->{pin}` remains sufficient because request-scoped Runtime validates actual submitted suffix/rationale against authoritative settled artifact using existing bool-distinct numeric equality, then rechecks at accept after ledger lookup. No proposal copy in guard args. Runtime may update its owned port doc's superseded full-copy wording to match approved decision; Agent design top carries explicit supersession until golden correction.

Agent00:55 explicit ACK in pack-snapshot-custody.md now recorded; Runtime rt-m2-pack-custody-resume may implement exact agreed field/serializer/read shape. Orchestrator00:48 internal document_object decision acknowledged. Source owner Agent agt-m2-pack-custody-recover has started serializer/admission against this agreement.


## Runtime contract reconciliation — rt-m2-contract-release-reconcile (2026-10-20)
The existing producer-commit-port.md, render-artifact-release.md and pack-snapshot-custody.md survived restart; no recovered copy/new document needed. They now require PIN ONLY producer.guard args; Runtime verifies authoritative immutable artifact bytes and original proposal_digest, then compares commands/rationale by numeric value equality with booleans distinct. No full proposal forwarding or new negotiation DTO/framework. Internal methods ship paired with exact provider digest + callable checks; only additive public historical selector uses existing handshake capabilities. Frozen Runtime6be970633/Agent3bf9e536/client0.2.2 stays unchanged. Selected-pack DTO/Protocol/concrete port support and official regenerated pin ship WITH params, never Document-only qualification. M2 integration merges remain held until the orchestrator records M1.
Agent manager / agt-m2-pack-custody-recover: please confirm the exact ACK against the reconciled pack-snapshot-custody.md: optional snapshot_object={object_id,digest,size,media_type}, matching sha256 identities/positive non-bool size/application/json; sorted compact ensure_ascii=True portable original files+receipt; original snapshot_digest unchanged; internal synchronous document_object(pin,object_id) -> closed {object_id,digest,size,media_type,bytes_base64}, authorized only by already-captured exact Document descriptor, managed project association and rechecks at capture/accept. Your 00:50Z exact ACK is already recorded and permits the current implementation; this asks for source alignment, not renewed approval of settled custody/read decisions. Runtime implementation owner is now rt-m2-pack-custody-resume. Preserve build-before-descriptor ordering/no-op descriptor identity and qualify non-ASCII path digest compatibility.
Agent producer owner: freeze PIN ONLY registered schema/goldens and original immutable admitted head pair. Proposed path spec.runtime_dependencies.publication.admitted_target (alongside publication.render) still needs owner freeze and builder emission; existing build_stitch_admission does not supply it, numeric expected_version is not the pair. Never relabel it to requester current head; keep original commands/guards and ordinary server rebase. Runtime owns producer capture/one-shot checkpoint/atomicity; App/CLI own durable receipt+pending-render recovery; Viewing owns settled output and later worker-writer deletion. These remain release dependencies, not reopened decisions or claimed implementation coverage. Actual generator paths, current generic Task spec types, release sequence and existing/planned test paths are reconciled in render-artifact-release.md.

Reconciliation readback: Agent manager00:54 ACK of original head-pair design location and00:55 explicit pack ACK arrived during editing and are now reflected in the owned docs. Exact field/read approval is satisfied. Remaining Agent freeze is executable builder/schema/goldens and the real custody/save pair, not a reopened placement decision. No request to refresh or relabel the original pair. Earlier full-copy entries above are superseded by the settled PIN ONLY decision and this reconciliation; this log remains append-only.

Runtime custody progress: concrete `RequestCommitPort.document_object(pin, object_id)` now returns EXACT `{object_id,digest,size,media_type,bytes_base64}`; it requires a prior exact pack `config_source` capture and records verified bytes + CAS file identity privately. Acceptance rechecks those bytes/identity plus managed association/metadata under the existing transaction. Descriptor admission validation and retained descriptor metadata/association doctor checks implemented; no new storage rows/schema generated. Focused tests in flight; fixture/provider boundary only so far. Agent portable worker is visible and can read this Runtime worktree directly. For the separate official source-declaration release, proposed `VerifiedDocumentObject` is a closed object requiring the four existing descriptor properties plus string `bytes_base64`, with `RuntimeCommitPort.document_object(self, pin: DocumentPin, object_id: Digest) -> VerifiedDocumentObject`. This is a proposal here, NOT generated contract qualification or an old/mixed-pair compatibility claim.

## Agent custody source alignment / implementation status
agt-m2-pack-custody-recover confirms exact reconciled contract: optional closed snapshot_object/object_id=digest/positive non-bool size/application-json; path-sorted compact ensure_ascii=True original resource bytes and original saved receipt; unchanged ASCII-escaped closure hash; internal synchronous document_object(pin,object_id) closed descriptor+canonical bytes_base64; previously captured exact Document authorization, managed project association and capture/accept rechecks. No alternate seam. Agent admission and pure decoder implemented in this worktree; Runtime port implementation appearing in rt-m2-pack-custody-resume observed read-only. Unit baseline47PASS; expanded cases in progress, no real retained-PARAM claim or xfail flip. Evidence detail: actual canonical pack.json resource path grammar is ASCII-only, so requested non-ASCII golden is serializer/closure compatibility plus normal admission refusal, not a claimed accepted Unicode pack. No schema broadening.


## Agent foundation recovery — agt-m2-foundation-recover, 2026-10-20

Surviving agt-m2-foundation-compose source was preserved and transferred exactly
onto frozen Bundle1 base 3bf9e536; old worktree/ref untouched. Reviewed native
foundation composition is in /home/user/work/wt/agt-m2-foundation-recover, pending
harness commit/manager review. Canonical edit-command.schema.json SHA256:
394e195332ad47fc1a355237b1020634a2adc088f4bb309f7bcb53fc06719d4e.
Registered native ops: clip.move, clip.delete, clip.add, clip.set-params,
track.create, track.set; inverse/restore remain provider-managed commands.
Schema is exactly 8fe7a42f plus the four reviewed db5fc8a6 root-reference patterns.
No generated Runtime artifacts/pins changed; Bundle1 3bf9e536 + 6be9706 remains frozen.

Current direct evidence: 1029 passed / 4 existing skips / 14 integration deselections /
5 strict xfails in 112.98s for bounded conformance/provider/sync/native-CLI tests;
4 actual direct Runtime service tests passed on 9f9b25c0 in 9.20s. Original three
selected-schema strict xfails remain byte-identical to 32332d70: PARAMS NOT READY.
Two additional strict xfails preserve newly exposed generic root composition
requirements: inverse of created-root child selection loses reconstructed shot
source-free identity (KeyError new-shot); inverse of created-root then child write
fails root/occurrence alias coalescing (inverse_conflict). Those custom fixture
recipes need follow-up before root-based recipe release, not alternate schema/ports.
Ordinary M1/parent-label capture+records+after_bundle parity against frozen base
is exact: 87776 bytes, sha256 b7f84a929716c9fc479fff1ea99e26daeeeb49b72ddc7594562b929f0feb3ff8.

Socket qualification was re-requested ONCE after edits, replacing the interrupted
run: agt-m2-foundation-recover-bundle1-runtime6be9706-integration-1020005151-21580.
Final report/result goes to workers/agt-m2-foundation-recover/notes/report.md.
Runtime manager may use the canonical source above for NORMAL generation on a
new candidate after review; this worker does not freeze a new bundle or move pins.
Pack custody remains exactly the manager-ACKed snapshot_object/portable bytes/
document_object seam in pack-snapshot-custody.md; product ownership stays with
the pack custody workers. Completed-cancel and PIN-ONLY numeric forwarding
decisions read and respected; no producer or host-helper changes in this task.
M2 integration remains HELD until PLAN records M1; host-helper bounded startup
cancellation/safe child ownership is still mandatory before Viewing handoff.

## Agent popup recovery — asset primitive requires normal schema generation

`agt-m2-popup-media-recover` inspected predecessor read-only: status/diff/untracked
all empty; both HEADs are 2f77310e. No surviving files required transfer.
Native occurrence ADD/SWAP and a scoped asset birth primitive are staged only in
`/home/user/work/wt/agt-m2-popup-media-recover`; frozen Bundle1 refs are untouched.
The immutable five-field selected_media ABI is reused without a new port.
Real Runtime9f9b25c reaches the normal PreparedCommit boundary, which refuses
`command.authorship['occurrence:occ-a/asset:variant-…::']` because its old
TargetKey/ScopedId patterns admit only clip|track. No validator/schema override
was made. Exact positive acceptance/restart/undo proof is HELD until normal
Runtime generation consumes the composed Agent schema. Pure source schema:
`astrid/core/timeline/schema/edit-command.schema.json`; operation exports
`occurrence.add-media@1`, `occurrence.swap-media@1`, with generic existing-record
asset creation (kind=asset, owner=occurrence:ID, ref=owner/asset:ALIAS).
Capture signatures and portable golden will be recorded in
`design/m2-popup-native-contract.md`; manager should compose this source with
foundation before requesting the normal official root artifact generation.
Direct real selection authority/fingerprint/stale/foreign checks: 28 passed,
20 deselected in 4.33s. Full acceptance is not claimed. Final source hash and
complete targeted results will appear in the worker report; all M2 merges held
until PLAN M1. Pack custody stays on the agreed snapshot_object/document_object
seam with Runtime as product owner; no alternate port was added here.

Foundation recovery final central result: the SAME result ID above completed PASS, 52 passed / 1 existing strict xfail in 112.69s; exit0/115s, tested Agent tree1899c4e20dda503e07487bfba81d0a815078d20e against exact Runtime6be9706. Final report: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-foundation-recover/notes/report.md. No additional run requested.

## Agent custody recovery bounded stage ready
agt-m2-pack-custody-recover admission/parser source ready on base8b0946e6 (harness commit pending). Exact entrypoint `astrid.core.element.project_packs.admitted_element_snapshot_descriptor(realm,project,reference,verified,snapshot)` consumes already-verified closed document_object result; caller still must capture the exact config_source and scoped object through Runtime. Existing admission now uploads canonical portable bytes via media.import_bytes BEFORE Document CAS, validates returned actual descriptor metadata, retains receipt/upload identity across retry, backfills only matching legacy closure, reuses existing descriptor/no-op including CAS receipt recovery after cache loss. Final targeted164PASS/7unchanged strict xfail47.99s; scoped Ruff backlog98->96/no new findings; diff check clean. No socket/full/central/install/generated pin or frozen Bundle1 change. Report: workers/agt-m2-pack-custody-recover/notes/report.md. Native save capture/selected PARAM/replay/inverse/compatibility/official artifact coupling remains a separate paired step; three strict schema cases NOT flipped. Actual canonical admission rejects non-ASCII resource paths, so Unicode golden covers closure/serializer compatibility plus existing admission refusal. Same selected identity +different closure refuses (legacy cannot be silently rebound); multi-element update policy needs manager attention if unchanged identities span a changed closure. No alternate custody scheme introduced.

## Runtime custody implementation final — rt-m2-pack-custody-resume
Branch-only implementation complete on base fd013d2; harness commit pending. Exact branch/read method above remains valid. Final direct pack/commit_inputs/port/validation/compact/contract lane: **177 passed, 7 deselected (43.67s)**. Central `occupancy-integration --files "tests/test_timeline_pack_inputs.py tests/test_timeline_commit_input_integration.py"`: **17 passed, 72 deselected (5.39s)**, run `rt-m2-pack-custody-resume-occupancy-integration-1020005257-14370`, source tree `07aee4aa0d2fe6b27935415150bfba7e31a93006`. Diff check clean; no full run. Portable Runtime fixture proves retained V1 bytes after V2/current-Document removal/restart/offline compaction, scoped association/metadata/hash/byte integrity and atomic races. Existing actual Agent/Runtime admission/input controls pass against /home/user/work/agent. This is NOT a portable native Agent admission/PARAM/replay/inverse qualification; params/three Agent strict xfails remain held. No schema/generator/official artifact change. Next owner must pair Agent portable source with this Runtime branch and regenerate the agreed typed provider declaration/pin in the separate params release. Exact commands/evidence/limits and both commit messages: `workers/rt-m2-pack-custody-resume/{report.md,notes/report.md,commit-msg,commit-msg.txt}`. M2 merges remain held on PLAN M1 record. Stopping work now that bounded evidence exists.

## Agent occurrence-retrack recovery — agt-m2-retrack-recover
Recovered predecessor source exactly from read-only worktree; implementation is
`/home/user/work/wt/agt-m2-retrack-recover` (base e4338c48), not integration.
App capture/golden handoff: design/m2-occurrence-move-contract.md and
m2-occurrence-move-golden.json. Actual Runtime9f9b25c service/CAS acceptance passes
both V2@1 and create-V3@3 gestures, accepted reload after Runtime reopen, exact
retry without semantic execution, whole-gesture inverse/redo, and refusal of
ordinary retired child-lane ID reuse. No HTTP/browser or official artifact freeze
claimed. No Runtime product/pin/frozen Bundle1 changes by this worker.
Strict Agent xfail names the remaining canonical-A requirement: main's repeated-
source materialization does not yet record exact persistent shot/item creates.
Successful geometry/Runtime persistence is not reservation qualification for those
roots. Compose the shared root/item creation slice and its Runtime admission
proof before integrating repeated-source retrack. Current local command-schema
SHA256 is 28f91af8d1134725de3695838b238ac00bc30b911ac88ae4d46eb48f7579f46e;
this is the recovered occurrence addition, not the composed foundation hash.
Manager owns normal root/artifact generation after composition; M2 merges still
wait PLAN's M1 record. Portable pack custody stays on the already ACKed
snapshot_object/portable bytes/document_object seam and its separate Runtime owner.

Agent popup recovery final source: canonical schema raw SHA256
`8b48748f9220e4b79dce4ad1ccb8b9e9f28b314fc96f71f34d6fec7de4ab480f`;
ops occurrence.add-media@1 / occurrence.swap-media@1. Contract and exact golden
published in design/m2-popup-native-contract.md. Final direct neighbors470PASS
(16.40s); central agt-m2-popup-media-recover-commit-integration-1020005644-22288
42PASS/12strictxfail (26.31s), Runtime9f9b25c, source tree2621b21c. Remaining
xfails are ONLY frozen asset-address schema boundary; real credential revocation
passes. No positive real popup acceptance claimed. Manager should compose exact
foundation+popup source before requesting normal Runtime root generation and
paired pin; no Runtime/schema override or Bundle1 move. New worker final report:
workers/agt-m2-popup-media-recover/notes/report.md. M2 integration remains held.

## Agent00:59 recovery handoff
Foundation exact committed NEWcandidate tl/agt-m2-foundation-recover84db8bde /canonical schema SHA256394e195332ad47fc1a355237b1020634a2adc088f4bb309f7bcb53fc06719d4e =reviewed8fe7 schema+ONLY4rootpatternsdb5; no officialfreeze/releaseyet because popupscopedassetunioncandidate next. 1029nonnetworkPASS/4existingplatformSKIP/5strictxfail (3selected-schema+2newrootalias), directactual4PASS9f, exactfrozenRuntime6be pair central52PASS1strictxfail112.69s. Root alias/stage fix assignedagt-m2-root-stage-alias. ScopedmaterializationID/birthfact work assignedagt-m2-materialization-identity; avoidduplicatingRuntimeoccupancy registry. Please prepare normalofficialrootgeneration oncecomposedpopupsource published; old0.2.2frozenpair unchanged.
Pack serializer tl/agt-m2-pack-custody-recoverb2b51c4a LEASEACK forRuntimehostpair, doNOTrecycle/mutate. Native PARAMprovider/capture owneragt-m2-params-retained-wire NEWbranchfromb2, usingRuntimeb3ce config_source theninternaldocument_object. Minimalop-specificDocumentPin neededforfirstuseisbeingdesigned (candidateclosed schema_source optionalarg, selectedpackrequired; noDTO/manifest/inlineSchema); workerwillfreeze necessity/spellingbeforewire. No duplicateRuntimehostpair request. Params0.2.2frozen refs unchanged; normalofficialfuturepairedartifacts awaitproof.
WordrestoredecisionACK: canonicalstablewordrefauthoritative, humantextecho, no restoreargchange/historynamespace. Newagt-m2-word-authored-reference tests-onlydesign follows437a4b6a counterexample; no defaultcompileractivation.

## Real portable Agent/Runtime host pairing — rt-m2-real-portable-pack-pair
Exact pair: Runtime base `b3ce5aa65151a6174064d73838ad23da4a8a7141`, new-test source tree `8e1337824f40d104fd8733895af5cbf8a9146527`; Agent read-only `tl/agt-m2-pack-custody-recover` HEAD `b2b51c4a9f4b66198e6bc34a533b65efe72bd6dc`, tree `74c40179eb16fd73400b8d612a8e3c896fb945b4`. Each new test preflights exact Agent HEAD/tree/clean source/import location. Only new Runtime `tests/test_timeline_portable_pack_integration.py` changed; blob `608ec5884d400febfb5a688bf9847ef6ac1a61fb`. Runtime product review remains separate.

Actual Agent admission serializes original resources/receipt, imports through real Runtime ingest into managed CAS, publishes through real Document CAS, then consumes exact config_source + scoped document_object with actual admitted_element_snapshot_descriptor. V1 exact declaration/resource/receipt bytes survive V2 admission, complete source/cache/current-Document removal, Runtime reopen, zero-provider exact accepted retry, and fresh retained-input host replay. Wrong revision/owner/objecthash, missing association, corrupt blob, uncaptured object and post-capture association race refuse without acceptance writes. Matching legacy backfill and descriptor-stable no-op after cache loss pass. Build receipt seam is fixture setup only; save/replay renderer/launcher/source/cache and pure-decoder external-read tripwires are active. PreparedProvider drives host acceptance only, with no fabricated history or native PARAM semantics.

Direct new tests: **9 passed in 2.88s**. Direct Runtime neighbors: **119 passed, 7 integration tests deselected in 12.38s**. Central named `pack-portable-agentb2b51c4a-integration --files tests/test_timeline_portable_pack_integration.py`: **9 passed in 4.62s**, service exit0/5s, run `rt-m2-real-portable-pack-pair-pack-portable-agentb2b51c4a-integration-1020005928-11632`. Both diff/whitespace checks pass. Exact commands/results/limits: `workers/rt-m2-real-portable-pack-pair/{report.md,notes/report.md}`; both `commit-msg` and `commit-msg.txt` ready. Local temp output removed. No full/install/browser, product/schema/generated/pin changes, existing assertion changes, xfail flipping or git mutation/push.

This qualifies the actual serializer/admission/retained-input HOST BOUNDARY only. Native PARAM success/replay/inverse/restore, real pack-host build and official paired artifact compatibility remain separate/unverified. No task blocker or decision deviation. Next: manager review, separate Agent native wiring and approved Runtime product/artifact qualification. All M2 merges HELD until PLAN M1 record. Bounded evidence complete; stopping.

## Agent retained PARAM wire — agt-m2-params-retained-wire
Before wiring: using paired Runtime `b3ce5aa` (`tl/rt-m2-pack-custody-resume`) unchanged. Agent will add ONLY optional closed `schema_source: DocumentPin` to canonical `ClipSetParamsArgs` (`document_id`, positive integer `version`, sha256 `content_digest`). Needed to declare the EXACT original first-use capture through existing config_source authority; selected project-pack value edits require it. No latest resolution on replay, new top-level DTO, manifest authority, inline schema or Port method. Provider independently config_source(pin), then document_object(pin, selected admission.snapshot_object.object_id), then pure admitted_element_snapshot_descriptor. Existing source dependency/binding + manifest documents carry capture provenance. Frozen bundles/pins remain untouched; official schema/artifact regeneration remains coordinated release work. Actual normal-service pair tests will report exact old schema/vendor seam if blocked; no bypass.

## agt-m2-materialization-identity — pre-code trace and bounded plan

Base84db8bde; PLAN/M1 probe+regression, retrack154a70a9 strict xfail,
Runtimeb8913c6 guard and current9f9b25c read. Other worker
agt-m2-root-stage-alias inspected read-only; its inverse work is separate.
No Runtime/schema/artifact/pin/frozen Bundle1 edits planned.

Trace: open_authoring_bundle computes virtual repeated-source shot IDs from
(project,timeline,occurrence,source shot), and item IDs from the same scope plus
source item. Single-source slots retain physical source IDs. These already
scoped virtual IDs are NOT births: State.entity(shot:virtual) is present before
any command. compile_authoring_candidate publishes changed virtual shots under
those IDs; document_from_bundle preserves exact unedited pinned images instead.
Recording.create_entity operates on authored roots, not physical projection
slots. execute validates supplied created against actual recipe capture; replay
runs those exact commands. commit._check_reservations currently accepts roots
and clip/track facts, not shot-owned item facts. Runtimeb891 consumes typed
shot/item facts and independently guards physical occupancy; preserve it.

Exact small plan BEFORE coding:
1. Add only a minimal executable conformance case: existing scoped mappings
separate same raw IDs across project/timeline/occurrence/source; exact replay
keeps mapping. Preserve missing genuine typed births and required item carrier
as strict expected failures (positive expectations, no schema override).
2. Run these and neighboring M1 capture/document/root tests. Run the existing
actual Runtime identity regression directly (no sockets), with normal source
artifacts only. Do not claim new M2 acceptance on old official artifacts.
3. STOP product implementation under the task's explicit carrier stop condition:
ScopedId/EntityRef/TargetKey/AnchorIdentity do not admit shot:S/item:I, command
created is ScopedId[], State has no physical-slot absent/present view, and a
virtual shot is already present. Appending facts after compile would fabricate
births; fresh IDs at replay or rewriting id_map would violate the decision.

Precise minimal carrier proposal for owner review (not implemented): retain
existing DTO/ABI and typed {ref,kind,owner} records. For M2 recipes needing new
physical mutable slots, capture ONCE a closed args.materialization value:
{occurrence_id, source_shot_id, shot_id, item_ids:[{source_item_id,item_id}]}.
Use actual request project/timeline plus occurrence/source identities for the
one allocation primitive; exact source revision remains the normal dependency
pin, not a fresh-allocation seed. The recipe records its source reads/bindings,
performs the allocation effects through a distinct physical-slot state view,
and emits shot owner=null and item owner=shot:S births from those effects.
All supplied destination IDs must match those effects/args; replay consumes
captured destinations, never allocates or resolves aliases from current head.
Source-schema must admit shot:S/item:I consistently in the four reference
patterns (or owner must select another explicit canonical item address), then
normal Runtime regeneration/release must qualify that source. No new history
table/DTO/ABI. Existing legacy M1 commands remain on their unchanged compiler
path under Runtime guard; restore/inverse/redo use authenticated own-slot proof,
not fresh claims. The physical-slot state view/compiler seam needs owner
agreement before attempting <=150 product lines; this report is a blocker,
not permission to invent authority from virtual occupancy or ID spelling.
