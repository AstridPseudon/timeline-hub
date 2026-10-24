## Report

Ported reviewed G4 historical source authority onto current `622b30a8c3`.

Changed only:

- `native_occurrence_shared.py`
- `commands.py`
- `commit.py`
- Three reviewed historical test files

The three source blobs exactly match reviewed `f55393e5b8`. Current test stubs were adapted for the present `open_bundle` API.

Tests:

- Cumulative 28 lane: 26 passed, 2 failed.
- Historical/non-last-owner + D20: 29 passed, 1 failed, 1 deselected.
- D20 lane: 9 passed.
- Runtime archive recheck on `rt-pin-36760ee0`: 1 passed.
- Ruff, private mypy, vendor lock, artifact manifest, compile, and `git diff --check`: passed.

Blocker: both failing production-session tests require the reviewed `sync.py` foreign-intent carrier, explicitly outside this task’s allowed files. Current path is `TimelineSession.commit → commit_many → _stage`, which locally executes the foreign command and raises `shared placement requires Runtime-authenticated source`. No prohibited change was made.

Commit message written; `BLOCKED` marker created.