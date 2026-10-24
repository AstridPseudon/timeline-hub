## Report

- Offline reproduction confirmed the popup target mismatch: raw `f2-agent-clip` is rendered as `occurrence:f2-occurrence-copy:f2-agent-clip`.
- No speculative DOM alias or guard change was made. A safe fix requires coordination with the A2 wrapper/provider owner because raw IDs currently trigger the provider’s retained-raw-ID collision guard.
- Worktree remains clean; `BLOCKED` marker and commit message were written.

Checks passed:

- Vitest: 4 files, 70 tests passed.
- TypeScript: root, app, and node configs passed.
- Scoped ESLint passed.
- `git diff --check` passed.

Browser/backend P2 was not rerun.