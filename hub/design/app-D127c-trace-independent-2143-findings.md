# D127c independent review findings

Verdict: `FAIL` for the prior packet as an independent qualification. The original
`NO_GO_ORIGINAL_ELEMENT` / original body `FAIL` is preserved. No profiling was
rerun and no product source was changed.

## D127c-IR-F001 — blocker — cProfile absence is not the same as a proved selector failure

The 2113 verdict records a completed Runtime boundary with HTTP 200 and marks the
cProfile projection `EXACTMISSING`. The 2132 source trace correctly cites that the
helper emits `summary["cprofile"]` only when `request["profile_eligible"]` is true
(`runtime/tests/helpers/p2_commit_phase_capture.py:1133-1134`). It also correctly
keeps the exact selector operand private.

However, the safe packet does not publish the actual summary's key set or the
internal `profile_eligible` value. Therefore the independent evidence establishes
at most: completed boundary observed; exact cProfile projection unavailable. It
does not establish whether an observed summary omitted `cprofile`, whether the
summary/profile record itself was absent from the safe packet, or which earlier
condition failed. The following remain distinct and unknown: helper source
selection, dispatch/prefetch provenance, actual `RuntimeHandler` input, the
`_has_element_command` gate, the exact `_is_element_request` predicate, and raw
pstats persistence.

Do not convert the original browser assertion into the selector predicate, and do
not claim an optimization cause. A later qualified run may use this source
relationship, but this packet cannot claim that the completed request definitely
crossed no eligibility sub-gate.

Sources: `app-D127c-element15200-review-2113-verdict.json`,
`app-D127c-element15200-review-2113-profile-totals.json`,
`app-D127c-profile-trace-return-2132/evidence/first-seam.json`,
`runtime/tests/helpers/p2_commit_phase_capture.py:542-564,1133-1134`.

## D127c-IR-F002 — blocker — helper hash is not bound to the recorded product Runtime

The 2132 manifest records product Runtime commit `ab1e4f6141987706132916e2da16477f5a019464`
and tree `7d8e77b2f5a4af79305c9212ce5174d3ea9fd657`, while recording
`runtime/tests/helpers/p2_commit_phase_capture.py` as hash
`095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d`.
The actual helper in the pinned product checkout is hash
`6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760`.
The `095c...` helper is in the separate normal-home Runtime at commit
`cf0b82dd47452a7a34fc63eb233e9b1dc0532806`, tree
`8d5683702f36034f27ee7f49737665d66dbc2b75`.

An explicit helper override is a source-supported explanation (D66 validates and
exports an explicit path/hash), and the earlier 2113 custody record calls the
normal-home receipt “dispatch gate only.” But the 2132 manifest does not record
that override path/origin, so its source tuple is not independently reproducible
as written. This is a custody/evidence defect, not a claimed runtime cause.

Sources: `app-D127c-profile-trace-return-2132/evidence/source-manifest.json`,
`app-D127c-element15200-review-2113-source-manifest.json`,
`scripts/testing/d66-plain-stack.mjs:241-256,377-384,652-672`,
the two read-only SHA-256 checks recorded in `source-manifest.json`.

## Preserved finite unknowns

- Provider outcome, App response, caller receipt, and browser wall outcome remain
  unknown despite the Runtime boundary being complete/HTTP 200.
- The exact command operand and private payload fields remain unknown.
- No raw pstats destination is configured by the reviewed bootstrap; raw pstats
  remains optional, not evidence of a selector result.
- No call graph, exact cProfile table, operation-cost attribution, or optimization
  cause is qualified.
