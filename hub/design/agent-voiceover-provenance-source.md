# Agent voiceover provenance property source

Date: 2026-10-20 (UTC)

Status: private Agent source proposal for cross-area ACK. This slice does not
retire WC5 and does not claim a completed outer producer settlement.

## Exact authored leaf

The existing `shot.set` command now accepts the closed property carrier:

```text
args.values.metadata.draft_voiceover
args.clear: "metadata.draft_voiceover"
```

The value is either a JSON object or explicit `null`; `clear` removes the leaf.
The command never accepts an arbitrary metadata key or replaces the metadata
root. It writes only `payload.metadata.draft_voiceover`. Existing sibling,
unknown, and namespaced metadata fields remain untouched. The normal command
validator still rejects non-finite JSON, and the recorder's JSON equality keeps
booleans distinct from numbers.

## Owner, source, and schema identity

- Owner semantics remain explicit occurrence ownership:
  `intent.ownership == "occurrence"`, selected by
  `occurrence:<id>/shot`. Shared ownership is not inferred or accepted. The
  existing occurrence and shot identity reads, `shot.owner` binding, exact
  source dependency, and source-bound materialization guards remain in place.
- Source fixture: the original `tests/packs/video_editing/test_draft_voiceover.py`
  `fixture`/`synthesis` outcome, including its text, text digest, settings,
  generated audio identity, run/task IDs, and base-head information. The
  outcome is lowered through the recorder in
  `tests/editing_conformance/test_recipe_shot_set.py`.
- Reviewed base: `c0644cf1a7b63c9bcff7f70502b953a07879c9f3`.
- New complete schema candidate SHA-256:
  `65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e`.
  The prior group candidate remains reproducible as
  `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb` after
  removing this property. The older `392`, `613`, and `6ba` floor hashes remain
  unchanged and are tested as such.

The metadata is authored informational data only. Runtime producer authority
continues to come from the existing guard/receipt path; this leaf cannot
authorize a producer, media, task, run, or publication.

## Remaining extent/audio blockers

This change does not lower the rest of the original voiceover candidate. The
current native command set still lacks an exact generated-audio source/duration
carrier and a native placement/parent ripple retiming command. Consequently,
the original audio materialization and `ripple` extent edits remain open; the
metadata leaf can be carried independently but cannot stand in for them.

The outer voiceover handoff also remains blocked on the actual normal Runtime
admission/requester proof: the current continuation path requires its exact
dependency shape. No Runtime restriction, producer authority, endpoint, DTO,
approval path, or legacy writer was changed here.
