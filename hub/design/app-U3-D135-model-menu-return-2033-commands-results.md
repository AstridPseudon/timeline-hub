# Commands and results

| Command | Result |
|---|---|
| `npm exec vitest -- run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 src/tools/video-editor/components/AgentChat/NewChatMenu.test.tsx -t 'keeps the compact, borderless selector\\|shows the level the row would use\\|starts exactly one chat from a row' --reporter=verbose` | 3 passed; remaining 58 were filtered by the exact test-name expression |
| `npm exec vitest -- run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 src/tools/video-editor/components/AgentChat/NewChatMenu.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMenu.test.tsx --reporter=dot` | 2 files passed; 127 tests passed |
| `npm exec tsc -- -p tsconfig.app.json --noEmit --incremental false` | passed; no output |
| `npm exec eslint -- src/tools/video-editor/components/AgentChat/NewChatModels.tsx src/tools/video-editor/components/AgentChat/NewChatMenu.tsx src/tools/video-editor/components/AgentChat/AgentChatMenu.tsx --max-warnings 0` | passed; no output |
| `git diff --check` | passed |
| scope, test-byte, and conflict-marker checks | passed; exact three source files, tests unchanged, no markers |
