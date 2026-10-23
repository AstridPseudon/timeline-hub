# Runtime R2r leaf inverse materialization handoff

Status: **blocked**.

The Agent1246 report and peer handoff classify the retained refusal as a Runtime leaf-stage physical turnover problem. A strict candidate was implemented in `_inverse_stage_boundaries` in the assigned Runtime worktree. It consumes authenticated `commit.materialization` bindings, maps source-history logical IDs through the actual stage owner/family and successor digest, applies only exact owner-preserving internal → shot → parent turnover, and requires complete payload and physical ownership equality afterward. Existing root, sequential, history/range, effect-binding, digest, ABA, and persistence guards remain intact.

The required Runtime targeted suite passes: 138 tests. Ruff, Pyright, AST parse, and diff checks pass. No test file was changed because the supplied causal regression could not be made to reach the diagnosed leaf boundary.

Both `/home/user/work/agent` at `f6116e1` and a private archive of the exact Agent `bfcf78db998868e4a7d92779a83cd3aaba82a98a` refuse the supplied deterministic fork + emitter undo at `_inverse_stage_root` with `inverse stage root differs from its sequential input`, before `_inverse_stage_boundaries` physical-map equality. The advertised durable auth-input/stage-comparison artifacts are absent, so this discrepancy cannot be resolved without fabricating evidence. Do not merge or claim the candidate as causal PASS until the manager supplies those artifacts or the exact original checkout pair.
