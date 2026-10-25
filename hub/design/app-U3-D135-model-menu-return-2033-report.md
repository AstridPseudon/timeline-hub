## Report

Implemented U3/D135 model-menu restoration in:

- [NewChatModels.tsx](/home/user/work/wt/app-U3-D135-model-menu-return-2033/src/tools/video-editor/components/AgentChat/NewChatModels.tsx)
- [NewChatMenu.tsx](/home/user/work/wt/app-U3-D135-model-menu-return-2033/src/tools/video-editor/components/AgentChat/NewChatMenu.tsx)
- [AgentChatMenu.tsx](/home/user/work/wt/app-U3-D135-model-menu-return-2033/src/tools/video-editor/components/AgentChat/AgentChatMenu.tsx)

Restored per-model New chat actions, `· Low` copy, and both menu families’ selector styling/start semantics. Tests and all other files remain unchanged.

Validation:

- Three targeted NewChatMenu nodes: 3 passed.
- Affected tests: 2 files, 127 passed.
- TypeScript: passed.
- ESLint: passed.
- `git diff --check`: passed.
- Exact three-file scope and conflict-marker checks: passed.
- No full/browser/build suites run.

Commit message written and `DONE` created. Final producer-first pin update remains pending as instructed; no blockers.