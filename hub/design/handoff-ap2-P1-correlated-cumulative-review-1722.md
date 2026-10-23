# Handoff — ap2-P1-correlated-cumulative-review-1722

**FAIL.** Cumulative review of `4578e756b1ca689266f526c14d5adb59409cae5a` against `4c4c9c77c96fab70c4efef09db9a3bc456b0d803` found two blockers:

1. The full second-case failure packet still uses generic `redactDiagnosticValue` for `before.head` (`three-products.p1-chain.spec.ts:913`) and `runtimeHistory.head` (`:925`), and emits `originalClip.asset` directly (`:916`). That is not the required strict allowlist and can preserve `body`/`principal` keys or unsafe asset strings.
2. New page event callbacks at `:77-119` are not wholly wrapped against synchronous callback throws; the afterEach catch does not cover those listeners. This violates the mandatory no-throw/every-async-event guard.

Fresh approved Node 20.19.4 evidence passed: pure diagnostics 8/8, Root/App/Node tsc, scoped ESLint, exact Playwright list of 2, cumulative diff check, three-path scope, suffix SHA `582dc8…`, and Composition artifact SHA `819acf…`. Actual mounted Runtime capture/refusal remains UNKNOWN; no source-only GO is claimed.

This is the second Luna FAIL after independent `1708`; route to manager Sol HARD. Full details: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-P1-correlated-cumulative-review-1722/report.md`.
