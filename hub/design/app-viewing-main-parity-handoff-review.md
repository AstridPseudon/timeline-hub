# App owner review: current-main Viewing parity harness

**APPROVE `701491b76f2f0af9cfcebacab74fc76adf220430` (`tl/vw-m3-main-parity-harness-type-fix`) as a TEST/CONFIG-ONLY merge onto `7bb885b638838588a0dff81b64b7c34960ac07f3`.** No blocking review findings. Actual four-case launch remains **HELD** pending the final safe App/Agent/Runtime/Composition pair/tuple, independently frozen dependency graph and fresh manager-controlled grant. This review issues no grant and claims no real parity qualification.

Read PLAN.md, App INBOX remote request at 11:14:53Z, and the exact final `.testresults.md`, `.patch`, `.filelist` artifacts. The owner's bounded task takes precedence over the INBOX's generic merge-request instruction: no merge was requested by this worker.

## Exact diff and current integration preservation

- Merge base: `667498cc49b4ec2b1ccd3a515eb87311c5126c93`. Candidate consists of port `877b7f33eb5fc8afe035d984d976683702819101` plus type fix `701491b76f2f0af9cfcebacab74fc76adf220430`.
- Exact branch delta: **32 files, +3213/-2**: three Playwright configs, two spec entry points, 26 Viewing test/support files, and one modified existing local test harness. This is 31 additions plus one modified file, not 31 total files.
- The modified harness only imports `TimelineClip` as a type and annotates two empty arrays. Independent TypeScript transpilation of current 7bb, port 877b and final 701491 emits identical JavaScript; SHA-256 `691abf4346ee8fadc3f69c22b0b555f24a7516dae410bc9928631a0c9148e02e` for all three. This is an erasure check, not a typecheck.
- Artifact patch is byte-identical to `git diff 667498cc4 701491b76`; SHA-256 `a3a054be91ad8f62116894807355c042d72866f7efa862ebb5ff558c7e27a4fc`.
- Applied that exact patch temporarily to this worker's current-7bb tree, with `git apply --check` succeeding. Compared every existing path outside the delta against its current-7bb Git blob: **5,877 paths, zero byte mismatches**. All 32 patched files match the candidate blobs exactly. See worker `source-proof.json`.
- Therefore the proposed merge retains current source, pins, manifests/lockfiles, vendor/artifacts, MediaScope, digest verification, render/download/admission product code, provider and private-fallback behavior. No old `320784f828a4` product closure or old Root provider is ported.
- Important ancestry limit: the *standalone candidate tree* predates the CORS fix. Its direct two-tree diff against 7bb also shows `src/shared/lib/media/mediaCrossOrigin.ts` and its test. These are existing integration-side changes, absent from the candidate's merge-base patch. The approval is for merging the exact test-only delta into current integration, preserving CORS; it does not authorize replacing current integration with the candidate tree.
- Current CORS Git blobs, retained unchanged during testing: product `ae079675e7aba67808a412f12dc289e8f613c643`; test `ffa8e9ad94b3cdde7beac57f711f6d28e8387ca2`.

## Reviewed gate behavior

- Four original case bodies remain: normal render/download, actual Player fixture readiness, positive Player/export comparison, and planted one-host picture mismatch only after the full passing baseline. All twelve frames remain `[0,37,44,45,52,89,90,120,121,135,143,164]`.
- Original 640x360 remains the default. Native 1920x1080 uses its separate named config, 2000x1200 viewport, and separately pinned Chrome 155 profile. Comparator checks native RGB dimensions/full buffers without resizing, channel error strictly greater than 2, maximum outside fraction `.001`. Boundary and planted-negative offline tests pass.
- The UI adapter uses current MAIN's `Rendered film` dialog, `Download` button, managed-object URL, authored filename and explicit existing blob fallback. Full fetch requires GET/fetch/200, no Range, exact Origin, no redirect, full length/digest and byte identity with the saved same-page blob. No product download fallback was added.
- Capture closes the result dialog and waits for dialog/backdrop removal **before seeking** the actual Player. Offline success/refusal ordering tests pass.
- Authority, snapshot/media digests, immutable revision closure, official Runtime client, exact 77-file Composition manifest, six peer files per consumer, browser byte pins and finally-postflight remain checked. Runtime and browser fixtures retain flock/QUIET boundaries. No threshold change, skip, expected-failure marker or new launch permission was introduced.
- Collection only registers cases. Both original and native1920 discovery passed with **all child-process launch and socket operations forbidden**. No setup/build, Runtime, pack host or browser was started during discovery.
- Pack-host adapter requires the existing helper in a frozen absolute Agent checkout and has no helper fallback. Credential-bearing stderr is drained, not retained; malformed protocol contents are replaced with generic errors. Download observation retains selected public headers/identity/bytes, never authorization or private location paths.
- Narrow diagnostic qualification retains raw errors; source-media failures, incomplete result proof, ambiguous requests, auth/catalog/admission failures and later media errors remain failures. New direct managed-fetch coverage retains full-transfer requirements.

