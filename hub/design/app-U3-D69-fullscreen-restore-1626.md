## D69 report

- Restored the frozen upstream shell-root test body unchanged (hash `40564bab…`) in [PanelFullscreenFrame.test.tsx](/home/user/work/wt/app-U3-D69-fullscreen-restore-1626/src/tools/video-editor/runtime/PanelFullscreenFrame.test.tsx).
- Added the minimal shell-aware behavior to [PanelFullscreenFrame.tsx](/home/user/work/wt/app-U3-D69-fullscreen-restore-1626/src/tools/video-editor/runtime/PanelFullscreenFrame.tsx), preserving standalone cases.
- Caller proof: `ExtensionPanelHost.tsx:128-133` renders `PanelFullscreenFrame` and wires fullscreen exit.

Tests:

- Focused Vitest: 15/15 passed.
- Old source regression check: 7 passed, restored case failed.
- TypeScript: `tsconfig.json`, `tsconfig.app.json`, `tsconfig.node.json` passed.
- Scoped ESLint and `git diff --check` passed.
- No browser, e2e, full-suite, or native tests run.

Assigned count: 1 restored, 0 remaining. Other audit findings were outside scope. Core source change should receive the planned independent review.

Commit message written and `DONE` marker created.