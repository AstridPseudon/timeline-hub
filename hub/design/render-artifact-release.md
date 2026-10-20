# Historical render and selected-pack artifact release recipe

Design/release instructions only, source-checked at Runtime `9f9b25c` (client 0.2.1).
Frozen writer bundle 1 is Runtime `6be970633cc82ab412428151e6bf42f3e7fc3081` +
Agent `3bf9e5368a956ef562c77e1beb0a745addf23daf`, client **0.2.2**, schema
`sha256:89a396aaa10a5ab6c29fb5f053bf12dd031be4a259c33ebc6a53489fcd5878d3`,
artifact `sha256:3b805d6946fd73c44144009021f44153b78ceeb5e5b1298cd2397a1f2dc19730`.
Do not regenerate or move that tuple. Later bundles get a new coordinated version.
M2 branch work is permitted; integration merges await the orchestrator's M1 record.

## Canonical sources and existing support

- Runtime owns `contract/openapi/workspace-v1.yaml`, `contract/schemas/task.json`,
  `contract/schemas/handshake-response.json`, `contract/schemas/timeline-commit.json`,
  `runtime_protocol/timeline_commit.py` (handwritten Protocol), concrete port/store
  validation and `_freeze_managed_render_inputs` in `runtime_protocol/store.py`.
  Agent owns `astrid/core/timeline/schema/edit-command.schema.json`; copy its reviewed
  exact bytes to `contract/schemas/edit-command.json`, preserving all prior supported ops.
- Historical admission adds closed optional `canonical_revision` under existing render
  `spec.params`: project_id, timeline_id, revision_id, publication_id, content_digest.
  publication_id is the accepted receipt_id. Existing `selector` remains in params;
  Runtime-frozen authority is returned in `Task.spec.spec.inputs.timeline_authority`.
  No new route or top-level AdmitTask field. Selector omission preserves current behavior.
- Existing Python `admit_task(spec=...)` and `Task.spec` use `Mapping[str, Any]`;
  `Task.from_json` copies the mapping. TS `admitTask` and `Task.spec` use
  `Record<string, unknown>`. They already carry opaque params, but neither validates nor
  types nested render admission/authority. No typed nested Task spec is implemented or
  automatically generated. Any future typed projection requires explicit source work,
  round-trip tests and regeneration; it is not a prerequisite to passing this selector.
- Python client source is `generators/python_client_template.py`; `generate.py` renders
  `packages/python/astrid_runtime_client/generated.py`. Official TS generation is
  `generators/generate.py:render_typescript_client`: it currently reads the checked-in
  `packages/typescript/src/generated.ts` and applies specific transforms, not general
  OpenAPI type generation. New projections require an explicit renderer change.
  `tools/generate_typescript_conformance.mjs` emits the separate conformance client only.
- `generators/timeline_commit_types.py` generates Runtime/Python/TS commit DTO modules
  from Agent/Runtime definitions and the existing OpenAPI receipt. It does not generate
  RuntimeCommitPort methods. `generators/timeline_commit_resources.py` emits the packaged
  `runtime_protocol/schemas/timeline-commit-bundle.json` reference closure. Declare internal
  VerifiedDocumentObject/producer pin types canonically, then generate; keep public
  Document/VerifiedDocument and HTTP request shapes unchanged. No generated hand edits.

## Compatibility and distinct digests

`SCHEMA_DIGEST` hashes length-prefixed relative paths and bytes: OpenAPI followed by
schemas in `contract/manifest.json` order. Metadata emitted by `generate.py` agrees in
Runtime/Python/TS. The artifact manifest version hashes its sorted per-file digest map;
these identities differ from payload/object hashes and client version.
`canonical_revision.content_digest` is `sha256:` over `canonical_json` of the accepted
parent payload. Snapshot-object digest hashes original portable bytes; pack snapshot_digest
retains the original admission closure algorithm. Never substitute one for another.
Producer proposal_digest is recomputed exactly from the authoritative immutable settled
artifact (excluding only proposal_digest), after CAS byte custody verification. Guard args
are **PIN ONLY**. Compare submitted commands/rationale by recipe numeric value equality
(1 == 1.0, booleans distinct), never hash caller-reserialized proposal copies.

