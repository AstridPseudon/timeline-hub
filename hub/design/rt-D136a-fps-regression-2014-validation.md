# D136a validation

## Source comparison

- Base: `a30e74e901a28b39c28facba3deb00d76f186e23`.
- Rejection introduction: Agent commit `6f4baa07603776840f0a78cc0cf459831bc026af`, `astrid/sdk/timeline/validation.py`, `_fps` lines 53–64 and `_fps_values` lines 81–92.
- Pristine Agent `origin/main`: `886a3183bd4a4a44f0a2c08fabec4e8edcbf7b55`; `astrid/core/timeline/validators/timeline.py:_timeline_fps` accepts positive scalar FPS and otherwise returns `30.0` without rejecting the open `theme_overrides.visual.canvas` value.
- Frozen R4 SDK candidate: `11caf1d9de291d76f491cf69f7942606b7471d7a`; no final-candidate validator at that ref.
- Owner: Agent. Runtime only dispatches the registered provider; no Runtime source was changed.

## Fix

`_fps` now accepts a list/tuple of exactly two positive integers using the same exact `Fraction` representation already used for the mapping spelling. It does not modify the authored value. Wrong shapes, non-integer members, zero/negative members, nonfinite scalars, and current typed declaration failures remain strict.

## Regression evidence

Exact parent source probe, loading `git show HEAD:astrid/sdk/timeline/validation.py` in memory:

- `tests/sdk/test_d136_fps_upstream_compat.py::test_production_caller_accepts_and_retains_upstream_fps_list[False]`: FAIL with `candidate.parent.config.theme_overrides.visual.canvas.fps: must be a finite number`.

Candidate:

- Own regression: `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --timeout=45 tests/sdk/test_d136_fps_upstream_compat.py` → **5 passed in 1.37s**.
- Nearest controls: `... tests/editing_conformance/test_commit_v2_validation.py tests/editing_conformance/test_commit_fps_d12.py tests/sdk/test_timing_compiler.py::test_fixed_source_window_and_rational_half_frame_ties` → **56 passed in 2.39s**.
- Ruff: **All checks passed** for the changed source/test files.
- mypy: **Success: no issues found in 2 source files**.
- pycompile and `git diff --check`: passed.

The accepted production path covers both dry-run and accepted commit, and asserts the canonical document retains the exact authored list. Invalid typed controls are refused atomically with no prepared or accepted writes.

## Limits

No full suite, nine-selector App rerun, Runtime/App/browser/socket suite, or 5 GB admission run was performed. The original nine test bodies and fixture remain untouched. No schema, generated client, pin, Runtime, App, fixture, source mapping, authority, or protocol change was made.
