Fixed both gaps: missing parent registry containers now use guarded writes, and valid child transitions no longer block unrelated parent replacement. All four former strict-xfail cases pass. Ordered replacement, exact inverse/redo, custody checks, and dependency refusals remain intact.

Final validation, all exit 0:

- Actual Runtime tests: **36 passed**.
- Neighboring tests: **309 passed, 5 existing xfailed**.
- Ruff and `git diff --check`: passed.

Commands ran from the assigned worktree:

```bash
P=/home/user/work/venv-agent/bin/python
O=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch
T=tests/editing_conformance
export PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD"
export ASTRID_RUNTIME_CHECKOUT="$O/workers/agt-m2-parent-media-real-proof/runtime-source"

$P -m pytest -q --tb=short -rx -p no:cacheprovider -m integration "$T/test_commit_runtime_parent_media.py"

$P -m pytest -q --tb=short -rx -p no:cacheprovider "$T"/{test_recipe_m2_parent_media,test_recipe_clip_delete,test_producer_insertion,test_recipe_occurrence_media,test_occurrence_media_manifest_inverse}.py

$P -m ruff check --no-cache astrid/sdk/timeline/{_command_state,_delete_commands,native_occurrence_media_commands}.py "$T"/{test_recipe_m2_parent_media,test_recipe_clip_delete,test_commit_runtime_parent_media,test_producer_insertion}.py

git diff --check
```

Process notes were moved outside the repo. [Detailed report](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-parent-media-real-gap-fix/notes/report.md>), flat handoff, `commit-msg`, and `DONE` are written.

No blockers. No full suite run. Authentic producer qualification and the S2 superset freeze remain separate follow-ups.