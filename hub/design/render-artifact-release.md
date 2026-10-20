# Historical render artifact release recipe
Status: design-only; Runtime base `9f9b25c`; never edit generated artifacts by hand.
1. Canonical contract and ownership
- Runtime owns `contract/openapi/workspace-v1.yaml`, `contract/schemas/task.json`,
  `contract/schemas/handshake-response.json`, and `runtime_protocol/store.py:_freeze_managed_render_inputs`.
- Add a closed five-field `canonical_revision` under render `spec.params`
  (project_id, timeline_id, revision_id, publication_id, content_digest); retain
  Runtime authority under `Task.spec.spec.inputs.timeline_authority`. No new route
  or top-level AdmitTask field.
- Agent owns `astrid/packs/rendering/pack.yaml` and
  `config/astrid-capability-census.lock.json`; Viewing owns producer use. Runtime
  must not take ownership of Agent packfiles.
2. Normal generators and projections
- Python source: `generators/python_client_template.py`, rendered by
  `generators/generate.py:render_python_client` into `packages/python/.../generated.py`.
  Add typed canonical-revision/render-param projections to existing `admit_task`,
  `Task.spec`, and `from_json` (no new operation).
- Official TS source: `generators/generate.py:render_typescript_client` over
  `packages/typescript/src/generated.ts`; add the same types to existing `admitTask`
  and `Task.spec`. `tools/generate_typescript_conformance.mjs` is conformance-only.
- `runtime_protocol/contract_metadata.py`, Python metadata, and TS `contract-metadata.ts`
  are `generate.py` outputs and carry the same digest.
3. Digest, advertisement, and compatibility gate
- `SCHEMA_DIGEST` hashes length-prefixed relative paths/bytes for OpenAPI followed by
  every schema in `contract/manifest.json`: the whole ordered contract set, not payload.
- `canonical_revision.content_digest` is `sha256:` over `canonical_json(payload)` for
  the accepted parent, as checked by `_freeze_managed_render_inputs`; not schema/snapshot.
- Extend `runtime_protocol/service.py:handshake`'s string `capabilities` with
  `rendering.render.historical_revision.v1`; add capabilities to inline OpenAPI
  HandshakeResponse (the external schema already requires it). Clients fail closed
  before admission when absent; old Runtime may ignore unknown nested params.
4. Release order and checks
- `0.2.2` is FROZEN. Release ordinary root bundle 2 first; historical bundle 3 only
  if needed, with its own coordinated contract version.
- Change canonical inputs, run `python generators/generate.py`, the documented
  `node tools/generate_typescript_conformance.mjs ... --check ...`, and
  `python scripts/artifact_manifest.py`; verify `generate.py --check` and
  `python scripts/artifact_manifest.py --check`. Agent then updates/checks `runtime.lock.json`.
5. Response and conformance
- POST `/v1/tasks` remains `201 {data: Task, receipt: CommittedMutation}`; GET remains
  `Task`, not a new wrapper. Extend schema/client parity/release/artifact/handshake tests
  and historical-admission tests for exact tuple, authority reflection, old-runtime
  fail-closed behavior, and atomic refusal.
