# vw-m3-scene-span-adjacency

## Change

- `spans_from_frames` now merges matching scene answers only when the prior span ends at the current answer's frame. Sparse answers such as frames 0 and 30 remain separate `[0, 1)` and `[30, 31)` spans.
- Added direct regressions for sparse answers and for contiguous matching answers with content, visible-clip membership, and finding boundaries.
- Duplicate/unsorted input is not sorted or treated as covered; non-adjacent rows remain separate. The one-sided-fade summary contract and all renderer/provider paths are unchanged.

## Before / after

Exact focused command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_host_scene.py -k 'spans_from_frames'
```

- Before source fix: **FAIL**, 1 failed, 1 passed, 18 deselected, exit 1. The sparse case incorrectly produced `[0, 31)`.
- After source fix: **PASS**, 2 passed, 18 deselected, exit 0.

## Checks

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m ruff check --no-cache astrid/core/timeline/scene_answers.py tests/packs/rendering/test_host_scene.py`: **PASS**.
- `git diff --check`: **PASS**.
- The targeted native contiguous-range command was attempted:
  `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/packs/rendering/test_host_scene.py -k 'large_native_batch_is_not_truncated or spans_from_frames'`.
  The two direct tests passed, but the existing native test errored during fixture setup because this worktree has no `remotion/node_modules/esbuild`; no install or node_modules copy was performed. Native 300-frame execution is therefore unverified here, while its existing test and expectation remain unchanged.
- No full suite, browser, socket, renderer parity, artifact/pin, generator, provider, save-path, or SDK changes were run or made.

## Remaining scope

The manager-reported 15 known strict scene gaps remain unchanged; no old tests or xfails were edited. The requested manager `QUIET.md` and worker `REVIEW.md` were not present in the available orchestration paths.
