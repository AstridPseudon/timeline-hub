# D127d bounded verification recipe

Status: `SOURCE_PREPARED` / `NOTRUN`.

The later candidate uses the existing D66/D73 exact-checkout and source-
preflight machinery with the selector `p2-element-verify`. Its suite body is
the existing single mounted element test selected by the unchanged grep:

```text
tests/e2e/local/three-products.p2-elements-assets.spec.ts
P2 mounted element edit: real catalog apply, exact params patch, reload and guarded Undo$
```

The registered service recipe carries the four exact source pins, Node
20.19.4, the existing `--import tsx` launcher, and
`D66_ELEMENT_VERIFICATION_ONLY='1'`. Source helper identity/hash validation
and all existing source guards remain required. The normal launch receives
private `D66_RUNTIME_LOG_DIR` stream retention, while `harness.ts` creates the
private stream directory without allocating a phase-capture sink.

The actual Runtime child receives a fresh runtime environment overlaid with
explicitly undefined measurement variables. It therefore has no capture
activation, sink, helper or helper hash, watchdog, phase ordinal, verification
selector, or `scripts/testing` bootstrap path. Existing teardown still writes
ordinary child stdout/stderr privately.

The route is intentionally bounded to the one element selector. Any attempt
to pair the verification descriptor with another suite is refused, and the
launcher requires the explicit route/arm agreement. The default `p2-element`
route remains the historical measurement-enabled route for existing controls.

Do not execute this recipe until Runtime provides the qualified COST-CANDIDATE
source/review/normal immutable receipt. At that point the manager may perform
the one separate source preflight and one normal body, retaining the original
five-second assertion, canonical/history/readback/reload/guarded-Undo checks,
and zero legacy-route assertions. No other body, profile, service, browser,
or full tour is included.
