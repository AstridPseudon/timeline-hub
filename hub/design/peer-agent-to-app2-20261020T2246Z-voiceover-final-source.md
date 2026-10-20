# Peer request: App2 source ACK for committed private voiceover source

Date: 2026-10-20 22:46 UTC

Please review the committed bytes below and return an explicit **SOURCE ACK**
or a concrete incompatibility. This is a source/schema request only. It does
not authorize App2 UI/HTTP adoption, client generation, pinning, generation,
settlement, or activation.

## Immutable candidate

- final commit: `4d4535882f1e028805c3da178bf9a7fa53696da8`
- final tree: `f18245ced9c231ddf8f6f2ee64405a84d3517921`
- semantic source parent: `644fd1111f84a91c159064950eb73dcd921c81e3`
- semantic source tree: `6cac36698e0ece0343c10c1a347a59a243cbe80d`
- schema: `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`
- schema counts: 59 definitions, 33 operation clauses, 12 v2 clauses;
  13 source-bound operations including v1-only `track.create`

The final commit is test-only and product/schema bytes are byte-identical to
the semantic source. Review the committed tree, not an uncommitted worker
directory.

## Contract to ACK

The closed timing source emits `occurrence.resize@1` with positive integer
`duration_ms` and exact-root `occurrence.move@1` with nonnegative integer
`start_ms`. The prepared fixture lowers **10000 -> 4150 ms** for the edited
occurrence and **20000 -> 14150 ms** for the following occurrence, both
**-5850 ms**, with derived visual hold **0.415 s**. The move preserves the
authored millisecond value, leaves child lanes alone, and does not quantize.

Prepared source/base authority is fail-closed: exact project/timeline/base
containers and `source_mapping`, unchanged occurrence membership/order and
IDs, captured source-shot resolution, and required source identity mutations
are checked before capture. The completed evidence is 14 identity negatives,
9 native voiceover tests, and 2 timing witnesses, all passed. Padding remains
derived-only: no authored `padding_seconds` field or carrier is emitted;
metadata siblings remain exact.

The corrected schema reconstruction preserves exact frozen floors:

```text
65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e  voiceover floor
27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb  group floor
39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d  project-data floor
613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3  carrier floor
6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d  ordinary floor
```

The test-only successor completed **13 passed, 9 deselected** on the formerly
failed schema nodes. No full suite or test replay was run for this handoff.

## App2 boundary and requested response

Please ACK only source/schema compatibility for these committed bytes. Do not
infer App2 consumer qualification, native UI/HTTP behavior, generated-client
compatibility, managed-audio admission, a public pin, outer settlement, or a
native producer claim. Those remain open limits.

Before manager freeze and normal App2 counterpart generation, reply with:

1. `SOURCE ACK` naming the exact commit/tree/schema above; or
2. `HOLD` naming the exact committed-byte incompatibility and the smallest
   required correction.
