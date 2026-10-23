# G3/P4 readonly review — `tl/agt-P4-shared-read-owner-0541`

Verdict: **FAIL**. Reviewed source is `47aa77266f2287ad14519b07ce0bba7d4bba2170`. No source edits were made.

The new owner selection in `astrid/sdk/_remote_timeline.py` is correct for the covered public-reader positive: exact `dependency_manifest.internal_timelines` pin `internal-1 → chapter-1` is used, and missing, malformed, or conflicting pins fail closed. Returned internal rows are checked for exact project, owner, and revision, and no latest fallback is used. The 22-test author selection passes.

Blocking findings:

- `_remote_timeline.py:67-70,129-133` accepts a returned parent row whose project/timeline/revision differs from the authenticated request. It overwrites project/timeline with inspection values and does not compare the returned revision. A direct mock witness accepted both a foreign parent envelope and `revision_id="other-parent"`; the resulting bundle exposed `other-parent`.
- The normal historical path remains broken for shared owners. `RemoteTimelines.diff` calls `astrid/sdk/authoring_revision_diff.py:60-61`, which still requests the internal revision under the parent timeline (`film`) instead of the exact manifest owner (`chapter-1`). A direct mock witness recorded `(project-1, film, internal-1)` and failed where `(project-1, chapter-1, internal-1)` is required. This is the concrete remaining bug requested by peer 0534, not speculation.

Evidence:

- `venv-agent` targeted selection (`test_remote_timeline_owner_scope.py`, `test_timeline_revision_diff_admission.py`, `test_timeline_show_views.py`): **22 passed in 15.84s**.
- Adding `tests/sdk/test_authoring_revision_diff.py`: **35 passed, 1 failed**; the failure is the existing legacy fixture's expected open without a dependency manifest, while the reviewed reader now refuses missing exact owner pins.
- Scoped Ruff: **PASS**.
- `make ruff PY=/home/user/work/venv-agent/bin/python`: **PASS**, 2149/2149.
- Persistent scoped mypy and `make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python`: **PASS**, 1914/1914.
- `runtime.lock.json` against producer `/home/user/work/wt/rt-pin-34eac004`: **PASS**.
- `scripts/artifact_manifest.py --check`: **PASS**.
- `git diff --check`: **PASS**.
- edit-command schema digest remains `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`; no pins/generated/schema edits.

Production caller: `timeline.open → timeline.store.fetch_bundle → RemoteTimelines.open_bundle`. No full/browser/live HTTP suite or P4 HTTP duplicate was run. Recommended repair is to validate the parent response tuple before projection, port exact manifest-owner selection and guards into `authoring_revision_diff`, add negative tests for foreign parent/wrong parent revision and the shared-owner diff path, then rerun the targeted selection.
