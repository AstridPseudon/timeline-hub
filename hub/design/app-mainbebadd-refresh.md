# App MAIN bebadd0e1 true refresh

## Source and resolved tree

- Repository: App.
- Base/first intended parent: `0d5009e18bee8e29f894dabf5db501a0fcea750f` (`tl/app-m2-mainbebadd-true-refresh`). Base tree before this refresh: `b323667662d565526d7c2395733f26e2c6380378`.
- Common ancestor: `574e97f44a81e0ec1a896fc3fb8626deb2f1edf0`.
- Incoming tip/second intended parent: `bebadd0e1283753e3805c2d61688e3dee8b929e2` (`origin/main`), whose parent is `9c59ed368c42e267e4c01be7a4329afb478282f5`.
- Dispatcher merge-parent directive: `bebadd0e1`; intended final commit parents are exactly `0d5009e18...` then `bebadd0e1...`.
- The six-commit `574e97f44..bebadd0e1` patch was applied to the working tree; no Git merge or commit was run. The incoming patch fingerprint is `7a94f9080790e842637ebee8791887620c830babcb12e88c5f32f64837c87fbb`.
- Resolved working-tree patch fingerprints: tracked files `b75fef52a69004cf2ae0d961e5683084480972f9609c9d42477f5bab6c004123`; full patch including untracked additions `c1d7e90b73fe378172dda89412c5bbdc342d492ed5407bb76cdabef0cb600a17`. Git does not expose a new tree object here because the harness owns the commit/index operation.

## Intent and assertion ledger

- All 174 incoming paths are represented in the resolved working-tree delta; no incoming path was omitted. MAIN infrastructure and chat cleanup are retained.
- MAIN's removal of its own retired release/configuration flags, runaway Timeline extension fixtures, and their snapshots/e2e tests is retained. Those were upstream-owned tests, not OUR Timeline behavior coverage.
- TrackInspector preservation coverage, including the a04f opaque-value preservation assertions, remains present and passing. Its command-backed production wiring remains present.
- The three original `useClipDrag.test.tsx` drag `it.fails` assertions remain unchanged: free multi-clip drag to a new bottom track, pinned-group cross-track drag, and pinned-group drag to a new track. No new expected-failure marker was added; the lane reports exactly three expected failures.
- Native Timeline command/opaque/retry assertions remain in `clipMoveCapture`, `authoringBundle.moveOpaque`, `authoringBundle.sharedOpaqueRemap`, `commitOutbox`, `commitSession`, TrackLabel command/capture/gesture, and `useTimelineOps` tests. They were not deleted, weakened, or converted to refusal expectations.
- Native browser/e2e source coverage remains in `tests/e2e/local/three-products.spec.ts` and `tests/e2e/timeline/command-outbox.spec.ts`; these were not run locally because browser/socket suites are centrally owned.
- App-owned move, label, `None`, delete, name, and automatic sections, plus App2's new ports, remain in the resolved tree. The incoming MAIN delta did not replace those behaviors.
- The only assertion-adjacent overlap adaptation was `useAgentSession.proposal-vertical.test.tsx`: it takes MAIN's current ACP-unavailable `503 acp_unavailable` fixture and cleanup while retaining the Timeline integration's exact-one-request, no-prompt, and no-proposal-apply assertions. This is chat-route fixture maintenance, not a Timeline wire change.

## Manual resolutions

- `config/vite/vite.config.ts`: kept Timeline Runtime operation admission/proxy and current fallback behavior; removed MAIN-retired editor fixture alias code.
- `scripts/dev-local-workspace.mjs`: kept the Timeline Runtime operation origin and removed the retired editor-only flag.
- `src/app/main.bootstrap-order.test.tsx`: adopted MAIN's current extension-runtime-before-render assertion without weakening it.
- `src/tools/video-editor/hooks/useAgentSession.proposal-vertical.test.tsx`: combined MAIN's current unavailable-ACP setup with the existing behavior assertions, as recorded above.
- `tests/e2e/local/support/harness.ts`: kept Timeline authoring/profile/source tuple configuration while accepting MAIN's release-config flag removal.

## Tests and checks

All Vitest runs used the established private public13 overlay at `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/full-main574-public13-8bd8f741/private13/node_modules`, the snapshot preload, an own worker cache/TMPDIR, `--configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism`, and no writes to shared dependencies.

1. Timeline command/TrackInspector/opaque/outbox/session lane (9 files): **325 passed**.
2. Timeline state/drag/render lane (9 files): **424 passed, 3 expected failures**. The three expected failures are the unchanged original drag cases listed above.
3. MAIN-overlap app/chat/provider lane (9 files): **241 passed**.
4. Targeted ESLint over 123 existing incoming TypeScript/TSX files: **exit 0**.
5. `git diff --check`: **exit 0**.

No full suite, browser/e2e/localhost/socket suite, build, project TypeScript check, or install was run. The central test service was not requested because this task explicitly says No full; manager should run the appropriate final suite after the harness creates the true two-parent commit.
