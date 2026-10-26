# B-T1 fixture evidence

Summary: added `conformance/fixtures/shot-layering-v1.json` using the Runtime shared-fixture location and canonical `*_ms` input timing. The fixture covers loose clips above, below, and on the same row; transparent empty shot areas; shot-only suffix tracks; two occurrences on one row; merged inner audio; and the missing-row top fallback with a warning. Added focused Runtime read/validation tests; no Agent or App product code was changed.

Commands and results:

```text
mkdir -p /tmp/w-099a21ba7e/B-T1-fixture-1-pytest && python -m pytest -q --basetemp=/tmp/w-099a21ba7e/B-T1-fixture-1-pytest tests/test_shot_layering_fixture.py
2 passed, 1 warning in 0.72s
```

The warning is pytest's existing `PytestConfigWarning: Unknown config option: timeout`.
An initial run without the isolated `--basetemp` also reached `2 passed` but exited during pytest's cleanup after a harness cleanup race removed `/tmp/.../pytest-current`; it was not used as acceptance evidence.

The fixture loader is the `load_shot_layering_fixture()` helper in `tests/test_shot_layering_fixture.py`, reading the checked-in path `conformance/fixtures/shot-layering-v1.json` with UTF-8 JSON decoding.

Decision: track arrays are top-first, matching the current App renderer and timeline row conventions. Canonical authored timing is milliseconds (`at_ms`, `duration_ms`); projected track IDs use `<occurrence_id>~<inner_track_id>`. The missing-row warning reuses the existing `timeline-patch/target-not-found` diagnostic code family and wording style.

Unresolved: none for the fixture contract. Agent and App consumers are intentionally unverified here and remain T2/T3 work.
