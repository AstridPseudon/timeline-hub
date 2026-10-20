Implemented portable pack admission and pure snapshot validation. The predecessor was clean; no recovery patch was needed. Both commit-message files are written.

Final targeted command:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/core/test_project_packs.py tests/core/test_project_pack_inputs.py tests/core/test_project_pack_snapshots.py tests/sdk/test_timeline_selected_schema.py tests/editing_conformance/test_recipe_scalar_commands.py tests/sdk/test_timeline_commit_provider_scalar.py
```

**164 passed, 7 unchanged strict xfails.** Diff check passed; scoped lint findings decreased.

Runtime retention, native PARAM replay/undo, and the paired artifact release remain unverified. Next: compose with Runtime’s custody implementation and qualify those paths before flipping the three schema cases. M2 merges remain held.

[Full report, decisions, limitations, and test results](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-pack-custody-recover/notes/report.md).