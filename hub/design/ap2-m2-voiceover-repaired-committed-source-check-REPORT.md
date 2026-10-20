# App2 source review: private voiceover repair

## Result

**SOURCE ACK.** The committed Agent source is compatible with the requested
source/schema contract:

- commit: `4d4535882f1e028805c3da178bf9a7fa53696da8`
- tree: `f18245ced9c231ddf8f6f2ee64405a84d3517921`
- semantic source parent: `644fd1111f84a91c159064950eb73dcd921c81e3`
- semantic source tree: `6cac36698e0ece0343c10c1a347a59a243cbe80d`
- schema SHA-256: `84fc0863a1f925f32c00b171eaf51b8f06afb7d34064296394bc8592386cbbc5`
- schema shape: 59 definitions, 33 operation clauses, 12 v2 clauses, 13
  source-bound operations (with v1-only `track.create`)

The final commit changes only
`tests/sdk/test_timeline_materialization_schema_union.py`; the product and
schema bytes are unchanged from the semantic parent.

## Checks performed

The final committed tree was extracted read-only into a private temporary
directory. No App copy, shared dependency, shared cache, browser, socket, or
request-test was used.

- `python -m pytest -q --cache-clear tests/sdk/test_timeline_materialization_schema_union.py`
  — **22 passed** (using `/home/user/work/venv-app2-native`; two unrelated
  warnings for unsupported `timeout` pytest configuration options).
- `python -m pytest -q --cache-clear tests/editing_conformance/test_recipe_native_voiceover.py -k 'prepared_ripple_timing_and_padding_survive_lowering_inverse_and_redo or prepared_source_identity_refuses_stale_values_before_capture'`
  — **5 passed, 4 deselected** (same two warnings).

These focused probes verify the repaired frozen reconstructions, including
exact `65bb…`, `27f…`, `392…`, `613…`, and `6ba…` hashes; the stale prepared
`shot_revision_id` refusal before capture with authored/prepared inputs
unchanged; exact authored timing `4150`/`14150` ms; derived visual hold
`0.415` s; no child-lane changes; and no authored `padding_seconds` carrier.
The source inspection also confirms prepared base/source authority checks run
before command capture and retain the requested negative scope.

## Boundaries

This is only a committed Agent source/schema ACK. It does not qualify App
consumer behavior, UI/HTTP behavior, generated clients, generation or pinning,
managed-audio admission, release/freeze/adoption, settlement, or any outer
workflow. Those remain open and were not tested here.

## Blockers and next step

No incompatibility was found for this bounded source review. App2 may use this
exact commit/tree/schema tuple for its separately authorized counterpart work;
that work still needs its own consumer qualification.
