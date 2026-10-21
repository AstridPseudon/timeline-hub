# Selected 18585 startup phase accounting

## Verdict

No existing retained evidence isolates the selected18585 startup boundary to
storage migration, one of the three `Promise.all` imports, workspace identity,
or the first React commit. The smallest justified next step is a runner-only
CDP capture attached to the existing selected DEV run. I did not run the
selected success case, change the product, change the route, add a ready flag,
increase the timeout, or replay the failing case.

The first unknown remains the sub-phase inside `src/app/main.tsx:102-124`:

```text
startApp
  await migrateAstridBrowserStorage()                         main.tsx:103
  await Promise.all([bootstrap, extension runtime, client])   main.tsx:112-120
  initializeVideoEditorExtensionRuntime()                     main.tsx:121
  await initializeWorkspaceRuntimeIdentity()                  main.tsx:122
  renderApp(rootElement)                                      main.tsx:123
```

The retained 18585 run stopped at the unchanged `#root > *` assertion with
the original 20,000 ms budget, on `/tools/video-editor`. Its final snapshot
eventually contains the real App shell (`Loading project`, empty `main`), so
the selector is not disproven. It does not provide the exact promise
settlement or React commit time.

## Source identity

The assigned App worktree is currently:

```text
HEAD bc6f9dd39c7e5154ddf075cb87b7202cf5702e65
main.tsx       sha256 227be15157c108bd504b69dd472b4ef87e6efa56b623cf30bd40a2a8b2923208
bootstrap.tsx  sha256 44419f1be81d163b5d216cc8283852ea3dd275b827ddf0308219bb9718553cf6
runtime client sha256 8c46cbd0ead2146ffa01118e9bc51f0730952b14495cdff6ce5439accb0859ee
Vite config    sha256 5f26c8fa9beae5691c7c94ae11d008eb6c548eb28aaa2b66887b7512efe6c70d
```

The retained 18585 failure was from App tree
`87d2350417a876e14b81c58b64da29f1a30b35b6`; it must not be silently
represented as the current tree. The preserved trace is:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/trace.zip
```

## What existing evidence can and cannot say

| Candidate | Existing seam/evidence | Result |
| --- | --- | --- |
| Storage migration | `main.tsx:103-107` is the only product boundary; `main.bootstrap-order.test.tsx:88-118` can plant migration failure/retry. | The retained browser trace has no migration completion event. Whether the successful migration promise was still pending at the cutoff is UNKNOWN. |
| `Promise.all` import evaluation | `main.tsx:112-120`; the trace has Vite resource snapshots and request timing for source modules. | Network completion is not JavaScript evaluation or Promise settlement. The trace cannot distinguish `bootstrap`, extension-runtime, or Runtime-client evaluation. UNKNOWN. |
| Workspace identity | `main.tsx:122`; `client.ts` loads the workspace config with the supplied fallback. The trace records `/runtime-config/v1/workspace.json` 404 followed by Runtime health 200. | The 404 is browser-frame traffic and is non-causal evidence: the loader falls back, and later health succeeds. Identity completion at the mount cutoff is still UNKNOWN. |
| First React commit | `bootstrap.tsx:147-155` calls `createRoot(...).render(...)`; Playwright snapshots show the eventual shell. | A snapshot is not a commit timestamp. The first child can be observed runner-side with a `MutationObserver`; current evidence does not record it. UNKNOWN. |
| Vite stderr | `spawnGroup()` in `tests/e2e/local/support/harness.ts:103-117` buffers child stderr; `startSelectedParamDevServer()` starts the existing Vite command at `:708-736`. | Warnings are retained in the central runner log, but the selected spec has no read-only accessor/attachment for the live tail. No module failure/error was captured. |

The retained trace has no `Debugger.scriptParsed`, `Debugger.paused`, or
source-evaluation records. Its network/resource snapshots therefore cannot
answer the import-evaluation question. `config/vite/vite.config.ts:173-176`
enables sourcemaps for a production build, but this selected case is the Vite
DEV server; a sourcemap setting does not add evaluation timing to the trace.

## Smallest runner-only capture proposal

This is a proposal for HOME review; it is intentionally not applied because
the selected spec and support harness are shared App files. It keeps the
existing `page.goto(`${harness.devOrigin}/tools/video-editor`)`, its route,
startup order, selector, and 20-second expectation unchanged.

1. Before the existing `page.goto`, create
   `const cdp = await page.context().newCDPSession(page)` and enable
   `Debugger`, `Runtime`, and `Log`.
2. Install `Debugger.setBreakpointByUrl`/`urlRegex` breakpoints before
   navigation. Use the current source URLs and zero-based CDP line numbers:

   ```text
   main.tsx:103,104,116,120,121,122,123 -> 102,103,115,119,120,121,122
   bootstrap.tsx:1 (root module evaluation)
   initializeVideoEditorExtensionRuntime.ts:1 (root module evaluation)
   client.ts:1 (root module evaluation)
   ```

   The `main.tsx` hits classify the migration call/return, the `Promise.all`
   continuation, extension-runtime call, identity call/return, and render
   call. The three root-module hits classify which dynamic import begins
   evaluation; they do not claim that its complete static dependency graph is
   evaluated until the `main.tsx:120` continuation is observed.
3. On each `Debugger.paused`, append only
   `{phase, url, line, performanceNow}` from the top call frame and resume
   immediately. On a timeout/failure, attach the bounded JSON through the
   existing Playwright `testInfo` channel. Do not pause for arbitrary
   inspection, rewrite source, or alter application globals.
4. Install a runner-side `MutationObserver` with `page.addInitScript` before
   the same navigation. Observe the document until `#root` exists and record
   the first transition to a non-empty `#root` as `react-first-child`. This is
   test-runner observation only; it does not add a product ready flag or touch
   React bootstrap code.
