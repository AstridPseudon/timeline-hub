Implemented WC6 bounded consumer proof on `e86f44d0`.

- Composed reviewed source `74fa9c67`.
- Preserved generated014 pin bytes and P1/F1/Scene/Root/AM behavior.
- Added authenticated same-alias rebind/inverse coverage and native document script support.
- Updated test fixture to exact Runtime `a0dca169…`; no `own_materialized_read` exemption.
- Narration/structural legacy positives remain open; no whole-WC6 deletion claim.

Evidence:

- Focused tests: **12 passed**
- Ruff + `git diff --check`: **passed**
- Native HTTP WC6 node: **1 passed**
- Targeted `test_authoring_media.py`: **71 passed, 1 deselected**
- Full suite: not run.
- One no-filter neighbor had a pre-existing `ModuleNotFoundError`; unchanged.

Handoff, commit message, and `DONE` marker written under the requested orchestration paths.