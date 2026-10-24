Implemented F-renderless-store in `resolve_ids` only: production readers select the existing `_raw_projection=True` path; two-argument custom readers retain their call shape. Reader failures propagate without retries. `remote.py`, original tests, and the strict `no_renderer` guard are unchanged.

Added one focused regression file, `tests/sdk/test_timeline_store_raw_reader.py`.

Validation used:

```sh
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=.:/home/user/work/runtime:/home/user/work/runtime/packages/python
export ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime
PY=/home/user/work/venv-agent/bin/python
```

Old-source RED:

```sh
$PY -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_store_raw_reader.py \
  --basetemp=/tmp/w-c9659a5d76/pytest-red-final
```

Result: **4 failed, 1 passed**. The Runtime-backed public opening failed at the guarded `readable_timing` import.

Changed-source GREEN:

```sh
$PY -m pytest -q -o addopts= -p no:cacheprovider \
  tests/sdk/test_timeline_store_raw_reader.py \
  tests/sdk/test_native_timeline_facades.py::test_remote_open_composition_raw_projection_is_renderer_free \
  tests/sdk/test_native_timeline_facades.py::test_remote_open_composition_uses_runtime_inspection_authority \
  tests/sdk/test_native_timeline_facades.py::test_remote_open_composition_retains_public_timing_enrichment \
  tests/sdk/test_native_timeline_facades.py::test_remote_show_uses_runtime_current_project_and_project_default \
  tests/sdk/test_native_timeline_facades.py::test_remote_default_timeline_must_belong_to_selected_project \
  tests/sdk/test_timeline_session_pair.py \
  tests/sdk/test_timeline_sync.py::test_clean_bundle_hydration_authenticates_exact_pair_without_pending_commands \
  tests/sdk/test_timeline_sync.py::test_clean_bundle_hydration_refuses_wrong_publication_for_revision \
  tests/sdk/test_timeline_sync.py::test_new_clean_session_captures_current_published_state \
  tests/sdk/test_timeline_sync.py::test_identity_change_cannot_send_existing_outbox \
  tests/sdk/test_timeline_sync.py::test_missing_authenticated_scope_never_defaults_identity \
  --basetemp=/tmp/w-c9659a5d76/pytest-green
```

Result: **21 passed in 29.44s**, including exact public base-pair and auth controls.

Static checks:

```sh
$PY -m ruff check --no-cache --output-format=json \
  --config 'include=["*.py"]' \
  astrid/sdk/timeline/store.py tests/sdk/test_timeline_store_raw_reader.py

$PY -m mypy --cache-dir=/tmp/w-c9659a5d76/mypy-green-cache \
  --hide-error-context --no-color-output --no-pretty --show-error-codes \
  astrid/sdk/timeline/store.py tests/sdk/test_timeline_store_raw_reader.py

git diff --check
```

Ruff, compilation of both files, and diff checks passed. Mypy parent/current each report one identical existing `store.py:373` `[arg-type]` diagnostic; normalized comparison found **no new diagnostics**.

Source identity:

- Agent base: `bb50a43c915ec00c05c5ee34569a040bab8e817c`; base tree: `045dd0b01a1bddc6e3c7b822894151a116eacf1b`.
- Proposed tree, calculated without Git mutation: `61fde39ee6e0d8c0505a963c3725fab8ccadbbe7`.
- Runtime: `1d9ddba546f8fb1300f55ff62607ed492719cbaa`; tree: `f56c396c4495547680b46e832565278d2c375e69`.
- Pre/post imports confirmed Agent modules from this worktree and Runtime modules from `/home/user/work/runtime`. Evidence is in `/tmp/w-c9659a5d76`.

Compatibility decision: inspect keyword support before calling, preserving observed two-argument overrides. Opaque callables without inspectable signatures remain unverified. This is source-mode qualification; no complete C0 HTTP qualification is claimed.

No blockers. Commit message and `DONE` written. Next: independent review, Agent home merge, then Runtime’s assigned original publication qualification. No original closure/followup body or full suite was rerun.