# Private voiceover source handoff — corrected and committed

Date: 2026-10-20 22:46 UTC

## Status

The corrected private Agent source is ready for bounded Runtime/App2 source
review. This handoff contains no code change or generation. The final commit
is the test-only successor of the semantic source:

- final committed ref: `tl/agt-m2-voiceover-schema-reconstruction-order-fix`
- final commit: `4d4535882f1e028805c3da178bf9a7fa53696da8`
- final tree: `f18245ced9c231ddf8f6f2ee64405a84d3517921`
- semantic source commit: `644fd1111f84a91c159064950eb73dcd921c81e3`
- semantic source tree: `6cac36698e0ece0343c10c1a347a59a243cbe80d`

The final commit changes only
`tests/sdk/test_timeline_materialization_schema_union.py`: it applies extent
stripping before group stripping and records the current extent hash. Product
and schema bytes are byte-identical to `644fd1111`; no old artifact was
mutated.

The complete current schema is
`astrid/core/timeline/schema/edit-command.schema.json`, SHA-256
`84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`.
It has **59 definitions**, **33 `EditCommand` operation clauses**, and **12
v2-versioned operation clauses**. The reviewed source-bound operation set is
13 operations; `track.create` is the v1-only member, so it is not counted in
the v2 clause total.

Source blobs in the final committed tree:

```text
c5aaacf98be9817f5b65dd5de7e889d0a1f483cc  astrid/sdk/timeline/native_voiceover.py
9c44c8004a0c16f6adba655c1f52d8177d24dd75  astrid/sdk/timeline/native_occurrence_resize.py
c397d6b7e424668180317980e68f79a9687783af  astrid/sdk/timeline/occurrence_commands.py
6a2285400e3f7f08a927e175c2f81d8f2550c973  astrid/core/timeline/schema/edit-command.schema.json
6ac53c517af4fa74b8116f5a704b31c8ef1f71bf  tests/editing_conformance/test_recipe_native_voiceover.py
39d31cdcf5d001f4888af4069b407a30b16e4054  tests/sdk/test_timeline_materialization_schema_union.py
```

## Closed timing carriers

The prepared ripple result is lowered as literal authored commands:

- `occurrence.resize@1`: the edited occurrence duration is **10000 ms ->
  4150 ms**, delta **-5850 ms**.
- `occurrence.move@1`: the following occurrence `start_ms` is **20000 ms ->
  14150 ms**, delta **-5850 ms**. The command writes the exact root
  `placement.start_ms` and preserves the agreeing `at_ms` mirror when present;
  it does not quantize through the frame clock or retrack child clips.
- The derived visual hold is **0.415 s**. Parent duration is unchanged in this
  supported prepared fixture; an unrepresented parent-duration change refuses
  before any partial result.

`occurrence.resize` is closed to a positive authored integer `duration_ms`.
`occurrence.move` is closed to an exact-root nonnegative integer `start_ms` and
retains the existing `{on, track, child_track}` form. Neither operation is a
generic placement or child-timing writer.

## Prepared source/base guards

The lowerer is fail-closed against replacing the original prepared source.
Before timing or media capture it requires exact equality of the captured and
prepared `project_id`, `timeline_id`, `base_parent`, `base_parent_payload`,
and `base_placements`; both `source_mapping` values must be mappings and
exactly equal; the captured source shot map must exist; and placement count,
order, `occurrence_id`, and `shot_id` must remain unchanged. Each placement
must resolve to its captured source shot. Prepared stale, wrong, missing, or
foreign source/base/placement identity mutations refuse before capture and do
not mutate either authored or prepared input. The normal Main prepared result
passes with the original source/base guards unchanged and no guard write.

The completed review evidence is **14 identity negatives passed**, **9 native
voiceover tests passed**, and **2 final timing witnesses passed**. The timing
witness includes exact 4150/14150/0.415 values, replay, inverse/redo,
materialized reload, sibling isolation, and metadata preservation.

## Derived-only padding policy

`padding_seconds` remains a prepared-result input used to derive literal
timing. It is not an authored field, metadata leaf, schema addition, source
mapping, placement mirror, parent config field, or Runtime/App carrier. The
lowerer records the resulting literal duration/move/hold effects only; it
does not persist or recompute a padding field. The completed witness confirms
no `padding_seconds` in the capture, authored metadata, or recorded write
paths, while existing metadata siblings remain exact.

## Exact schema reconstructions

The corrected floor test passed all frozen reconstructions on a deep copy; no
frozen artifact or public schema was edited:

| reconstruction | exact SHA-256 | meaning |
| --- | --- | --- |
| complete current extent source | `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5` | current 59-definition / 33-op source |
| remove extent additions | `65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e` | voiceover floor |
| remove voiceover leaf from that copy | `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb` | group floor |
| remove group additions, retain project-data addition | `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d` | project-data floor |
| additionally remove project-data addition | `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3` | private carrier floor |
| remove all reviewed carrier additions and v2/reference deltas | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` | ordinary source floor |

The exact successor check was **13 passed, 9 deselected**. No test replay is
claimed in this handoff; these are completed results from the successor and
corrected-source review.

## Qualification boundary

This is a private Agent source handoff only. It does not claim Runtime managed
audio admission, native HTTP/door pairing, normal outer requester admission,
settled `authoring_proposal`, pinning, generation, App2 UI/HTTP consumption,
or a native producer claim. `generation.generate_speech` and any inner audio
artifact remain distinct from the outer voiceover workflow. No fake source
metadata, public pin, old artifact mutation, outer settlement, or activation
is authorized. Runtime and App2 must ACK these committed bytes explicitly
before manager freeze and normal counterpart generation.
