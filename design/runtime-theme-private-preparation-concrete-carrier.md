# Runtime M3 theme private-preparation carrier

Status: concrete handoff, implementation held until the four owners use this
same carrier. Agent, App, and Viewing have ACKed the boundary in the peer notes
listed below. This is a private continuation of the existing managed render
invocation; it is not a route, public DTO, provider, store, schema, or second
resolver.

## Carrier decision

Use the existing named file input at both existing admission layers:

```json
{
  "name": "theme",
  "object_id": "sha256:<digest>",
  "digest": "sha256:<same-digest>",
  "filename": "theme.json",
  "required": true
}
```

The scheduler-facing copy is `execution_request.inputs`; the capability-facing
copy is `spec.inputs.theme`. The task's ordered `input_object_ids` must mirror
the `execution_request.inputs` object IDs exactly, with the theme object added
after the frozen canonical media IDs. Runtime already enforces this mirror in
`runtime_protocol/store.py:_normalize_execution_request()` (428-479), and the
worker binding projects the same ordered names and IDs in
`runtime_protocol/remote_worker_deployment.py:_spec_input_bindings()` (597-651,
710-728). The existing Agent pack declares `theme` as a file input
(`astrid/packs/rendering/pack.yaml:904-912` in the frozen candidate).

The result is not inline Theme JSON. The private preparation invocation settles
one ordinary CAS-backed object result in the existing `outputs[]` settlement
field: JSON bytes, `filename: "theme.json"`, `media_type: "application/json"`,
`output_port: "theme"`, `role: "result"`, and durable lifecycle. Runtime's
existing `_stage_outputs()` and `_associate_managed_outputs()` validate and
publish those bytes (`runtime_protocol/service.py:7778-8033`,
`runtime_protocol/store.py:5312-5422`). The existing task result then exposes
the retained association (`runtime_protocol/store.py:3212-3244`); its
`object_id` and `digest` are the same CAS identity, and the SDK's existing
`InvocationResult.outputs.managed_outputs` exposes the same row
(`astrid/sdk/results.py:157-183, 234-273`). The requester forwards that row as
the named descriptor above. No raw bytes, caller hash, or new result DTO is
needed.

## One managed preparation and its authority

The requester invokes the normal managed `rendering.render` path with its
existing `project`, `timeline_ref`, profile, facts, idempotency identity, and,
for a working preview, the existing candidate plus retained base binding. The
private entry is the already existing SDK internal-dispatch seam
`_invoke_internal_result(..., _include_internal=True)`
(`astrid/sdk/invocation.py:3781-3839, 4419-4475` in the frozen candidate), not
a new capability or public mode.

At Runtime, the continuation runs through
`RealmStore._freeze_managed_render_inputs()` and `create_task()`:

1. Runtime resolves the project-scoped timeline and freezes projected
   `config`/`registry`, canonical media IDs, and `timeline_authority`
   (`runtime_protocol/store.py:1741-1805, 2001-2172`). The authority includes
   project/timeline identity, config version, head event/hash, config/registry
   hashes, parent revision/content digest, dependency digests, snapshot digest,
   publication, and managed media admissions (`store.py:2135-2166`).
2. `rewrite_spec_snapshots()` keeps the existing snapshot CAS publication and
   project association (`runtime_protocol/snapshot_refs.py:142-220`). The
   private continuation supplies the already Runtime-authorized `theme.json`
   source to the managed host alongside this frozen snapshot; it does not
   accept `theme_id`, a slug lookup, inline browser JSON, or a caller digest.
3. GenericHost materializes the admitted named input under the attempt-owned
   root. The worker receives only that file, the frozen timeline/config/facts,
   profile, and normal execution binding. It receives no project API scope and
   never receives `projects:write`; Runtime remains the sole project/CAS
   publisher. The Agent task adapter passes the existing materialized `theme`
   file to the renderer, as already required by the existing named-input
   boundary.
4. Agent calls exactly once:
   `_resolved_theme_for_render(timeline_path, runtime_theme_path)`.
   That function accepts only the attempt-local `theme.json`, merges the
   frozen timeline's `theme_overrides`, and returns the complete `{id, visual}`
   value (`astrid/packs/rendering/shared/rendering_backend/__init__.py:62-123`).
   Agent canonicalizes those bytes and emits the ordinary CAS object result.
   The slug is metadata only; no second resolver or ambient checkout lookup is
   permitted.

The current Runtime cannot select this pre-admission source from the timeline:
`theme` is only a slug and the normal managed freeze currently rejects an
extra input ID when it does not equal the canonical media list
(`runtime_protocol/store.py:2105-2117`; schema witness:
`runtime_protocol/schemas/timeline-commit-bundle.json:4760-4764`). Therefore the
smallest concrete Runtime boundary is one private continuation in the existing
managed invocation that (a) obtains one already-authorized project Theme
object, (b) appends its exact ID to the frozen ordered input list, and (c)
returns it through the existing CAS result path. It must not become a new
source-selection API. If no existing producer can provide that object, Runtime
reports the missing producer/source binding rather than treating the slug as
authority.

Before final render acceptance, Runtime repeats the existing checks, not a
Theme-specific authority system: project association and CAS byte/size/digest;
the exact ordered `input_object_ids`/named descriptor; the frozen
`timeline_authority`; normalized `required_facts`; selected profile and host
readiness; idempotency/replay identity; and the same saved selector or closed
candidate/base binding. Saved and working-copy snapshot provenance remains
`prepare_snapshot()`'s revision check or working-copy base check
(`runtime_protocol/snapshot_refs.py:114-139`), with capture validation retaining
the candidate plus base requirement. A CAS-only or base-less candidate is not
certified.

## Owner split / peer ACKs

- **Runtime:** select/bind the already-authorized source, own `input_object_ids`,
  named descriptor admission, project/CAS publication, and final recheck.
- **Agent:** own the private semantic preparation; call the one resolver once,
  canonicalize `{id, visual}`, and return the existing managed output row. It
  does not mint authority.
- **App:** requester/forwarder only. Preserve the existing managed invocation,
  candidate/base and idempotency fields; forward the returned descriptor. Its
  `theme_id`, browser-resolved value, and client hash are never authority.
- **Viewing:** consume only `materialized_objects["theme"]`/`theme.json` in the
  existing task adapter. No slug lookup, second transport, or source rule.

This matches Agent's ACK/HOLD review, App's 2026-10-20 23:28 ACK, and Viewing's
2026-10-20 23:24 ACK in the orchestration design/hub. Until Runtime supplies
the bounded pre-admission source carrier, explicit-theme parity remains
uncertified and the existing default fallback is unchanged.
