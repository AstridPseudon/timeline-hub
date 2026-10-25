# U3/D135 validation

Source packet review: PASS (`PASS_CORRECTED_ARTIFACTS`). The reviewed packet records 16 files, 81 preview headers, 14 marker-bearing hunks, 67 clean hunks, 13 semantic conflicts, and one mechanical import union.

Candidate validation: PARTIAL. The manager established an index-only automatic merge; HEAD remains `d5a1d1ab6550187e377fd7387d300102b8b82ece`, with the upstream tuple recorded in `merge-parent`. `.git/MERGE_HEAD` and `.git/MERGE_MSG` are absent by this manager route. Only the five approved paths were manually resolved; the two automatic-merge `NewChatMenu` paths remain manager-owned DU state.

Commands run:

- `sed -n '1,260p' .../PLAN.md` — PASS, plan read.
- `git status --short` / `git ls-files -u` — PASS, automatic merge present; unmerged paths are the five approved paths plus manager-owned `NewChatMenu` delete/update paths.
- `git diff --check -- public/install-manifest.json src/tools/video-editor/components/AgentChat/{AgentChat.test.tsx,AgentChat.tsx,AgentChatMenu.tsx,TourChatPanel.tsx}` — PASS.
- `rg -n '^<<<<<<<|^=======|^>>>>>>>'` over the five approved paths — PASS, no markers.
- `node -e 'JSON.parse(...)'` on `public/install-manifest.json` — PASS.
- `npm exec eslint -- --max-warnings 0 src/tools/video-editor/components/AgentChat/AgentChat.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentChatMenu.tsx src/tools/video-editor/components/AgentChat/TourChatPanel.tsx` — PASS under Node 20.19.4.
- `npm exec tsc -- -p tsconfig.app.json --noEmit --incremental false` — FAIL only in automatic-merge `NewChatMenu.tsx` DU content (`selectedModel` and implicit callback types); the approved `AgentChat.tsx` `chatModelId` error was fixed.
- `npx vitest run --config config/testing/vitest.config.ts --maxWorkers=2 src/tools/video-editor/components/AgentChat/AgentChat.projectContract.test.tsx src/tools/video-editor/components/AgentChat/AgentChat.test.tsx src/tools/video-editor/components/AgentChat/AgentSetupCard.test.tsx src/tools/video-editor/components/AgentChat/TerminalNudge.test.tsx` via central test service — FAIL: 3 files passed, 1 failed; 159 passed, 2 failed. The two failures are project-contract generic/setup warm-up recovery observations that remain on `Getting Codex ready…` while the existing bridge read retry settles.
- `node scripts/installer/update-manifest.mjs --runtime-checkout /home/user/work/runtime --agent-checkout /home/user/work/agent --plan` — REFUSED: runtime checkout HEAD `e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9` does not match qualified manifest source pin `ab1e4f6141987706132916e2da16477f5a019464`.

No merge, fetch, checkout, rebase, reset, commit, final pin write, full suite, browser/tour/ZIP/build, or Runtime/outbox source edit was run. The harness still owns the final commit and exact two-parent ancestry.
