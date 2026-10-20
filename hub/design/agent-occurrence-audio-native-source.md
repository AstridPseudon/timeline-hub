# Agent occurrence audio native source slice

2026-10-20. Bounded source candidate on Agent base `c0644cf1a7b63c9bcff7f70502b953a07879c9f`. This is a new source hash; frozen schema/source identities `39211e63a50b9fb495fdf3feb5beaf0e4d0b4eab9a7e13f4d5f769e0d317429d`, `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`, and `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` were not modified.

## Source and compatibility

Changed product paths only:

- `astrid/sdk/timeline/_media_inputs.py`: accepts verified `audio/*` alongside image/video; audio and video both require the existing finite-positive Runtime-carried `duration_seconds`.
- `astrid/sdk/timeline/native_occurrence_media_commands.py`: maps audio media to an explicit raw child track with `kind: "audio"`; image/video continue to require `kind: "visual"`.

The existing `occurrence.add-media` and `occurrence.swap-media` operation names, version 1, five-field `MediaSelection`, registry create-or-require policy, occurrence isolation, raw child identity, typed birth/materialization recording, source-window endpoint checks, source-unit hold, speed, and strict inverse are unchanged. No new operation, DTO, endpoint, lookup, raw adoption, caller duration, whole-child replacement, or audio-as-visual fallback was added.

No schema change was needed. `MediaSelection` remains the closed five-field definition and `OccurrenceAddMediaArgs.row` remains the existing open literal row; the current schema has 58 definitions and 32 operation conditions, with the affected operation argument definitions unchanged. Raw schema SHA-256 remains `27f2e3edaffdfc49665a858c5c1d6989dd89ef200932679b77367bc459329cfb`.

Changed product-source manifest (UTF-8 lines of `sha256sum path`, final newline included) SHA-256: `1f6a291392a3f1cf753187185784497037d57a172bbffb0f1572add260856893`.

```text
9bb997e5b0a675969b2e4e5eff0d4329ba9ecce1d9b4529339663a2187fcc58e  astrid/sdk/timeline/_media_inputs.py
09cde00d9aa6c658cfdd71da7413eb8a0480d8495f81e2de09c22f03268fb549  astrid/sdk/timeline/native_occurrence_media_commands.py
```

## Proof

Changed test path: `tests/editing_conformance/test_recipe_occurrence_media.py`.
It retains the existing image/video capture, replay, registry, selection, materialization, and inverse neighbors, adds focused audio add/swap cases, and adds:

- one real PCM WAV source whose duration is read from its WAV header; the existing `capture_track_create` and occurrence media recorder capture an explicit raw `voiceover` audio track, `clipType: "media"`, `from=0`, `to=duration`, `hold=duration`, and `speed=1.5`; the recorded exact five-field selection replays and strictly inverts;
- malformed non-positive intrinsic duration refusal;
- wrong-track (`visual` instead of `audio`) refusal, with both negatives proving no bundle writes.

The WAV case is source-only and uses the existing `verified_media` recorder seam. It does not claim Runtime managed-object admission, native HTTP, CAS custody, or a generated-client qualification.

## Validation

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_occurrence_media.py
64 passed in 4.77s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_m2_parent_media.py tests/editing_conformance/test_recipe_m2_placement.py tests/editing_conformance/test_recipe_m2_shot_pool.py
177 passed in 26.10s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_current_union_schema.py tests/sdk/test_timeline_materialization_schema_union.py
54 passed in 156.48s

PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/sdk/timeline/_media_inputs.py astrid/sdk/timeline/native_occurrence_media_commands.py tests/editing_conformance/test_recipe_occurrence_media.py
PASS

git diff --check
PASS
```

No full/full-* suite, release, pin, generation, Runtime HTTP/native occurrence acceptance, or independent peer review was run. The central test service was not requested because this slice has no live-socket requirement.

## Remaining gaps and next step

Audio occurrence birth still requires a separately captured existing raw audio track; this operation does not create a track. Automatic audio placement, shared/materialized occurrence media, ripple/parent retiming, outer voiceover proposal/requester settlement, and the producer's provenance carrier remain outside this slice and are not claimed qualified. The existing handoff's Runtime admission restriction also remains unchanged. An independent peer should review this source candidate before any freeze or adoption.
