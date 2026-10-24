Repaired only the three allowed control artifacts: exact blob hashes, structural mounted-proof checks, repository `tsc` recipe, and regenerated patch/evidence. Protected sources remain unchanged.

Validated on committed HEAD `09ae405158bba0d0c1f4bf5502649dea9c04854f`:

- `/opt/node20/bin/node --import tsx --test tests/e2e/local/support/gate5-fault-order.test.mjs proposal-controls-v4.mjs` — **7/7 PASS**
- `/opt/node20/bin/node --import tsx proposal-controls-v4.mjs --lint` — **PASS**
- `/opt/node20/bin/node --import tsx proposal-controls-v4.mjs --types` — **PASS**
- `/opt/node20/bin/node --import tsx proposal-controls-v4.mjs --hashes` — **PASS**
- `git diff --check 5d7550ca7d005f948695ee3dc1d49273890bf59c HEAD --` — **PASS**
- `git diff --check HEAD --` — **PASS**
- `git apply --reverse --check --unidiff-zero proposed-v4.patch` — **PASS**

Used zero-context Git output to avoid patch whitespace and manual hunk rewrites. The existing root `tsc` recipe does not establish semantic coverage of protected tests; evidence states that limit.

Published byte-exact corrected artifacts under `ORCH/design` and updated the existing D75b/P3 row truthfully. No browser, service, full suite, or repeated lifecycle/neighbor run.

No blockers. Commit message and `DONE` written; harness commit and independent whole-path/home qualification remain next.