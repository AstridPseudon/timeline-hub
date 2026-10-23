# A3/P2 popup preview mock port handoff

Result: PASS.

Restored the exact donor `ShotTimelinePreview.test.ts` blob from
`9c8f7857b0ff1e661b4843b9771c87c6f012d480`, adding only its 36-line runtime,
command, asset, and mounted-editor mocks. The four cumulative A3 blobs are
exact donor matches; the only changed worktree path is that preview test.

Focused evidence: caller 9/9, real A3 receiver 25/25, preview 25/26. The
single preview failure is the unchanged raw `__proto__` baseline at line 752;
it was neither skipped nor weakened. Scoped new-test ESLint and `git diff
--check` pass; no package or lock changes. See the worker report for exact
commands, hashes, and the reused 1032 TypeScript evidence.
