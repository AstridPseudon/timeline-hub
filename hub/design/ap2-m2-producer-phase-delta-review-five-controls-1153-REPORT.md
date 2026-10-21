# App producer phase-delta review — 1153

`P` = `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-producer-complete-execution-prereqs-diagnosis-1132`.

## Verdict

**HOLD.** The 1150 sidecar conversion is independently acceptable, but the required prerequisite closure is not currently clean. I did not run the authorized preflight or any of the five controls.

## Independent review of 1150

- Original harness: `P/outer-controls-run.py`, SHA-256 `ff1ae8404f39d765b01429ce706fa0affb6a163b632c20506a9705f103ec7234`.
- Sidecar: `P/outer-controls-run.phase-corrected-1150.py`, SHA-256 `a4b3f89d9f15f9fbd095e5b6b658605807f7b0099e8337f0cb4dea11ebdf662e`.
- Direct `diff -u` shows only the two authorized hunks: absent `before` `temps.jsonl` is treated as an empty event list, and `before` asserts zero created/leaked temps.
- The original preflight refusal occurs before the runner's `mktemp`; the correction therefore preserves the early refusal, status 1, one custody shell, zero child, zero build stub, and no packet without fabricating an event.
- The `after`, `absent-output`, `copy-failure`, and `success` temp, cleanup, dispatch, and evidence assertions are byte-identical. No source/helper/pin/version, launch-stub, guard, or artifact-closure rebinding was performed by 1150.
- The D01 ordinary-batch ledger row remains OPEN; this is only a process-harness conversion.

## Prerequisite audit and first meaningful failures

The audit was read-only and stopped at the first actionable prerequisite failures.

1. `(cd "$P" && sha256sum -c SHA256SUMS)` failed because the retained manifest requires `REPORT.md` with SHA-256 `ce0ed96342c3a77ce5ef71ffeb754f6885606a387971222f085de964878b53f4`, but `P/REPORT.md` does not exist. Only lowercase `P/report.md` exists, with SHA-256 `6e0eca1405e283f3c719cdff19468b07c08ee9c4e6a3defd25651f1a5cfa8aed`. All earlier checksum entries printed `OK`; the manifest is nevertheless not a passing closure.
2. `flock -n /home/user/work/.app-m1-browser.lock true` failed. `lslocks` showed no attributable owner in this namespace, and `fuser` could not inspect the lock (`Cannot open a network socket`). No matching producer/browser/build process was visible in the bounded process scan, but the required lock-free/resource-safe condition cannot be established.

Other read-only checks passed before the HOLD:

- Keeper HEAD/tree are `5863411a8c2400db719b5385002b05af0a2b3891` / `31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89`; keeper porcelain is clean.
- The ignored keeper dependency link resolves exactly to `/home/user/work/app/node_modules`; the worker KEEP marker exists at `P/workers/app-pin-5863411a/KEEP`.
- Locked App source hashes match the 1132 values: wrapper `329cfca7…`, spec `6666c036…`, helper `df1faac4…`, config `5b880cef…`; the launch stub remains `4299795135db4be3b83b41d9034cb1519b529925865222f9af866029df9264b7`.
- Frozen Agent and Runtime objects/trees resolve to the recorded `8130a401…`/`236c3e57…` and `2c4ac180…`/`7ab412cc…` pairs.
- The current App worktree is clean, no `P/controls` directory exists, and available disk was above the 5 GiB floor (12,455,408 KiB available on the checked filesystem).
- Static inspection of the sidecar confirms each case gets a physical `TemporaryDirectory`, creates a physical `case/tmp`, and exports that path as `TMPDIR`; this was not dynamically exercised.

An auxiliary Python exact-diff assertion command compiled both files but then rejected its own malformed expected diff-header string. The direct `diff -u` result above is the reliable scope check; no control or product behavior was inferred from that auxiliary checker.

## Execution accounting

- Exact 1132 next-preflight command: **not run**.
- Five controls (`before`, `after`, `absent-output`, `copy-failure`, `success`): **0/5**, not run.
- Failure propagation/retention counts: **unverified**; no run artifacts or packet claims.
- Browser, build, daemon, startup probe, localhost, socket, install, and actual producer execution: **not run**.
- No repo files, docs, `.gitignore`, suites, pins, operations, or product specifications were changed.

## Recommended next step

The manager should first reconcile the 1132 manifest/report naming mismatch and establish which process owns `/home/user/work/.app-m1-browser.lock`. After both are resolved, a fresh worker may repeat the prerequisite gate and, only if it passes, run the exact one preflight followed by the sidecar's five controls. Do not repair the manifest or bypass the lock in this task.
