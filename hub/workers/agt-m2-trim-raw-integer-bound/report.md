Fixed raw integer trim bounds. For duration `9007199254740995`, native/model now author `9007199254740994.0` at exact end and refuse genuine overrange before writes.

The documented rule uses the immediate binary64 predecessor when converting the exact interior floor still exceeds the raw bound. All original 17 vectors remain unchanged; 17 new vectors cover integer/float boundaries and collapse controls.

Final test commands, both exit 0:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_clip_trim.py tests/sdk/test_timeline_media_verbs.py tests/sdk/test_timeline_clip_trim_provider.py tests/editing_conformance/test_recipe_m2_clip_split.py tests/editing_conformance/test_recipe_m2_clip_add.py tests/sdk/test_timeline_clip_add_provider.py tests/editing_conformance/test_recipe_m1_commands.py
```

**431 passed.**

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_editing_helpers.py tests/sdk/test_timeline_checkout.py tests/sdk/test_timeline_checkout_facade.py tests/sdk/test_timeline_cuts.py tests/sdk/test_timeline_param_values.py tests/packs/timeline/test_edit_verbs.py tests/packs/timeline/test_verbs_working_copy.py
```

**168 passed, 17 existing lane exclusions, 4 existing warnings.** Scoped Ruff and diff checks passed; original golden unchanged.

No blockers. No full or App/browser qualification run. Next: refresh the shared App handoff copies from the updated repository document/vectors, then qualify App parity.

[Report]( /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-trim-raw-integer-bound/notes/report.md) contains details. `commit-msg` and empty `DONE` written.