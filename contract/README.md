# Workspace protocol contracts

## Artifact manifest

`artifacts.json` lists the sha256 of every file consumers copy or rely on (OpenAPI, schemas,
fixtures, generated clients), plus a `version` that is the digest of that list. It is generated, never
hand-edited: run `python scripts/artifact_manifest.py` after changing any listed file. The default
test lane runs `--check` and names each path that drifted. Consumers pin it through their
`vendor.lock.json` (producer version plus a per-file digest), so a change here fails their boundary job.

## Timeline shot composition boundary

The separately versioned shot-composition contract in
`schemas/shot-composition.json` is Runtime-owned. It defines publication
identity, exact-head/CAS context, dependencies, occurrences, and the known
shot-payload core. The payload stays open so consumers can preserve opaque app
extensions. Runtime-managed media metadata owns media identity and kind, and
the schema marks `ManagedMediaRegistry` as a Runtime-specific registry.

Nested `TimelineConfig` and clip semantics belong to the pinned
`@banodoco/timeline-schema` package. Runtime materializes that package's JSON
Schema and references it from the parent config and internal-timeline payload;
the shot envelope does not carry a second hand-maintained config definition.
Audio is optional in the shot payload. Nested timeline audio clips/bindings
remain authoritative, and a legacy aggregate descriptor is read-only when
present. Unknown payload fields are preserved by consumers. Visible clip
duration is source duration divided once by positive speed, with parent
occurrence duration acting as a visible interval cap; renderer frame rounding
is checked against the shared vectors.

`openapi/workspace-v1.yaml` is the canonical HTTP contract for the neutral
workspace runtime.  The schemas under `schemas/` are the closed JSON Schema
definitions referenced by the OpenAPI document.  They intentionally contain no
Astrid, Astrid App, or product-specific types.

The protocol uses a clean, digest-pinned version (`workspace.v1`).  A client
must complete the handshake before using any non-health operation.  Every
state-changing request carries an idempotency key and mutating resources expose
an opaque `version` for optimistic concurrency.

Task admission may include an immutable `storage_estimate` derived from the
same canonical input snapshot as the task spec. `scratch_bytes` is the peak
additional temporary space needed while the task runs; `output_bytes` is the
maximum final output written before temporary data is released. The runtime
checks their sum against current free space at admission and again at claim.
When the field is absent, the registered capability estimates remain the
backward-compatible fallback.

## Astrid binding

Astrid binds a typed task family, project identity, ordered CAS/input
references, and idempotency key to a Runtime-owned workspace task and run.
Workers claim and settle that work through the Runtime contract. Settlement,
output provenance, receipts, and event history remain Runtime-owned and are
the canonical readback surface for Astrid App's gallery and timeline consumers.
Product clients must not bypass this boundary with a direct database client or
legacy task-table fallback.

## Output locations

Runtime owns durable output bytes in the realm CAS at
`cas/sha256/<first-two>/<remaining-digest>`. Attempt scratch and settlement
staging are temporary and are not public result paths. Managed-output rows are
the portable readback identity. An explicit export materializes bytes under
the separately configured export root; the returned `destination.filename` is
the authoritative local filename. If a requested export filename already
exists or is too long for the host's temporary-name byte budget, Runtime keeps
the same root and chooses a deterministic association-scoped direct filename
rather than overwriting it or failing on the private staging sibling.

## Timeline commit ABI

`schemas/timeline-commit.json` defines detached ABI 1 envelopes and the complete
immutable closure. `schemas/edit-command.json` is the byte-identical Agent-owned
command schema pin, including recorder leaves; Runtime does not redefine them.
`python generators/generate.py` also emits the Runtime/Python TypedDict modules
and TypeScript commit types. These are plain JSON-shaped values, with no runtime
validation or renderer dependency. Acceptance validates finite JSON, closure
identity and recorder consistency separately; types alone do not grant authority.
Commit clients preserve the `{data, receipt}` envelope, including the distinct
preview status with a null receipt. Restore requires both current head pins.


The unpublished 0.2.13 candidate combines the connector and write-authorized,
keyed persisted views with the complete frozen Agent S2 command schema from
`26ef2bbb31b4892fdd7c15ee5b20700bd40cb933`, raw SHA256
`a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`
(48 definitions, 22 operations). S2 only adds the optional existing DocumentPin
`schema_source` to ClipSetElementArgs and updates its description. S1 remains
an immutable compatibility floor alongside Runtime 0.2.10, 0.2.3 and 0.2.2.
Normal generation checks the complete schemas before writing any outputs;
the 0.2.2 check proves the five explicit additive regex changes. Other rewrites
still require review. Source snapshots and provenance live in
`tests/fixtures/published-command-schemas/`.

After copying an authorized schema and updating `generators/release.json`, run
`python generators/generate.py`, normally regenerate the independent TypeScript
conformance client as described in the repository README, then run
`python scripts/artifact_manifest.py`. Run each generator again with `--check`.
This candidate does not publish a release or change consumer pins. Agent view
callers must adopt the explicit key and write authority together with the final
qualified client pin.
