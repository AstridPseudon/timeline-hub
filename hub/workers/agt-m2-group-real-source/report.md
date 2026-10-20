Implemented real CAS media and admitted `segments` source binding before legacy-parent construction. Preserved the detached golden, rational fps, groups, opaque fields, ordering, and exact pins.

Validation:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-m2-trusted-bootstrap /home/user/work/venv-agent/bin/python -m pytest -q --tb=short -p no:cacheprovider -m 'integration or not integration' tests/sdk/test_timeline_group_migration_runtime.py tests/sdk/test_timeline_group_migration_provider.py tests/editing_conformance/test_recipe_m2_group_migration.py
```

**56 passed, 2 failed, 1 existing xfailed.** Both setup variants pass GET/inspect, retained v1 reads after source v2, and reopen. Both positive migration tests remain red: Runtime rejects `shot:new-shot::` in authorship before provider execution. Accepted reload/inverse/redo remain unverified.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/sdk/test_timeline_group_migration_runtime.py tests/editing_conformance/test_recipe_m2_group_migration.py
git diff --check
```

Both passed. No full/network suite ran.

Next: officially regenerate and pin the bundle-2 root/group artifacts, then rerun unchanged positives. All M2 merges remain held.

[Detailed report and exact helper/source tuple](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-group-real-source/notes/report.md). Both commit-message files written; temporary output cleaned.