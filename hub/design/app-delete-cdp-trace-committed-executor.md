# App Delete CDP trace — committed executor

## Result

The committed opt-in trace reproduced the first real parent-delete failure and identified a small App bug. The source fix and focused regression are in this worker's App worktree; a fresh untraced browser qualification remains for the next gate.

Source was pinned exactly to App commit `a6a7b1ba866e786ead1d5fbc8a80657a20ccdf64`, tree `2ccb9f864770bc714a8e5ad9f5b28bc8762fb655`, descended from `f732a73a4ee35cc9510f53b6f0e4f69dc8486702`. The paired sources were Agent `8130a401bf44a518d5a40ae274d398b8c560be55` / tree `236c3e57e0265c52b81ba8085de3193026176bff` and Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / tree `7ab412cc4bcbe517efcfa806e092336390312e18`.

## Central diagnostic

Registered and ran exactly one new strict wrapper with `TIMELINE_DELETE_KEYBOARD_TRACE=1`:

```text
app-m2-delete-cdp-trace-committed-executor-e2e-parent-delete-cdp-trace-committed-tree2ccb9f86-agent8130-runtime2c4-public13-e2e-integration-1020192806-5181
```

Command requested:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-m2-delete-cdp-trace-committed-executor e2e-parent-delete-cdp-trace-committed-tree2ccb9f86-agent8130-runtime2c4-public13-e2e-integration)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

Result: exit 1 after 333 seconds. The first real Delete case failed at its unchanged assertion with `wire.posts.length === 0` after 90 seconds; the strict two-case runner stopped, so the conflict case did not run. Source, public13/all77, Runtime/all75, peer, cache, and Chromium 141 pre/post guards passed. No legacy write occurred.

## Captured cause (secrets redacted)

The readable CDP attachment is preserved in the central run's browser artifact ZIP as `delete-keyboard-listener-scopes` (resource SHA `b5fc3059777858d236a3729555d5aec22b837bfc`). It records:

- Selected owner/path: the parent clip `f2-app-clip`, not an occurrence or pinned group; the displayed clip set contained `f2-app-clip` and `f2-transition-clip`.
- Call path: the real window Delete handler reached the real `handleDeleteClips`, then `clipDeletePort.capture`; no injected state, port, callback, handler call, or synthetic request was used.
- Port state: the existing command session object exposed `clipDeletePort`, `port`, `getState`, `recover`, `retry`, `flush`, `undo`, `observe`, and `dispose`. The session state was not refused for missing port; the capture exception happened before `finish` or `submit`.
- First refusing guard: `src/tools/video-editor/commands/commitSession.ts:341` threw `Displayed timeline does not match the raw authoring basis`. The captured current head had the matching project/timeline and revision, but its publication was unknown (`null`) while the session display head had a publication. The strict `null !== displayHead.publicationId` comparison was therefore the first false guard.

The trace also contains unrelated background promise rejections from unavailable project-chat/Supabase surfaces. They occurred after the capture exception and are not the Delete cause.

## Fix

The native clip-delete capture guard now treats a null current publication as unknown, matching the existing nullable comparison for clip move, while retaining project, timeline, and revision checks. A focused regression asserts that a matching revision with an unknown publication captures successfully without enqueueing a write.

## Evidence after the fix

```sh
NOTES=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-delete-real-handler-hard-diagnosis/notes
node --require "$NOTES/vitest-runner.cjs" node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 src/tools/video-editor/commands/commitSession.clipDelete.test.ts
```

PASS: 1 file, 25 tests.

```sh
node node_modules/eslint/bin/eslint.js src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/commitSession.clipDelete.test.ts --max-warnings 0
git diff --check
```

PASS.

No fresh untraced real browser case was run after the fix, and no full suite, TypeScript check, install, local browser, or shared dependency write was performed. The next step is one fresh central untraced strict real-case run on the harness-committed fix, then the normal two-case qualification if that case passes.
