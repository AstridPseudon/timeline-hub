# F-zip-dry rehearsal: agent (tf-zip-agent), PARTIAL, BLOCKED at step 3

Rehearsal only. Nothing pushed, no edits to the repo, tests, pins or locks.

## Step results

| Step | Result | Notes |
|---|---|---|
| 1. Integration commit, tree, base ancestry | PASS | see SHAs below |
| 2. Squashed patch base..integration | PASS | 8,548,648 bytes; 820 files; +157,292 / -9,604 lines |
| 3. Fresh upstream clone at base, `git apply --check` + apply, tree equals integration | **BLOCKED** | `git checkout --detach 431681a6d` in the fresh clone was denied by the permission system. Not routed around, per the brief. |
| 4. Apply to live upstream tip | NOT RUN | needs the same working-tree apply as step 3 |
| 5. Typecheck, lint, smoke on the applied fresh tree | NOT RUN | depends on step 3 |

## SHAs and trees

- Integration `tl/integration` (agent, /home/user/work/agent): `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe`
- Integration tree (`8c355a48e^{tree}`): `c4d72b065d6e68c92e4335120cc016cadf53b06a`
- Hub ref `hub/timeline/agent/tl/integration`: `8c355a48e4cc2a8ec9d5ed6873a585d2540a2dbe` (identical)
- Base `431681a6d`: `431681a6d3cfa0bba2c8c9baa03f152d33032df1`
- `git merge-base --is-ancestor 431681a6d <integration>`: yes
- Live upstream `refs/heads/main` (`git ls-remote https://github.com/peteromallet/astrid-agent refs/heads/main`): `74f3f7edba35230d0a01824eae7b663143e6aa5b`
- Fresh clone `origin/main` (cloned during this run): `74f3f7edba35230d0a01824eae7b663143e6aa5b`, equal to live.
- `git merge-base --is-ancestor 74f3f7edb <integration>`: yes. The U2b upstream merge is already in integration.

## Patch (step 2)

- Command: `git -C /home/user/work/agent diff --binary 431681a6d 8c355a48e`
- Size: 8,548,648 bytes
- Files: 820 (`git diff --numstat`)
- Lines: +157,292 / -9,604
- Product vs tests (heuristic by path and name: `tests/`, `test_*`, `*.test.*`): 514 test-like, 306 product-like. The heuristic is rough; the test-like group holds +128,445 / -3,324 lines.
- Patch file: `$ORCH/workers/tf-zip-agent/tmpdir2/zip-agent.patch`

## Step 3 refusal (exact)

The clone succeeded: `git clone --filter=blob:none https://github.com/peteromallet/astrid-agent <worker>/tmpdir2/fresh` (3041 files). The next command was denied:

```
git -C .../workers/tf-zip-agent/tmpdir2/fresh checkout -q --detach 431681a6d 2>&1 | tail -3
Permission to use Bash with command git -C .../tmpdir2/fresh checkout -q --detach 431681a6d 2>&1 has been denied.
```

Other notes:
- The brief names `/tmp/w-78364032e4` as tmpdir. A `mkdir` there needed approval (path outside the session's working directories), so the scratch files went under `$ORCH/workers/tf-zip-agent/tmpdir2/` instead.
- Step 4 is degenerate: the squashed patch base already contains the live tip 74f3f7edb, so most hunks will be "already present" against the tip, not real conflicts. The meaningful drift check is the ancestry result above (no drift remains).

## Not run

- No typecheck (ruff, mypy), lint, or `pytest --collect-only -q` ran on the applied tree. Step 5 needs step 3.
- The integration worktree (`/home/user/work/wt/tf-zip-agent`, HEAD `8c355a48e`, clean) was not used as a substitute for the fresh-tree check.

## Next step

Allow `git checkout --detach <sha>` inside a fresh clone under the worker tmpdir, or give the fresh clone a checkout another way the owner approves. Then rerun steps 3 to 5. Expected result: the applied tree equals `c4d72b065d6e68c92e4335120cc016cadf53b06a`.
