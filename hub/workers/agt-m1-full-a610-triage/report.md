## Completed

- Classified all 109 current non-passing nodes: 62 persisted, 47 additional.
- Preserved the four resolved consumer-node proofs and one resolved baseline node.
- Added [report.md](/home/user/work/wt/agt-m1-full-a610-triage/notes/report.md) and the exact machine-readable [inventory JSON](/home/user/work/wt/agt-m1-full-a610-triage/notes/full-a610-classification.json).
- Appended the dated classification to the absolute design review.
- No product or test changes made.

## Evidence

- Central targeted run: `35 failed, 112 passed, 2 skipped, 14 errors`.
- Central admission test: `1 error in 2.71s`, reproducing the generated-client import failure.
- Node probe confirmed Node 20 `.ts` import failure and Node 22 success.
- JSON validation, exact node-set equality, and `git diff --check` passed.
- No full suite resubmitted; no socket/process-host tests run locally.

## Decisions / blockers

- 46 additional nodes classified as supported-environment fixture problems.
- One RunPod ownership node remains `UNKNOWN` because child stderr is discarded and exact same-environment baseline evidence is unavailable.
- M1 remains **HOLD**.
- The requested `a610-env-triage-integration` suite is not registered; recommended next step is to register it and run exact baseline/current representative comparisons.