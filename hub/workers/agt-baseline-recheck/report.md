The 109-node baseline re-run is complete. Under the recommended `remotion-0010-nodes` env, 27 of the 109 nodes are still red: 23 are environment, 3 need a decision, and 1 is flaky. The full write-up is at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/agent-baseline-recheck-0900.md`. The DONE marker is written. The worktree is clean and I made no repo changes.

**Recommended env: `remotion-0010-nodes` (0.0.10).** The product expects 0.0.10 (`remotion_runtime.py:48`), and the snapshot pins 0.0.10 (`remotion/package.json:18`). On 0.0.8 and 0.0.12, about 40 nodes fail the version gate. The TextCard node compares the runtime's `package.json` against the snapshot, so it passes only on 0.0.10. The baseline's 109 was measured on 0.0.8, so many of its reds were the wrong runtime. Moving to 0.0.12 needs the snapshot pin and the expected version bumped together, which is an owner decision.

**Runs** (all against `integration:agent`, the clean integration worktree at `931d7ec5`):

| Suite | Result | Note |
|---|---|---|
| `remotion-env-nodes` (0.0.8) | 26 failed, 68 passed, 15 errors | TextCard red |
| `remotion-0010-nodes` (0.0.10) | 12 failed, 82 passed, 15 errors | TextCard green |
| `remotion-0012-nodes` (0.0.12) | 26 failed, 68 passed, 15 errors | TextCard red |
| single node, 0.0.10, `--no-cache` | 1 passed | the 120-400 budget node |

**Per group, baseline (0.0.8) → 0.0.10 after fixes:**
- **A (27):** 27 red → 0 red after the rerun. The 120-400 node failed once in the full run and passed alone.
- **B, D, E, F, I, K (4, 11, 34, 3, 1, 1):** all pass.
- **C (3):** 3 red → 2 red. The `pack_root` error is gone; two nodes now fail `assert 2 == 1` on inventory reads.
- **G (1), H (7), M (15):** still red in every env.
- **J (1):** still red in every env.
- **L (1):** the import error is gone, but the file's tests are deselected by `addopts` and never run in a named suite.

**Remaining reds, 0.0.10, with owner:**
- **G, ENV (agent-owner decision):** the child `worker_process.py` imports `astrid` at module top (line 42). `venv-agent` has no `astrid`, and `env -i` sets no `PYTHONPATH`. The child's stderr is discarded. I did not run it, so this is confirmed from code only.
- **H, ENV:** `python -I -c "import astrid"` → `ModuleNotFoundError`. Same root as G. One editable install of `astrid` into the supported venv would fix both.
- **M, ENV:** needs a VibeComfy checkout at `/home/vibecomfy/vibecomfy`, which does not exist. Provision it or add a path override.
- **J, decision → recommend fixing the test.** The product's `CommandCleanupUnresolved` wrapper is intentional and load-bearing, since the task path catches it explicitly (`generic_host.py:9814`). The test should expect that type, keep the same message match, and assert the `CleanupUncertainError` as `__cause__`. This changes an expected exception type, not a removed behaviour, but it should be flagged in the commit.
- **C count (2), decision → recommend fixing the test.** The second inventory read is deliberate: `remotion_runtime.py:606` re-verifies inside the Remotion probe. Replace the exact count with "every read returns the identity the launch records." Making the probe reuse the bootstrap's read would be a product change.
- **A flake (1):** `registry corpus changed during owned discovery` on the full run only. Likely concurrent suites sharing the runtime checkout, which I have not proven. Investigate if it recurs in a solo run.
- **L, unverified:** needs an `-m integration` suite for that one file. I did not request one because `suites.conf` is orchestrator-owned.

**For the orchestrator:** repoint `full-remotion-integration` (line 43), `consumer-regressions-integration` (line 31, which holds the TextCard node) and `real-pack-host-integration` (line 38) from `agent-remotion` to `agent-remotion-0010`. I did not test the plain `agent full` suite, which sets no Remotion env at all.
