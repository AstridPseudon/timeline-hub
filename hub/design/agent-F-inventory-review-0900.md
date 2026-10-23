# Agent F inventory review 0900 — FAIL

Source tree: Agent worktree `HEAD`
`1b8ade983157f238c5a0f7d312c385f400f97400`, author base
`e837e18c5156e762eca05e6d9bb15779cf847b60`.

## Verdict

**FAIL** on one bounded documentation finding. The 0847 implementation delta
passes its exact acceptance group and the independent no-weakening audit, but
the giant-file rationale contains stale current-inventory counts.

## Finding and bounded fix

`docs/giant-file-rationale.md` line 58 says the current M1-owned timeline
snapshot has `timeline/cli.py` at 4,127 lines and `timeline_sheet.py` at 1,313
lines. Current `wc -l` counts are 4,045 and 1,470. The table rows are 4,043
and 1,470; all 37 current oversized Python files have 37 existing rationale
entries and satisfy the ±50-line table tolerance. Update only the closing
sentence to truthful current counts; do not increase the 1,200-line budget or
add an exemption. This is the sole FAIL reason.

## Evidence

- Exact 11 nodes from the author brief: **11 passed in 43.47s**.
- Fork neighbours (`test_recipe_occurrence_fork.py`,
  `test_provider_occurrence_fork.py`, `test_commit_runtime_occurrence_fork.py`):
  **26 passed in 6.49s**.
- Metadata validator negatives: **8 passed in 20.42s**; authoring/projection
  invalid-meta nodes: **2 passed in 2.51s**.
- `make ruff PY=/home/user/work/venv-agent/bin/python`: **2149/2149**.
- `scripts.reshape.compare_mypy_baseline`: **1912/1912**.
- `scripts/vendor_lock.py check runtime.lock.json --producer
  /home/user/work/wt/rt-pin-34eac004`: passed.
- `scripts/artifact_manifest.py --check`: passed.
- `git diff --check e837e18c5 HEAD`: passed; worktree clean.
- Frozen schema and runtime lock hashes match base exactly:
  `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d` and
  `320d278366bc344aad35f3564845d9b62d9cc5f2e000a8a4cc6b6fea508d6cd2`.

An exploratory command with four nonexistent pytest node names collected no
tests; it is excluded from evidence and was followed by the corrected passing
metadata commands. No full, browser, live-socket, heavy journey, or duplicate
farm suite was run.

## Audit decisions

- `occurrence.fork` is provider-only as briefed: actual `operations()` registry
  uses closed `FORK_PARAMETERS`, unknown fields are rejected, and the 26 fork
  tests cover provider/runtime behavior, golden-like captured command use,
  replay, and guarded undo. No wire cohort tuple was added.
- No promised `timeline.open`/`commit`/helper/fork API was removed.
- Removed root metadata exports have no production callers or supported public
  surface use; canonical `validators.meta` exports and direct production
  imports remain. `DocumentPatchError` remains the emitter production error;
  only the unused alias was removed.
- The optional full-fixture `meta` omission preserves the fixture’s substantive
  coverage and dedicated namespace/type/size/depth/invalid-value negatives.
- No generated maps, schema/client tuple, pin, lock, or shared dependency was
  changed. The two deleted files are exactly the explicitly named stale root
  P1 handoffs.

Recommended next step: make the one documentation-only count correction and
rerun the giant-file node plus diff check. No source fix is requested.
