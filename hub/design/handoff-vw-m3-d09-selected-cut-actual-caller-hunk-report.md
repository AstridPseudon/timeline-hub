## Result

- Updated the production `render_lipsync` caller to skip private `model.mouth_box` when validated public Scene ROI rows cover the exact selected frames.
- Private fallback, pixel statistics, frame membership, denominator, and `>2%` threshold remain unchanged.
- One production-line diff; no tests or APIs added.

## Verification

- Selected-cut public13 lane: **23 passed**.
- Crop-equivalence and motion neighbors: **42 passed, 2 skipped**.
- `py_compile` and `git diff --check`: passed.
- No full suite, browser, render, managedproof, activation, install, or network run.

Artifacts: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-selected-cut-actual-caller-hunk/report.md), [commit-msg](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-d09-selected-cut-actual-caller-hunk/commit-msg). `DONE` created.