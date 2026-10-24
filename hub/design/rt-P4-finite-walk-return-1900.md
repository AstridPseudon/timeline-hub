## Completed

- Restored eager sibling snapshot semantics in `finite_json` by snapshotting container child references before traversal.
- Added synchronized in-place mutation regression test.
- Changed only:
  - `runtime_protocol/timeline_commit_validation.py`
  - `tests/test_timeline_validation_walk.py`

## Validation

- Focused union: **173 passed, 1 deselected**
- Historical tamper tests: **12 passed**
- Ruff: passed
- Compile: passed
- `git diff --check`: passed
- Pyright: one unchanged nullable-URI diagnostic; zero new diagnostics
- Three old/new control pairs all passed:
  - **5.69% wall improvement**
  - **6.09% user CPU improvement**
- Reused unchanged profile counts: 1,418 finite walks, 889 schema validations, 440 image captures, 110 sequential captures, 107 historical replays.

Evidence is under the worker evidence directory. Original P4 gate remains open and was not run.

Commit message written and `DONE` marker created.