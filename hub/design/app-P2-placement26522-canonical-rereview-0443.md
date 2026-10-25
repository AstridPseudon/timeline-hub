# PASS — P2/A3 canonical placement rereview

Applied exact `ddb764adcf` blobs to clean `3199118dce`, preserving D97 adoption files.

- Spec SHA-256: `c75baf23fa743c19c9f4bfa5822aa69c8776188436f82a9c27bbf82431c21845`
- Support SHA-256: `4e1bedd0d4bc721c41f269d5eaba785e0e66bb4d3b81cc8dc29ef72bcabd53f0`
- Only the two assigned files changed.
- `DONE` and commit message created.

Evidence:

- Node controls: **134/134 passed** (`131` receipt, `1` placement receipt, `2` seed-window).
- Saved `a4df` probe: **5/5 invalid mutations accepted**.
- Final `ddb` probe: **0/5 accepted**; all rejected.
- Extra/missing records, wrong owner, fabricated payload, opaque/sibling/prior-row mutations: rejected.
- Root/App/Node TypeScript checks under `.app-tsc.lock`: passed.
- Scoped ESLint with `--max-warnings 0`: passed.
- `git diff --check`: passed.
- Protected specs, product files, pins, generated files, and vendor kit hashes unchanged.

The projection now derives expected parent/shot/child/manifest/digest identities from original canonical data, intended row/media, and the Agent provider’s deterministic materialization rules. Existing request, history, reload, legacy-route, and native inverse/undo predicates remain intact. No browser, service, build, install, or full suite was run.

Recommended next step: harness commit and normal merge; defer browser/full-suite qualification to the central test service.