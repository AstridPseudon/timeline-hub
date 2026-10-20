Implemented shared interior rounding for native trim and `Clip.trim`. Exact-end and just-below requests now author `to=hold=9.999999` within raw duration `9.9999999`. Genuine overrange requests and collapsed intervals refuse before writes. The original golden remains unchanged.

Final targeted commands, run from the assigned worktree:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_recipe_m2_clip_trim.py tests/sdk/test_timeline_media_verbs.py tests/sdk/test_timeline_clip_trim_provider.py tests/editing_conformance/test_recipe_m2_clip_split.py tests/editing_conformance/test_recipe_m2_clip_add.py tests/sdk/test_timeline_clip_add_provider.py
```

**281 passed.**

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/test_timeline_editing_helpers.py tests/sdk/test_timeline_checkout.py tests/sdk/test_timeline_checkout_facade.py tests/sdk/test_timeline_cuts.py tests/sdk/test_timeline_param_values.py tests/packs/timeline/test_edit_verbs.py tests/packs/timeline/test_verbs_working_copy.py
```

**168 passed, 17 default-lane deselections, 4 Pillow deprecation warnings.** Targeted Ruff and diff checks passed.

[Contract and exact formula](/home/user/work/wt/agt-m2-trim-interior-rounding/docs/timeline-trim-precision.md) and 17 vectors are exported for App. [Detailed report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-trim-interior-rounding/notes/report.md) includes the pinned-source reproduction.

No blockers. No full suite or live Runtime/browser qualification run. Commit message and `DONE` written. Next: orchestrator review, then App parity qualification.