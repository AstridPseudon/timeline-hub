# G3/P4 integrated reader readonly review — PASS

## Verdict

Readonly integrated-source review: **PASS**.

Exact integrated commit: `168a5c9b32e31c7f8db14a96153a3d1955054734`.
Exact tree: `123a5832553dc43093dbbb3fc8d73ce01d59e49f`.
The commit is a merge of `6131704b36807e165575fa944ba984cc847059c8` and
`bd23946157d863b39a8c0e3c41ea489455e08b1b`; its tree is byte-identical to
`bd239`. `bd239` is an ancestor of the integrated tree, and there are no
commits after the merge or unrelated ancestry changes.

The merge delta from the first parent contains exactly four paths:

- `astrid/sdk/_remote_timeline.py`
- `astrid/sdk/authoring_revision_diff.py`
- `tests/sdk/test_authoring_revision_diff.py`
- `tests/sdk/test_remote_timeline_owner_scope.py`

The four product/test blobs exactly match reviewed `a8132afba38ca66b1c815ed2c99404a66a02337f`:
`bc8b9fce`, `db106a74`, `8f59a4b1`, and `7fffe374`, respectively. Root
`report.md` is absent from the integrated tree. The worktree was clean before
and after verification.

## Qualified owner-read scope

The source-authenticated reader is qualified for:

- parent tuple validation (`project_id`, `timeline_id`, `revision_id`), with
  mismatch refusal;
- shot tuple validation (`project_id`, `shot_id`, `revision_id`), including
  foreign/mismatched pin refusal;
- internal tuple validation (`project_id`, authenticated owner
  `timeline_id`, `revision_id`), including missing, foreign, wrong-owner and
  mismatched pin refusal;
- historical exact parent/shot/internal closure reads from the authenticated
  manifest, with no mutable-head/latest fallback;
- the production `timeline.open` → `store.fetch_bundle` →
  `RemoteTimelines.open_bundle` path and `RemoteTimelines.diff` →
  `read_authoring_revision` path.

This is a readonly source/integration qualification only: **P4 is not DONE**.
The original single/ten-note HTTP-body proof was intentionally not run, per the
task boundary.

## Evidence

- `PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_remote_timeline_owner_scope.py tests/sdk/test_timeline_revision_diff_admission.py tests/sdk/test_timeline_show_views.py tests/sdk/test_authoring_revision_diff.py`
  — **45 passed in 13.07s**.
- Scoped Ruff on the four changed source/test files — **PASS**.
- Scoped private mypy with `/home/user/work/venv-agent-typecheck-v2/bin/python`
  and the repository-configured `follow_imports=skip` — **PASS**, 2 source
  files, no issues.
- `make ruff PY=/home/user/work/venv-agent/bin/python` — **PASS**, current
  `2149`, baseline `2149`.
- `make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python` —
  **PASS**, current `1914`, baseline `1914`.
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-34eac004`
  — **PASS** (`runtime.lock.json` matches producer manifest).
- `PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python scripts/artifact_manifest.py --check`
  — **PASS**.
- `git diff --check` and `git diff --cached --check` — **PASS**.
- Import-origin smoke — Agent modules resolve from
  `/home/user/work/wt/agt-P4-reader-integrated-0613`; `runtime_protocol` resolves
  from `/home/user/work/runtime/runtime_protocol/__init__.py`.
- Targeted collection — **45 tests collected**, including parent/shot/internal
  tuple refusals and real show/open/diff cases.

## Notes and limits

The first pytest attempt without `PYTHONPATH=/home/user/work/runtime` failed
before collection because `runtime_protocol` is a shared Runtime source
dependency; the corrected command above passed. The worker-provided `tmpdir`
path is a sentinel file rather than a directory, so private tool caches were
placed under `/tmp/agt-P4-reader-integrated-0613-*`; no shared dependency or
cache was modified.

An explicit scoped-mypy `--follow-imports=silent` experiment reports one
pre-existing diagnostic at unchanged `_remote_timeline.py:228`; the configured
repository gate (`follow_imports=skip`) passes and the full ratchet remains
1914/1914. The neighboring `test_timeline_revision_diff_admission.py` has
four pre-existing Ruff findings, but it is not part of the four changed blobs;
the full Ruff ratchet is unchanged.

No source, generated/schema, pin, dependency, executor, HTTP-body, full,
browser, farm, native14 or crash24 files were edited or tested.
