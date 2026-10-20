# Portable admitted pack snapshot custody
Status: custody and internal read APPROVED by orchestrator (pack-object-read00:48). Agent manager ACK00:55 exact field/serialization/read shape below; implementation proceeds on held Agent/Runtime branches. No integration release before PLAN M1; params paired official artifacts and real retained-input tests remain required.
Source: Runtime base `9f9b25c`; Agent integration project_packs.py and agt-m2-pack-schema-capture pure resolver; same `astrid.project-pack` / `astrid.project-pack/v1`.

1. Existing admission row remains `{id,kind,revision,snapshot_digest}` with ONE optional field:
   `snapshot_object = {"object_id":"sha256:<64 lower hex>","digest":"sha256:<same>","size":<positive integer>,"media_type":"application/json"}`.
   Descriptor keys are closed; reject bool size, inconsistent ids/digest, wrong MIME, extra keys. Missing field is legacy, not an empty snapshot.
2. One portable CAS object contains strict UTF-8 JSON `{"files":[{"path":P,"sha256":H,"bytes_base64":B}],"build_receipt_base64":R}`.
   Agent serializes with `json.dumps(sort_keys=True,separators=(",",":"),ensure_ascii=True,allow_nan=False).encode("utf-8")`; files sorted by original path.
   P is the original canonical pack-relative POSIX resource path; H is lowercase raw SHA256; B/R are canonical RFC4648 padded base64 of ORIGINAL bytes.
   No schema copy, global index, new manifest authority, archive extraction, absolute paths, traversal, duplicate paths/keys, symlinks or invented build receipt.
   Existing <=256 resources / <=64MiB decoded resource limit remains; envelope/receipt also obey existing Runtime object-transfer size limit.
   `snapshot_digest` remains the ORIGINAL closure hash over sorted `[{path,sha256}]` using admission json.dumps(sort_keys=True,separators=(",",":"),ensure_ascii=True); CAS descriptor hashes entire portable bytes separately.
3. Admission order: capture/recheck original resources -> verify existing build -> preserve exact `.build-receipt.json` bytes -> project ingest -> Document CAS -> advance local index.
   Build the descriptor-free candidate first: including receipt-bearing object hash in that candidate would create a hash cycle. Its original selectionDigest is not the final Document digest.
   Use existing SDK `media.import_bytes` / `ingest_project_object`, Runtime `service.ingest` / `_ingest_transfer`; require returned actual descriptor and `project_objects.relation=managed`.
   Verify actual returned size/MIME/hash against serialized bytes; do not trust requested MIME when CAS dedup returns preexisting metadata.
   Runtime validates supplied descriptor and scoped association at existing create/update Document boundary and on every capture; Agent owns content serialization and closure/build/revision validation.
   Failed build/upload/Document CAS never advances selection; an unused managed object after CAS failure is acceptable under existing custody, not a new transaction journal.
   Exact-key retries reuse captured bytes and original upload/Document identities. Never mutate a published descriptor; no-op re-admission reuses it.
4. Resolve exact owner from `pack_id`, stable default/named Document id, realm/project relative_manifest, then EXACTLY ONE admission matching element id/kind/revision.
   Ordinary authoring binding supplies `{document_id,version,content_digest}` through existing command/dependency input declaration; never infer latest during replay.
   Existing `config_source(pin)` admits real pack kind and returns UNCHANGED VerifiedDocument. It retains existing declaration/closure/history authority and detached exact content.
   Byte access requires a minimal provider read: `document_object(pin: DocumentPin, object_id: Digest) -> VerifiedDocumentObject`.
   Return closed `{object_id,digest,size,media_type,bytes_base64}` with the same verified descriptor plus canonical base64 of actual CAS bytes; JSON-safe, no local path.
   Evidence: `contract/schemas/document.json` and VerifiedDocument are both CLOSED, so attaching bytes to either or altering pinned content cannot satisfy the current contract.
   This is an internal RuntimeCommitPort addition, NOT an HTTP endpoint or public request/Document/VerifiedDocument DTO change; generated provider contract must reflect it.
   Only a previously captured config_source pack Document containing that exact descriptor authorizes this read; guessing an object id or importing caller bytes never authorizes it.
   Runtime reads only managed project CAS, verifies metadata/size/raw SHA, captures object identity, and rechecks association+metadata+bytes under acceptance authority/transaction.
   Agent decodes strictly and passes resources/receipt into shared `admitted_element_descriptor`; verify original closure, selected revision, owner/project and successful existing receipt identity.
   No renderer, launcher, network, source directory or artifact cache read inside commit/replay/undo. Changed known params use descriptor.schema; opaque params/explicit clears retain current policy.
5. Retain EXACT Document JSON including descriptor in existing `timeline_document_input_contents`, exact binding in `_bindings`, publication/revision link in `_links`.
   Record existing `source` dependency and manifest `documents` pin; selected exact element ref/owner and consumed object must be evidenced by captures/records, not extra caller authority.
   Extend port.validate/persist and `timeline_commit_inputs` validation so accepted input cannot reference an uncaptured/mismatched object; write links in SAME acceptance transaction.
   Live first-use Document V1 -> V2 between capture/accept refuses atomically. Already-retained reachable V1 stays V1 through V2/re-admission, replay, inverse and restore.
   Current actor/project authorization plus existing managed association are rechecked; removing current Document/selection is not a revocation of an accepted historical pin.
