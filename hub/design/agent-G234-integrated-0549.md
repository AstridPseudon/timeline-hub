# PASS — agt-G234-integrated-0549

Readonly integrated proof for current Agent head `ea302e0f504c12e7f71c21745e1ef99cac014d9a`, tree `40ce07e330d9a378350677f871e49a65336b6b8e`.

The merge has parents `900ba8f09cff705b5d2db8d31021e4c2ad3f7786` (fork/provider join) and `31a5e8d3c858d0e4cb1b333b95175862f07f5fa6` (reviewed G234 join). Exact whole-tree equality with `31a5` is not claimed: `31a5..HEAD` is the intended 13-path fork/provider composition, and Git auto-merged `commit.py`/`validation.py`.

## Integrated proof

Current fork root-input authentication is present in `native_occurrence_fork.py`/`_root_inverse.py` and covered by the provider/recipe tests. D12 historical-reference preservation and invalidation checks remain in `validation.py`/`_commit_timing_validation.py`; legacy replay landing metadata remains wired through `commit.py`/`rebase.py` and its dedicated provider tests. Focused assertions preserve full v2 request DTOs, stable idempotency, full accepted/merged/historical-rebased `{data, receipt}` fields, canonical document/head/revision/digests, records/effects/steps/dependencies/history/undo steps, structured conflict/invalid details, and preview `would_status`.

The mounted production caller is present: `TimelineSession`/sync seals the request and render publication calls `commit_assembly` through the authenticated requester path with `group_id`; `RuntimeCommitService` replays with the authenticated request and evaluated landing head, validates the result, and returns the authoritative preview/accept outcome.

Protected audit passed for 12 named paths unchanged from `31a5`, covering 5292 native-word-anchor fixtures, 076 inverse-binding tests, public facade/schema controls, document emitter, Runtime 34eac lock/artifact metadata, and d106/f252 client/schema-floor state. `runtime.lock.json` still names producer `34eac0041b0891e9011966b39bcbd26053fde5bc`.

## Exact evidence

All direct runs used `/home/user/work/venv-agent/bin/python`, explicit `PYTHONPATH="$PWD:/home/user/work/runtime"`, and the worker temp root resolved from the task's `tmpdir` file (`/tmp/w-4594387876`). Import-origin assertions printed:

```text
AGENT_ORIGIN /home/user/work/wt/agt-G234-integrated-0549/astrid/__init__.py
RUNTIME_ORIGIN /home/user/work/runtime/runtime_protocol/__init__.py
```

Focused command:

```text
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_commit_legacy_text_reference.py tests/sdk/test_timeline_inverse_binding.py tests/sdk/test_timeline_commit_provider_document.py tests/editing_conformance/test_document_patch_emitter_engine.py tests/sdk/test_timeline_render_publication.py tests/sdk/test_timeline_narration_commit.py tests/editing_conformance/test_provider_occurrence_fork.py tests/editing_conformance/test_recipe_occurrence_fork.py
```

Result: **131 passed, 1 deselected in 8.91s**.

Legacy replay metadata command:

```text
/home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_commit_provider.py::test_legacy_rebase_records_landing_step_metadata tests/sdk/test_timeline_commit_provider.py::test_replay_accepts_legacy_request_head_and_builds_steps
```

Result: **2 passed in 1.19s**.

Exact original live nodes, using compatible Runtime `85dafdf46742b02ae5e4a300656cd6f5d68f0d4d` and explicit root imports:

```text
/home/user/work/venv-agent/bin/python -c '... pytest.main(["-q", "-o", "addopts=", "-p", "no:cacheprovider", "-m", "integration", "tests/sdk/test_timeline_pristine_initialize_runtime.py::test_remote_create_empty_uses_live_commit_bootstrap_and_exact_replay", "tests/sdk/test_timeline_render_publication.py::test_requester_render_reaches_real_task_admission_after_commit"])'
```

Result: **2 passed in 5.73s**.

Quality and integrity results:

- scoped Ruff: **0 findings**;
- scoped private mypy: **10 source files, no issues**;
- `make ruff PY=/home/user/work/venv-agent/bin/python`: **2149/2149**;
- `make mypy PY=/home/user/work/venv-agent-typecheck-v2/bin/python`: **1914/1914**;
- vendor lock against frozen `rt-pin-34eac004`: **PASS**;
- artifact manifest: **current**;
- `git diff --check 31a5..HEAD`: **PASS**;
- final worktree: clean.

No source changes, skips, xfails, budget increases, full/browser/heavy/farm/Runtime20/native14 runs, or Proof-owned HTTP duplicate bodies. R2 stage-3 redo, V2 FPS-anchor, and current-show parallel work remain unqualified.

**Disposition: PASS.**
