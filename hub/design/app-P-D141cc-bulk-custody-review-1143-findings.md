# D141cc bulk custody findings

Verdict: `PASS_CUSTODY_TEST_PASS` for `p2-transition-none-bulk@original` only.

- The accepted Sol1047 `dispatches[3]` recipe is the exact source of the native argv, cwd, environment and paths. The native log records one `--submit` invocation, exit 0, one preflight ID and one normal ID.
- Both durable request directories are `pass`/exit 0 and retain `KEEP`. The normal `wait-test` for the exact recorded ID exited 0. No second submit, manual request creation, alternate selector, or artifact relocation occurred.
- The retained normal body has one readiness test and one P2 test. Both XML reports are complete with one test, zero failures, zero skipped and zero errors. The untouched original P2 source checks raw transition absence, unknown-field preservation, parent/config clip order, exact v2 request and reads, history/reload, zero legacy-route traffic and guarded undo.
- Four exact detached clean source pins match the manifest. The production D66 builder hash/blob, native artifact hash, service manifest hash, raw request/snap hashes and test source hashes independently match retained claims.

Non-blocking disclosed limits:

- The author trace has 73 samples from `2026-10-26T11:34:57Z` through `11:40:58Z`, independently recomputed from the real file. Its minimum is `5,185,191,936` bytes: below the one-time 5.2 GB admission floor but above the 4 GB standing stop. Manager admission was already recorded at `11:34:28Z`; this does not change the settled admission-once rule. No trace was backfilled.
- The author records the sampler as signalled and reaped. The retained service-source checkout was cleaned after completion, so its recorded clean head/tree in the manifest is the available witness.
- This is not an overall P2/platform GO, REG0, final-build, ZIP, or any other selector verdict. The prior finite source-check failure and lifecycle/startup gaps remain historical limits; no repair or rerun was made.
