# G5 test-import migration

## Result

Migrated the two surviving `document_diff` imports in the assigned test files to
the real G3 `astrid.sdk.timeline.emitter` / guarded `doc.patch` path. No product
source, emitter, provider, Runtime, schema, pin, contract, or unrelated test
file was changed. No compatibility alias was added.

The authoring-feedback cases now assert exact `doc.patch` carriers for parent
timing, narration/media, null-to-absence clearing, parameter clearing, and
track writes. Presence loss, mirror/canonical, and noncanonical pinned-base
refusals remain refusal assertions. The native-sheet case now emits and checks
the exact parent and source-bound internal patch changes, with its accepted
HTTP body and canonical/reload/inverse assertions otherwise retained.

## Verification

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/agt-G5-test-imports-final-authoring tests/timeline/test_authoring_feedback.py`
  - **30 passed**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest --collect-only -q -o addopts= -p no:cacheprovider tests/timeline/test_authoring_feedback.py tests/editing_conformance/test_native_sheet_current_runtime.py`
  - **49 collected**, including the migrated native-sheet test; collection succeeds after deletion of `document_diff.py`.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --basetemp=/tmp/agt-G5-test-imports-emitter tests/editing_conformance/test_document_patch_emitter_engine.py tests/editing_conformance/test_document_patch_emitter_v2.py tests/editing_conformance/test_native_sheet_ordinary.py tests/sdk/test_timeline_sheet_native.py`
  - **135 passed**.
- Scoped Ruff on both changed files: **All checks passed**.
- Scoped mypy on both changed files: **Success: no issues found in 2 source files**.
- `git diff --check`: **passed**.
- Retired-symbol audit over both changed files: no `document_diff`, `DocumentDiffError`, or `document_diff_to_commands` occurrences.

## Unqualified / blocked

The full `tests/editing_conformance/test_native_sheet_current_runtime.py`
Runtime HTTP integration body was intentionally not executed in this worker.
All 49 cases in that file, including
`test_http_emitter_null_presence_and_track_roundtrip_is_authenticated`, remain
unqualified beyond collection and require the existing central test service.
No full, browser, native14, P1/P4, or socket suite was requested.

## Decision

The retired adapter's native-op expectations were moved to the current generic
carrier only where the current G3 emitter owns the behavior. Exact paths,
previous-value state, null/absence, source-bound refs, shared/preservation
assertions, and current refusal guards remain explicit. No missing G3 behavior
was invented.
