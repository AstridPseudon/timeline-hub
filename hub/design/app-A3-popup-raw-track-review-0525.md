# A3 Review: FAIL

Findings:

- `timeline-asset-plans.ts:284-292` does not reject `disabled: true`, although Runtime’s authoritative inactive guard does. This can emit an invalid popup ADD instead of refusing locally.
- The required mounted occupied-V2 production-positive test is absent. The author’s temporary persistence test hung/OOMed and was removed; retained persistence coverage has only 6 unrelated tests.

Production carrier verified: `ShotTimelineMediaControls` → `useTimelineCommandsService` → `commands/media.ts` → planner → A2 outbox. No dormant executor or legacy writer was used.

Tests:

- Planner + `ShotTimelineMediaControls`: 17 passed.
- Adjacent media/drop/provider tests: 119 passed.
- Popup data-provider A3 tests: 36 passed.
- Retained command persistence: 6 passed.
- TypeScript root/App/Node: passed.
- Changed-file ESLint: passed.
- `git diff --check`: passed.
- Environment used Node 22.22.0; no Node 20 runtime was available.

No product files changed; worktree is clean. No full/browser/backend suite run per brief.