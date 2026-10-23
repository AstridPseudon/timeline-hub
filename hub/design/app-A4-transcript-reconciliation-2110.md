Implemented A4 mounted transcript witnesses in only [project-transcript-host.persistence.test.tsx](/home/user/work/wt/app-A4-transcript-reconciliation-2110/src/tools/video-editor/lib/project-transcript-host.persistence.test.tsx).

Added:

- Legacy config-mirror fallback witness: records A2’s exact pre-transport refusal.
- Mounted caption/review reconciliation request and persisted outcome.
- Collision/shared-row mounted outcomes using full-v2 `doc.patch` requests.
- Existing tests and implementations unchanged.

Verification:

- Vitest: 4 files, 56 tests passed.
- ESLint scoped with `--max-warnings 0`: passed.
- Three TypeScript projects under flock: passed.
- `git diff --check`: passed.
- Node: v22.22.0.
- HEAD: `001145ce1dcba562ab082620e965e73bac1857d1`
- HEAD tree: `e9fc8619a263ac4dee427ec7acd8478b3d03d359`

Remaining gaps are honestly captured: config-mirror fallback emits no request because A2 refuses the contradictory mirror; collision/shared-row cases are accepted generic patches rather than legacy `transcript.associate` refusals; persisted legacy review deletion is not encoded.

No full/browser/live suite was run. Commit message written and `DONE` marker created.