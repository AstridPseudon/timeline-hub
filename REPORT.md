# Gate 6 pack-host startup cause report

## Outcome

Central run `vw-m3-gate6-all-prereqs-cleared-one-run-0327-e2e-viewing-gate6-built909-0240-1021032844-28523` failed after 129 seconds: all five cases failed identically at App `bootstrap.ts:238` with:

`Pack-host helper reported failure; pack-host startup cleanup failed`

The five failures are one fixture/bootstrap failure, not five case-specific failures. The harness fixture had reached `harness.ts:280` (`startRealPackHost`) after the DirectHarness setup. No case body, Player page, export, frame/audio capture, or parity comparison ran.

### Original startup failure versus cleanup failure

The original failure is proved only to be the helper's valid newline-delimited `status:"failed"` response before a valid `status:"ready"` response. The exact inner `error_type` and `error_location` are **UNKNOWN** in the retained run evidence:

- The five retained Playwright traces and error contexts contain only the wrapper summary and the App stack at `bootstrap.ts:238`.
- No run-local `generic-host.log`, `generic-host.json`, `generic-host.ready.json`, or raw helper JSON payload survived cleanup.
- The helper's CLI would have emitted the secret-free `error_type` and `error_location` at `real_pack_host.py:236-242`, but the App caller does not preserve that payload. It maps any `status:"failed"` at `bootstrap.ts:169` to `Pack-host helper reported failure`; it also drains stderr at `bootstrap.ts:145`.

The cleanup error is secondary and understood. On a failed status, the caller's `protocolFailure` flag is set. `stop()` sends `stop\n` only to the direct helper child (`bootstrap.ts:207-218`) and then rejects at `bootstrap.ts:222` because the failed protocol did not establish the required ready/stopped state. The catch at `bootstrap.ts:236-240` appends `pack-host startup cleanup failed` to the original generic message. This does not identify the original missing prerequisite.

The helper itself has ownership-safe cleanup: `real_pack_host.py:109-126` locks support state, compares the current registration with its captured state, refuses foreign/reused identity, retires only the owned host group, checks survivors, and waits for the owned child (allowing production custody to have reaped it). The central post-run census found no residual pack-host, browser, Runtime, or Vite process. No orphan is being ignored; however, because the raw custody files were not retained, whether the generic host was ever spawned is **UNKNOWN**.

## Prerequisite boundary

The complete offline preflight passed 21/21. It proved the frozen source tuple, clean/immutable helper carrier, package/peer maps, Python origins, Node 20.19.4, Chrome 155, App dist/GET, and five-case discovery. It did not execute the helper's live handoff and host-start checks.

The helper's supported live sequence (`real_pack_host.py:158-209`) is:

1. Validate realm, support, discovery, Runtime instance, worker credential location, actor, and scopes.
2. Require a fresh host registration, then authenticate the worker credential and verify Runtime health/identity.
3. Run Agent `ensure_pack_host(..., startup_idle_seconds=30)`.
4. Adopt only a source-bound live child, require host `ready` plus `rendering.render`, then poll the Runtime capability catalog for ready `rendering.render`.
5. Yield to the caller and later retire only the owned host during cleanup.

The retained evidence proves the helper carrier and its Python process were usable far enough to emit a valid failure response. It does not distinguish a failure in the handoff, live Runtime check, source/inventory/boot-manifest checks, host launch/readiness, or final Runtime capability-catalog check. No product, fixture, authority, DTO, or guard change is justified by the available evidence.

## Frozen tuple and commands

The run used the exact retained tuple from `gate6-20261021T0240/source-tuple.json`:

