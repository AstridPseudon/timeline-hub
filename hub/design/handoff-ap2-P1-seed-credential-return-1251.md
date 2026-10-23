# Handoff: AP2 P1 seed credential invocation

PASS: App harness-only fix is ready at `tests/e2e/local/support/harness.ts`.

The embedded seed Python caller previously passed the credential-file filename as a `str` to `AstridClient.open`. Current Agent `resolve_runtime_connection` treats explicit strings as bearer tokens, whereas explicit `pathlib.Path` values use the supported credential-file reader. The caller now imports `Path` and passes `Path(case['credential'])`. This is the complete diff: 2 insertions, 1 deletion, one hunk; no product auth changes and no fixture/assertion changes.

Evidence: the synthetic resolver probe passed; the existing Agent resolver unit `test_explicit_credential_file_needs_no_parent_metadata_probe` passed (1 passed, 2 deselected); all three requested TypeScript checks, targeted ESLint, and `git diff --check` passed. The old failure's unauthorized-invalid-bearer boundary is explained by the string-vs-Path mismatch. No secret values were read or recorded.

The original live service, browser/e2e, build, heavy/full suites were not run under this worker's limits. The prescribed worker `tmpdir` is a file, so the isolated resolver test used a private `/tmp` directory. After harness commit, perform the committed-delta check and manager-owned original-service verification.
