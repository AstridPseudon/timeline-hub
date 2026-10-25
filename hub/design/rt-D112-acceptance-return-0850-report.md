## D112 return report

Implemented private diagnostics only:

- Exact old-source RED / candidate GREEN replacement controls using the same corrected test source.
- Candidate native finite-N curve with registered-provider lifecycle, external-state revalidation, counters, sizes, timing, startup/refusal/stderr witnesses.
- Fixed diagnostic Ruff `I001/F401/PLW1510`.
- Product and protected test sources remain unchanged from `be828d92`.

Tests:

- Central targeted run `rt-D112-acceptance-return-0850-targeted-1025090253-22356`: **3 passed**.
- Ruff, Pyright, `py_compile`, Node syntax, and `git diff --check`: **passed**.
- Identity controls: baseline **3 expected failures**, candidate **3 passes**.
- Curve: all native rows accepted, but `flat_verification_work=false` and `flat_wall_observed=false`; no flat-curve pass claimed.

Evidence:

- [Identity summary](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D112-acceptance-return-0850/evidence/identity-controls/summary.json)
- [Curve result](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D112-acceptance-return-0850/evidence/finite-curve/run-9233-1792918986781364164/result-candidate-curve.json)

The remaining release blocker is the measured non-flat candidate curve. No original SWAP-409 reproduction or repeated native ADD/SWAP/Undo pair was performed. `DONE` and the requested commit message were created.