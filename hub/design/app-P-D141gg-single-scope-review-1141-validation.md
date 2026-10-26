# Validation

- Exact command run with output redirected only to the new reviewer file:

  node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141gg-single-scope-prep-1137/evidence/check.mjs /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141cc-submit-owner-sol-1047/evidence/dispatch-recipes.json /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141gg-single-scope-prep-1137/evidence/dispatch-recipe.json verify > /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141gg-single-scope-review-1141/evidence/same-check.stdout.json

- Result: exit 0; JSON output status=PASS.
- Read-only source checks: all four expected detached checkout HEAD/tree pairs matched and were clean; builder file SHA/Git blob matched retained source metadata; packet command bytes matched pure builder output; original execution inputs matched byte-for-byte.
- Data-only checks: derived suite/row names and hashes, private future paths, environment path references, registration=false, and native IDs absent.
- No product or full-suite tests were run by instruction. No browser, service, body, request-test, registration, or submit path was invoked.
- Author first-tool sampler failure before evidence-directory creation is retained as a limitation, with no backfill claim.
