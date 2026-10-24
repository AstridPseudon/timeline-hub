## Report

- Reproduced baseline: lifecycle file had 12/13 passing; failure was line 331 querying stale “Set up Astrid.”
- Cause: current live Home CTA is “Get the app” (`PublicAstridHeroCta.tsx`); direct-entry `/home?experience=app` and storage/navigation setup were correct. Matching upstream `2a288e6` has identical relevant source/test blobs.
- Fix: changed only the test query to the live exact CTA label. All dialog closure, Vision focus, navigation, replay cancellation, and strict assertions remain unchanged.

Validation:

- Vitest lifecycle file: 13/13 passed.
- Root/App/Node TypeScript checks: passed serially.
- Scoped ESLint: passed.
- `git diff --check`: passed; exactly one file, one-line delta.
- No full/browser/service/backend/build runs performed.

No blockers. Commit message written for `app-F-full-home-lifecycle-1132`; completion marker created.