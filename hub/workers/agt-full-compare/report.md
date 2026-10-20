## Agent full-suite compare: run A has 2 new failures; run B still running

The comparison doc is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-full-compare-0720.md`, and `DONE` is created. The worktree is clean, and I made no repo changes and no commit-msg. I did not request any full* suite.

**Run B (`agt-m2-stack-sync-2-…-1020063510-102`) has not finished.** Its status is `running`, so this report covers run A only.

### Run A: `agent-full-remotion-integration-1020062923-20811`

- Status `fail`, tree `1d140ead`.
- Counts: 81 failed, 11783 passed, 453 skipped, 16 xfailed, 30 errors. The baseline was 79 failed, 11732 passed, 453 skipped, 30 errors.
- Failure nodes: 111 lines (81 FAILED + 30 ERROR), against 109 in the baseline.
- **FIXED: 0.** All 109 baseline nodes still fail.
- **NEW: 2.**

| New failure | Likely cause | Relates to |
|---|---|---|
| `tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup` | Assertion at `test_remotion_render_contract.py:95`. The snapshot `remotion/package.json:18` pins Composition `0.0.10`, but the runtime checkout `/home/user/work/runtimes/agent-remotion/package.json` still pins `0.0.8`. The pin came from `fc6c1f26` (adopt Composition 0.0.10). | Public10/Composition adoption and the runtime checkout, not the Agent code. |
| `tests/reshape/test_repo_hygiene.py::test_live_tree_passes_repo_hygiene` | Assertion at `test_repo_hygiene.py:227` returns `['design/']`. `scripts/reshape/check_repo_hygiene.py:249` flags the root `design/` dir because it is not in `ROOT_DIR_ALLOWLIST`. The dir was added by `fd82c36c` and trimmed by `ac1c7db1`, which removed four docs and left two contract files. | Doc removal. |

Neither failure touches D05, D06, the D09 slice, the capture chain, or the M2 stack.

**Verdict: 2 new, not 0.** A decision is needed on the `design/` root: allowlist it, or move the two contracts under `docs/`. The Remotion pin needs aligning in the runtime checkout.

### Unverified

I did not re-run either new test locally. The causes come from the log tracebacks and from inspecting the trees.
