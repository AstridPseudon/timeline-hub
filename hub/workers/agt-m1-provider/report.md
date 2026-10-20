Implemented [commit.py](/home/user/work/wt/agt-m1-provider/astrid/sdk/timeline/commit.py): **435 product lines**, complete immutable closure conversion, scoped input hydration, guarded inverse/history, server replay, and three-attempt CAS retry. Runtime results return unchanged; core owns the sole recorder.

Final focused command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/tmp/agt-m1-provider-corrected-overlay /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py --basetemp=/tmp/agt-m1-provider-final-provider --tb=short
```

**50 passed in 10.32s.** The external overlay imports the real correction core; no command stubs were committed.

Neighbor command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD:/tmp/agt-m1-provider-corrected-overlay /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_commit_provider.py tests/sdk/test_timeline_commit_provider_document.py tests/timeline/test_authoring_bundle.py --basetemp=/tmp/agt-m1-provider-final --tb=short
```

**74 passed, 1 default-lane deselected.** Ruff, targeted mypy, whitespace checks, and actual Runtime factory/digest smoke passed.

Restore explicitly refuses until its adapter lands. Multiple undo targets require one inverse command in chronological order. Commit message written; worktree caches removed.

No full suite, live Runtime acceptance, or restart/socket journey was run. Next: integrate the corrected core and provider, then run the central durability and renderer-off journey.