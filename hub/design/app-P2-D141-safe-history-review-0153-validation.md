# D141 validation record

All checks were read-only. No product tests, imports, browser runs, request
replays, tsc, lint, or source changes were performed; those are not applicable
to this evidence-only review.

Validation results:

- `sha256sum` against the manager publication receipt: PASS for all five
  publication originals, including byte counts.
- `git show 22c30a0:evidence/*` hash comparison: PASS for all five committed
  evidence files.
- Structural parse of retained 3118 `error-context.md`: PASS; two actual-only
  objects, 22 paths per object, zero expected-side structural lines.
- Safe path comparison against published `extra-fields.json`: PASS in both
  object instances; array kinds are retained for `dependencies` and `owners`.
- Git commit/tree and source-blob checks for current and prior tuples: PASS.
- Current retained manifest, JUnit, readiness XML, log, and diff hashes: PASS.
- Prior retained `d66.tgz` archive, JUnit, readiness XML, manifest, request,
  and source-plan hashes: PASS.
- Prior original XML parse: PASS for 8 total, 2 passed, 2 failed, 1 error,
  3 not-run; automatic-placement case PASS at 88.78 seconds.

No raw artifact was extracted to a new file, copied, edited, or deleted.