Current startup checks exact interface_version=1 + contract_digest. For internal
`document_object` and `producer_attempt`, release paired definitions/implementations plus
Agent callable checks; old/mixed ports fail closed. No negotiation DTO/framework or ABI2.
For the additive PUBLIC historical selector only, old Runtime may ignore unknown params:
add `rendering.render.historical_revision.v1` to existing `service.handshake` string
capabilities, reconcile inline OpenAPI HandshakeResponse with the already-required external
capabilities schema, and require the capability before use. Verify returned selected tuple;
keep pending render intent if unsupported. This capability is planned, not advertised today.

## Source, version, artifacts, consumers

1. Agent freezes each reviewed command-schema/golden source with Runtime. Ordinary/root
   bundle 2 may ship independently; **params must ship with** portable pack admission,
   `document_object` capture/recheck/retention/integrity and real Agent retained-input
   PARAM/replay/undo evidence. Agent custody ACK exists at 00:50Z; current owners are
   `agt-m2-pack-custody-recover` and `rt-m2-pack-custody-resume`. Document-only tests do
   not release params. D13 bundle 3 additionally needs PIN ONLY goldens, original immutable
   admitted head-pair source frozen/emitted by Agent (design path ACK 00:54Z:
   `spec.runtime_dependencies.publication.admitted_target`), producer port/checkpoint and
   requester outbox/historical-admission proofs. Never relabel that pair to requester head.
2. On each composed candidate, Runtime selects a fresh coordinated version in
   `generators/release.json` (next available after 0.2.2; manager assigns it, not frozen here).
   Land reviewed canonical definitions, concrete internal methods/Protocol and any public
   historical schema/handshake changes together. Existing generator stamps client Python
   pyproject, TS package/package-lock, metadata and exports from that version; root Runtime
   pyproject version is separate. Do not infer a new version from a schema digest.
3. Run `python generators/generate.py`. Update canonical conformance fixtures for changed
   public responses. Run `node tools/generate_typescript_conformance.mjs --contract
   contract/openapi/workspace-v1.yaml --schema-manifest contract/manifest.json
   --component-manifest contract/component-manifest.json --source-root . --fixture-root
   conformance/fixtures --check`. This check is not an official-client generator.
   Run `python scripts/artifact_manifest.py` LAST, then `python generators/generate.py
   --check` and `python scripts/artifact_manifest.py --check`. Inspect expected source and
   output diffs; artifact coverage includes both commit DTO modules and packaged schemas.
4. After the harness commits the Runtime candidate, publish its exact source SHA, client
   version, SCHEMA_DIGEST and `contract/artifacts.json` version through existing bundle
   coordination. Agent sets runtime.lock.json source_commit, then runs
   `python scripts/vendor_lock.py update runtime.lock.json --producer <exact-runtime-checkout>`
   and `python scripts/vendor_lock.py check runtime.lock.json --producer <exact-runtime-checkout>`.
   App refreshes official TS parity/pins in the same coordinated change. Agent/Viewing own
   `astrid/packs/rendering/pack.yaml` and Agent's capability census lock refresh as needed.
   Qualify the exact pair before exposing params or historical/D13 consumers. No stale-pin
   compatibility writer; all M2 integration merges stay held until the orchestrator M1 record.

## Required qualification (not claimed by this document)

Existing bounded release anchors: `tests/test_timeline_commit_contract.py`,
`tests/test_client_release.py`, `tests/test_typescript_generator.py`,
`tests/test_artifact_manifest.py`; extend existing provider/port tests for exact digest and
missing/noncallable internal methods. Pack suites and actual Agent paths are listed in
pack-snapshot-custody.md; preserve their original success expectations and flip the three
strict xfails only on actual retained-input proof. Historical suite
`tests/test_render_historical_admission.py` is planned, absent from this base. Use existing
`tests/test_canonical_render_admission.py`, `tests/test_direct_render_admission.py`,
`tests/test_timeline_render_publication.py` and producer acceptance/settlement anchors in
producer-commit-port.md. Prove old-Runtime capability refusal, exact five-field authority,
zero-write failures, Node numeric forwarding, restart/exact retry and receipt-to-render
recovery before retiring D13. POST remains `201 {data: Task, receipt: CommittedMutation}`;
GET remains Task. Full/live/browser suites run only via the central service when assigned.
