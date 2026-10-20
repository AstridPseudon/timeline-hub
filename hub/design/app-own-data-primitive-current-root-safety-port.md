# App own-data primitive current-root safety port

## Result

Applied the approved own-data write safety hunk to the current App integration
root and added the direct `AuthoredState` regression. No scalar implementation,
gesture, Playwright helper, ancestor cohort, API, wire, or guard changes were
introduced.

The compact worker wording named `clipScalarCapture.test.ts`, but the current
root has no `clipScalarCapture.ts` or scalar test. The App manager brief
explicitly requires the direct primitive test instead; the added test is the
approved `clipMovePrimitives.test.ts` from 4ad52c973, byte-for-byte.

## Exact source/tree identity

- Base/current integration commit: `d12d0909746c552dee6dac7b5d8459e8e1f27679`
- Base/current integration tree: `c91e3c07f293658aa0f26dd180ac464c45b71559`
- Worker branch: `tl/app-m2-own-data-primitive-current-root-safety-port`
- Reference production delta commit: `46c15aee5fd08aa71a49b0378eb694491f8482da`
- Reference production tree: `93042fb19a46d121a9a843a75a9fe85b426fe67a`
- Approved direct-test source: `4ad52c973`
- Working tree status: only `clipMovePrimitives.ts` modified and
  `clipMovePrimitives.test.ts` added.
- Uncommitted working trees do not have a Git tree SHA until the harness
  commits them. Changed-file SHA-256 values:
  - `src/tools/video-editor/commands/clipMovePrimitives.ts`:
    `d7514e9f893a7ef9845e26c781342dbf705488cb3e2d8dfed35ad9d5f5fb1233`
  - `src/tools/video-editor/commands/clipMovePrimitives.test.ts`:
    `b93f1367fde457047c6836fb308550d8ff34c22a5f7eac81642d6e7546e69bcc`

## Exact diff

`clipMovePrimitives.ts` is exactly the six-line production delta from
46c15aee5:

```diff
     let target = this.entity(ref)!;
     for (const key of path.slice(0, -1)) {
-      if (!object(target[key])) throw new ClipMoveError('write requires recorded container creation');
+      if (!has(target, key) || !object(target[key])) throw new ClipMoveError('write requires recorded container creation');
       target = target[key];
     }
     const key = path[path.length - 1];
     if (state.state === 'absent') delete target[key];
-    else target[key] = copy(state.value);
+    else Object.defineProperty(target, key, {
+      value: copy(state.value), enumerable: true, configurable: true, writable: true,
+    });
```

The added direct test is byte-identical to
`4ad52c973:src/tools/video-editor/commands/clipMovePrimitives.test.ts`.
It covers ordinary own `__proto__`, `constructor`, `prototype`-adjacent/literal
keys, null/unknown values, ordering/JSON visibility, cloning, clears, explicit
owned containers, and refusal of inherited or missing containers while retaining
the original recorder guards.

## Tests

Passed with the existing private13 Vitest runner, the approved `__dirname`
preload, `--configLoader=runner`, `--no-cache`, one worker, and no shared-cache
writes:

```text
PRIVATE13_NODE_MODULES=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/full-main574-public13-8bd8f741/private13/node_modules TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-own-data-primitive-current-root-safety-port/vitest-tmp NODE_OPTIONS=--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/full-main574-public13-8bd8f741/private13/node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipMovePrimitives.test.ts src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts
Test Files  3 passed (3)
Tests       37 passed (37)

PRIVATE13_NODE_MODULES=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/full-main574-public13-8bd8f741/private13/node_modules TMPDIR=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-own-data-primitive-current-root-safety-port/vitest-tmp NODE_OPTIONS=--require=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs node /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/full-main574-public13-8bd8f741/private13/node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/clipMovePrimitives.test.ts src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/genericPatchCapture.test.ts
Test Files  4 passed (4)
Tests       115 passed (115)
```

Also passed `git diff --check`. The first runner attempt without the preload
failed before tests because the repository config uses CommonJS `__dirname`
under runner loading; it was corrected with the existing preload, with no
bundled-config fallback. No full suite, project typecheck, build, browser,
socket, install, or scalar suite was run; the scalar module is absent from this
current root by design.

## Decisions, blockers, next steps

- Decision: use the manager-approved direct primitive test rather than add the
  unlanded scalar module named in the compact task wording.
- No implementation or behavior decision was changed; the hunk preserves own
  dynamic leaves and requires own recorded containers, while keeping unknowns,
  nulls, order, and original guards.
- No blockers. The harness should commit these two App files, then the manager
  can merge/qualify the port before activating the current-root native writers.