5. Add a read-only bounded Vite-stderr tail to the same diagnostic attachment.
   The smallest support seam is an accessor over the already-buffered
   `Managed.stderr` in `DirectHarness`; it must not change the child command,
   start order, or output policy. If HOME declines that shared accessor, omit
   stderr from the capture and state that limitation; do not invent a second
   Vite process.

The resulting ordered event set is reviewable without guessing:

```text
migration-call -> migration-return
import-root-hit[bootstrap|extension|client] ...
promise-all-return -> extension-call -> identity-call -> identity-return
render-call -> react-first-child
```

The first missing event at the original cutoff is the first unknown. A missing
`promise-all-return` with all three root-module hits means static import
evaluation or a transitive module side effect remains unresolved; a missing
root-module hit identifies the import not yet evaluated; an identity call with
no return identifies workspace identity; a render call with no
`react-first-child` moves the boundary to React scheduling/commit. Migration
is isolated by the two main breakpoints rather than by network inference.

## Offline proof of the phase seam

The existing unit seam already proves that an ephemeral delayed startup phase
is observable without a browser or localhost. In
`src/app/main.bootstrap-order.test.tsx:52-86`, the test plants a promise that
does not resolve in `initializeWorkspaceRuntimeIdentity`, observes
`['extension-runtime-install', 'workspace-runtime-identity']`, asserts that
`renderApp` has not run, then resolves the promise and observes `render-app`.
This is the same boundary accounting needed by the proposed CDP event reducer;
it does not prove the selected case's responsible dependency.

## Commands and results

Read-only/source and retained-evidence inspection:

```text
sed/nl/rg over PLAN.md, the two required diagnosis/owner reports, startup sources,
selected spec, harness, Vite config, and retained trace
PASS: source locations, route, selector, timeout, stderr and trace limitations recorded above
```

Targeted existing startup tests:

```text
npx vitest run --config config/testing/vitest.config.ts --no-cache \
  src/app/main.bootstrap-order.test.tsx src/app/main.runtime-origin.test.tsx
PASS — 2 files, 6 tests; duration 2.02s
```

An initial attempt with `--configLoader runner` was not used as evidence:

```text
npx vitest run --config config/testing/vitest.config.ts --no-cache --configLoader runner ...
NOT EVIDENCE — config startup failed because this repo's Vite config uses __dirname
```

No browser, localhost, selected actual, replay, full suite, timeout increase,
or product/bootstrap/route/harness/spec edit was performed by this worker.
