## Done

Copied the three files from `fa702ec…` verbatim onto base `6c33025…`:

- `d21-environment.ts`
- `d21-environment.test.ts`
- `three-products.mounted-readiness.spec.ts`

All blobs match exactly; no other paths changed. Protected P1/P2/Gate-5/harness files remain unchanged.

## Verification

- D21/readiness controls: passed.
- Scoped ESLint: passed, zero warnings.
- Root, App, and Node TypeScript checks under FD-4096 lock: passed.
- Playwright collection-only: P3 1, P1 2, P2 8.
- `git diff --check`: passed.

The current exact donor contains 14 test declarations; the earlier report stated 13. I preserved the donor exactly and did not alter tests.

No browser, provider, native, backend, or full suite was run.

Commit message and `DONE` marker created.