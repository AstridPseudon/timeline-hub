Implemented a distinct `finite_json` walk optimization that removes scalar pending-tuple allocations while preserving fresh checks and traversal order.

Three uncontaminated whole-control pairs improved **4.58% wall / 3.34% CPU** overall. Native validation counts matched exactly: 1,418 finite checks and 889 schema validations.

Validation:

- Focused run: 171 passed; one new test failed and was corrected. Final new controls: **11 passed** on baseline and candidate.
- Affected redo-history tamper tests: **12 passed**.
- Ruff, compilation, diff checks: passed.
- Pyright: **zero new diagnostics**; one unchanged existing nullable-URI error.

[Exact commands, results, raw profiles, XML, logs, exits and source hashes](../rt-P4-cost-continuation-sol-1847/evidence/measurement.md) are preserved in the worker’s durable evidence directory. `commit-msg` and `DONE` are written.

No blockers to this source result. **Core/security review is required before merge.** The original 45-second P4 gate and two Agent restart timeout nodes remain open and were not rerun.