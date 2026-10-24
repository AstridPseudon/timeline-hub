## D66 report

Implemented automatic exact-checkout selection in `scripts/testing/d66-plain-stack.mjs`.

- Agent route: `/home/user/work/wt/agt-pin-<current-head8>`
- Runtime route: `/home/user/work/wt/rt-pin-<current-head8>`
- Explicit overrides remain supported.
- Missing/stale routes report the exact current HEAD and required checkout path.
- Selected HEADs remain captured and propagated to Runtime, Agent, collection, manifest, and import readback.

Source state:

- Agent normal/route: `ef036398…`, tree `1be86f3…`; route `/home/user/work/wt/agt-pin-ef036398`, clean detached.
- Runtime normal: `5c1a03f…`, tree `dfe90e5…`.
- Queued Runtime route: `/home/user/work/wt/rt-pin-bc227de0`, `bc227de0…`, tree `1d410a67…`, clean detached but stale against the current normal home.
- App: `76914e74…`, tree `009d7949…`.
- Composition: `635f4de0…`, tree `5ab5191a…`.

Checks passed:

- Node 20 syntax checks.
- Focused harness tests: 5 passed.
- Scoped ESLint.
- `git diff --check`.

Negative `--collect` checks correctly refused:

- Empty inherited source inputs: requested `rt-pin-5c1a03f1`.
- Explicit stale Runtime route: rejected `bc227de0…` and named current `5c1a03f…`.

A positive `--collect` is blocked until the exact detached Runtime checkout for current HEAD `5c1a03f…` is provisioned. No browser, service launch, original journey, or full suite was run.