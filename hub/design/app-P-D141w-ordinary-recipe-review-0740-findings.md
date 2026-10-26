# D141w ordinary controller review

## Independent verdict

- Pure production-builder binding: **PASS**. The unchanged builder at `/home/user/work/app/scripts/testing/d66-plain-stack.mjs` is blob `59b65214bc74c1ca118b097bc3b13c0ffe480a93`, SHA-256 `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`, and 49,914 bytes. It matches the historical 0545 builder byte-for-byte. The genuine exports reproduce eight selectors, 16 commands, and 16 UTF-8 rows with exactly one LF.
- Executable controller recipe: **FAIL pending three narrow corrections** below. No registration, checkout request, preflight, body, test, or full run was made by this review.

## Findings

### D141w-C1 — `--submit` is not pinned by the documented command

The documented command in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141w-final-head-binding-0736/evidence/controller-plan.md` sets only `D66_SUBMIT_TARGET` and `D66_SUBMIT_SUITE`. In the real caller, that means `explicitSubmitTuple()` returns null and `captureSubmitPins()` reads the mutable normal homes at invocation time. It does not bind the reviewed App `82e9e13ddf1d7ec6c736521b2eb091dca9877598`, Agent `ecdc242ed9b673f641759ecf029f95e89a2c6f92`, Runtime `95d98f038320d5d46bd679ac000ab3e15825c935`, and Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40` tuple.

The same command leaves the submit artifact at the shared default derived from `TMPDIR` and selector name. A repeated selector can therefore resume an old artifact. The packet’s exact App and Agent checkouts are absent, so this is a prospective binding, not an actual-checkout claim.

Narrow fix: after exact App and Agent checkout materialization and verification, pass all twelve exact `D66_*_SHA`, `D66_*_TREE`, and `D66_*_CHECKOUT` variables, plus a unique absolute `D66_OUTPUT_DIR` or `D66_SUBMIT_PLAN_PATH` per selector. Keep the reviewed `D66_SUBMIT_TARGET` and `D66_SUBMIT_SUITE`. Do not use the expected-but-not-current `8585ed9c` metadata.

### D141w-C2 — `--submit` owns preflight and body request; the listed continuation duplicates them

`submitUnlocked()` in `/home/user/work/app/scripts/testing/d66-plain-stack.mjs` performs, in order: exact checkout requests and receipt waits; source validation; registry registration; preflight `request-test`; preflight `wait-test`; normal/body `request-test`; and artifact persistence. The `submitPlainPlan()` text printed after success repeats the request commands as a plan, but they have already happened.

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test` creates a new result ID on every invocation. Following the printed continuation after `--submit` therefore duplicates the preflight and body, including a second body. The supported resume path is the artifact/lock path in `submitUnlocked()`: it reuses the recorded preflight ID, waits it, and requests the normal suite only when the normal ID is absent. There remains a crash window after a normal request returns and before its artifact save; this is why a manager must not add a second manual owner.

Narrow fix: run one owner only. `--submit` performs registration, preflight request/wait, and normal request. After it returns, wait only the `artifact.normal` ID recorded by the submit artifact. Do not run the printed `request-test` continuation. On refusal, retain the first error, stop the affected action, and use no alternate route.

### D141w-C3 — paired admission and continuous-trace wording is not the installed route

The current `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run` checks admission separately for every `request-test` request. Its ordinary light floor is 5,000,000,000 available bytes; default heavy is 5,200,000,000; and the installed low-disk refusal is at or below 4,500,000,000. The code starts the disk sampler only for a heavy body. `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/d141-disk-trace.py` samples every five seconds and records `keep=true` only in a validated heavy-body trace.

The D141w plan’s “paired preflight/body unit” and “one continuous 5-second KEEP trace across” that pair therefore overstate what the installed seam guarantees. A current no-receipt journey has no measured-floor receipt; a light preflight has no heavy trace. The current `d141g-...-82e9e13d-submit` name also does not match the old hard-coded heavy special case `d141g-p2-automatic-child-placement-520d7e4f-submit`.

Narrow fix: describe preflight and body as separate admissions, with the body’s actual installed class. State only that the existing route provides a five-second KEEP trace for heavy bodies and has the installed 4.5-GB refusal seam. Do not promise a trace or a 4.0-GB stop for a no-receipt light journey. Do not add a paired kit, exception, new permission condition, or speculative registry author.

## Preserved non-findings

The C0 v2 request/reply field set is preserved; no wire change is needed. The D141s-c paired kit remains dropped, and the historical 0545 packet remains unregistered. Modern schema 4 is not a defect because the dropped kit never reads it. D141j’s exact `NOT REPRODUCED`/unknown-cause wording and the second-failure four-diagnostic preconditions remain correct. The expected `8585ed9c` metadata drift is not a defect; current Agent production binding is prospective `ecdc242e`.
