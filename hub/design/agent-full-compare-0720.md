# Agent full-suite compare vs 109-node supported-env baseline

Read-only comparison. No repo changes, no commit-msg, no full* suite requested.

## Baseline

- Set: `$ORCH/design/agent-supported-env-baseline-109.md`, FAILED/ERROR lines from `$ORCH/tests/agent-full-remotion-integration-1020031037-28578/log.txt`.
- Counts: 79 failed, 30 errors, 11732 passed, 453 skipped.
- 109 node IDs, de-duplicated after stripping the ` - <reason>` tail that pytest appends to truncated ERROR lines.

## Run A: agent-full-remotion-integration-1020062923-20811

- Status: `fail`, exit 1, 3033 s.
- Tree: `1d140ead1c70eb87d93b3d0493f76d60a34eede4`, integration:agent (commit 481e600b).
- Companions: runtime `abbdcfc3`, app `b8064ecf`, composition `ff0536bb`.
- Command: `env -i ... ASTRID_REMOTION_PROJECT_DIR=/home/user/work/runtimes/agent-remotion ... /home/user/work/venv-agent/bin/python -m pytest -q -n 3` (suite `full-remotion-integration`).
- Counts: 81 failed, 11783 passed, 453 skipped, 16 xfailed, 30 errors, 563 subtests passed, 3030.79 s.
- Failure lines: 111 (81 FAILED + 30 ERROR). All 109 baseline nodes still fail.

### Diff vs baseline

- **FIXED: 0.** No baseline node passes now.
- **NEW: 2.**

| # | Node | Status |
|---|---|---|
| 1 | `tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup` | NEW |
| 2 | `tests/reshape/test_repo_hygiene.py::test_live_tree_passes_repo_hygiene` | NEW |

### Causes of the new failures

**1. `test_text_card_renders_visible_markup`: Composition 0.0.10 pin not in the runtime checkout. Environment and public10 adoption, not a D05/D06/D09 or M2 change.**
- Traceback: `tests/packs/rendering/test_remotion_render_contract.py:95`, `assertEqual(runtime_package, snapshot_package)`. The message is "selected Remotion runtime /home/user/work/runtimes/agent-remotion/package.json disagrees with snapshot package.json".
- The snapshot `remotion/package.json:18` pins `@banodoco/timeline-composition` to `artifacts/banodoco-timeline-composition-0.0.10.tgz`. The runtime checkout `/home/user/work/runtimes/agent-remotion/package.json` still pins `...-0.0.8.tgz`.
- Introduced by `fc6c1f26` "feat(rendering): adopt Composition 0.0.10 with bundle 1 parent track labels", which is after the 4a75f68f baseline. The runtime checkout was not moved to the same pin.
- Fix direction: align the runtime checkout's pin with the snapshot, or the test's environment. Not an Agent code defect. The test was green on the baseline because both sides were 0.0.8.

**2. `test_live_tree_passes_repo_hygiene`: a new root `design/` directory is not in the root allowlist. Doc-tree change, related to doc removal.**
- Traceback: `tests/reshape/test_repo_hygiene.py:227`, `find_unknown_root_entries(tracked) == []`. Actual value `['design/']`.
- `scripts/reshape/check_repo_hygiene.py:249` flags any tracked top-level dir not in `ROOT_DIR_ALLOWLIST`. The allowlist (about lines 41-75 of that file) has `docs`, `tests`, and no `design`.
- `design/` did not exist at the baseline (4a75f68f has no `design/` tree entry). It came from `fd82c36c` "docs(timeline): add audio and visual compile contracts with golden vectors", which is in the range after the baseline.
- `ac1c7db1` "docs(design): move review and process notes out of the repo" removed four files (-416 lines) from `design/` but left `design/audio-compile-contract.md` and `design/visual-compile-contract.md`, so the directory still exists and is still tracked.
- Fix direction: either allowlist `design` (a deliberate root doc dir), or move the two contracts under `docs/`. This is a hygiene policy decision, not a test bug.

### Not relevant to the new failures

- No new failure touches D05 (`astrid/core/timeline/inverses.py`) or D06 (`astrid/core/extensions/`).
- No new failure touches the D09 slice (check.py formatters, onscreen evaluator).
- No new failure touches the capture chain.
- No new failure touches the M2 stack. Run B has not reported (see below).

## Run B: agt-m2-stack-sync-2-full-remotion-integration-1020063510-102

- Status at the time of reading: `running` (started 07:20:17 UTC, log still growing at 07:27 UTC).
- Per the brief, B is **not** reported here. Run B has no results yet. Re-run this comparison once `status` reads `fail` or `pass`.

## Verdict

**2 new failures (not 0 new):**
1. `tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup`: runtime checkout still pins Composition 0.0.8, snapshot pins 0.0.10 (`fc6c1f26`).
2. `tests/reshape/test_repo_hygiene.py::test_live_tree_passes_repo_hygiene`: root `design/` dir (from `fd82c36c`, trimmed by `ac1c7db1`) is not allowlisted.

Neither is a D05/D06/D09 or M2 regression. The baseline 109 are unchanged: 0 fixed.

## Unverified

- I did not re-run either new test locally. Causes come from the log tracebacks and tree inspection.
- Cause 1 assumes the runtime checkout at `/home/user/work/runtimes/agent-remotion` is the one the run used, which the `ASTRID_REMOTION_PROJECT_DIR` env in the run request confirms.
