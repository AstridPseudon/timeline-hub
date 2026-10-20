# App native-None current registered executor

Date: 2026-10-20

## Central result

- TestID: `app-m2-none-current-registered-executor-e2e-native-none-current-root-a835-agent8130-runtime2c4-e2e-integration-1020152825-10578`
- Suite: `e2e-native-none-current-root-a835-agent8130-runtime2c4-e2e-integration`
- Result: **FAIL / product blocked** — 1 passed, 1 failed; exit 1; 274s total.
- Central result summary: `counts: 1 failed 1 passed (2.6m)`.

## Exact source tuple

- App declared source: commit `d36fe2e9d807503b32f61d22c15a9f138da6d48c`, tree `a835e61ead2794456615e5161d7d683136fcb9da`.
- Central snapshot preserved the exact App tree; its materialized App HEAD was synthetic (`a04753aa7b4ea0843fadfed31a651c98db193a03`), so the strict launcher validates the declared full-40 SHA environment and exact tree without requiring synthetic snapshot HEAD equality.
- Agent keeper: `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime and producer: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- public12 Composition archive: SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
- Tracked public source attribution: `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`.

## Preflight and build evidence

The strict launcher validated all full-40 source environment values before build, Agent8130/Runtime2c4 checkouts and clean status, Runtime all 75 manifest artifacts, public12 all 77 archive/package files, React/Remotion peers, vendor locks/source checks, exact two-test discovery, Chromium 141.0.7390.37 (SHA-256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`), short `TMPDIR=/tmp/tl-none-current-c1`, and unset `ASTRID_PUBLIC_CHECKOUT` / `ASTRID_APP_DIRECT_DIST`.

The fresh hosted build passed (`vite build`, 1m34s). Postflight passed: source checkouts, all75/all77 package bytes, peers, vendor source verification, and shared dependency caches were unchanged.

Discovery output selected exactly 2 real `M2 native None` tests in `three-products.spec.ts`.

## Case results

1. **Single: passed.** The central test completed raw transition absence, Runtime commit, reload, inverse, lost acknowledgement, Runtime restart, exact retry request/body/key/receipt, and zero legacy traffic assertions.
2. **Bulk: failed before commit.** After selecting the real `None` option, the transition combobox rendered `__none__` instead of `None` at `three-products.spec.ts:1385`. The test stopped before the bulk commit, so bulk raw absence, atomic commit, 409 draft retention, inverse, and zero-legacy assertions are unverified.

## Product cause and next step

`NO_TRANSITION` is the sentinel `__none__` in `clip-panel-primitives.tsx`. The single selector provides an explicit `SelectValue` child that renders `None`; the bulk selector at `BulkClipPanelBody.tsx:575` provides only `<SelectValue placeholder="None" />`, so Base UI exposes the selected sentinel text. The smallest product fix is to render the bulk selector's `NO_TRANSITION` value as visible `None` while retaining the command-backed clear path and all existing assertions. No product or test assertion was changed in this task.

No full suite, project TypeScript, install, framePCM, or additional browser run was performed after the product failure.
