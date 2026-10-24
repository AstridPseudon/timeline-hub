# P2-11933 verdict report

Verdict: **NO-GO / FAIL** for SAME historical signal `11933`.

- Source: App `d6ed8cbda122d810d5836ebfce3c56c10e76e9b4`
- Tree: `542b772e6deed676b917f857708445b7d37a5aa8`
- Worktree: clean; no product, test, registry, or source edits.

Actual retained run:

- `wait-test app-P2-final-pure-integrated-1036-full-e2e-three-products-1024115551-11933`
- Exit 1, 469s: **0 passed, 3 failed, 5 not run**
- Native seed/history, hosted build, selector collection, and mounted readiness passed.
- Failures:
  1. Element Apply line 391: status node absent after 5s. H36 observed scoped commit request/key and `pending`; response, failure, abort, receipt, and server outcome remain UNKNOWN.
  2. Popup line 464: expected track `V2`, received `plate`; failed before accepted/reload/undo checks.
  3. Parent line 299: HTTP 200 accepted/merged-shaped response, but `receipt_id` differed from POST key (`txn-*` vs UUID key).

The five unrun cases were registerAsset, automatic child placement, popup SWAP, and both transition-none cases. No historical cause or GO was inferred.

Evidence/custody:

- H36 original, retained copy, and attachment are byte-identical: SHA-256 `08509524d5fd04f181b3fac8d0cdd211a32e2f4a107c4e78807ae4713e8533a4`.
- D21 artifacts were retained at the recorded Playwright output and attachment paths; source modes distinguish observed, declared, and unknown facts.
- Actual daemon/provider source identity, compiled runtime base, and full snapshot SHA/parents are unavailable; no Git pin was promoted to actual daemon custody.
- C0 request/reply preservation remains source-qualified through App → outbox/provider → generated Runtime client, including idempotency, canonical document/digest, IDs, steps/dependencies, merge mode, publisher, and receipt guards.

Tests:

- `node --import tsx --test tests/e2e/local/support/p2-element-diagnostic.test.ts tests/e2e/local/d21-environment.test.ts` — **2 passed**
- Retained pure qualification on the exact d6ed source: 695/695, 67/67, 30/30, 11/11; TypeScript, lint, Python compile, and diff checks passed.
- `git diff --check` — passed.

Commit message supplied at the required path; `DONE` marker created. Recommended next step: resolve the three strict boundaries, then run a fresh full P2 tuple; this historical signal must remain NO-GO.