# D136a independent review validation

## Verdict

- Source: **FAIL**. The candidate's strict FPS policy crosses from the typed `config.output.fps` field into the open `theme_overrides.visual.canvas` namespace without contract evidence.
- Behavior: **FAIL**. The candidate rejects upstream-accepted open-path forms and changes the effective FPS for accepted rational spellings.
- Evidence: **PASS (bounded)** for source/blame/matrix review and targeted controls. This is not accepted functional proof for the full 5 GB body.
- Release: **BLOCKED**.

## Source and semantic review

The pristine validator at `astrid/core/timeline/validators/timeline.py:171-187` reads only a positive scalar from `theme_overrides.visual.canvas.fps`; all other values take its documented `30.0` fallback. The shared schema has `ThemeOverrides.visual` as an object with `additionalProperties: {}` (`astrid/core/timeline/schema/timeline-config.schema.json:480-505`), so `canvas` and its contents are open. In contrast, `TimelineOutput.fps` is a typed number (`:506-537`). C0 does not define this TimelineConfig field and cannot justify converting the open canvas path into a typed parameter.

The candidate's `_fps_values` (`astrid/sdk/timeline/validation.py:72-109`) collects both typed output FPS and open canvas FPS. Its `_fps` (`:53-69`) rejects all non-positive/non-finite/non-rational forms and now admits only the added exact two-integer list/tuple in addition to scalar and exact rational mapping. This is the same introducing boundary blamed to `6f4baa07603776840f0a78cc0cf459831bc026af`, called by the production dispatcher at `astrid/sdk/timeline/commit.py:1399-1418`.

The same authored `[30000,1001]` canvas input has different results: pristine `_timeline_fps` returns `30.0`; candidate `_timing_evaluators._fps` returns `Fraction(30000,1001)`. The exact rational mapping has the same mismatch because pristine `_timeline_fps` does not parse mappings. The candidate therefore does not satisfy “same resulting behavior including fallback,” even for the one newly accepted list.

## Exact finite input audit

The read-only provider matrix used fresh `document_fixture(shared=False)` realms and the existing `_service_call` dispatcher for each value. Pristine `validate_timeline` accepted every listed value at the open canvas path. Candidate production validation rejected:

1. Non-object `canvas` values: boolean, number, string, and array.
2. Object `canvas.fps` values: `null`, booleans, strings, arbitrary mappings, zero/negative scalars, empty/one/three-item arrays, non-integer arrays, and zero/negative arrays.

Candidate accepted positive finite scalars, exact positive integer numerator/denominator mappings, and exact positive two-integer arrays. The last two still differ from pristine's `30.0` fallback when authored under the open canvas path. `canvas=null` and `canvas={}` are not independently blocking because candidate treats them as absent and both retain the upstream fallback, but the other non-object canvas forms are rejected.

## Commands and results

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_d136_fps_upstream_compat.py tests/editing_conformance/test_commit_v2_validation.py tests/editing_conformance/test_commit_fps_d12.py tests/sdk/test_timing_compiler.py::test_fixed_source_window_and_rational_half_frame_ties` → **61 passed in 2.68s**.
- Parent-source replay of the exact pre-candidate `_fps` implementation against the production dispatcher and `[30000,1001]` → **CommitRejected**, `candidate.parent.config.theme_overrides.visual.canvas.fps: must be a finite number`.
- Candidate own regression portion → **5 passed** (included in the 61-pass command); authored list retention and dry-run/accepted paths pass, strict invalid typed controls refuse atomically.
- `.../venv-agent/bin/python -m ruff check astrid/sdk/timeline/validation.py tests/sdk/test_d136_fps_upstream_compat.py` → **All checks passed**.
- `.../venv-agent/bin/python -m mypy astrid/sdk/timeline/validation.py tests/sdk/test_d136_fps_upstream_compat.py` → **Success: no issues found in 2 source files**.
- `.../venv-agent/bin/python -m py_compile astrid/sdk/timeline/validation.py tests/sdk/test_d136_fps_upstream_compat.py` with private `/tmp/rt-D136a-fps-review-2021-pycache` → **PASS**.
- `git diff --check a30e74e901 ebb32e7598` → **PASS**.

## Scope limits

No source/test/fixture/App/Runtime changes were made by this review. The 5 GB admission was **NOTRUN** because the filesystem reported 4.46 GB free, below the 4.6 GB source-only floor; no heavy or invented admission was attempted. Full, browser, socket, native, provider-elsewhere, original9, P4, and core suites were not run under the task rules.
