# App2 bounded source contract review: voiceover complete-root timing

Status: **HOLD**. The exact requested Agent candidate does not satisfy the
source guards, so this review is not a SOURCE ACK and authorizes no App
consumer work.

## Exact bytes reviewed

- Agent commit: `0700acf090143e5e1f8dc58a53594856d0c3feeb`
- Agent tree: `f86843e1817efde27ca36018ecd132b403c255eb`
- Schema SHA-256: `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`
- `native_occurrence_resize.py`: `fad7f6db9fdf65ade0ed1df05343519ea495e118f2fc39d33153600ed1ff1c38`
- `occurrence_commands.py`: `8ace5a9aaa05a6e6549e29e34ec305319f29e98c4ca86128c86e4a180e1de061`
- `native_voiceover.py`: `5384f27f72a34136fd1800c1d0ef308d823c32d3bb674dd9910e816e2096106c`

The candidate does have the requested closed timing shapes. The schema makes
`OccurrenceMoveArgs.start_ms` an integer with `minimum: 0` and mutually
exclusive with `on`, `track`, and `child_track`
(`astrid/core/timeline/schema/edit-command.schema.json:3224-3270`). The
resize implementation requires a positive integer duration and writes only
the occurrence root duration (`astrid/sdk/timeline/native_occurrence_resize.py:29-45`).
The exact-root move validates a nonnegative integer, writes the root
`placement.start_ms` and agreeing `at_ms` mirror, and leaves child lanes
untouched (`astrid/sdk/timeline/occurrence_commands.py:120-174`).

## Concrete incompatibilities

1. **Frozen voiceover floor is not reconstructed.** The existing floor test
   `tests/sdk/test_timeline_materialization_schema_union.py:134-139` expects
   `65bb68acbfbc72dabbbc83eab66e5309fe5cf5f42c1acb4bc821c62434742a1e` after
   removing only the extent addition. On the exact extracted candidate the
   reconstruction hashes to
   `a57330f736e79707146bb03683bc291dace95a2693146143b2cddd0aea5d524a`.
   The current `OccurrenceMoveArgs` still contains the new `start_ms` union
   after `OccurrenceResizeArgs` is removed. The peer must restore the prior
   move-args shape when constructing this floor (remove `start_ms`, restore
   required `on`/`track`/`child_track`, and preserve the old properties), then
   rerun the frozen floor assertions.

2. **Stale prepared shot revision is accepted.** In the exact candidate,
   `capture_draft_voiceover` assigns `candidate = prepared["candidate"]` and
   immediately calls `_capture_timing` without validating source identity
   (`astrid/sdk/timeline/native_voiceover.py:148-149`). A minimal executable
   probe changed the prepared first placement's `shot_revision_id` to
   `revision-foreign`; lowering returned successfully with commands:

   ```text
   ACCEPTED_STALE_SHOT_REVISION_ID: revision-foreign
   COMMANDS: ['occurrence.resize', 'clip.set', 'occurrence.swap-media', 'shot.set']
   ```

   The peer must add a fail-closed pre-capture identity check covering the
   exact project/timeline/base containers, equal `source_mapping`, unchanged
   occurrence membership/order and IDs, captured source-shot resolution, and
   the source identity fields including `shot_revision_id`. This is the
   smallest correction needed before a consumer can rely on the carrier; it
   does not require a new padding field, quantization rule, or transport/store
   field.

## Minimal executable evidence

The exact candidate was extracted with `git archive` into a private `/tmp`
directory and tested with the read-only shared Python environment. Command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$TMP_VOICE_ACK" \
  /home/user/work/venv-app2-native/bin/python -m pytest -q -p no:cacheprovider \
  "$TMP_VOICE_ACK/tests/sdk/test_timeline_materialization_schema_union.py::test_extent_proposal_preserves_the_prior_voiceover_schema_hash" \
  "$TMP_VOICE_ACK/tests/editing_conformance/test_recipe_native_voiceover.py::test_original_voiceover_outcome_lowers_to_audio_and_metadata_commands_with_inverse" \
  "$TMP_VOICE_ACK/tests/editing_conformance/test_recipe_native_voiceover.py::test_prepared_ripple_timing_and_padding_survive_lowering_inverse_and_redo" \
  "$TMP_VOICE_ACK/tests/editing_conformance/test_recipe_occurrence_start.py::test_exact_ms_preserves_multilane_children_and_canonical_materialized_source"
```

Result: **1 failed, 5 passed**. The failure is the frozen `65bb…` hash
assertion above. The five passing assertions cover the existing voiceover
lowering/inverse, ripple values, and exact-root child-preserving timing
behavior selected for this bounded review. Pytest emitted only the existing
unknown `timeout`/`timeout_method` configuration warnings; no test behavior
was changed.

The stale-revision probe was an inline call to the existing
`_voiceover_bundle_and_outcome` fixture and `capture_draft_voiceover`; it
passed only because the candidate accepted the mutation, which is the
reported incompatibility.

## App consumer boundary

No App product source was changed or activated. Current ordinary App timing
consumers remain clip-scoped: `ordinaryScalarMember.ts:20-29` exposes the
existing `clip.set` scalar shape, and `ordinaryMoveMember.ts:12-44` validates
the existing absolute `clip.move` shape. They do not consume the Agent
`occurrence.resize@1` or exact-root `occurrence.move@1` carriers. This review
therefore makes no generated-client, wire, provider, pin, adoption, browser,
socket, or full-suite claim.

## Not run / next step

No full suite, `request-test`, browser, socket, generation, pinning,
adoption, or App copy was run. Request a new exact Agent candidate after the
two corrections above; then repeat this same bounded source review before
any App consumer work.
