Implemented only the EOF whitespace removal in `previewRevision.ts`.

Validation:

- `git diff 925ef330b --check` — passed.
- No tests rerun; whitespace-only change.
- No claim made for `npx tsc --noEmit`; the actual App check is `npm exec tsc -- --noEmit -p tsconfig.app.json`, handled by the manager.

Commit message written to the requested path. No blockers or unrelated changes.