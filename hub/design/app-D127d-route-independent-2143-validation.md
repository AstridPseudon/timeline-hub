# D127d independent static validation

## Result

`FINITE_UNAPPLIED`; route authorization `FAIL_FOR_NO_HOOKS_AUTHORIZATION`;
scope and custody `PASS`; acceptance `NOTRUN`; Runtime cost candidate
`PENDING`.

## Read-only checks run

- `git rev-parse HEAD` and `git rev-parse HEAD^{tree}` matched the recorded
  App tuple: `b5c9eadfa1950f46feac50d7d6a89c47f27f4881` /
  `8e10af0976b012205f27a18a432c750a27de0725`.
- `git status --short` and `git diff --stat` showed a clean App worktree.
- SHA-256 and Git blob checks matched the four prior D127d App source
  identities for the launcher, launcher test, mounted body, and helper guard.
- SHA-256 and Git blob identities were recorded for the App caller/outbox,
  generated Runtime DTO/client, operation host, Runtime helper, C0 contract,
  and timeline commit schema in `source-manifest.json`.
- `node --check scripts/testing/d66-plain-stack.mjs` passed.
- `node --check scripts/testing/d66-plain-stack.test.mjs` passed.
- Python `ast.parse` passed for the App `scripts/testing/sitecustomize.py` and
  the read-only Runtime helper.
- Python JSON parsing passed for all prior JSON evidence inputs and the new
  `review.json`/`source-manifest.json` after creation.
- Static source/AST inspection confirmed the production caller is
  `useTimelineSave` -> `createLocalSaveSession` -> durable outbox -> Runtime
  `commitTimeline`; the mounted P2 element body asserts v2 request shape,
  canonical readback, reload, guarded Undo, and no legacy route traffic.

## Findings recorded

- The prior D127d finding that `p2-element` has no supported normal no-hooks
  arm is independently confirmed.
- The helper activation mechanism is explicit and source-pinned: the harness
  passes a capture sink during authoring, `sitecustomize` sees the explicit
  capture environment, and the helper starts tracing/sampling/cProfile/
  watchdog behavior.
- The scope distinction is corrected: private ordinary Runtime stdout/stderr
  retention is not itself measurement. Current harness coupling means the
  future candidate needs a bounded `startRuntime` seam that omits only the
  capture sink/environment while retaining stream writes.
- C0 sections 1-5 and 7 are statically consistent at the App boundary for
  request construction, doc.patch intent preservation, outbox conflict/retry
  custody, reply decoding, inverse Undo, and history consumption. Runtime
  authority and behavioral acceptance remain unverified.

## Deliberately not run

No product tests, Vitest, e2e journey, typecheck, lint, preflight, checkout,
install, bootstrap, service, registration, submission, browser, localhost,
socket, Runtime request, body, profiler, sampler, diagnostic capture, full
suite, or repeated product test was run. No source or test was edited.
