## Report

- Classified all 17 errors from exact `79b/tree6de`: all were the same pytest setup failure, `fixture 'native_host' not found`; no Sprite assertion or product source was reached.
- Added rendering-scoped fixture registration in [conftest.py](/home/user/work/wt/agt-tests-full10744-sprite-setup/tests/packs/rendering/conftest.py); removed only the ineffective duplicate registration line from [test_sprite_scene_capability.py](/home/user/work/wt/agt-tests-full10744-sprite-setup/tests/packs/rendering/test_sprite_scene_capability.py).
- Preserved all 45 original assertions, including geometry, UNKNOWN states, declarations, and installed-byte checks.
- Targeted central tests:
  - `renderer-peers12-integration`: **17 passed** (xdist, 37.98s)
  - `native-script-current-integration`: **17 passed** (44.26s)
- Ruff: passed. `git diff --check`: passed.
- No full rerun, shared dependency/profile writes, product changes, skips, or xfails.
- No child-profile mismatch was proven because the historical run failed before host setup.

Artifacts: [classification](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-full10744-classification.md), [report](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-tests-full10744-sprite-setup/report.md). `commit-msg.txt` and `DONE` were created.