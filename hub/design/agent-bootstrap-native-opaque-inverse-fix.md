# Agent bootstrap opaque inverse repair

## Result

Implemented the bounded `timeline.init` inverse repair on Agent base `e86f44d0`
in worker `agt-m2-init-opaque-disjoint-inverse`.

`astrid/sdk/timeline/native_initialize.py` now performs the existing exact
pristine-parent check against the raw input bundle without recording a
whole-parent read. It still records the four authored absence reads for
`config.output`, `name`, `slug`, and `registry.assets`, then writes only those
four fields. Consequently a later `parent.opaque` write is disjoint and is
preserved exactly through inverse and redo. The existing strict inverse,
identity, birth, and pristine-history guards remain unchanged; no inverse
bypass, whole-bundle restore, ancestor exemption, history rewrite, schema,
wire, client, or release change was made.

The Agent golden was refreshed only to describe the actual consumed read
footprint (the three copies of the obsolete raw-parent read were removed).
The direct conformance test adds the four original opaque values
`null`, `false`, `[]`, and `{}` in one exact init -> opaque edit -> serialized
reload -> inverse -> redo scenario using `pristine_initialize.json`.

## Evidence

All commands used the worker source and read-only shared dependencies:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_pristine_initialize.py tests/sdk/test_timeline_pristine_initialize_provider.py
31 passed in 2.90s

ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a0dca169 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_pristine_initialize_runtime.py::test_pristine_init_crash_resume_reload_undo_retry_and_redo
1 passed in 3.39s

ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-a0dca169 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_next_command_cohort_runtime.py::test_pristine_init_first_birth_reload_undo_and_missing_word_source
2 passed in 11.57s

git diff --check
passed
```

The actual Runtime provider path was `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`
via `/home/user/work/wt/rt-pin-a0dca169`; no fake SQL/history/provider setup
was introduced. No full suite, browser, live socket, App, wire, schema, pin,
or release qualification was run.

## Changed paths

- `astrid/sdk/timeline/native_initialize.py`
- `tests/editing_conformance/test_pristine_initialize.py`
- `tests/editing_conformance/fixtures/pristine_initialize.json`

The pending harness commit message is in the worker commit-msg path. App2
bootstrap activation remains downstream work and should use this Agent source
only after its normal matched pair is re-qualified.
