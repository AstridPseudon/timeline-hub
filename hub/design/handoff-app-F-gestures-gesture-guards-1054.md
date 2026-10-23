# App F gesture-guards handoff

PASS on base `7e0af6c9cda5a81a89505b006fcd653d4a5fc770`.

The 22 focused failures were caused by semantic gesture tests still invoking the retired pre-U3 direct capture-port service/drag harness. U3’s current upstream editor deliberately removed that wiring: public `moveClip`/`trimClip` use `state.ops.applyEdit`, while mounted drag completion uses `applyResolvedClipMove` and then the same A2 save funnel. The production caller is therefore current A2, not the dormant adapter leaf.

The only touched product-repo path is `src/tools/video-editor/commands/semanticGestures.test.ts`. Positive cases now exercise the live A2 callback and current resolved drag callback. Direct adapter tests still preserve absent-capture, invalid-time, cross-track, host, projection-identity, outbox, and native-trim refusal outcomes. Obsolete snap-query cases now verify the current planner result reaches `applyResolvedClipMove`; no old capture port, TS executor, outbox, persistence, provider, or P1/P2 source was restored.

Evidence: focused Vitest 25/25; scoped ESLint PASS; `git diff --check` PASS; locked App `tsc --noEmit -p tsconfig.app.json --pretty false` exit 0. The original focused baseline was 22 failures / 3 passes. No full or browser suite was run.
