## Report

Blocked by the existing command surface:

- `placement.unplace` rejects video clips.
- `clip.delete` only accepts `parent/clip:<id>`, not occurrence-owned raw video children.
- No existing occurrence-child delete command exists.
- No product/schema/fixture changes were made.

Evidence: shared video row `occurrence:occ-a/clip:placed`, source window `0..4`; exact delete attempt refused with `clip.delete v1 requires one parent clip identity`.

Tests:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider --basetemp=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-video-unplace-native/pytest-neighbors tests/editing_conformance/test_recipe_m2_shared_auto_placement.py tests/editing_conformance/test_recipe_m2_shot_pool.py tests/editing_conformance/test_recipe_clip_delete.py tests/editing_conformance/test_recipe_m2_placement_create_unplace.py
```

Result: **200 passed in 23.05s**. No full suite requested.

Added:

- [notes/report.md](/home/user/work/wt/agt-m2-video-unplace-native/notes/report.md)
- [agent-video-unplace-native.md](/home/user/work/wt/agt-m2-video-unplace-native/docs/design/agent-video-unplace-native.md)

`BLOCKED` and commit message supplied to the harness. Next decision: extend the existing guarded delete handler for occurrence children, or provide an existing occurrence-child delete command.