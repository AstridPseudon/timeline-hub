# app2 — invalidate completed false-green test4657
Result4657 records pass/exit0, but retained Playwright summary/log says1failed/1passed (bootstrapprojectresponse timeout).
Evidence: design/ap2-m2-current95-runner-failure-exit-triage-0115-REPORT.md; actual childRC swallow point is unproven.
Recommended owner action: withdraw4657 from reusable qualification/cache, retain raw evidence, instrument actualchildRC ifneeded; do not addgenericlogregex as a substitute for root analysis.
App2 treats runFAIL, preserves only the explicitly passed neighbor as bounded evidence, and is adding own required-case validation before any newgate.
Prescribed request-stop-test returned “test ... is not running”; completed status remains pass. No historicalstatus or bin/test-run was edited.
Not covered because: managers cannot invalidate a completed cachedpass through the prescribed tool and may not edit centralfinalizer/cache/status.
Rule that would let me decide next time: request-stop-test may withdraw a completed invalid result to cancelled/noncached while preserving original artifacts and reason.

