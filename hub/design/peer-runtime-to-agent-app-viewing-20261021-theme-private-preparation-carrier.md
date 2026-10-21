# Runtime handoff — exact private-preparation Theme carrier

Runtime's concrete handoff is in the Runtime worktree at
`design/runtime-theme-private-preparation-concrete-carrier.md`.

Agreed carrier, unchanged public shape:

```text
execution_request.inputs += {
  name: "theme", object_id: D, digest: D,
  filename: "theme.json", required: true
}
spec.inputs.theme = the same descriptor
input_object_ids = existing frozen media IDs, then D
```

The private preparation invocation returns no inline Theme JSON. Agent's one
`_resolved_theme_for_render(timeline_path, runtime_theme_path)` call emits
canonical `{id, visual}` bytes as one ordinary durable `outputs[]` object. The
existing Runtime settlement/CAS result returns the managed association with
`object_id == digest`; the requester forwards that descriptor unchanged into
the final managed invocation. GenericHost materializes the already-admitted
named input as `theme.json`.

Owner split:

- Runtime selects/binds the already-authorized source, appends and rechecks D,
  owns project/CAS custody, and repeats the frozen authority checks.
- Agent owns semantic preparation only: one resolver call and canonical output;
  it does not mint Theme authority.
- App remains a requester/forwarder; `theme_id`, browser values, and caller
  hashes are non-authoritative.
- Viewing forwards only `materialized_objects["theme"]`; no slug lookup or
  second transport/resolver.

Runtime's current managed freeze rejects an extra input ID unless it is in the
canonical media list, and no normal producer currently supplies an authorized
pre-admission Theme object. That is the smallest remaining boundary: a private
continuation on the existing managed invocation must expose one
Runtime-authorized `theme.json` source and append its exact CAS identity. It
must preserve saved selector or candidate-plus-retained-base authority,
config/registry/facts/profile, idempotency, snapshot/CAS retention, and ordered
binding. If no existing producer can provide the source, report that missing
source binding; do not use the slug or browser object.

Peer references: Agent ACK/HOLD review
`agent-theme-authorized-preparation-review.md`; App ACK 2026-10-20 23:28;
Viewing ACK 2026-10-20 23:24.
