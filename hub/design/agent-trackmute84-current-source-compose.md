# Agent track mute current-source handoff

Status: **SOURCE ONLY**. This is the unfrozen current-source composition for
the reviewed `452` track-mute proposal. It does not authorize Runtime/App
generation, pins, native adapters, activation, or any frozen artifact update.

## Exact source and schema

- Current private source floor: Agent commit `6a8dfb2286659dd67c108a230d24f14ba4599344`, tree `5f5449a2b668c96a9bc816cea1dd73eacc04f7ab`.
- Reviewed mute source: `45201ef4fdb330635ed99035f6eded65f07f88b4`.
- Reviewed full-source composition reference: `1c18c8c84cec366ce683349858fb2399435c9265`.
- The old `452`/`1c18` schema was not copied wholesale. The change is composed
  directly onto current private schema floor `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`.
- New canonical schema:
  `astrid/core/timeline/schema/edit-command.schema.json`
  SHA-256 `0f0b7e9356506f60f3058d35e67d52ee5ecc66002fb40d8772a0b13fc10e6890`;
  59 definitions, 33 operation clauses, 12 explicit v2 clauses.
- Changed source file hashes:
  - `astrid/core/timeline/schema/edit-command.schema.json`: `0f0b7e9356506f60f3058d35e67d52ee5ecc66002fb40d8772a0b13fc10e6890`
  - `astrid/sdk/timeline/_scalar_commands.py`: `5bd7760401f3b17d2bc8542b14e63a0ab19db60a2f072281dbc324d651104a88`
  - `tests/editing_conformance/test_recipe_track_scalar_fields.py`: `7998213e56be0ff12de449859c5feebd6fccb0104ca7676d8711f1836219e9f9`

## Bounded contract

Only the existing closed `track.set@1` carrier is extended:

```json
{"schema_version":1,"op":"track.set","version":"1",
 "select":"parent/track:<id>","args":{"values":{"muted":true},"clear":[]}}
```

```json
{"schema_version":1,"op":"track.set","version":"1",
 "select":"parent/track:<id>","args":{"values":{},"clear":["muted"]}}
```

`values.muted` is boolean-only. `null`, non-boolean values, unknown fields,
set/clear overlap, duplicate clears, and non-empty intent remain refused.
Clear removes the raw leaf; it never writes `false`, `null`, or a default.
Absent and explicit `false` remain distinct. The existing scalar recorder keeps
label, volume, active, owner, collection order, and opaque siblings intact;
capture retains the original exact leaf state and existing exact inverse,
rebase, equal-forward, strict-inverse, ABA, and v2 materialization behavior.

## Exact floor reconstruction

`tests/sdk/test_timeline_materialization_schema_union.py` now has
`without_mute(schema)`. It removes only `TrackSetArgs.values.muted`, restores
`clear.items` from `enum ["label", "muted"]` to `const "label"`, and restores
the prior description. Applying that strip to the new schema reconstructs
exactly `84fc...` with 59 definitions, 33 operation clauses, and 12 explicit
v2 clauses. All earlier ordinary, carrier, project-data, group, voiceover,
extent, and frozen-S2 floors remain checked; no old 58/32 schema is imported.

## Consumer handoff

- App2 and Runtime may review this exact current-source schema and the bounded
  merge-shaped commands above.
- A future consumer must not reinterpret App replace mode as mute clear.
- No Runtime/App/generated-client/pin/generation/activation file changed.
- Live callers: **NONE**.
- Prior bounded Runtime and App2 source ACKs for reviewed `452` remain the
  applicable compatibility evidence; this document claims no native or wire
  qualification.