## Independent commands and results

Working directory: `/home/user/work/wt/app-m3-viewing-main-parity-handoff-review`, with the exact patch temporarily applied to current 7bb. `node` was `/opt/node22/bin/node` **v22.22.0**; this is bounded offline/handler evidence, not the actual gate's required Node 20.19.4 environment. Shared dependencies were read-only; no installs or shared cache writes were requested.

Define:

```sh
W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m3-viewing-main-parity-handoff-review
```

1. Offline test files:

```sh
NODE_OPTIONS="--require=$W/offline-only.cjs" TSX_DISABLE_CACHE=1 node --import tsx --test --test-concurrency=1 tests/e2e/timeline/viewing-parity/*.test.ts
```

**PASS: 11/11 files, 0 failures, 0 skipped, 12.42 s.** Includes synthetic fixture video generation/native PNG/lossless decode, strict comparators, authority, diagnostics, transfer, source guards and close-before-seek unit coverage; no product render or browser. Log: `offline-tests-verified.log`.

2. Current handler/CORS neighbors:

```sh
NODE_OPTIONS="--require=$W/offline-only.cjs --require=$W/vitest-runner-compat.cjs" node node_modules/vitest/vitest.mjs run --no-cache --configLoader=runner --maxWorkers=1 --no-file-parallelism --config config/testing/vitest.config.ts src/tools/video-editor/components/TimelineRenderControls.test.tsx src/tools/video-editor/hooks/useRenderState.test.tsx src/shared/lib/media/mediaCrossOrigin.test.ts
```

**PASS: 3 files, 103 tests, 7.75 s.** Socket guard remained enabled. Private compatibility preload supplies the existing config's `__dirname` for runner loading; both config/testing and config/vite use it solely to resolve `../..` to this same project root. Candidate/config source was not edited. Log: `render-handler-tests-verified.log`.

3. Discovery only (each command):

```sh
REVIEW_COLLECTION=1 NODE_OPTIONS="--require=$W/offline-only.cjs" node node_modules/@playwright/test/cli.js test --list --config playwright.viewing-parity.config.ts
REVIEW_COLLECTION=1 NODE_OPTIONS="--require=$W/offline-only.cjs" node node_modules/@playwright/test/cli.js test --list --config playwright.viewing-parity.normal-profile-native1920.config.ts
```

**PASS: exactly four cases each; no child process or socket permitted.** Logs: `discovery-original.log`, `discovery-native1920.log`.

4. Targeted lint:

```sh
node node_modules/eslint/bin/eslint.js tests/e2e/local/support/harness.ts tests/e2e/timeline/viewing-parity/*.ts tests/e2e/timeline/player-export*spec.ts playwright.viewing-parity*.ts --report-unused-disable-directives --max-warnings 0 --no-cache
```

**PASS: exit 0, no warnings/errors.** Log: `eslint.log`.

5. `git diff --check`: **PASS**. Exact artifact comparison, current blob comparison and type-erasure comparison: **PASS**, as above; `source-proof.json` and `transpile-proof.json` retain results.

Review-run setup failures were resolved without changing candidate files: initial guard blocked esbuild and Vitest fork helpers; wrapping execFile initially lost its promisify contract (9/11 files passed until corrected); runner loading exposed the legacy config's undefined `__dirname`. Corrected private guard/preload produced the passing runs above. A Node spawnSync Git read also returned sandbox EPERM; Python Git reads followed by in-process transpilation completed the erasure proof. Earlier failed attempt logs remain in the worker directory; they are not claimed as candidate regressions or passing evidence.

## Limits, disposition and next steps

Viewing's earlier 82 render tests, 11 offline files, targeted tsc, ESLint and discovery were read as prior evidence only. The passes above are this worker's independent evidence on the patch over current 7bb. No isolated tsc or project tsc was run; erased annotations and focused lint/tests were sufficient for this bounded review.

No full suite, central test request, localhost/live socket, actual four-case execution, browser, build/install, real Runtime/pack host, output render, pixel/audio parity or owner-film validation was performed. Source tuple and deployed dependency-graph qualification remain pending; the synthetic graph tests do not certify the installed graph. Fresh grant remains a manager launch prerequisite and was not supplied or inferred.

All temporary candidate files were removed by reversing the exact patch after testing. Final worker worktree is clean (`git status --short` empty; `git diff --exit-code` exit 0); no source changes, build output, KEEP marker or merge request remains. Reports and private review helpers/logs are confined to the requested shared paths.

Recommended next step: App manager may submit the exact reviewed test-only branch through the normal merge queue, verify CORS is retained in the resulting tree, and keep the actual four-case launch held until the final safe tuple/graph and fresh grant are ready. No settled decision was changed; no blocker remains for this review task.
