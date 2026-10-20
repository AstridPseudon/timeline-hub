# Runtime spec-reference real-capture port

Status: focused saved-revision control passes; this is not an M3 or registered-rendering completion claim.

## Port

`tests/test_spec_reference.py::test_visualize_task_hydrates_exact_saved_revision_and_refuses_missing_source` now uses the existing real-capture fixture convention:

- ingests the fixture media into the test project;
- bootstraps the timeline through `TimelineCommitStore`;
- accepts `tests/fixtures/capture_authority.json` through `_publish`;
- loads and registers the startup Agent provider, then projects the accepted closure with `project_capture`;
- passes the real media digest as the task's managed `input_object_ids`.

The original task admission, exact revision hydration, host materialization, and missing retained parent refusal assertions remain. No Runtime guard, DTO, endpoint, renderer, scene-evaluation, or unrelated test was changed.

## Evidence

Runtime worktree: `7e160c5d254a9b3d42a28672a2d7e2ac1acd5ca8` before this test-only diff.

Current Agent source used by the direct check: `/home/user/work/agent`, `490c10ac12d55f75d698213487353a7912d33067`.

Passed after the media-input correction:

```text
ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider -m integration tests/test_spec_reference.py::test_visualize_task_hydrates_exact_saved_revision_and_refuses_missing_source
1 passed in 1.91s
```

The one central marked-integration batch was run once on the pre-correction snapshot. It reported `165 passed, 5 failed, 4 deselected`; the target failed only because its real media digest was omitted from `input_object_ids`. The four neighbor failures were the existing Agent `RenderRequest.verified_source` API mismatch in `test_capture_candidate_actual.py`; they were not changed.

No full suite, browser, renderer, live socket, physical PCM, or scene-evaluation test was run or claimed.
