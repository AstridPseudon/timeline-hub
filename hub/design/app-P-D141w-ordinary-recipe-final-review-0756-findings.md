# D141w ordinary recipe final review

## Verdict

- Pure builder binding: **PASS**.
- Prospective ordinary controller recipe: **PASS** after the three 0740 findings are resolved in the 0747 source-only packet.
- Actual controller/body and popup execution: **NOTRUN**. No checkout request, registration, request-test, wait-test, body, browser, or full suite was run.

## Findings in one pass

### D141w-C1 — resolved PASS

The packet binds all twelve exact `D66_{APP,AGENT,RUNTIME,COMPOSITION}_{SHA,TREE,CHECKOUT}` values, `D66_SUBMIT_TARGET=app-pin-82e9e13d`, one unique `full-d141-<selector>-82e9e13d-submit` suite per selector, and unique absolute `D66_OUTPUT_DIR` and `D66_SUBMIT_PLAN_PATH` paths. The genuine Node/tsx argv ends in `--submit` only. App and Agent exact checkouts are correctly prospective and absent; they are not falsely claimed materialized.

### D141w-C2 — resolved PASS

The unchanged `submitUnlocked()` path owns exact-checkout waits, source preflight, registration, preflight request/wait, normal/body request, and artifact persistence. The printed `request-test` lines are explanatory and must never be repeated. After return, the controller waits only the actual `artifact.normal.id`. A crash after a returned request but before artifact persistence requires existing request/artifact-state inspection; if finite custody cannot be proven, retain the first error and stop. No duplicate body or alternate route is permitted.

### D141w-C3 — resolved PASS

The custom `D66_SUBMIT_SUITE` names begin with `full`, so normal and derived `-preflight` requests are independently heavy under the existing `test-run`. Each requires strictly more than `5,200,000,000` available bytes without a measured receipt, owns its own genuine five-second `KEEP` trace, and retains the existing initial refusal at or below `4,500,000,000` bytes. The dropped D141s-c kit is not used. All 16 rows were regenerated through the unchanged `serviceRecipe`; all 16 hashes and byte counts match the packet. All 16 command bodies equal 0736; only prospective row suite names differ. No generic full-e2e rename is introduced.

## Mandatory standing-stop handoff

The standing `4,000,000,000`-byte stop policy remains mandatory and is separate from the test service’s `<=4,500,000,000` initial admission refusal. The live `test-run` starts the existing sampler for heavy bodies and records actual bytes every five seconds, but contains no automatic 4-GB kill guard. The future App manager/controller is therefore the owner of the existing supported route: poll the actual heavy body’s trace, issue `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-stop-test <actual-test-id> "D141 standing 4GB stop reached"` at the standing stop, then use `wait-test` and retain the cancellation/raw trace. This is an existing route, not a new tool, body, permission gate, kit fix, or weakened stop.

Current read-only availability is `5,250,732,032` bytes before the approximately `0.28 GB` preparation; this does not establish post-preparation `>5,200,000,000` headroom. Do not dispatch until actual post-preparation headroom is measured. Later normal release may use only the exact App `82e9e13d` and Agent `ecdc242e` checkouts after detached/clean verification and sufficient headroom.

## Preserved decisions

D141j remains conditional on an actual popup PASS: no current cause or fixed claim; a repeat failure stops the line pending the four visible diagnostic fields. Exact App/Agent pins are absent at packet generation. Metadata `8585` drift is expected pending D141v; no re-pin. IDs `8912`/`19479` remain held and `18617` cancelled originals remain retained. Raw KEEP/source objects remain retained. C0 v2 is unchanged, including the complete request, command, step, merge, idempotency, accepted/merged, conflict, invalid, and preview surfaces. No product, test, pin, registry, queue, hub, Git metadata, kit, or checkout mutation was made.
