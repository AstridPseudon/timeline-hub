## D125 report

Prepared:

- [facts.json](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D125-local-fallback-prep-1356/evidence/facts.json>)
- [facts.md](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D125-local-fallback-prep-1356/evidence/facts.md>)
- [recipe.md](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D125-local-fallback-prep-1356/recipe.md>)
- [preparation-only.json](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D125-local-fallback-prep-1356/preparation-only.json>)

Verified all four exact receipts/checkouts, frozen App identity, Node `v20.19.4`, source hashes, pure `buildSubmitPlan`/`serviceRecipe` output, suite collision absence, and JSON/shell syntax.

Commands/results:

- `git rev-parse HEAD`, tree, status: expected `fe3309d...`, `e55f0d...`, clean.
- Node/npm identity and SHA-256 checks: passed.
- Pure D66 API check: exit 0; no submit/preflight/request calls.
- `jq empty`, `bash -n`, `git diff --check`: passed.
- Durable `p2-submit-plan.json`: absent.

No product files, tests, registry, shared dependencies, checkouts, preflight, submit, or body were changed/run.

Current disk availability is `5,149,011,968` bytes, below the required `5,200,000,000` admission threshold. Proof has not issued explicit cannot-host, so fallback remains unauthorized. Recheck space and venue handoff before using the exact recipe.