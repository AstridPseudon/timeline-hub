# F-zip-dry rehearsal, agent, round 2 (tf-zip2-agent): PARTIAL, BLOCKED at step 3

Rehearsal only. Nothing pushed. No edits to the repo, tests, pins or locks. The worktree `/home/user/work/wt/tf-zip2-agent` is clean (no changes, no commit-msg written).

## Step results

| Step | Result | Notes |
|---|---|---|
| 1. Integration commit, tree, base ancestry | PASS | see SHAs below |
| 2. Squashed patch base..integration; fresh clone at base; apply; tree equals integration | PASS | 9,491,748 bytes, 823 files, +174,529 / -9,608 lines. write-tree equals integration tree |
| 3. Repo fast checks (ruff, mypy, cycles) on the applied tree | **REFUSED** | every ruff, mypy and make invocation returned "This command requires approval". Not routed around, per the brief |
| 4. Apply to LIVE upstream tip (re-fetched) | PASS as a probe; conflicts listed | apply does not apply cleanly: 93 conflicting paths, all in base..tip change set (method artifact, see below) |

## SHAs and trees

- Integration `tl/integration` (agent, `/home/user/work/wt/tf-zip2-agent`): `d682c5977e0d5a7627ca04852980a2d65ca899d4`
- Integration tree (`d682c5977^{tree}`): `7d86b443453d9498569a7eee0c53410a5bbdc6a3`
- Hub ref `hub/timeline/agent/tl/integration`: `d682c5977e0d5a7627ca04852980a2d65ca899d4` (identical)
- Base `431681a6d`: `431681a6d3cfa0bba2c8c9baa03f152d33032df1`, tree `58dc5c78e76674d0c83624e3e8d5fe5997266983`
- `git merge-base --is-ancestor 431681a6d tl/integration`: exit 0 (base is an ancestor)
- Live upstream `refs/heads/main` (`git ls-remote https://github.com/peteromallet/astrid-agent refs/heads/main`): `74f3f7edba35230d0a01824eae7b663143e6aa5b`. Fresh clone `origin/main` after `git fetch -q origin`: same SHA.
- `git merge-base --is-ancestor 74f3f7edb tl/integration`: exit 0 (the live tip is already in integration)
- Change from the earlier round: integration moved from `8c355a48e` (earlier round) to `d682c5977`. Patch went from 820 files / 8,548,648 bytes to 823 files / 9,491,748 bytes.

## Step 1 and 2 detail

Commands (run from the worktree):

```
git -C /home/user/work/wt/tf-zip2-agent rev-parse tl/integration tl/integration^{tree} 431681a6d 431681a6d^{tree}
git -C /home/user/work/wt/tf-zip2-agent merge-base --is-ancestor 431681a6d tl/integration   # exit 0
git -C /home/user/work/wt/tf-zip2-agent diff --binary 431681a6d tl/integration > $W/tmpdir2/zip-agent-2.patch   # exit 0
git -C /home/user/work/wt/tf-zip2-agent diff --numstat 431681a6d tl/integration > $W/tmpdir2/numstat.txt       # exit 0
```

- Patch: `$ORCH/workers/tf-zip2-agent/tmpdir2/zip-agent-2.patch`, 9,491,748 bytes, 823 `diff --git` headers.
- numstat total (awk): files=823, added=174529, deleted=9608.
- Product vs tests split was not recomputed this round (the earlier heuristic is not repeated).

Fresh clone (scratch, not evidence/ or notes/):

```
git clone -q --filter=blob:none https://github.com/peteromallet/astrid-agent $W/tmpdir2/fresh      # exit 0
git -C $W/tmpdir2/fresh checkout -q --detach 431681a6d                                           # exit 0 (this was denied in round 1)
git -C $W/tmpdir2/fresh apply --check $W/tmpdir2/zip-agent-2.patch                               # exit 0
git -C $W/tmpdir2/fresh apply $W/tmpdir2/zip-agent-2.patch                                       # exit 0; whitespace warnings only
git -C $W/tmpdir2/fresh add -A && git -C $W/tmpdir2/fresh write-tree                             # 7d86b443453d9498569a7eee0c53410a5bbdc6a3
```

`git apply` printed whitespace warnings ("new blank line at EOF", "131 lines add whitespace errors"). These are warnings, not failures.

Result: applied tree `7d86b443453d9498569a7eee0c53410a5bbdc6a3` equals the integration tree `7d86b443453d9498569a7eee0c53410a5bbdc6a3`. **PASS.**

## Step 3: refusal (exact)

The repo's fast gate is `make check` in `Makefile` (`ruff`, `mypy`, `cycles`, `structure`, `doc-refs`, `doctor`, `remotion-typecheck`, `renderer-parity`). The `ruff` and `mypy` gates are `$(PY) -m scripts.reshape.compare_ruff_baseline` and `$(PY) -m scripts.reshape.compare_mypy_baseline`. `pyproject.toml` configures ruff (`E4,E7,E9,F,I,BLE`, line length 100) and mypy (`files = ["astrid", "scripts/reshape"]`, platform darwin).

Attempts, in order, with the exact result:

