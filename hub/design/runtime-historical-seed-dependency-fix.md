# Runtime historical seed dependency fix

Status: setup repaired; the required historical-only gate reached the original
journey and stopped at its first post-fix failure.

## Change

- `tests/historical_audio_fixture.py` now derives the private child bootstrap's
  media dependency rows from the already-remapped immutable publication
  manifest and persists them through Runtime's existing `_persist_closure`
  helper. Shot and internal-timeline edges remain deferred until the authored
  occurrence-bearing publication.
- Removed the attempted second private bootstrap publication. Runtime's normal
  headless-timeline guard rejects a headless shell after `_persist_closure` has
  legitimately installed dependency rows; the existing private closure helper
  is the valid setup path.
- Added a normal Runtime reopen/admission check and an actual SDK
  `timelines.open_bundle` read through the normal door before returning the
  historical fixture. No product, schema, health, artifact, or original
  journey assertion changed.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD/tests:$PWD:/home/user/work/agent" /home/user/work/venv-runtime/bin/python -m py_compile tests/historical_audio_fixture.py tests/test_timeline_public_s2_mixed_cli_journey.py` — passed.
- `git diff --check` — passed.
- Direct fixture control using `prepare_pcm_historical_audio_film` — passed,
  including Runtime reopen/admission and closure equality.
- Required central request:
  `rt-m2-historical-seed-media-dependency-raw27-historical-only-integration-1020185145-6547`
  (`raw27-historical-only-integration`, selected `historical-audio`, literal
  deselected) — **1 failed, 1 deselected**, Runtime snapshot tree
  `53378df69d33812f902c9b51819b552b23eaae4a`.

The central run passed startup admission and the normal SDK `open_bundle`
control, then stopped at the first later failure in the unchanged journey:
`tests/test_timeline_public_s2_mixed_cli_journey.py:209`,
`KeyError: 'media_id'` while the existing view assertion indexes the captured
asset registry entry. The historical fixture's registry entry carries the
captured `object_id`; the accepted trim/retry path had already run. I did not
change that assertion or retry the gate.

## Handoff

The dependency-graph/bootstrap issue is fixed and independently admitted. The
remaining failure belongs to the preserved original journey/asset-field
contract and is unverified as a full historical-positive pass.
