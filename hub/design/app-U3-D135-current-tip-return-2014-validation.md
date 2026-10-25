# U3/D135 validation

## Passing checks

- `npm exec vitest -- run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 src/tools/video-editor/components/AgentChat/AgentChat.projectContract.test.tsx -t 'recovers a (generic|setup) warm-up failure'` — 2 passed, 37 filtered.
- The required affected run before the menu repair: `AgentChat.test.tsx` 73 passed; `AgentChat.projectContract.test.tsx` 39 passed; `AgentSetupCard.test.tsx` 42 passed; `RuntimeConnectionPanel.test.tsx` 47 passed; it exposed the menu contract failures without weakening tests.
- Post-repair focused run over `AgentChatMenu.test.tsx` and the affected `NewChatMenu.test.tsx` predicates — all selected `AgentChatMenu` predicates passed; 31 selected `NewChatMenu` predicates passed.
- `npm exec tsc -- -p tsconfig.app.json --noEmit --incremental false` — completed with no diagnostics (exit 0).
- Scoped ESLint with `--max-warnings 0` over touched AgentChat sources/tests and the two actual upstream pointer files — exit 0.
- `git diff --check` — exit 0.
- Conflict-marker scan over manifest, AgentChat, RuntimeConnectionPanel, and ToolbarPointer — no matches.
- `git diff --quiet 36e1ef39c03c2c91a36fd964e3a2385a410bc06c -- src/shared/components/RuntimeConnection/RuntimeConnectionPanel.test.tsx src/shared/components/ToolbarPointer/ToolbarPointer.tsx` — exit 0.

## Remaining gate

The focused post-repair run still has 3 upstream `NewChatMenu.test.tsx` failures:

1. `keeps the compact, borderless selector...` expects the upstream selector classes.
2. `shows the level the row would use...` expects the upstream `· Low` copy.
3. `starts exactly one chat from a row's New chat button...` expects the upstream per-model button.

All three are supplied by the upstream `NewChatModels.tsx` implementation, while this candidate retains the unified-menu `NewChatModels.tsx` implementation. That file is outside the exact seven-file authorization; changing it would violate scope. No tests were skipped, weakened, rewritten, or marked xfail.

## Not run

No full suite, browser/e2e suite, live-socket suite, build, ZIP, or profile run was requested or run.
