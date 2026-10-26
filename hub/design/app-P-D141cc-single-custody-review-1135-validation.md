# Validation

Read-only validation performed after review output creation:

- Parsed all review JSON with Python standard-library `json`; PASS.
- Recomputed the accepted dispatch recipe SHA-256 and raw worker/native log hashes; PASS against the recorded values.
- Checked the exact selector namespace, request directory, assigned submit artifact, lock, and output directory; no actual request/row/artifact was present.
- Checked the review worktree with `git status`, `git diff --stat`, and `git diff --exit-code`; clean and unchanged.
- Checked all four detached source pin HEAD/tree pairs and clean states; exact.
- No browser, pytest, Vitest, TypeScript, lint, build, service body, request-test, wait-test, or stop-test was run by this review.

The worker's own final validation command is separately recorded as failed by `KeyError: 'native_invocation_count'`; this review does not promote that failure to PASS.
