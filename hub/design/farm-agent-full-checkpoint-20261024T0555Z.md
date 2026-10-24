Ask: Agent credits exact nodes / Owner: Agent / By: 2026-10-24T06:30Z

Node lists: farm-agent-full-checkpoint-20261024T0555Z-nodes-failed.txt (281 ids) and -nodes-errored.txt (187 ids). No junit file was produced, so passed ids cannot be enumerated. Non-gate checkpoint.

**FAIL.** 288 failed, 17335 passed, 4 skipped, 187 errored (all in setup). The run covered integration:agent HEAD 9cd3dbe865a941c052bda04ae0d61306d18f8f26, tree 57f0231da0d7904ecd8778169973d6384e0ae141. This is not the selected 8657e836 / tree b5cbc402, and I did not relabel it.

## Run
- **Result:** test id `agent-full-farm-1024050351-26511`, wait-test exit 1, 2836 s (pytest 2833 s). 565 subtests passed.
- **Command:** `env ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-45c3a7f4 PYTHONPATH="$PWD:/home/user/work/wt/rt-pin-45c3a7f4" /home/user/work/venv-agent/bin/python -m pytest -q -n 3`
- **Runs:** submitted once and not resubmitted. I re-waited on the same id after wait-test hit its limit.
- **Preflight:** the suites.conf row exists once, both pin worktrees are clean at their expected SHAs (45c3a7f4 and 8657e836), and 18 GB of disk was free.
- **Raw result file:** no junit file was produced. The only raw artifact is the pytest log, `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agent-full-farm-1024050351-26511/log.txt`, SHA256 `06d435fed2622a4d9a8680e1071a650d5e34272090b08af5fe3ba0bd274dea06`.
- **Harness warning:** `runner.log` says `tests/cache/eadd90558ae9452a1ed95355f7f2ac0f: No such file or directory`, so this result may not have been cached. I did not touch it.

## Node lists
Both lists are in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/tf-agent-full-farm-0503/`:
- `nodes-failed.txt` has 281 unique FAILED node ids.
- `nodes-errored.txt` has 187 unique ERROR node ids. All 187 are phase=setup, with no teardown or collection errors.
- I did not write `nodes-passed.txt`. The `-q` log lists only failed and errored ids, and without a junit file I can't enumerate the 17335 passed ids.
- The summary says 288 failed but only 281 FAILED lines exist. I can't account for the 7 missing from the log alone; there are no `SUBFAIL` lines.
- Failures have no phase recorded in the log. The ones I sampled errored inside the test call, but I did not check every one.

## Failures by cause
This is a rough grouping from the error text, with counts as occurrences in the log. I did not map every node to a cause, and a node can show more than one.

**Environment (unprovisioned Remotion/Node peers)**
- 187 setup errors across the rendering pack and `tests/core/execution/*_custody_d40`, `test_d09_managed_scene_only` and `test_scene_real_public_summary_rle`.
- Messages:
  - "requires provisioned renderer peers" (33)
  - `KeyError: 'ASTRID_REMOTION_PROJECT_DIR'` (33)
  - "missing provisioned peer: …/remotion/node_modules/react" (42)
  - "no Node v20.19.4 for the renderer … found only v22.22.0 at /opt/node22/bin/node" (29)
  - "registry fixture requires the explicitly selected Remotion runtime" (9)
- Related failures with the same cause: the `@banodoco/timeline-composition` package is not found (16) or "missing rendering components" (13), and TypeScript from the selected Remotion runtime is missing (11).
- This points at the farm's Remotion and Node setup, not the code under test. I did not test that.

**Harness (runtime pin import)**
- `ModuleNotFoundError: No module named 'runtime_protocol'` (about 61 including subprocess children), `No module named 'astrid'` in child processes (9), and `cannot import name 'external_pack_sources' from 'runtime_protocol'` (48).
- The `generic_host` child processes (`capability 'unrelated.calculate' child exited 1`, 46) mostly fail this way. `tests/core/execution/test_generic_host_actions_v3.py` accounts for 53 failures.
- The `external_pack_sources` ImportError means the pinned Runtime at 45c3a7f4 does not export that name, while this Agent tree expects it. That is a possible Agent/Runtime pin mismatch, product or harness, and I couldn't tell which.

**Likely product (Agent timeline/SDK state)**
- `TimelineEditError: could not open 't' in 'p'` / conflict revision-publication (20)
- `CommandError: missing authenticated fork materialization` (19)
- `KeyError: '_runtime_document'` (42)
- `_FakeTimelines` has no `history` (7)
- Files:
  - `tests/editing_conformance/*` (about 60 failures)
  - `tests/sdk/test_timeline_open_commit*.py`
  - `tests/sdk/test_timeline_persistence.py`
  - `tests/sdk/test_timeline_public_command.py`
- I read these as product-side, but they could also come from the Runtime pin mismatch above.

## Unverified
- I did not check whether the integration head would pass with a provisioned Remotion/Node environment or a different Runtime pin.
- I did not compare against the selected tree b5cbc402.

I made no code changes in the worktree. I wrote the `commit-msg` and `DONE` files in the worker folder. The harness refused my `rm` of an empty `x-probe` file I created there, and I did not work around it, so please delete `workers/tf-agent-full-farm-0503/x-probe`. The scratch parsers are in `/tmp/w-7d4aa45640/`.
