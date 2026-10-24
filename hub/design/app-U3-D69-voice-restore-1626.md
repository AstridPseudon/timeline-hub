## D69 report

Implemented:

- Restored the frozen upstream voice-off test body unchanged; hash matches upstream: `d2925e…522fc`.
- Restored the gated voice matrix and corrected existing additional assertions.
- Fixed the proven regression in `AgentChat.tsx`: mic, shortcut, placeholder, and voice hint now honor `CHAT_VOICE_ENABLED=false`.

Tests/checks:

- Node 20.20.0 Vitest: 58/58 passed.
- Scoped ESLint: passed.
- TypeScript: passed.
- `check:no-raw-skips`: passed.
- `git diff --check`: passed.
- No browser/full suite run.

Changed files:

- [AgentChat.test.tsx](/home/user/work/wt/app-U3-D69-voice-restore-1626/src/tools/video-editor/components/AgentChat/AgentChat.test.tsx)
- [AgentChat.tsx](/home/user/work/wt/app-U3-D69-voice-restore-1626/src/tools/video-editor/components/AgentChat/AgentChat.tsx)

No blockers. Enabled-voice branch is represented in the matrix but unexecuted because the production gate is currently false. Commit message and `DONE` marker were written; independent protected-change review remains for the merge queue.