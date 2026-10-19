## Report

Implemented preview revision provenance bound to the throttled Player delivery:

- Added committed/local/unavailable revision labels.
- Threaded revision metadata through the config mailbox with generation guards.
- Preserved cached committed labels when a newer target is unavailable.
- Added focused coverage for throttling, acknowledgements, stale generations, cached results, and no-cache failures.

Tests:

```text
Vitest: 4 files, 44 tests passed
ESLint: passed
git diff --check: passed
```

Typecheck remains blocked by two unrelated existing errors in `RuntimeConnectionProvider.tsx` and `AgentChatNewChatButton.tsx`.

Host wiring gap: `canonicalCompositionError` does not currently expose the attempted target revision ID. The UI therefore shows a generic unavailable-target message unless `targetRevisionId` is supplied on the error. A future small seam should expose that ID from the loader/host without changing persistence.

Commit message written to the required path. No commit performed; harness will commit the worktree.