- Agent source `d0a5072bbe7b7ce9489f43aa0a81027ec400343b`, tree `6adb4a1190dfb2874e101565f37eccd392b1ae2f`, imports from `/home/user/work/wt/agt-pin-d0a5072b`.
- Helper carrier `b70b9d569b2c80885d72734c61cd57e64c3715a8`, tree `687f077c4771e3dbb66bfb7ff2b98f310ac054b6`, file SHA-256 `bc75d73f21c6310efad7fc41e4a3d790bfe3a8975e0eb96c08c3dec63e62961b`, `/home/user/work/wt/agt-pin-b70b9d56/tests/packs/rendering/real_pack_host.py`.
- Runtime SERVER `8f105c26e3b62f9c2683f717a9773a12bc775a8e`, tree `b7f456d5135cba6049980ebc43a91c7a72ab8f7e`; runtime graph SHA-256 `4913a37e5403c8372a283dcca8fd30c846b636abd88f59cfc572809d2fd0bd3c`.
- Runtime official PRODUCER `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`; official artifact `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`; generated client `sha256:dd542c8c04ceec1af3d21413cf82ac6316879c0f3d2dacae5f88754c3b395ee8`.
- App `909d2bfa186985db9791be0ab090b9f4e7824f9b`, tree `79728118ec633070581beff0e283fdff1a74f2d2`.
- Composition `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`, tree `13e375534fffd704305eced5686699d2c8c9c948`.
- Agent Python: `/home/user/work/venv-agent/bin/python`; Runtime imports resolve from `/home/user/work/wt/rt-pin-8f105c26`. App spawned the explicit Agent Python with `PYTHONPATH=<Agent d0a source>:<Runtime 8f source>:<old PYTHONPATH>` and the helper path above.

The exact helper command was:

`/home/user/work/venv-agent/bin/python /home/user/work/wt/agt-pin-b70b9d56/tests/packs/rendering/real_pack_host.py --realm-dir <harness.realmDir> --support-dir <harness.supportDir> --discovery-file <supportDir>/discovery.json --source-checkout /home/user/work/wt/agt-pin-d0a5072b --runtime-instance-id <harness.runtimeInstanceId>`

The retained grant/marker were issued for this tuple; this report did not issue, consume, replay, or clean them.

## Physical boundary: Chrome/export not reached

Chrome 155 was **not launched**, and no real browser or export body was reached. This is established by the actual traces, not by the `Running 5 tests using 1 worker` line:

- Each trace begins with Playwright `context-options` showing `browserName:""`, then the `harness` fixture and the `fixture` fixture.
- Each trace records the error at `bootstrap.ts:238` from `harness.ts:280` and has no browser/context/page launch event.
- The browser fixture's only launch is `harness.ts:292` (`chromium.launch(...)`), and the fixture dependency graph places it after `fixture`; `fixture` fails at `harness.ts:280` before that line is reachable.
- The five case bodies are at `cases.ts:229,246,267,277,317`; none was entered. No export, media, frame, audio, or comparison bytes qualify for release.

The helper's own generic-host launch boundary remains **UNKNOWN** because its registration, ready file, and log were cleaned and not retained. The evidence proves a helper process emitted the failed status; it does not prove a generic host child launch. The Chrome binary hash, grant, marker, test listing, and token/marker metadata are not physical-attempt evidence.

## Minimal correction and release decision

No environment repair can be named honestly until the missing helper failure payload is preserved. The minimal existing test/diagnostic correction is to retain, before cleanup, the helper's secret-free failed stdout line (`error_type`/`error_location`) and the owned `generic-host.log`, ready/state files, host PID birth identity, and custody result. Preserve stderr only under the existing secret-safe policy; do not expose credential-bearing text. Then classify the exact prerequisite failure and repair only that existing environment path.

Release 14 remains held. No qualifying handoff or pin exists; draft bytes remain held. No retry, service/browser/host launch, renderer, grant, marker, or guard change was performed by this worker.

## Evidence and inspection commands

Primary evidence:

- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m3-gate6-all-prereqs-cleared-one-run-0327-e2e-viewing-gate6-built909-0240-1021032844-28523/`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-built909-wrapper-correction-0240/gate6-20261021T0240/`
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-gate6-all-prereqs-cleared-one-run-0327/preflight-0327-final.json`

Read-only commands used: `cat`/`jq` on the retained tuple, grant, marker, preflight, and central result; `sed`/`nl` on the frozen App bootstrap/harness, helper, and Agent host-bootstrap sources; `find` and `rg` for all run-local helper/log/status payloads; `unzip -p <trace.zip> test.trace` for all five Playwright traces; and `git status --short --branch` on the assigned Composition worktree. No test suite was run because this was a report-only investigation and no product code changed.
