# D141 validation

Status: PASS for the evidence-only repair; execution status remains NOT RUN.

Read-only checks performed:

- the prior evidence-only worker HEAD is `1f627095d55f35dba0947a4ecb6b339785dafbdc`; its working-tree content is compared against base `5696769dfca056676cde1ab46d8bc94354b3a44a`.
- `git diff --name-status 5696769dfca056676cde1ab46d8bc94354b3a44a --` is empty after deleting exactly `evidence/recipe.json` and `evidence/source-manifest.json`; the base tree is `0748df404125114a0f68b701fa76f43abd3fc79a`.
- git status --short reports only the two scheduled deletions (`evidence/recipe.json` and `evidence/source-manifest.json`) relative to the prior evidence-only commit; no other repository paths are changed.
- git rev-parse 7ca61bb3280beca21d98a854af266a382f7ce5df^{tree} = 974de7cd08900872eeb0bd6f6004d44323e01fab.
- Base package/lock/runtime hashes and frozen-upstream package/lock/runtime hashes match the values in source-manifest.json.
- jq empty succeeds for evidence/recipe.json, evidence/source-manifest.json, and evidence/findings.json.
- The registered route is read from tests/suites.conf:69: npm test -- --maxWorkers=3.
- The existing request-test route accepts only worker metadata or integration:<repo>; no route or framework was added.
- No full suite, pristine comparator, browser journey, import, collection, build, lint, typecheck, checkout, fetch, merge, or commit was run by this worker.

The final U3 record remains a pending gate: its manager route hit the linked-worktree metadata permission failure and left six unresolved paths. Therefore no final App head, MAIN GO, D141 receipt, Vitest count, Node count, or pristine outcome is asserted.
