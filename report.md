# G3/P4 shared-owner read repair

Status: complete on base `6131704b3`; worktree remains uncommitted for the harness.

## Changes

- Imported only the two-file `47aa77266` reader delta into `_remote_timeline.py` and `test_remote_timeline_owner_scope.py`.
- `open_bundle` now authenticates the returned parent `(project_id, timeline_id, revision_id)` before projection, authenticates returned shot and internal child tuples, and resolves internal reads only through the exact authenticated `dependency_manifest.internal_timelines` owner pin. Missing, malformed, ambiguous, or mismatched pins fail closed; there is no latest fallback or guessed owner.
- Historical `RemoteTimelines.diff` now uses the same exact manifest-owner rule through `_authenticated_internal_owners` in `authoring_revision_diff.py`, including returned child tuple validation.
- Added the complete normal transport manifest shape to the historical fixture without changing its existing assertions, plus a shared-owner historical positive and wrong-parent/foreign-parent and child negatives.

Production callables:

- `astrid/sdk/remote.py:458` `RemoteTimelines` → `astrid/sdk/_remote_timeline.py:27` `_RemoteTimelineRevisionMixin.open_bundle` (CLI `show`/revision readers).
- `astrid/sdk/remote.py:1572` `RemoteTimelines.diff` → `astrid/sdk/authoring_revision_diff.py:29` `read_authoring_revision` → `:10` `_authenticated_internal_owners` (historical diff).

## Evidence

- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_remote_timeline_owner_scope.py tests/sdk/test_timeline_revision_diff_admission.py tests/sdk/test_timeline_show_views.py tests/sdk/test_authoring_revision_diff.py` — **45 passed**.
- Scoped Ruff with `venv-agent` — **PASS**.
- Scoped mypy with persistent `/home/user/work/venv-agent-typecheck-v2/bin/python` — **PASS**.
- `PYTHONPATH="$PWD:/home/user/work/runtime" make ruff PY=/home/user/work/venv-agent/bin/python` — **PASS**, 2149/2149 baseline.
- `PYTHONPATH="$PWD:/home/user/work/runtime" make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python` — **PASS**, 1914/1914 baseline.
- `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — **PASS**.
- `scripts/artifact_manifest.py --check` — **PASS**.
- `git diff --check` — **PASS**.

The exact pytest command without the runtime checkout on `PYTHONPATH` failed during collection with `ModuleNotFoundError: runtime_protocol`; the corrected command above uses the established shared runtime source and does not alter shared dependencies.

## Review state

- Incoming `design/agent-P4-shared-read-review-0553.md` readonly review: **FAIL as received** (the parent tuple and historical shared-owner defects described there were real).
- Local repair witnesses and all focused regressions: **PASS**.
- Independent post-repair readonly review: **REQUIRED/PENDING**; no new independent reviewer was run in this worker.

No full/browser/live HTTP suite was run. No actual HTTP body, schema, generated file, pin, executor, or managed edge was changed.
