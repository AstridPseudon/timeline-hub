## Report — F-D52-core-five

Completed read-only actual-home1330 verification. No repository files changed; no commit needed.

Artifacts verified:

- XML: 204301 bytes, SHA256 `5dbab3763e4339a8463186735dcb57799fb04da94bc3beced11115245f5eb31e`
- Map: 29006 bytes, SHA256 `279468169f07472f806632dcff46f2631d932acd0640eb61c1034e201edcc510`

All five named cases are present and PASS:

| Case | Param | Map order | XML time |
|---|---|---:|---:|
| `test_captured_config_root_rejects_tampering_without_mutation` | `native-order` | 6 | 0.080s |
| `test_root_config_history_rejects_tampering_without_mutation` | `native-order` | 72 | 0.160s |
| `test_retained_app_fork_reload_undo_restores_exact_closure` | none | 97 | 0.560s |
| `test_fork_output_guard_allows_independent_parent_edit_and_preview_redo` | none | 182 | 1.957s |
| `test_valid_fork_history_distinguishes_output_consumers_from_retained_sibling` | `retained-sibling` | 183 | 1.204s |

This closes the five on original actual-home1330 scope: three retained Runtime PASS cases plus two held fork-redo cases now directly evidenced as PASS in the authentic XML/map. Prior source/body identity remains byte-equal for Agent `47b744dfe908…` versus held source; Runtime custody is `becfe6db88b2…`. The current fork failures at orders 11, 13, 98, and 99 are distinct and were not conflated.

Checks:

- XML/TSV exact membership and durations: PASS
- `sha256sum`: PASS
- `git diff --check`: PASS
- Worktree status: clean
- Typecheck/lint/tests/full/browser/HTTP: not run, prohibited/N/A

Limits remain explicit: this is historical actual-home1330 evidence, not current e68/AgentD60 or final-tuple proof; no aggregate substitution or whole-v2/HTTP inference. `DONE` marker created.