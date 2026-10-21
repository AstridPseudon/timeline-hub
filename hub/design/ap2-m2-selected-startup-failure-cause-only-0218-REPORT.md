# AP2 M2 selected startup failure diagnosis

## Result

The selected20336 failure is not a wrong combobox selector, an auth refusal, or
missing pinned fixture data. The direct DEV page reached the intended URL, but
the App had not mounted before `openSeededTimeline` checked the combobox.

The demonstrated root cause is a cold DEV startup module graph behind the App's
pre-mount gate:

1. The selected test calls `page.goto(`${harness.devOrigin}/tools/video-editor`)`.
   The retained trace URL is exactly `http://127.0.0.1:42075/tools/video-editor`.
2. The document returned 200 and loaded the real `src/app/main.tsx`.
3. The `main.tsx` request took about 3.33 seconds to complete. It then loaded
   `bootstrap.tsx`, the extension runtime, and the Runtime client, followed by
   the eager App graph.
4. At the failed assertion, the DOM still contained the boot layer and an
   empty `#root`; it contained no Router/Layout/editor/provider DOM and no
   combobox of any name.
5. The trace has only Vite connecting/connected console messages, no page
   error, no failed request, and no Runtime or bridge request. The module
   requests for React, `routes.tsx`, providers, and related source files were
   still pending when the five-second `openSeededTimeline` assertion expired.

The source explains the blank DOM: `src/app/main.tsx` calls `renderApp` only
after the startup imports and `initializeWorkspaceRuntimeIdentity()` resolve.
`void main()` has no rejection handler. Therefore a still-transforming DEV
graph leaves the boot shell and empty root, without reaching route, auth, or
fixture readiness.

## Route, config, and data boundary

`tests/e2e/local/support/harness.ts:startSelectedParamDevServer()` starts Vite
on a fresh loopback DEV port and the test navigates to that `devOrigin`; this
is not the hosted `dist` URL. `config/vite/vite.config.ts` uses
`optimizeDeps.entries: ["index.html"]`, has no `cacheDir` setting, and the
central wrapper's `VITE_CACHE_DIR` is not read by this App config. The trace
does not prove shared-cache contamination or identify a particular failed
dependency, so neither is claimed as the cause.

The trace contains no `/api/runtime`, `/v1`, bridge health, project, timeline,
or element-admission request before the failure. The seeded project was
created by the harness, but the browser never reached the code that reads it.
Thus auth, Runtime readiness, selected P1/P2 pins, and data availability are
not implicated by this result.

## Smallest source-owned correction proposal

Keep the selected assertions and all P1/P2/refusal/draft/retry/reload/undo
behavior unchanged. Reduce the pre-mount DEV graph in `src/app/routes.tsx`:
retain the selected `VideoEditorPage` path, but lazy-load the five unrelated
eager main-tool pages and render them through the existing `Suspense`
`LazyLoadingFallback`. This is the smallest source-owned direction supported
by the trace: `routes.tsx` currently eagerly imports those pages before any
route can mount, while the selected URL needs only the video-editor route.

This is a proposal, not an applied fix or a claimed qualification. The trace
does not justify changing the selector, adding waits/retries/navigation, or
changing the test to accept an unmounted route. If the route graph is later
shown to reject rather than merely remain pending, the next source correction
must use the exact Vite error; no specific missing module is demonstrated by
20336.

## Verification

Central retained result inspected:

- `ap2-m2-selected-corrected-single-gate-0212-ap2-m2-selected-real-p1-history-fixture-fix-1021021417-20336`
  — exit 1; one selected test; failure at `support/app.ts:81`; hosted build
  passed before the DEV browser phase.
- Retained trace:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/trace.zip`
- Retained driver log:
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/driver.stderr`

No local tests, browser, socket, full suite, gate, install, or retry were run
in this diagnosis. The worktree remains source-clean; no product or test file
was edited. Read-only checks `git status --short` (clean) and `git diff --check`
(passed) completed.

## Decisions and blockers

- Preserved every original P1/P2, refusal, draft, lost-ACK retry, reload, and
  undo assertion.
- Did not convert the selector assertion, add a timeout/retry, or infer a
  Runtime/auth/fixture defect from a page that never mounted.
- The exact Vite child-server error is not retained, so a source correction
  naming one specific dependency is blocked. The demonstrated evidence is
  limited to cold DEV graph completion not occurring before the existing
  assertion.

