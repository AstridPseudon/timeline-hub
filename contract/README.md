# Workspace protocol contracts

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
Astrid, REIGH, or product-specific types.

The protocol uses a clean, digest-pinned version (`workspace.v1`).  A client
must complete the handshake before using any non-health operation.  Every
state-changing request carries an idempotency key and mutating resources expose
an opaque `version` for optimistic concurrency.

Task admission may include an immutable `storage_estimate` derived from the
same canonical input snapshot as the task spec. `scratch_bytes` is the peak
additional temporary space needed while the task runs; `output_bytes` is the
maximum final output written before temporary data is released. The runtime
checks their sum against current free space at admission and again at claim.
When the field is absent, registered **static** capability estimates remain the
backward-compatible fallback. A request-estimated descriptor requires the exact
pair in the existing task envelope. Both integers and their sum must fit
0..2**53-1. Runtime validates identity and numeric bounds; the source-fenced host
owns estimator recomputation and equality before producer work.

`GET /v1/capabilities?catalog_version=2` returns `catalog_version: 2` alongside
`items`/`next_cursor`. Each row replaces the two legacy numeric fields with
`storage_estimate`: `{mode: "static", scratch_bytes, output_bytes}`,
`{mode: "request_estimated", estimator: {id, version, implementation_digest}}`,
or `{mode: "unavailable", reason}`. The optional `storage_estimate_contract` on
an executor capability descriptor declares that same shape; legacy descriptors
remain static. Metadata persists in existing executor descriptors, matched by
exact capability ID and digest. Conflicting declarations refuse readiness.
Standalone capability registration remains static and rejects that field.

Default catalog v1 keeps static rows unchanged and reports request-estimated
rows as `unsupported` with `request_estimated_requires_catalog_v2`. V2 preserves
the estimator identity but currently reports `unavailable` with
`request_estimator_execution_not_integrated`. Registration and claim also refuse
readiness for these rows; this Runtime increment does not enable production
execution pending admitted producer preparation and host recomputation. Catalog
versions other than 1 or 2 refuse with HTTP 422 `validation_error`.

Health and handshake advertise `operation_versions`, generated from the full
OpenAPI inventory. The explicit `info.x-operation-version` is the legacy
workspace.v1 singleton default; `x-operation-versions` on an operation declares
an exact finite supported set (a scalar normalizes to a singleton). A requirement
for v1 matches `[1, 2]` and does not match `[2]`. `schema_digest` remains the exact
source digest, independently of semantic compatibility. Both routes report the
same runtime epoch/session and daemon instance identity. Compatibility metadata
never grants an authenticated route, project, actor, or write permission. Client
baseline/optional feature gates and any verified legacy digest mapping remain
consumer-owned; no 16bb fallback is supplied here.

## Astrid binding

Astrid binds a typed task family, project identity, ordered CAS/input
references, and idempotency key to a Runtime-owned workspace task and run.
Workers claim and settle that work through the Runtime contract. Settlement,
output provenance, receipts, and event history remain Runtime-owned and are
the canonical readback surface for Reigh's gallery and timeline consumers.
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
