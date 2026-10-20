The cut list is written to `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-baseline-109-cutlist.md`, and the `DONE` file is created. This was read-only analysis: I changed no repo files, ran no suite, and wrote no commit message.

## Result

All 109 nodes are classified. Counts are against the exact 109-node set from the full-remotion-integration log (79 FAILED, 30 ERROR).

| Class | Nodes |
|---|---:|
| FIX | 86 |
| ENVIRONMENT | 23 (one of these provisional) |
| DELETE | 0 |

## Main findings

- **Group A, 27 nodes, S, agent: test-harness pollution.** `tests/conftest.py:15-18` puts `PYTHONPYCACHEPREFIX` into `os.environ` under `env -i`. The Remotion probe refuses that key (`remotion_runtime.py:200-222`), and the host copies the whole environment (`host_bootstrap.py:734`). The 13 host-bootstrap `RemotionValidationError` nodes and the 14 host-recovery errors come from this. The 63-node normal baseline never hit it because the Remotion variable is unset there. This is the highest-yield change. The expected effect is from code reading only; I did not run it.
- **Group E, 34 nodes, M, agent: stale module path.** The tests import `astrid.packs.runpod.executors`, which was moved to `shared/common.py`. Separately, `runpod_lifecycle` is a pinned dev-extra that is not installed in `venv-agent`. The env owner needs to install it, or the path fix just moves the failure.
- **Group D, 11 nodes, S, agent: wrong Node assumption.** The pixel-shape tests import a `.ts` file directly with Node 20.19.4, which is the pinned version. The repo already has an esbuild-based pattern to copy.
- **Group H, 7 nodes, and group M, 15 nodes: environment.** H needs astrid importable in the child interpreter, and M needs a VibeComfy sibling checkout that does not exist here.
- **Group G, 1 node: provisional environment.** The owned-host child probably cannot import astrid, because its stderr is discarded. This is an inference from code. It needs one confirming run.

## Decisions I made

- Classified the generic-host failure (group J) as FIX, expecting `CommandCleanupUnresolved` with the original cause chained. The alternative is a product fix if the owner decides the wrapper is wrong.
- Recommended no deletions. Every failing node still covers behaviour the product has.
- Group C (3 nodes, `PosixPath.pack_root`) is not pinned to specific node IDs. The code only lets one test in that file reach the failing fake. The second trace in the log falls in a section that does not use it, so either the trace attribution or the count is off. One targeted run resolves it.

## Unverified

- No node was run. Groups A, B and D are expected to pass after their fixes but are not verified.
- Group E's behavioural failures are unknown until the imports resolve.

## Suggested work-down order

1. A (conftest), then B, which is the same remotion-env cause family.
2. D, F, C, I, J, L (small, test-side).
3. E, once the env owner has installed `runpod-lifecycle`.
4. Confirm G with one run.
5. Decide H and M with the env owner.
6. K last, against the final tree, since the line counts move with every commit.
