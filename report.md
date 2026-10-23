# G3/P4 shared-read owner-scope readonly review

## Verdict

**FAIL — source review is not landable as-is.** Reviewed `47aa77266f2287ad14519b07ce0bba7d4bba2170` with no source edits. The intended internal owner selection is correct for the covered positive, but two concrete scope gaps remain:

1. `astrid/sdk/_remote_timeline.py:67-70,129-133` does not validate the returned parent envelope against `(project_id, timeline_id, revision)`. It overwrites returned parent project/timeline with inspection values and takes the returned row's revision without checking it. An ad-hoc mock with a foreign parent project/timeline or `revision_id="other-parent"` therefore returned `OK`; the resulting bundle carried `other-parent` for the latter. This violates the required foreign-project and returned-revision refusal checks.
2. The normal `RemoteTimelines.diff` path still calls `astrid/sdk/authoring_revision_diff.py:60-61`, which requests `get_project_timeline_revision(project_id, parent_timeline_id, internal_revision)`. With the authenticated closure's internal pin owned by `chapter-1` and parent timeline `film`, the exact call was `(project-1, film, internal-1)` and failed; it must select the authenticated manifest owner. This is the concrete remaining bug cited by peer 0534. It is a refusal rather than a latest fallback in the mock, but it means the normal historical reader is not functional for the required shared-owner closure.

The changed `open_bundle` path does correctly parse exact `dependency_manifest.internal_timelines` rows, refuses missing/malformed/conflicting pins, calls the pinned owner (not the parent timeline), and explicitly rejects foreign-project/owner/revision fields in the returned internal row. No latest fallback was observed.

## Production path and scope

The mounted caller is `timeline.open` → `astrid/sdk/timeline/store.py:641-651` `fetch_bundle` → `client.timelines.open_bundle` → `_RemoteTimelineRevisionMixin.open_bundle`. The historical diff caller is `RemoteTimelines.diff` → `read_authoring_revision`; it is not covered by the two-file owner patch.

Only the assigned source/test files were reviewed:

- `astrid/sdk/_remote_timeline.py`
- `tests/sdk/test_remote_timeline_owner_scope.py`

The branch diff is exactly those two files. No production source, tests, pins, generated files, or shared dependencies were changed in this review.

## Verification

Import origins:

- `astrid`: `/home/user/work/wt/agt-P4-shared-read-review-0553/astrid/__init__.py`
- `runtime_protocol`: `/home/user/work/runtime/runtime_protocol/__init__.py`
- persistent mypy: `/home/user/work/venv-agent-typecheck-v2/lib/python3.11/site-packages/mypy/__init__.cpython-311-x86_64-linux-gnu.so`
- pytest: `/home/user/work/venv-agent/lib/python3.13/site-packages/pytest/__init__.py`

Commands and results:

- `TMPDIR=/tmp/agt-P4-shared-read-review-0553-cache PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_remote_timeline_owner_scope.py tests/sdk/test_timeline_revision_diff_admission.py tests/sdk/test_timeline_show_views.py` — **PASS, 22 passed in 15.84s**.
- The same selection plus `tests/sdk/test_authoring_revision_diff.py` — **FAIL, 35 passed, 1 failed**. `test_open_saved_revision_reports_corrupt_closure_as_protocol_error` expects the legacy fixture without an authenticated `dependency_manifest` to open; the reviewed code correctly refuses it with `integrity_error` (`pinned internal revision has no exact owner timeline`). This is an existing regression/fixture mismatch that must be reconciled with the exact-manifest requirement.
- `.../venv-agent/bin/ruff check --no-cache astrid/sdk/_remote_timeline.py tests/sdk/test_remote_timeline_owner_scope.py` — **PASS**.
- `make ruff PY=/home/user/work/venv-agent/bin/python` — **PASS**, current 2149 equals baseline 2149.
- `.../venv-agent-typecheck-v2/bin/mypy --no-incremental --cache-dir /tmp/agt-P4-shared-read-review-0553-cache/mypy-persistent astrid/sdk/_remote_timeline.py tests/sdk/test_remote_timeline_owner_scope.py` — **PASS**, no issues in 2 files.
- `make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python` — **PASS**, current 1914 equals baseline 1914.
- `.../venv-agent-typecheck-v2/bin/python -m scripts.reshape.compare_mypy_baseline` — **PASS**, current 1914 equals baseline 1914.
- `.../venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004` — **PASS**, lock matches producer.
- `.../venv-agent/bin/python scripts/artifact_manifest.py --check` — **PASS**, manifest current.
- `git diff --check` — **PASS**.
- `sha256sum astrid/core/timeline/schema/edit-command.schema.json` — `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`; unchanged.

No full/browser/live-HTTP suite was run, as instructed. No P4 HTTP body was added or duplicated.

## Recommended next steps

Update the owner patch to validate the parent response's exact project/timeline/revision before projection, and update `authoring_revision_diff` to derive the internal owner from the authenticated dependency manifest with the same fail-closed checks. Add focused negative tests for foreign parent envelope and wrong parent revision, plus the shared-owner historical diff path. Then rerun the 22-test selection and the existing authoring-diff neighbors before Proof starts.