6. Actual roots: `store.integrity_report` selects ALL `objects` digest/size rows, hashes their CAS bytes and `_cas_orphans` treats only absent object rows as orphaned (store.py5830ff).
   Existing durable `objects` + managed `project_objects` association retain blob independently of mutable Document/local files; retained JSON provides the historical descriptor edge.
   No new retention table, column, synthetic media pin or root manifest. Current product has no deletion of objects/project_objects; future pruning must walk retained admission descriptors.
   `upgrade.compact_idempotency_ledger` expires receipt payloads/terminal specs then VACUUMs, never deletes these object/input rows; extend its regression proof, not its schema.
   Extend `TimelineCommitStore._verify_inputs`/`integrity_errors` to validate retained descriptor -> existing object metadata/project association; deep CAS already verifies actual bytes.
   Doctor must detect deleted association/object metadata and missing/corrupt blob, including V1 after current Document removal; do not claim existing JSON-only check covers that edge.
7. Legacy rows remain readable. Explicit existing re-admission backfills ONLY if original resource closure matches old snapshot_digest and original build/revision checks succeed.
   Replace that identity's missing field, do not append duplicate id/kind/revision rows or silently choose a different closure. Multiple matches refuse as existing exact resolver requires.
   Missing/unbackfillable selected snapshot: PARAM edit refuses `pack snapshot unavailable; re-admit pack`; unrelated edits remain unchanged. Never guess schema or resolve from local disk in save.
8. Ownership/implementation: Agent serialization/admit/pure resolver/known-param capture; Runtime descriptor admission validation, CAS association/read/capture/retention/integrity.
   `rt-m2-pack-custody-resume` now owns Runtime product paths atop the completed `rt-m2-selected-pack-input` Document-only stage; Agent owner is `agt-m2-pack-custody-recover`. Contract worker edits design/coordination/report only. Existing Document-only proof is PARTIAL and does not qualify blob retention.
9. Required Runtime paths: `runtime_protocol/{service.py,timeline_commit.py,timeline_commit_port.py,timeline_commit_inputs.py,timeline_commit_store.py}`, `contract/schemas/timeline-commit.json` and normal generated types/resources. `runtime_protocol/timeline_commit.py` owns the handwritten Protocol signature.
   Agent paths: `astrid/core/element/project_packs.py`, `astrid/sdk/timeline/{capture.py,_scalar_commands.py}`, existing Runtime port adapter and generated dependency pin.
   Required Runtime suites: `tests/test_timeline_commit_inputs.py`, `test_timeline_commit_port.py`, `test_timeline_commit_input_integration.py`, `test_timeline_pack_inputs.py`, `test_runtime_compact.py`, `test_timeline_commit_validation.py`, `test_timeline_commit_contract.py`.
   Required Agent suites: `tests/core/test_project_packs.py`, `tests/core/test_project_pack_inputs.py`, `tests/sdk/test_timeline_selected_schema.py`, `tests/editing_conformance/test_recipe_scalar_commands.py` and actual Runtime selected-param/replay/inverse proof.
   Suite availability: test_timeline_pack_inputs.py is on Runtime selected-pack/custody branches, absent from base9f9b25c; Agent project_pack_inputs/selected_schema/recipe_scalar files are on the Agent schema/custody branches, not claimed integrated.
   Cover successful admission/backfill/no-op retries; descriptor/schema/path/base64/hash/build/revision/scope negatives; dedup metadata mismatch; source/capture/association races; V2+restart+source/cache/current-Document removal.
   Prove historical CAS-only PARAM replay/undo, exact accepted retry, retained descriptor loss/corruption doctor refusal and offline compaction survival; keep original behavior expectations and flip THREE strict xfails only on real evidence.
10. Release: Agent exact ACK exists (00:50Z, explicitly confirmed at 00:55Z); reconciliation confirmation was requested in runtime-coordination.md. No further approval of settled custody/read decisions is required. Runtime owns canonical VerifiedDocumentObject definition in `contract/schemas/timeline-commit.json`, handwritten Protocol declaration, concrete port and integrity checks. Existing `generators/timeline_commit_types.py` emits DTO types, not port methods; `generators/timeline_commit_resources.py` packages the referenced schema closure. Run `generators/generate.py` and normal release/artifact checks; see render-artifact-release.md. Pin compatible Runtime+Agent provider digest/artifacts WITH params, never alter frozen 0.2.2. Agent owns admission/resolver and actual retained-param/replay/inverse coupling.
    Keep public wire DTOs and interface_version=1 unchanged; existing exact contract_digest pairing plus callable document_object check fail closed on old/mixed pairs; add compatibility tests.
    Preserve original snapshot_digest algorithm including ensure_ascii=True for non-ASCII resource paths; qualify this against the resolver, whose current _json_digest uses ensure_ascii=False. No silent historical rehash. Params stays held until real retained-input proofs pass; other bundles unaffected. M2 integration remains subject to orchestrator PLAN gate.
