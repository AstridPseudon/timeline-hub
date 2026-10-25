# Commands and results

| Command | Result |
|---|---|
| `npm exec vitest -- run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 src/tools/video-editor/components/AgentChat/NewChatMenu.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMenu.test.tsx --reporter=dot` (Node 20.19.4) | PASS; 2 files, 127 tests |
| `npm exec vitest -- run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 src/tools/video-editor/components/AgentChat/AgentChat.projectContract.test.tsx -t 'recovers a (generic|setup) warm-up failure without creating another session' --reporter=verbose` (Node 20.19.4) | PASS; 2 tests, 37 filtered by explicit name |
| `request-test app-U3-D135-cumulative-review-2040 targeted --files "src/tools/video-editor/components/AgentChat/AgentChatMenu.test.tsx src/tools/video-editor/components/AgentChat/NewChatMenu.test.tsx"` then `wait-test` | PASS; 2 files, 127 tests |
| `npm exec tsc -- -p tsconfig.app.json --noEmit --incremental false` (Node 20.19.4) | PASS; no diagnostics |
| `npm exec tsc -- -p tsconfig.node.json --noEmit --incremental false` (Node 20.19.4) | PASS; no diagnostics |
| Scoped `npm exec eslint -- --max-warnings 0` over touched/resolved App TypeScript files | PASS; no warnings |
| `git merge-tree --write-tree d5a1d1ab65 36e1ef39c0` | Expected conflicts: 5 content plus 2 NewChatMenu modify/delete; reviewed tree `55af6818d129b633b3a36cbd5c5510a50e178d66` |
| Merge-tree outside-blob comparison against `e9041a2621` | PASS; exactly 7 expected resolution paths |
| Final return path comparison `git diff --name-only e9041a2621 eba8b345c1` | PASS; exactly the 3 authorized model-menu sources |
| Ancestry, parent tuple, conflict-marker, unresolved-index, diff-check, AST, hash, and manifest audits | PASS |

The central service command used its supported runner wrapper (`npx vitest`, `--maxWorkers=2`) for mechanics confirmation; the exact required command was also run directly with the private Node 20.19.4 runtime and `npm exec`.
