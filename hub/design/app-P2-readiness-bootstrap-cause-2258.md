## Report

Implemented a bounded harness-only diagnostic repair.

- Preserved the real bootstrap order and readonly `UNKNOWN` boundary.
- Added finite safe bootstrap stages: context, navigation, connection, selection, outbox-read.
- Existing diagnostics now expose the bootstrap failure class/stage without exposing the private cause.
- Main D28 test body remains byte-identical (`5d36c124…`).
- No product, generated, schema, lockfile, or journey-body changes.

Cause classification:

- Observed: native seed/history passed; mounted readiness failed after 6.2s at `initialOutboxRead.status`, with all 8 P2 cases not run.
- Reconstructed: the broad bootstrap catch erased whether context, navigation, connection, selection, or readonly outbox access failed.
- Live causal stage: still `UNKNOWN`; no new browser/service run was authorized. The prior trace was not retained accessibly.

Checks:

- `node --import tsx --test tests/e2e/local/d21-environment.test.ts tests/e2e/local/mounted-readiness-safety.test.ts` — PASS, 2 subtests.
- Scoped ESLint on 4 changed files — PASS, zero warnings.
- Locked root, App, and Node TypeScript checks — PASS.
- `git diff --check` — PASS.
- Changed scope verified: 4 permitted harness/safety files only.

Commit message written and `DONE` created. Recommended next step: manager runs the single meaningful live diagnostic with `PLAYWRIGHT_OUTPUT_DIR` exported before the leaf, then inspects the safe JSON/private trace.