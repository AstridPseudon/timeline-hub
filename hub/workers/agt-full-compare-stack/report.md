## Verdict: the M2 stack adds 0 new failures

The M2 run (`agt-m2-stack-sync-2-full-remotion-integration-1020063510-102`, status fail, exit 1) has exactly the same 111 FAILED/ERROR nodes as the integration run. A `diff` of the two sorted lists returned exit 0. Compared with the 109-node baseline, M2 is a strict superset with 2 extra nodes, and both are already in integration. Nothing from the baseline was fixed.

| Run | Failed | Errors | Passed | Skipped | xfailed | Unique FAILED+ERROR |
|---|---:|---:|---:|---:|---:|---:|
| Baseline 1020031037-28578 | 79 | 30 | 11732 | 453 | not recorded | 109 |
| Integration 1020062923-20811 | 81 | 30 | 11783 | 453 | 16 | 111 |
| M2 1020063510-102 | 81 | 30 | 12998 | 453 | 14 | 111 |

**The two nodes new relative to baseline, both inherited from integration:**
1. `tests/packs/rendering/test_remotion_render_contract.py::TextCardVisibleMarkupTest::test_text_card_renders_visible_markup`. Cause: `test_remotion_render_contract.py:95` fails because the runtime checkout pins Composition `0.0.8` while the snapshot pins `0.0.10` (`fc6c1f26`). Owner is the runtime checkout and env pin, not an M2 area.
2. `tests/reshape/test_repo_hygiene.py::test_live_tree_passes_repo_hygiene`. Cause: `test_repo_hygiene.py:227` fails on the tracked root `design/` dir, which is not allowlisted. `design/` is tracked in the M2 tree `0afb198d`. Owner is docs/hygiene.

**Brief premise does not hold:** the brief says groups A, B, C, D, E, F, I, K and L were fixed on integration. They are not. Every node in those groups still fails in both integration and M2, with the same causes (for example `ERR_UNKNOWN_FILE_EXTENSION` for D, `No module named 'astrid.packs.runpod.executors'` for E, `NameError: name 'signal'` for F). Fixed vs baseline is 0.

The full 111-node list, grouped by cutlist label, and the per-group trace evidence are in the report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-full-compare-stack-0805.md`

## What I did
- Extracted FAILED/ERROR nodes from the three logs and diffed the sorted lists. The M2 and integration lists are identical.
- Grepped the M2 log to confirm the cause messages for each group.
- Ran one read-only `git ls-tree` to confirm `design/` is in the M2 tree.
- No repo changes and no test runs. `DONE` is created. I did not write `commit-msg` because the task makes no repo change.

## Unverified / to check
- M2 shows +1215 passed and 2 fewer xfailed than integration. The summaries do not explain this. Check which tests moved from xfailed to passed before accepting the M2 tree. This does not change the failure verdict.
- Some group traces (B, C, I, J, K) are not in the kept tracebacks of this run. Their node IDs are still in the failing set, and their causes come from the cutlist.
