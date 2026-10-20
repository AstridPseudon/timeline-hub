# App M2 shot-name hook retirement fix

## Source identity

- Reviewed App source SHA: `04810b121ddc36112025e30f9a83630aaff2eece`
- Reviewed App tree: `e86392403b3259cbc562aec9b4974fb292830a3b`
- Worktree: `/home/user/work/wt/app-m2-shot-name-hook-retirement-fix`
- Resulting commit SHA/tree: not materialized by this worker; `.git` is read-only and the harness will commit the worktree.

## Delta

Only these two files differ from the reviewed source:

- `src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.ts`
  - Added a hook-owned mount lifetime ref.
  - Effect setup re-arms the ref; cleanup retires the pending save and marks the hook unmounted.
  - Both accepted and refused Promise continuations require the hook to remain mounted, in addition to the existing pending-promise and shot-scope guards.
- `src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.test.ts`
  - Added the deferred-save/unmount regression: resolving after unmount calls neither editor action.
  - Existing accepted-completion and exact refusal-draft tests remain unchanged.

Exact delta:

```text
2 files changed, 35 insertions(+), 2 deletions(-)
git diff --binary SHA-256: fbca6c52726f175121e416c3bea257a8c54ad6b94f9da1de472c14b51638b11d
git diff --check: PASS
```

Baseline blob IDs and resulting worktree file SHA-256 values:

```text
useNameEditing.ts
  baseline blob: 09aedfae2fe1d27b74a9e833bc5a0ac187a9fb66
  worktree SHA-256: 884651d931ea8d22c9fbca844fb2f9b66af0bdc6d127e5fbcf38ce3446942e25
useNameEditing.test.ts
  baseline blob: 79e91d55d464c7a6a53fda5e1f228bf6fdb2e6bb
  worktree SHA-256: d4c5d612fa3b39e466f1579ff40cc95444599dd76d07f750cfdc20cdb9a4e52e
```

No other shot-name source file changed.

## Results

Targeted Vitest used the worker-owned private12 wrapper/config, the existing `__dirname` preload, `--configLoader=runner`, `--no-cache`, one worker, and no shared Vite cache:

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-shot-name-hook-retirement-fix/runner-paths.cjs /tmp/app-coherent-deps12/node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-shot-name-hook-retirement-fix/vitest.private12.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/shotSetCapture.test.ts src/tools/video-editor/commands/shotSetSession.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx src/tools/travel-between-images/pages/ShotEditorView.test.tsx src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.test.ts

PASS: 6 files, 120 tests.
```

```text
node_modules/.bin/eslint src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.ts src/tools/travel-between-images/components/ShotEditor/hooks/editor-state/useNameEditing.test.ts --max-warnings 0

PASS
```

Not run: full/project suite, typecheck, build, browser/native gate, localhost or socket tests, install, or integration. This report makes no integration or retirement claim. KEEP for the imminent native browser gate.
