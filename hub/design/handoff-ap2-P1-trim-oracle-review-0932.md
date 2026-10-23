# P1 trim previous-value oracle — independent review handoff

Status: **PASS**. The `tl/ap2-P1-trim-previous-oracle-0928` change is a truthful, minimal test-only correction and does not weaken P1.

The branch is based on `94b19e363047c1446608ff42ee11b0f34c906c69`. Its only changed path is `tests/e2e/local/three-products.p1-chain.spec.ts`, with exactly one expression changed at line 431: `before.value` from `SPLIT_AT` (`2`) to explicit source start `0`.

Parent/current file SHA-256: `d72798b2301973bfdabcf3b07c2746896e9ec5cd6188bebeda53733c070647a8` / `06104227304e7bab77e8f3f2de131ef26a949db437d02c2b2d7e20a25c057518`.

Parent/current file blobs: `f8f86de446538d1bcf07774564256ecabefc7026` / `6d428522d630fb30115707d6f364b9bd28d23e51`.

Parent/current trees: `c3752a0ff4978f400feb22e45f65b976188c7807` / `0ce82a6ab7733b9275311ee014527b628e30bdc0`.

The seed authors `from: 0`; the accepted split's unchanged full-clip equality preserves that source start while placing the right clip at `at: 2`. The Source In trim to `3` therefore guards previous `0`. The old `SPLIT_AT` oracle confused placement with source and contradicted the unchanged positive split assertion. The corrected `0` is an observed-boundary guard, not a waiver. All other original assertions—including raw/new-ID/order, opaque/null/absence, reads, accepted/merged/refused, Agent, lost ACK, restart/rollback, digest, and history coverage—remain unchanged.

Checks passed: original P1 Playwright `--list` selected exactly 2 tests; scoped ESLint; root/App/Node TypeScript checks (App within 180 seconds); `git diff --check`; normal Runtime/Agent lock and clean-pin checks; private exact Composition graph (`819acf6b…`, 80 files, v0.0.14); and normalized one-expression/no-outside-blob controls.

No browser/service/HTTP/socket/build/full-suite/original-chain execution was performed. This is not an original P1 behavioral pass or H3 go decision. Recommended next step: merge-review the test-only delta, then the manager owns one original chain execution after the current test-only port; preserve the remaining original assertions and the settled owner/OPS boundaries.
