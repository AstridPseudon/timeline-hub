# Runtime voiceover4d source review — SOURCE ACK

Date: 2026-10-20 UTC  
Worker: `rt-m2-review-voiceover4d-source-boundary`

## Verdict

**SOURCE ACK** for the committed Agent source/schema only.

The exact reviewed candidate is Agent commit
`4d4535882f1e028805c3da178bf9a7fa53696da8`, tree
`f18245ced9c231ddf8f6f2ee64405a84d3517921`. Its semantic source parent is
`644fd1111f84a91c159064950eb73dcd921c81e3`, tree
`6cac36698e0ece0343c10c1a347a59a243cbe80d`. The final commit changes only
`tests/sdk/test_timeline_materialization_schema_union.py`; the product and
schema bytes are identical to the semantic parent.

The canonical schema is
`astrid/core/timeline/schema/edit-command.schema.json`, SHA-256
`84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`:
59 definitions, 33 operation clauses, and 12 v2 clauses. Runtime’s current
public schema remains the separate S2 artifact; this ACK does not claim that
artifact, a generated private successor, or a public pin.

## Source/schema findings

- `occurrence.resize@1` is closed to an exact-root occurrence selector and a
  positive integer `duration_ms`. The handler requires a stable occurrence and
  shot identity, reads the existing `MAP_FIELDS` timing codecs, and writes only
  `occurrence.duration_ms`. It does not quantize, normalize, retrack children,
  rewrite parent extent, or persist padding.
- `occurrence.move@1` retains the existing `{on, track, child_track}` branch.
  The additive branch is mutually exclusive exact-root `start_ms`, an integer
  with minimum zero. The handler writes authored `placement.start_ms` and an
  existing `at_ms` mirror only; it does not pass through frame quantization or
  retrack child clips. `root_identity()` rejects nested paths and ambiguous
  `::` identities. Existing lane/child-lane behavior is unchanged.
- Voiceover lowering performs `_validate_source_identity()` before any timing
  or media capture. It compares project/timeline/base containers and
  `source_mapping`, preserves occurrence membership/order and IDs, resolves
  each captured source shot, and checks prepared source/revision identity
  fields against the captured shot pin. A stale prepared source therefore
  refuses before the first command is captured.
- The supported ripple fixture lowers literal authored values `10000 -> 4150`
  ms and `20000 -> 14150` ms, both `-5850` ms, with derived visual hold
  `0.415` s. Unrepresented parent/child timing changes refuse. No
  `padding_seconds` field is authored, stored, or emitted.

The corrected floor reconstruction consumes the exact frozen hashes:

```text
65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e  voiceover
27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb  group
39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d  project-data
613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3  carrier
6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d  ordinary
```

## Independent evidence

The final commit was archived into a private temporary directory; no Agent
worktree or shared dependency was changed. Using
`/home/user/work/venv-agent/bin/python`, `PYTHONDONTWRITEBYTECODE=1`, and
`-p no:cacheprovider`:

```text
pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_materialization_schema_union.py
22 passed in 1.04s

pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_occurrence_resize.py
14 passed in 0.70s

pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_native_voiceover.py
9 passed in 2.39s

pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_m2_group_move.py
29 passed in 3.08s
```

The 9 native voiceover cases include both source-bound timing witnesses; the
committed handoff’s prior evidence of 14 identity negatives was reviewed and
the final source-level identity guards were independently exercised by the
native and resize controls above. No full, integration, HTTP/door, renderer,
audio, or browser suite was run.

## Explicit boundary

This is a reciprocal Runtime **source/schema** ACK only. It does not approve
managed audio admission, the actual outer
`video_editing.sync_draft_voiceover` producer/requester/settlement path, a
settled artifact, pinning, generation, native HTTP qualification, App
consumption, activation, release, or writer retirement. Runtime manager owns
any future private generation, freeze, pairing, and release decision.

No executable source/schema incompatibility was found.
