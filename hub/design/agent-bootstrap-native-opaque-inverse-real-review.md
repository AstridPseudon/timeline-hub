# Agent initializer opaque inverse — real-provider review

## Decision

**APPROVE** the bounded initializer candidate at source tree `HEAD
4296a7091d30543d3839fe703c0f0626f9882ebe` plus the test-only change in
`tests/sdk/test_timeline_pristine_initialize_runtime.py` (working-tree patch
SHA256 `c733c4eca7aba5c5252892857ed5113a2f974fde4fbe25dbb36d18536755583f`).
This approves the Agent initializer behavior and its real-provider proof for
shared review. **HOLD** App2 consumer activation, public release, and adoption;
this worker did not qualify those boundaries.

## What was reviewed

- `timeline.init` retains the complete raw-parent pristine guard at capture,
  while its recorded reads are only the four authored/consumed paths:
  `config.output`, `name`, `slug`, and `registry.assets`.
- The existing direct four-value opaque cases (`null`, `false`, `[]`, `{}`)
  remain strong successful expectations and pass serialized reload -> inverse
  -> redo. Existing pristine-history, order/intervening-write, birth, and
  exact-retry refusal coverage remains present; no expected success was
  weakened.
- The added real-provider regression uses Runtime `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`:
  accepted init -> accepted disjoint opaque track row containing the four raw
  values -> Runtime restart/reload -> initializer undo -> redo. It asserts the
  absent `label`, exact raw values and array order, collection order, canonical
  document, head pair, and five-entry history closure.
- `astrid/core/timeline/schema/edit-command.schema.json` and
  `tests/editing_conformance/fixtures/pristine_initialize.json` are unchanged.

## Evidence

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_pristine_initialize.py tests/sdk/test_timeline_pristine_initialize_provider.py
31 passed in 3.50s

ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_pristine_initialize_runtime.py::test_pristine_init_crash_resume_reload_undo_retry_and_redo tests/sdk/test_timeline_pristine_initialize_runtime.py::test_pristine_init_real_provider_preserves_disjoint_opaque_row_after_reload_undo_redo tests/editing_conformance/test_next_command_cohort_runtime.py::test_pristine_init_first_birth_reload_undo_and_missing_word_source
4 passed in 10.97s

git diff --check
passed
```

No full suite, browser, socket, App activation, schema/wire/pin, or public
release qualification was run. The real regression intentionally uses a
single disjoint opaque row after a `timeline.init` publication; the existing
actual a0 test covers the full App-default batch's init/retry path, while the
direct golden covers all four original opaque initializer inverse cases.
