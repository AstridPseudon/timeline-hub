# Handoff: ap2-P1-diagnostics-return-1049

The P1 failure-only diagnostics now use `tests/e2e/local/p1-diagnostic-safety.ts` for bounded UTF-8 formatting, quoted/nested credential redaction, and a guarded logger. `three-products.p1-chain.spec.ts` uses it for structural, open-chain, and second-case failure output; both diagnostic catch paths preserve and rethrow the original assertion. Fake-only coverage is in `p1-diagnostic-safety.test.ts`.

Targeted fake tests, lint, diagnostics-module typecheck, and `git diff --check` pass. Browser/full suites were intentionally not run. A broad direct TypeScript command still reports existing alias/import/name issues outside this change; see the worker report for exact details.
