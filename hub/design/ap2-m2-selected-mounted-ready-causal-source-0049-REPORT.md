# AP2 M2 selected mounted-readiness causal source

## Result

Repaired the first selected-gate failure in the App fixture only:

- `tests/e2e/local/support/app.ts:74` keeps the real
  `[data-testid="runtime-connection-status"]` / `data-state="connected"`
  assertion and gives it the existing 20-second cold-mount allowance.
- No selector, assertion expectation, DOM element, transport mock, route,
  bootstrap product code, schema, pin, credential, or Runtime source changed.
- The approved selected seed-order/admission fix `24165cb37` remains intact.

The prior selected worker report was reconstructed from its worker-local
`report.md` and central gate evidence because the shared literal
`design/WORKER-REPORT.md` had been overwritten by the Main95 worker. It is not
used as selected evidence.

## Causal evidence

The one authorized selected gate was:

`ap2-m2-selected-seed-approved-real-gate-0040-ap2-m2-selected-real-p1-history-fixture-fix-1021004112-13123`

It used App tree `8bbb519eb4de1a9ea59ef80c6fc7f8190e49e628` and failed before
P1 at `three-products.selected-param-dev.spec.ts:45` because the status
locator was absent. Hosted build and test collection passed; no P1/P2 history,
removal, refusal, draft, retry, restart, reload, undo, or zero-legacy claim
was made.

The retained sanitized trace shows `/tools/video-editor` returned HTTP 200 and
loaded the real `src/app/main.tsx` and `src/app/bootstrap.tsx`. At the failed
assertion the page still had the boot shell and an empty `#root`; the cold Vite
module graph was still loading. This distinguishes a cold bootstrap/mount
timeout from a stale selector or refused route. Current source confirms the
status is mounted by `RuntimeDocumentBoundary` through the real
`RuntimeConnectionGate` and `RuntimeConnectionPill`; the connected branch
still emits the status element.

The selected compatibility tuple remains the reviewed one:

- App seed source: `24165cb37b46a5c1a6676bd646d01f18e9552ee9`
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`
- Composition public13: archive
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`,
  77 regular files; Runtime artifact guard is the reviewed all75 set.

## Changed export and live callers

`expectConnected` remains the only changed export. Its live callers are the
existing local journey specs:

- `tests/e2e/local/direct-journey.spec.ts`
- `tests/e2e/local/three-products.selected-param-dev.spec.ts`
- `tests/e2e/local/three-products.spec.ts`
- `tests/e2e/local/shot-name-command.spec.ts`
- `tests/e2e/local/track-label-command.spec.ts`
- `tests/e2e/local/parent-trim-command.spec.ts`
- `tests/e2e/local/clip-delete-command.spec.ts`

All continue to assert the same real status selector and connected state.

## Checks

Passed:

- `git diff --check`
- `npx eslint --no-cache --max-warnings 0 tests/e2e/local/support/app.ts`
- `npx playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list` — exactly one test collected

Not run: the central real gate, browser execution, localhost/live sockets, or
full suite. The selected P1/P2 journey remains unverified until the
orchestrator reviews this source packet and authorizes the next central run.

## Next step

After source review, run the one selected central gate against this committed
fixture correction and the exact Agent8130/Runtime2c4/public13 tuple. Do not
change the selected assertions or custody/admission path.
