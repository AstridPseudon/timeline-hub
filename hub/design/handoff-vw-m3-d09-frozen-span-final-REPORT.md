# D09 SDK summary test-style packet

## Result

Prepared the corrected, unapplied D09 SDK summary patch at `PATCH`. Applied
the peer frozen-span correction privately, formatted only the newly
introduced `tests/sdk/test_scene_summary_projection.py` with Ruff, validated
the private patch, and reversed it. The product worktree is clean.

The product change remains bounded to `astrid/sdk/timeline/check.py`: warning
rows are projected into copied records, with `dataclasses.replace` for frozen
dataclass spans and a copied mutable fallback. Detailed input rows are not
mutated; membership/findings remain intact; adjacent rows are merged only
when class/content match and frame boundaries touch; sparse gaps are not
bridged; `GAP` remains distinct from `COVERED` + `EMPTY`.

## Source and changed paths

- Source/tree: `/home/user/work/wt/vw-m3-d09-summary-new-test-style-packet`, branch `tl/vw-m3-d09-summary-new-test-style-packet`, clean base `520fd2179`.
- Unapplied patch paths: `astrid/sdk/timeline/check.py`, `tests/sdk/test_scene_summary_projection.py`.
- Durable payload: `PATCH` in this worker directory.
- Assertion preservation: 7 assertion statements in the new test file; all 7 remain unchanged in meaning and assertion content after formatting.

## Evidence

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/sdk/test_scene_summary_projection.py tests/sdk/test_scene_caller_preservation.py tests/sdk/test_coverage_empty_cut.py` — **22 passed in 0.80s**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m ruff format --check tests/sdk/test_scene_summary_projection.py` — **1 file already formatted**.
- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m ruff check tests/sdk/test_scene_summary_projection.py` — **All checks passed**.
- `git diff --check` while privately patched — **passed**.
- `git apply --check PATCH` after reversing from the clean product tree — **passed**.
- `git status --short --branch` after reverse — clean branch, no source/test changes.

## Decision and limits

The peer patch was applied as the settled correction; no source-shape or
wire-shape deviation was needed. No full suite, browser, renderer, live
socket, install, managed proof replay, activation, physical/API run, or
private geometry deletion was run or performed. Existing `check.py` formatting
and lint backlog was intentionally left untouched because only the newly
introduced test file was in formatter/lint scope.
