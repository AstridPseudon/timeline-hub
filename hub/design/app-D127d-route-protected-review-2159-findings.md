# D127d independent source/protected-test review

## Verdict

`PASS_SOURCE_REVIEW`; acceptance is `NOTRUN`. Runtime COST-CANDIDATE remains
`PENDING`. This review found no source defect requiring a return before App
normal merge.

## Findings

- **D127d-R001 — guard-confirmed.** `p2-element-verify` is a distinct suite
  descriptor with the exact original element file, count, grep, and retained
  stream behavior. `main()` requires the explicit `D66_ELEMENT_VERIFICATION_ONLY=1`
  arm, so a no-env or mismatched suite invocation fails closed before submit or
  preflight. `serviceRecipe()` adds that selector to both registered D73
  preflight and normal commands. The no-env `--submit` probe was intentionally
  not allowed to submit and failed at the guard as designed.
- **D127d-R002 — resolved.** The actual spawned Runtime environment is rebuilt
  by `runtimeEnv()`. In verification mode it removes capture activation and
  sink, both helper path/hash pairs, watchdog, Runtime log/phase variables,
  the verification selector itself, and the `scripts/testing` bootstrap path.
  The harness still keeps private ordinary child stdout/stderr and writes them
  with directory mode 0700 and stream mode 0600. The targeted D127d test checks
  the two actual spawned child environments and retained bytes.
- **D127d-R003 — held by scope.** No candidate Runtime source, source
  preflight, service registration, localhost/browser flow, original body,
  profiling, collector, benchmark, checkout, acquisition, or install was run.
  The later one-body verification remains conditional on the independently
  qualified Runtime cost candidate and the D130 SWAP/WAL/recovery/full-tour
  hold.

## Plan/C0 boundary review

The App boundary remains consistent with PLAN A2/A3/P2 and C0 §§1–5/7: the
unchanged production caller uses the registered Runtime commit service through
the existing App outbox/public Agent APIs; the named v2 request/reply contract
is not rewritten here. Runtime closure, acceptance, conflict, receipt,
history, effects, dependency, and guarded-undo authority are not claimed by
this static App review.

No source/test edits were made by this reviewer.
