Implemented D127 in the two authorized files:

- Added bounded `top_leaf_frames` nearest-safe projection.
- Added truthful lifecycle labels and separate `buffer_complete`.
- Preserved budgets, privacy, watchdog cancellation, and existing assertions.
- Added adversarial leaf, bounds, lifecycle, exception, and duration tests.

Tests:

- Offline focused: `21 passed, 2 deselected`
- Ruff, helper-only mypy, py_compile, and `git diff --check`: passed.
- Exact full file command: `21 passed, 2 failed` because sandbox socket creation is denied.
- Central targeted run queued but blocked by disk floor; no result claimed.

Evidence and commit message are recorded under the assigned worker directory. DONE created.