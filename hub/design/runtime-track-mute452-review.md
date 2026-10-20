# Runtime source review: Agent track mute 452

## Decision

**SOURCE ACK.** Agent candidate `45201ef4fdb330635ed99035f6eded65f07f88b4`, with
schema SHA-256 `6826fc7d8cec337f6c015db21b0a223ec4a438a18204e4e07f6fca91f594c0b7`,
is compatible with the bounded Runtime/App2 carrier review. No Runtime code,
generated artifact, schema pin, native adapter, or frozen `current392` artifact
should change as a result of this ACK.

## Verified source contract

- The candidate changes only the Agent `track.set@1` source schema, its scalar
  capture docstring, and focused conformance tests. `values.muted` is a raw
  boolean leaf write; `clear: ["muted"]` removes the raw leaf.
- Main's canonical top-level track shape declares `muted` as optional
  `boolean`: `TrackDefinition` is `total=False`, and
  `astrid/core/timeline/schema/timeline-config.schema.json` requires only
  `id`, `kind`, and `label` for a track. Absent, `false`, and `true` are valid;
  `null` is invalid. The authored source therefore preserves absence and does
  not normalize a missing leaf to `false`.
- The existing scalar handler writes/clears one leaf and retains the existing
  target identity, owner/source dependency, exact raw-leaf expectation,
  authorship, recorder, inverse, retry, and replay guards. The candidate tests
  cover the absent/present states, opaque sibling preservation, inverse/redo,
  stale same-property refusal, disjoint label replay, and occurrence owner
  binding. Existing `label`, `volume`, `active`/other unsupported siblings, and
  opaque data are not replaced by the one-leaf operation.
- App2's existing `track.update` merge behavior copies only supplied scalar
  fields, including top-level `muted`, and preserves unspecified siblings.
  App2 replace mode remains a separate whole-mutable-field operation; it must
  not be reinterpreted as `track.set` mute clear. App2's validator rejects
  non-boolean `muted` values.

## Runtime boundary

No extra Runtime port, endpoint, request envelope, provider ABI, or DTO family
is required. Runtime's existing `/v1` timeline commit request carries the
Agent `EditCommand`; the port and recorder are already generic over command
leaf writes and tagged absent/present states. The current Runtime worktree
still intentionally pins the prior public schema SHA-256
`a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`; that is
correct for this source-only review and must not be changed here.

One schema nuance is inherited from the existing label carrier: JSON Schema
admits a set/clear overlap, while the Agent scalar handler rejects overlap
before execution. This is not a new Runtime mismatch; the candidate's focused
handler contract retains the established behavior.

## Evidence

Probe command (read-only, no files written):

```text
python - <<'PY' ... Draft202012Validator(candidate edit-command schema) ... Draft7Validator(Main timeline-config schema) ... PY
```

Result:

```text
set-true: True
clear: True
null: False
schema-overlap-admitted: True
main-absent: True
main-false: True
main-true: True
main-null: False
```

The existing 113 Agent focused tests were not rerun per task scope. No full,
browser, socket, native, generation, pin, normal-artifact, or `current392`
qualification was run.

## Future floor

This ACK is for the unfrozen sibling source only. Any later composition or
qualification must compose it onto the full `392` floor and preserve all
`current392` semantics and fixture bytes. It is not a replacement for
`current392`, and no mutation of that artifact is authorized by this review.
