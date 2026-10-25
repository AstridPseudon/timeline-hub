# U3/D135 report

Implemented the authorized App candidate updates:

- Applied verified upstream `36e1ef39...` pointer/runtime-panel changes exactly.
- Fixed both warm-up recovery tests via deterministic fixture status handling.
- Adapted `NewChatMenu` to the retained unified model-menu API.
- Preserved legacy `AgentChatMenu` behavior and upstream update prompts.
- Wrote required evidence and commit message files.

Validation:

- Warm-up gate: 2 passed.
- Affected AgentChat/project-contract/setup/runtime tests: passed except discovered menu incompatibilities.
- Focused post-repair tests: all selected `AgentChatMenu` predicates and 31 `NewChatMenu` predicates passed.
- TypeScript: passed.
- Scoped ESLint: passed.
- Diff/conflict checks: passed.

Blocked: 3 upstream `NewChatMenu` assertions require changes to unauthorized `NewChatModels.tsx`:

1. Selector class styling.
2. Selector `· Low` copy.
3. Per-model “New chat” button.

No tests were weakened or skipped. Full/browser suites were not run. See [findings.json](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-U3-D135-current-tip-return-2014/evidence/findings.json>) and [validation.md](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-U3-D135-current-tip-return-2014/evidence/validation.md>). BLOCKED sentinel created.