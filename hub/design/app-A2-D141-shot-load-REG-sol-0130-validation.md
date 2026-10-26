# A2 D141 REG validation — unchanged frozen base

Base `867cb2737af1b46dc608c7cd37c349e920fe9422`; tree `2b44a46ca51d880c6a00da4c19aa8629b55eb7dd`. No product or test edits; no GREEN candidate.

Node: `/opt/node20/bin/node --version` → `v20.20.0`. Dependencies resolve to `/home/user/work/app/node_modules` and were not changed.

## Commands and results

1. `PATH=/opt/node20/bin:$PATH /opt/node20/bin/node node_modules/vitest/vitest.mjs run src/tools/video-editor/lib/shot-group-pack-commands.test.ts --maxWorkers=3 --no-cache --configLoader=runner` → exit 1 before collection: existing config uses `__dirname`, undefined in runner mode. Zero test executions.
2. `PATH=/opt/node20/bin:$PATH /opt/node20/bin/node node_modules/vitest/vitest.mjs run src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts --maxWorkers=3 --no-cache --configLoader=runner` → same config startup error; zero test executions. This was issued before the first process returned; no source had changed.
3. `PATH=/opt/node20/bin:$PATH /opt/node20/bin/node node_modules/vitest/vitest.mjs run src/tools/video-editor/lib/shot-group-pack-commands.test.ts src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts --maxWorkers=3 --no-cache --configLoader=runner --config /tmp/w-87ce9d448e/vitest-d141.config.mjs` → exit 1; **21 passed, 1 failed, 22 total; 1 file passed, 1 file failed**. Workspace guard suite 16/16 PASS; shot-group file 5/6 PASS. Exact D141 failure `expected 3 to be 2`, unchanged assertion `shot-group-pack-commands.test.ts:397`. Raw targeted output follows below.
4. `PATH=/opt/node20/bin:$PATH npx --no-install tsc --noEmit -p tsconfig.app.json` → exit 0, zero diagnostics.
5. `PATH=/opt/node20/bin:$PATH npx --no-install tsc --noEmit -p tsconfig.node.json` → exit 0, zero diagnostics.
6. `PATH=/opt/node20/bin:$PATH npx --no-install eslint src/shared/lib/placement/placementService.ts` → zero diagnostics, exit 0. (Executed in a command cell followed by successful `git diff --check`; empty lint log.)
7. `git diff --check` → exit 0, no output; repeated after verification.
8. `git status --short` → empty. Source manifest rehashed all six traced files and confirms original blobs unchanged.

No full suite or socket/browser service was used. Test fetch is mocked; no localhost needed. No before/after test repeat: there is no edit/candidate. Initial failures were config startup, followed by one actual execution of the two targeted files.

## Private wrapper

Only `/tmp/w-87ce9d448e/vitest-d141.config.mjs` and `/tmp/w-87ce9d448e/vite-cache` were used for config/cache. The wrapper dynamically imports the **existing** repo config, supplies its existing directory constant to runner mode, and disables Vitest caching. Since both `config/testing` and `config/vite` resolve `../..` to the same root, the existing Astrid helper resolves the same vendored source. No repository config/setup/alias/test source was changed.

```js
globalThis.__dirname = "/home/user/work/wt/app-A2-D141-shot-load-REG-sol-0130/config/testing";
const { default: config } = await import("/home/user/work/wt/app-A2-D141-shot-load-REG-sol-0130/config/testing/vitest.config.ts");
export default { ...config, cacheDir: "/tmp/w-87ce9d448e/vite-cache", test: { ...config.test, cache: false } };
```

## Actual targeted output

```text

 RUN  v4.1.5 /home/user/work/wt/app-A2-D141-shot-load-REG-sol-0130

 ✓ src/shared/lib/placement/__tests__/placementService.workspaceV1.test.ts (16 tests) 788ms
     ✓ places a generation by publishing a new head revision  639ms
 ❯ src/tools/video-editor/lib/shot-group-pack-commands.test.ts (6 tests | 1 failed) 58ms
     ✓ deep-copies document nodes and registry refs with final-video lineage and no shared objects 14ms
     ✓ refuses media-bearing duplicates before task admission or timeline mutation 9ms
     ✓ polls a command at the caller-supplied cadence until succeeded 2ms
     ✓ refreshes the document view to the promoted primary variant 1ms
     × duplicates only the explicitly active non-default timeline and never touches relational storage 27ms
     ✓ refuses the retired promote-primary family before task admission or timeline mutation 2ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/tools/video-editor/lib/shot-group-pack-commands.test.ts > shot-group pack commands > duplicates only the explicitly active non-default timeline and never touches relational storage
AssertionError: expected 3 to be 2 // Object.is equality

- Expected
+ Received

- 2
+ 3

 ❯ src/tools/video-editor/lib/shot-group-pack-commands.test.ts:397:27
    395|     // The version check and the compare-and-swap cycle each load the …
    396|     // and no media task is admitted: a group with no final video has …
    397|     expect(runtime.loads).toBe(2);
       |                           ^
    398|     expect(runtime.publishes).toEqual(['rev-2']);
    399|     expect(paths).toEqual([]);

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯


 Test Files  1 failed | 1 passed (2)
      Tests  1 failed | 21 passed (22)
   Start at  01:37:33
   Duration  2.57s (transform 1.55s, setup 544ms, import 1.60s, tests 847ms, environment 1.50s)

```
