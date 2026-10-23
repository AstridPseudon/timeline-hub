# G3/P4 shared-owner read final review

Status: **PASS** for `a8132afba` on parent `6131704b3`. Readonly review; no
source changes made by this reviewer.

## Scope and findings

`git log --oneline --reverse 6131704b3..a8132afba` contains exactly the own
first-return commit `a8132afba`; `git diff --name-status` contains only:

- `astrid/sdk/_remote_timeline.py`
- `astrid/sdk/authoring_revision_diff.py`
- `tests/sdk/test_remote_timeline_owner_scope.py`
- `tests/sdk/test_authoring_revision_diff.py`
- `report.md`

The two prior FAIL findings are repaired. `open_bundle` validates the returned
parent `(project_id, timeline_id, revision_id)` before projection, then validates
shot and internal response tuples. Both reader paths resolve internal revisions
only through the exact authenticated `dependency_manifest.internal_timelines`
owner pin. Missing, malformed, conflicting, mismatched, and foreign data fail
closed; no latest fallback or guessed owner is present. Historical fixture
metadata is a faithful complete transport manifest; existing corrupt-closure
and cross-owner refusal assertions remain active.

Production callables traced:

- `astrid/sdk/timeline/commit_session.py:237` `timeline.open` →
  `astrid/sdk/timeline/store.py:641` `fetch_bundle` →
  `astrid/sdk/remote.py:458` `RemoteTimelines` →
  `astrid/sdk/_remote_timeline.py:27` `open_bundle`.
- `astrid/sdk/remote.py:1572` `RemoteTimelines.diff` →
  `astrid/sdk/authoring_revision_diff.py:29` `read_authoring_revision` →
  `:10` `_authenticated_internal_owners`.

## Evidence

- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_remote_timeline_owner_scope.py tests/sdk/test_timeline_revision_diff_admission.py tests/sdk/test_timeline_show_views.py tests/sdk/test_authoring_revision_diff.py` — **45 passed**.
- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m ruff check astrid/sdk/_remote_timeline.py astrid/sdk/authoring_revision_diff.py tests/sdk/test_remote_timeline_owner_scope.py tests/sdk/test_authoring_revision_diff.py` — **PASS**.
- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent-typecheck-v2/bin/python -m mypy astrid/sdk/_remote_timeline.py astrid/sdk/authoring_revision_diff.py tests/sdk/test_remote_timeline_owner_scope.py tests/sdk/test_authoring_revision_diff.py --hide-error-context --no-color-output --no-pretty --show-error-codes` — **PASS**.
- `PYTHONPATH="$PWD:/home/user/work/runtime" make ruff PY=/home/user/work/venv-agent/bin/python` — **PASS**, 2149/2149.
- `PYTHONPATH="$PWD:/home/user/work/runtime" make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python` — **PASS**, 1914/1914.
- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — **PASS**.
- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check` — **PASS**.
- `git diff --check` and `git diff --check 6131704b3..a8132afba` — **PASS**.
- Import origins: Agent modules resolve from this worktree; `runtime_protocol` resolves from `/home/user/work/runtime/runtime_protocol/__init__.py`.

No full/browser/live HTTP suite or Proof-owned P4 HTTP body was run, as
instructed. No pins, generated/schema files, executors, or shared dependencies
were changed. PASS permits Proof to stage its originaltenHTTP work on the exact
callable source.
