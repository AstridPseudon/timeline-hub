# Agent occurrence extent source contract

Status: **PRIVATE SOURCE PROPOSAL — Runtime/App2 contract ACK required before
generation, pin, release, Runtime pairing, or consumer activation.** This
proposal adds no Runtime DTO, endpoint, store, public pin, activation, or
producer/generation behavior.

Published: 2026-10-20T21:47:55Z (UTC)

## Exact source

Base: `tl/agt-m2-voiceover-native-command-builder`, Agent HEAD
`1cea89a17`.

- Schema: `astrid/core/timeline/schema/edit-command.schema.json`
  SHA-256 `166644a84067b4f40fe6cc4a0d0047cfe2e4fb2678ca1d7b2fc9d48c605cfa41`
- Handler: `astrid/sdk/timeline/native_occurrence_resize.py`
  SHA-256 `fad7f6db9fdf65ade0ed1df05343519ea495e118f2fc39d33153600ed1ff1c38`
- Registry: `astrid/sdk/timeline/commands.py`
  SHA-256 `d6172dd2511aed829ed95d4702e431a325503acd488a3ec72bedea5862eee10f`
- Witness: `tests/editing_conformance/test_recipe_occurrence_resize.py`
  SHA-256 `12c9fa40d3f7510adda083da6181153150de7b9b661ad1285adc693202eb74e8`
- Floor control: `tests/sdk/test_timeline_materialization_schema_union.py`
  SHA-256 `704be67a96003c8d316ae04b9ca99b688c68de2558595cdb08bd212464e28f3f`

## Closed command

The private operation is `occurrence.resize@1`:

```json
{
  "schema_version": 1,
  "op": "occurrence.resize",
  "version": "1",
  "select": "occurrence:<stable-occurrence-id>",
  "args": {"duration_ms": 4150},
  "intent": {"ownership": "occurrence"}
}
```

`duration_ms` is the exact stored Main field: a finite, positive authored
integer count of milliseconds. Missing, `null`, zero, negative, fractional,
boolean, and non-finite values are refused. The operation does not accept
seconds, floats, rationals, inferred owners, display IDs, child selectors, or
absence/null as a clear policy; Main has no valid absent/null occurrence
duration. Existing raw rational timing codecs (`source_offset`, `speed`) and
all `MAP_FIELDS` are read as the current basis and preserved byte-for-byte;
there is no quantization, normalization, root replacement, array replacement,
or parent extent write.

The selector must resolve to one canonical occurrence. The recorder reads the
occurrence ID, shot ID, optional shot revision ID, occurrence collection and
`placement.owners` selection, then writes only `occurrence.duration_ms`.
Shared occurrences and legacy pinned groups fail closed at the existing
materialization/migration boundaries. The existing recorder supplies exact
before/after expectations, inverse/redo, ABA/intervening-write refusal, and
disjoint replay.

## Source-floor reconstruction

The current candidate is 59 schema definitions and 33 operation clauses. The
following exact reconstructions are asserted by the floor test:

- Remove only `OccurrenceResizeArgs` and its `occurrence.resize` clause:
  voiceover floor `65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e`.
- Remove the voiceover metadata leaf as well:
  group floor `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`.
- Remove group, project-data, voiceover, and extent additions:
  immutable ordinary floors `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`,
  `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`, and
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.

## ACK request

Runtime/App2 should ACK this exact source/schema and the floor reconstruction
before any generation, freeze, pin, release, Runtime pairing, or consumer
activation treats the carrier as available. The original voiceover behavior
suite remains unchanged; this carrier covers only the existing occurrence
extent scalar and does not claim the separate parent ripple/padding carriers.
