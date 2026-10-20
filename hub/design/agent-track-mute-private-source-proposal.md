# Agent bounded track mute private source proposal

Status: **SOURCE ONLY — Runtime and App 2 bounded source review required before
generation or native consumer activation.** This candidate does not change
generated clients, Runtime pins, App writers, public artifacts, or the frozen
current 392 artifact.

## Exact candidate identity

- Base commit: `d30894a7abfa6e3163c13a59175b4a0d298c7fea`
- Candidate final commit: 45201ef4fdb330635ed99035f6eded65f07f88b4
- Candidate source tree: `77a91bb81761a7cf4a2c6199e01b494e62a8f49f`
- Canonical schema: `astrid/core/timeline/schema/edit-command.schema.json`
- Previous current-main schema SHA-256: `a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef`
- Candidate schema SHA-256, recomputed from the committed ref: `6826fc7d8cec337f6c015db21b0a223ec4a438a18204e4e07f6fca91f594c0b7`
- Changed source file SHA-256 values:
  - `astrid/sdk/timeline/_scalar_commands.py`: `84b09f7fa0a0a6ae824bc64ca4e8e7e54ae4cce5e73e759bfcfff1cb231cea91`
  - `tests/editing_conformance/test_recipe_track_scalar_fields.py`: `7998213e56be0ff12de449859c5feebd6fccb0104ca7676d8711f1836219e9f9`
- Tracked source/schema diff SHA-256: `e9a1417953bf87ca4a9ec5fece8bb554be1e0660b955db2cbd73ef800a100db0`

The prior current-main schema floor and all published fixture bytes remain
unchanged. The separate frozen current 392 source identity
`39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d` was not
edited or regenerated.

## Main semantics and bounded contract

Main declares `TrackDefinition.muted?: boolean`. Main's merge-mode
`track.update` copies only the top-level `muted` member when supplied; an
absent member remains absent in authored state. Main rejects `null` and other
non-boolean new values. Main's reader may default absent mute for display, but
this Agent source does not normalize authored state.

This proposal extends only the existing closed `track.set@1` carrier:

```json
{"schema_version":1,"op":"track.set","version":"1",
 "select":"parent/track:<raw-id>",
 "args":{"values":{"muted":true},"clear":[]},"intent":{}}
```

```json
{"schema_version":1,"op":"track.set","version":"1",
 "select":"parent/track:<raw-id>",
 "args":{"values":{},"clear":["muted"]},"intent":{}}
```

- `values.muted` is boolean only; `null`, numbers, strings, unknown fields,
  set/clear overlap, duplicate clears, and non-empty intent are refused.
- `clear: ["muted"]` removes the raw leaf. It never writes `false`, `null`,
  or a default.
- Existing `label` set/clear forms remain unchanged.
- The existing selector/recorder supplies the stable target identity,
  explicit owner binding, parent/source dependency, exact raw leaf
  expectation, authorship, inverse, retry, and replay guards.
- Each proposed mute command performs one leaf write/clear through the
  existing handler; it never replaces the track row. Opaque
  label/kind/role/opacity/volume/app/unknown siblings and parent config
  survive unchanged.

App 2 and Runtime must review and pair this exact source contract before a
generated schema/client or native mute adapter is produced. The consumer must
emit only the bounded merge-shaped commands above; Main replace mode must not
be reinterpreted as mute clear.

## Evidence

Focused tests cover Main-shaped capture/golden fields, absent/null/bool raw
presence, exact inverse/redo, occurrence owner binding, stale same-property
refusal, disjoint label replay, opaque sibling preservation, and closed-args
refusal.

No Runtime/App generation, pin, activation, full suite, browser/socket
journey, or frozen artifact update was performed.
