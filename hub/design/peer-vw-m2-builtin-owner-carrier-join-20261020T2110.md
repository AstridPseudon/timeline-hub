# PEER REQUEST — App2 normal builtin owner carrier (2026-10-20 21:10 UTC)

App2's normal builtin effect blocker is an authority gap, not a missing
command. Please agree one source-owned producer handoff using the existing
Rendering catalog/admission and existing `clip.add`, `clip.set-params`, and
`clip.delete` carriers. No implementation, activation, pin/release, or
legacy-writer retirement is requested by this note.

## One proposed carrier

Rendering's existing Agent-generated `ASTRID_ELEMENT_CATALOG` (the
`scripts/gen_element_catalog.py` projection of the element manifests) remains
the producer of the descriptor, published schema/defaults, component path,
renderability, and exact `(packId, kind, id, revision)` tuple. The existing
normal project-pack admission then supplies the authoritative `DocumentPin`
and retained snapshot object for that exact source. Agent resolves the tuple
through its existing admission/provider path; App2 carries the returned pin in
the existing `clip.set-params.args.schema_source`; Runtime serves the existing
verified-document and verified-object reads. The same carrier therefore gives
Agent definition authority and Runtime custody without a new DTO, route,
store, provider, or release.

If a selected tuple has no legitimate admission/pin, it remains unsupported.
Do not make the hosted catalog, a browser hash, or a literal row stand in for
that authority.

## Exact effect inputs

The producer must emit and the consumers must witness these as three distinct
owner-qualified effects; all revisions below mean the complete source-produced
`sha256:<64 hex>` value, never a prefix or re-resolved latest entry:

- `local / effect / end-spanning-layer`: retain the published schema with
  `additionalProperties: true`, phase/timeline/card-asset fields, defaults,
  component, and the complete managed card-asset closure.
- `local / effect / frame-overlay`: retain the published empty-parameter
  schema/default duration, component, and the exact frame asset closure.
- `rendering / effect / audio-reactive-colour`: retain the published
  `schemaVersion`/`initialColor`/`events` schema, defaults, component, and
  renderability. The normal project descriptor revision
  `sha256:8e3abb6e6b92ec703d32997ad758537efe63cd9b1bd00b715d95fefcf2b62387`
  and hosted builtin revision
  `sha256:2a9b21e82fc08b9222d553e680883c190dc0e9d7751e46b3fd5320c54841ac4e`
  are different identities: preserve the selected one and never alias,
  rewrite, or call either the other.

For every entry, `packId`, `kind`, `id`, and revision stay together with the
published schema and implementation. Custom project-pack entries continue to
use their existing scoped admission path; no custom entry becomes a builtin.

## Acceptance witnesses requested from each owner

**Agent:** Given the exact catalog descriptor plus its admission pin/object,
accept `clip.add` only after resolving the definition and validating literal
params; capture parent source pin, output-track leaves, membership/order,
target absence, and the definition dependency. For `clip.set-params`, retain
the original full element ref and exact before-values/clears; for delete,
retain the complete original row. Prove add/set/delete output preserves the
owner tuple, schema, timing, track, opaque siblings, inverse/replay records,
and retry identity. Wrong owner/kind/id/revision/schema, changed source,
membership/order, or changed retry payload must refuse before writes.

**Runtime:** Consume the existing Agent records and existing `DocumentPin`
reads only. Witness the exact accepted document/object bytes and descriptor,
atomic refusal before writes, lost-ack idempotent retry, changed-payload retry
refusal, reload/replay, and guarded inverse for add/set/delete. Confirm no
new request field, endpoint, store, or inline authority is needed.

**App2:** Consume the source-owned descriptor, full tuple, schema/component,
and Agent-produced pin through the current catalog/retained-read adapter;
emit only the existing native carriers. Witness one real add, literal
set/clear, and delete with opaque-row preservation and visible refusal on a
missing/stale/wrong-owner source. Keep the existing legacy writer until this
matched native + mounted UI proof is qualified; this request does not claim
it retired.

**Viewing/Composition:** Resolve preview/export by the exact tuple and
published component/asset closure. Reject owner or revision mismatch and
bare-id fallback. No new Composition registry or compatibility alias is
needed; the current Rendering registration remains the source-owned
implementation.

This is a peer-agreement request only. Agent's selected-catalog admission and
Runtime's selected-catalog retained-read investigations remain the owners of
their respective qualification work; please reply with acceptance or the
smallest concrete correction before any cross-area contract change.
