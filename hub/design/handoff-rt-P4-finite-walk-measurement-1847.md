# R-P4 fresh finite validation cost

Base: Runtime 1bae0e8cc; Agent head and exact per-run fixture/source hashes are
recorded in each *-source-sha256.json. The control is the same existing genuine
finite history test used by workers 1804 and 1827:
`tests/test_timeline_inverse_historical_image.py::test_redo_reopens_exact_retired_images_with_one_native_write`.
All control invocations passed. This is in-process production-caller evidence,
not the original P4 ten-note HTTP body or either retained restart timeout node.

## Decision and scope

Retained one distinct change in timeline_commit_validation.py::finite_json:
walk reverse child iterators with a stack of container frames, rather than
allocate/pop a pending (child, leaving) tuple for every scalar. Retain exact
builtin JSON types, finite floats, all string-key checks, ancestor cycle checks,
repeat traversal of shared children, reverse child order, key-error precedence,
unbounded iterative depth, and fresh local state on every call. No validation
boundary, result, value, authority, history, receipt, or schema cache was added.
No auth/store/schema/provider/ABI product source changed. No new dependency or
engine, no installs, Git writes, full suites, HTTP/browser/original-body runs.

The retained 1804 profile identified finite_json (1,418 calls, 0.829s self / 1.760s
inclusive) as distinct measurable work outside the failed resolver/evolve/cache
experiments. Those seams were not retried. Fresh profiles confirm the hypothesis:
finite_json self 0.622529 -> 0.468373s; inclusive 1.345803 -> 0.844319s. Profile
seconds include instrumentation and are attribution, not latency claims.

## Uninstrumented paired whole-control timings

Times include interpreter/pytest startup and the whole genuine control. CPU is
user + system from parent resource.getrusage(RUSAGE_CHILDREN) deltas around the
subprocess; wall is parent perf_counter. Exact wrapper source is measure.py.txt.
The source file was restored to the captured baseline/candidate bytes between
separate processes; there was no in-process patching or instrumentation.

| Pair | Old wall | New wall | Old CPU | New CPU |
| --- | ---: | ---: | ---: | ---: |
| 1 | 7.642979 | 7.241687 | 7.256781 | 7.055407 |
| 2 (new then old) | 7.539601 | 7.241459 | 7.190853 | 6.949135 |
| confirm | 7.850657 | 7.495423 | 7.662756 | 7.367870 |

Aggregate gain: 4.58% wall / 3.34% CPU. Each valid pair improves both metrics
(wall 3.95-5.25%; CPU 2.77-3.85%). These are small-workload measurements, without
claiming a confidence interval or that they resolve the original 45s gate.
Raw old-3/new-3 are excluded: new-3 accidentally overlapped old-profile. The
contaminated data was retained and one replacement pair run after profiling.
The old-profile timing also overlaps that run; only its counts/attribution are
used. The raw profile's source line and finite-walk generator entries confirm
that it loaded the old source. The initial harness attempted /usr/bin/time,
which was absent; no measured run used it.

## Unchanged counts

validation-counts.json compares primitive and total calls across all native
jsonschema and referencing functions, and selected production boundaries:
**zero count differences**. Both profiles contain 1,418 finite walks, 889 schema
validations, 440 canonical-image captures, 110 sequential-capture validations,
107 historical sequential validations and 496 auth.validate calls. Native
schema descend calls are 534,988 (968 primitive), evolve 492,103, type keyword
226,255; all unchanged. The existing retained-capture test also asserts exact
54 CanonicalDocument + 2 Recorder + 56 finite checks with fresh values.

## Verification and limitations

* focused-command.txt: 171 passed, 1 failed, 1 deselected in 51.81s. The failure
  was solely a new test's assumption about Draft7 $ref sibling behavior; it also
  failed with the unmodified native validator. The new control was corrected
  to test real dialect-specific dependencies/dependentRequired dispatch, while
  comparing native/candidate nested error context. No pre-existing test changed.
* walk-typed-final-command.txt: corrected and typed new controls, 11 passed in
  1.61s. walk-baseline-final-command.txt: same final controls pass unchanged
  baseline too, 11 passed in 1.38s. There are 161 passing existing focused tests
  plus 11 passing new controls; the existing nine ordinal attacks pass.
* history-final-command.txt: all 12 affected redo native/effect/source tamper
  cases passed in 33.72s. Genuine finite history control passed in every measured
  old/new process and both profile processes.
* static-ruff-final-command.txt: Ruff 0.16.8 passes. static-compile-final-command.txt:
  py_compile passes. static-diff-final-command.txt: git diff --check passes.
* Pyright 1.1.414: zero new diagnostics, confirmed against the same baseline
  source and final tests with explicit existing-venv dependency paths. Both
  commands exit 1 on the same existing resource.id() URI | None argument error
  (old line81/new line84); final tests have no diagnostics. Raw output and
  normalized comparison in pyright-delta.json are retained. An initial config
  with absolute include paths scanned scratch by mistake; that raw failure is
  retained separately from final scoped results.
* Installed-wheel test deliberately deselected because this brief forbids
  installation. No behavior test expectations weakened/skipped/deleted in source.
* Prior 1827's two historical text-binding restore refusals were not rerun or
  reclassified as new regressions; this change does not address that seam.

No blockers to this measured source result. D47 remains held. Original P4 45s
and two Agent restart timeout nodes remain OPEN. Core/security review is required
before merge; after review the orchestrator decides the next original-gate run.
