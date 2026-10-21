# Selected 18585 startup-boundary diagnosis

## Verdict

Selected result 18585 remains **not qualified**. It failed at the unchanged
20-second `#root > *` assertion before any selected P1 edit. No live caller,
test, product source, route, timeout, or harness was changed.

The earlier report's claim that the workspace-config 404 caused the mount
failure is corrected. The 404 is real captured evidence, but it is not a
demonstrated cause.

## First browser boundary

The earliest unresolved browser-side boundary is the existing pre-render
startup chain in `src/app/main.tsx:102-124`:

1. `startApp()` awaits browser-storage migration at line 103.
2. Lines 112-120 await the `Promise.all` of `bootstrap`, the video-editor
   extension runtime, and the Runtime client modules.
3. Line 122 awaits `initializeWorkspaceRuntimeIdentity()`.
4. Line 123 calls `renderApp(rootElement)`.

The preserved trace proves that the chain had not produced a committed
`#root` child at the beginning of the assertion, and that the first committed
child was visible only at the end of the 20-second window. It does **not** show
which individual promise, module evaluation, or React scheduling phase was
still pending at the exact cutoff. That finer-grained dependency is **UNKNOWN**.

Captured timing:

- `test.trace`: navigation finished at `23389.671`; the mount expectation
  began at `23397.664` and ended at `43736.947` with the original 20,000 ms
  timeout.
- `0-trace.trace`: the post-navigation DOM snapshot at `23388.055` contains
  `<div id="root"></div>` with no child.
- The browser network trace shows the main module at monotonic time
  `18971.809` (HTTP 200, 4,299.688 ms), followed by the bootstrap/runtime
  module graph. The last recorded source-module traffic in that graph ends
  around `42534`, all with HTTP 200 responses.
- The captured `workspace.json` request starts at `42843.954` and returns 404
  at `42851.789`, before the 20-second assertion cutoff. This request therefore
  does not identify the unresolved dependency.
- The final Playwright DOM snapshot at `43728.503` contains a direct child of
  `#root`, with the App header and an empty `main`. The accessible DOM says
  `Select project` is `Loading project`; this is DOM evidence, not screenshot
  interpretation.

The selector is therefore not proven wrong. In the final captured DOM,
`#root > *` is the actual first App surface. No replacement selector is
justified and the test must not be edited in this diagnosis.

## Workspace-config wording correction

The captured browser request was:

```text
GET http://127.0.0.1:37831/runtime-config/v1/workspace.json
status 404
Referer: http://127.0.0.1:37831/tools/video-editor
Sec-Fetch-Dest: empty
server: AstridRuntime/0.1 Python/3.12.3
```

This is browser-frame traffic, not fixture/Node setup traffic. The source
contract makes it non-causal for this mount:

- `src/integrations/runtime/workspaceRuntimeConfig.ts:18-26` returns the
  supplied fallback whenever the response is non-OK.
- `src/integrations/runtime/client.ts:85-95` calls that loader for the
  same-origin page.
- `tests/e2e/local/support/harness.ts:744-746` supplies all three expected
  identity values used as the fallback.

The existing authoritative producer is preserved in
`scripts/runtime-discovery-proxy.mjs:79-105,404-416`: it reads the Runtime's
published discovery data and answers `workspace.json`; the Runtime publishes
`discovery.json`. This is also recorded in the HOME result
`peer-app-to-app2-20261021T0413-existing-workspace-producer-result.md`.
The selected DEV harness points its Vite target directly at the Runtime at
`tests/e2e/local/support/harness.ts:738`, which explains why this particular
captured request reached the Runtime. That observation does not authorize a
Vite/route/bootstrap refactor.

The same browser frame later reached:

```text
GET http://127.0.0.1:37831/api/astrid/v1/health
status 200
monotonic time 43087.109
Referer: http://127.0.0.1:37831/tools/video-editor
Sec-Fetch-Dest: empty
```

Thus the retained evidence shows a reachable Runtime after the 404. It does
not show a selected commit, handshake/admission journey, or any P1/P2 result;
those remain unverified because the test stopped at startup.

## Browser-frame versus fixture/Node traffic

The test-runner trace places fixture setup before page navigation:

- harness fixture: `3035.739`–`12198.124`;
- browser launch/context/page creation: through `12578.829`;
- selected seed fixture: `12579.227`–`17497.612`;
- page navigation: starts `18878.046`.

The `workspace.json` 404 and the later health 200 have a page referer and
`Sec-Fetch-Dest: empty` in `0-trace.network`; they are browser requests.
They must not be attributed to the Node fixture's direct Runtime calls.

## Stderr and error evidence

`driver.stderr` contains only the recorded Browserslist/PostCSS/Rollup
warnings and no browser exception, failed module response, or Runtime
transport error. The Playwright error context records the exact failure:

```text
expect(page.locator('#root > *').first()).toBeAttached({ timeout: 20000 })
Error: element(s) not found
```

The preserved page DOM at failure is the App shell with `Loading project` and
an empty `main`; it is consistent with startup not reaching the required
first committed frame within the original budget. It is not evidence that a
test-only selector or screenshot surface is wrong.

## Smallest justified next correction

No code correction is justified by this read-only diagnosis. Do not change the
workspace-config route, add a fallback response, increase the 20-second
budget, add a ready flag, navigate/recover around startup, or replace the
selector.

The smallest next investigation is source-level phase accounting around the
already-existing boundaries in `src/app/main.tsx:102-124` and
`src/app/bootstrap.tsx:147-155`, followed by one newly authorized actual only
after the responsible owner decides which existing startup work can be made
fast enough. Preserve the original startup positions and budget, and preserve
all P1/P2, draft/refusal, retry, reload, and undo assertions. The current
evidence does not support choosing a particular promise or a selector fix.

## Evidence paths

- Result summary/log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-selected-approved-real-scope-one-case-0342-ap2-m2-selected-real-p1-history-fixture-fix-1021034300-18585/summary` and `log.txt`.
- Preserved trace: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace/three-products.selected-pa-e0e73-fusal-retry-reload-and-undo/trace.zip`.
- Preserved DOM/error context: the same directory's `error-context.md`.
- Preserved Vite child stderr: the same worker's `central-trace/driver.stderr`.
- Earlier causal wording and correction: `design/ap2-m2-selected-0342-result-cut-or-cause-0344-REPORT.md` and `design/peer-app-to-app2-20261021T0413-existing-workspace-producer-result.md`.

## Commands and verification

This was a read-only diagnosis. I ran source/trace inspection commands using
`sed`, `nl`, `rg`, `unzip -p`, and a stdin-only Node JSON parser over the
preserved Playwright trace. No browser, localhost/socket, selected actual,
full suite, unchanged test replay, install, or build was run. No targeted test
result is claimed for this diagnosis.
