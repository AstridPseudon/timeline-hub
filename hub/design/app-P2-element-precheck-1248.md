Implemented the scoped P2 element updates.

- Added bounded real-panel Apply states: `idle`, `applying`, `applied`, `refused`, `unknown`, with fail-closed projection and no raw text/data/URL output.
- Added diagnostic controls for positive, negative, pending, abort, late-response, teardown, and malformed UI states.
- Corrected only element case receipt joins: authoritative `receipt_id` is used for params Undo/publication; request keys remain idempotency keys.
- Modified only:
  - [p2-element-diagnostic.ts](/home/user/work/wt/app-P2-element-precheck-1248/tests/e2e/local/support/p2-element-diagnostic.ts)
  - [p2-element-diagnostic.test.ts](/home/user/work/wt/app-P2-element-precheck-1248/tests/e2e/local/support/p2-element-diagnostic.test.ts)
  - [three-products.p2-elements-assets.spec.ts](/home/user/work/wt/app-P2-element-precheck-1248/tests/e2e/local/three-products.p2-elements-assets.spec.ts)

Validation:

- Node diagnostic suite: 27 passed.
- Mounted Vitest neighbors: 97 passed.
- Serial locked TypeScript checks: root/app/node passed.
- Scoped ESLint: passed.
- `git diff --check`: passed.
- Playwright list-only: 23 tests collected; no browser execution.
- No full, original, service, or product-latency tests run.

Protected hashes:

- Tour unchanged: `2e8fc72b…` → `2e8fc72b…`
- Popup unchanged: `05370adc…` → `05370adc…`
- Original unchanged: `95d9a3e7…` → `95d9a3e7…`
- Elements changed only for receipt binding: `5f82ec90…` → `a819d3c2…`

Behavior ledger row: `P2/D55b-element | diagnostic + element case 377–467 | pending UI was previously unknown; request key was used as publication identity | bounded Apply enum + authoritative receipt joins | app | P2 | branch-only, pending independent review | 27 diagnostics, 97 mounted neighbors, types/lint/list checks passed`.

Independent security/protected review remains required before merge. Commit message and `DONE` marker were created; harness will commit the branch.