Added the exact App fixture, fade/cap vector, focused tests, and contract documentation. Editor clamp positives remain intact; product code is unchanged.

Focused command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-m3-visual-cap-fade-vector /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_compile_contracts.py tests/timeline/test_shot_composition_projection.py tests/core/timeline/test_shot_composition_projection_volume.py
```

Result: **51 passed, 2 unchanged audio xfails**. Focused Ruff and `git diff --check` passed.

Public evaluation confirms opacity **1 raw versus 0.5 projected** at frame 105; both exclude frame 120. MAIN render confirmation remains pending. The handoff identifies the App and Agent source-shortening seams without changing policy.

[Viewing handoff](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-visual-cap-fade-vector.md) · [Detailed report](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m3-visual-cap-fade-vector/notes/report.md)

Expanded JSON, `commit-msg`, and `DONE` are written. No full suite, pixels, or Runtime acceptance claimed.