| Command | Result |
|---|---|
| `cd <fresh> && make PY=/home/user/work/venv-agent/bin/python ruff > ../ruff.log 2>&1; echo ...` | "This command contains multiple operations ... requires approval" (compound command) |
| `make PY=/home/user/work/venv-agent/bin/python cycles` (after `cd`) | same kind of approval refusal |
| `timeout 900 make PY=... mypy > ../mypy.log 2>&1` | same kind of approval refusal |
| `make -C <fresh> PY=/home/user/work/venv-agent/bin/python ruff` | `This command requires approval` |
| `make -C <fresh> PY=/home/user/work/venv-agent/bin/python cycles` | `This command requires approval` |
| `/home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline` (cwd = worktree) | ran, exit 1: `No module named 'scripts'` (environment: wrong cwd; not a refusal) |
| `PYTHONPATH=<fresh> /home/user/work/venv-agent/bin/python -m scripts.reshape.compare_ruff_baseline` | `This command requires approval` |
| `/home/user/work/venv-agent/bin/ruff --version` | `This command requires approval` |
| `/home/user/work/venv-agent/bin/mypy --version` | `This command requires approval` |
| `/home/user/work/venv-agent/bin/python -c "print(1)"` | ran, prints `1` (the venv interpreter itself is allowed) |

Stopped here. I did not use `python -m ruff`, `python -m mypy`, or other routes to the same tools. Nothing ran for step 3, so no ruff, mypy, cycles, or smoke result exists.

Classification: **environment / permission** (the sandbox refused the ruff, mypy and make binaries). Not a product failure. The brief lists ruff, pyright, and venv binaries as allowed; in this run they were refused.

## Step 4: live tip probe

Fresh clone `$W/tmpdir2/live`, `git checkout -q --detach 74f3f7edba35230d0a01824eae7b663143e6aa5b` (exit 0).

```
git -C $W/tmpdir2/live apply --check $W/tmpdir2/zip-agent-2.patch   # exit 1
git -C $W/tmpdir2/live apply --reject $W/tmpdir2/zip-agent-2.patch   # exit 1; scratch only, log in tmpdir2/live-apply.log
```

Result of the check:

- Conflicting paths: **93**.
  - 87 files applied with rejected hunks (230 rejected hunks in total). Their `.rej` files are in the scratch clone.
  - 1 file failed as a whole: `tests/packs/rendering/test_timeline_inspector_viewer.py` ("patch does not apply").
  - 2 files the patch modifies but upstream deleted: `tests/packs/runpod/conftest.py`, `tests/test_runtime_correctness_inventory.py` ("No such file").
  - 3 new files the patch adds that upstream already has at tip: `tests/test_lane_registry.py`, `tests/test_skip_guard.py`, `tests/test_skip_policy.py` ("already exists").
- Check: all 93 conflicting paths are in `git diff --name-only 431681a6d 74f3f7edba35230d0a01824eae7b663143e6aa5b` (a Python set check: `conflict_in_base_to_tip 93`, `conflict_not_in_base_to_tip []`).
- Also, `tip_in_integration` exit 0 (ancestry above).

Interpretation: the squashed patch is `base → integration`. Integration already contains the live tip, so the patch contains the upstream base→tip changes once more. Applying it to the tip double-counts them. These conflicts are a method artifact, not real drift. The real drift check is ancestry, and it passes. This matches the round-1 note that most hunks would show as already-present.

Classification: **method / harness** (the probe applies a base-relative patch to a newer tip).

Deferred drift per the upstream rule (App `6e3445ee9`, Runtime `6162e0e33`) is not part of the agent repo. Nothing to list for agent.

## Not run

- Step 3 (ruff, mypy, cycles, structure, doc-refs, smoke): refused, see above.
- No pytest of any kind. The full suite is not requested by this brief, and no test-service request was made.
- The step 3 smoke subset was never selected. No `make check` result exists.

## Recommended next steps

1. Owner or orchestrator: allow `make`, `ruff`, `mypy` (and the venv `python -m scripts.reshape.compare_*_baseline` gates) in worker sandboxes, or name an approved wrapper for the `make check` gates. Then re-run step 3 on `$W/tmpdir2/fresh` (already at the applied tree `7d86b443…`).
2. For the live-tip question, use ancestry (`tip_in_integration = yes`) as the drift check, not a base-relative apply. A base-relative apply to a newer tip is always noisy.
3. Commit path for the hub: the integration tree `7d86b443453d9498569a7eee0c53410a5bbdc6a3` is what a fresh checkout of base plus this patch yields, so the content round-trips.

## Files

- Patch: `$ORCH/workers/tf-zip2-agent/tmpdir2/zip-agent-2.patch`
- Numstat: `$ORCH/workers/tf-zip2-agent/tmpdir2/numstat.txt`
- Fresh applied clone: `$ORCH/workers/tf-zip2-agent/tmpdir2/fresh`
- Live-tip probe clone and apply log: `$ORCH/workers/tf-zip2-agent/tmpdir2/live`, `tmpdir2/live-apply.log`
- Tip changed-file list: `$ORCH/workers/tf-zip2-agent/tmpdir2/tip-changed.txt`
