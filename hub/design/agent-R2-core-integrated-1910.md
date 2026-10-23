# R2 readonly actual-home integrated proof: PASS

Date: 2026-10-23 UTC. Worktree: `/home/user/work/wt/agt-R2-core-integrated-1910`.

## Identity and source union

- Agent HEAD before and after: `9a095a95178e0bb89ef3b2024d6502d47b35ac25`.
- Agent tree before and after: `5cb1c3a0f00b82d992712d98409bf13a5579fc2b`.
- `git diff cd7f9f0a3 HEAD`: clean; HEAD tree exactly equals `cd7f9f0a3` tree.
- The eight current blobs exactly match reviewed sources: six from `255751f40a38263b8a032d15b807a3a3e2742a9c` and two from `d146b4204f6f9efa526134d810e581a282377a9a`. Full mapping is in `evidence/source-identity.txt`; complete source copies are in `evidence/source/`.
- No tracked R2 report artifact is present. Final Agent status is clean.
- Exact execution Runtime remained clean at commit `2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d`, tree `f79a2355cfb39d9ada7721978bd20d5702105778`.

## Commands and results

Collection-only verification (unfiltered requested selectors):

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-R2-core-integrated-1910:/home/user/work/wt/rt-pin-2a9e347f /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider --collect-only tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_transient_root_baseline.py::test_native_stage_keeps_authored_root_and_full_accepted_baseline
23 tests collected in 0.59s
This is 22 ABA cases plus exactly 1 original transient-root baseline case.
```

Single permitted actual integrated run (same selectors; private external observer added through `PYTEST_PLUGINS=observer`):

```text
PYTEST_PLUGINS=observer R2_ACTUAL_ROOT="$PWD" R2_EXACT_RUNTIME=/home/user/work/wt/rt-pin-2a9e347f R2_OBSERVER_OUTPUT=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R2-core-integrated-1910/evidence/observer.jsonl PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="/home/user/work/wt/agt-R2-core-integrated-1910:/home/user/work/wt/rt-pin-2a9e347f:/tmp/w-a133d2571d" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_inverse_aba_partition.py tests/editing_conformance/test_transient_root_baseline.py::test_native_stage_keeps_authored_root_and_full_accepted_baseline
```

The actual command used the exact requested test paths. Result: **23 passed in 17.25s**.

External observer evidence: 23 before/after case records, all passed; all eight critical source hashes were constant before/after every case. It retains module origins and hashes, complete critical source snapshots, and numbered source/range snapshots in `evidence/observer.jsonl`, `evidence/observer-summary.txt`, `evidence/source/`, and `evidence/critical-source-ranges.txt`.

## Quality and retained pins

- `python scripts/vendor_lock.py check runtime.lock.json`: **ok**.
- `python scripts/artifact_manifest.py --check`: **artifacts.json is current**.
- `git diff --check` and cached diff check: **pass**.
- Reused exact-tree quality evidence; did **not** rerun full Ruff 2149 or private Mypy 1912.
- Retained ancestry/pins: R1 `f078d0229`, reader/store `75fde1b96`, registry `22f1cb169`, A4 `14fc0740f`, Runtime lock source `34eac0041b0891e9011966b39bcbd26053fde5bc`, schema digest `d106dfe8212500709b4072d7bc0486f83c27d5d8de33d215cb52b9ea7d46357d`, Composition artifact `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`.
- Credential scan of the final worktree diff: **0 matches**.

## Scope and limits

This is Agent provider/source plus detached provider-fixture evidence only. The narrow tests install synthetic `runtime_protocol` ABI modules; the observer records the real execution Runtime origins before fixture replacement, but this run makes no actual Runtime authentication, HTTP, daemon, browser, or end-to-end claim. No full suite, original SDK-four, or duplicate semantic review was run. G5 child diagnosis remains owned by worker 1907; it was not duplicated. P1 remains NO-GO.

The help probe for `artifact_manifest.py` ignored `--help` and regenerated `artifacts.json`, but its SHA-256 remained identical to HEAD and final status/diff are clean; the proper `--check` then passed. No durable product/test/generated/pin change resulted.

## Blockers and next step

No blocker for this scoped proof. Orchestrator may consume this PASS and the retained prior quality evidence; do not repeat the 23-case semantic run or broaden it into Runtime/HTTP/browser/full qualification.
