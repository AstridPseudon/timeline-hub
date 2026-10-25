## PASS — independent P2 popup traffic review

Reviewed `f5052b75d0` against parent `364f124b5c`. No repository source was authored during review.

The Runtime source independently confirms `POST .../inspect` is read-only: it requires `projects:read`, calls `inspect_timeline`, and reads immutable revision closure data without publication/history mutation. App canonical polling calls this exact endpoint with `{ limit: 1 }`.

Predicate coverage:

- Accepts only exact `POST /v1/projects/{project}/timelines/{timeline}/inspect` or mounted `/api/runtime/v1/.../inspect`.
- Rejects query/hash, trailing/sibling/encoded paths, wrong methods, broad prefixes, unknown routes, old save routes, and extra `/commit` routes.
- Requires all classified inspections to return HTTP 200.
- Preserves exact expected request-object equality, POST/`/commit` checks, media-import-only exclusion, canonical/digest/receipt/identity/history/reload/undo/raw-field assertions, and all waits/timeouts.
- The expected commit remains the sole actual film mutation; no synthetic request set was substituted.

Old/new witness: the pre-correction collector is genuinely RED with the seven observed inspect POSTs; the new exact classifier is GREEN. The dedicated adversarial probe also passed.

Checks:

- Node oracle: **3/3 passed**
- Old-RED/new-GREEN predicate probe: **passed**
- `tsc -p tsconfig.app.json --noEmit`: **passed**
- `tsc -p tsconfig.node.json --noEmit`: **passed**
- Scoped ESLint with `--max-warnings=0`: **passed**
- `git diff --check`: **passed**
- Worktree: clean

No browser/service/full suite was run. The retained first wire failed before reload/undo; no later credit is claimed.

Hashes:

- Popup spec: `d68b773a14eccb287fa907c1bde80fb6987c74839e3b869670555a5811534562` → `ab66f693430d62ec537f18d1d6aa7bc211bbc48d2b3fb555ef34dc9ec96a4dea`; final blob `33763eb5435aa6e357a2ff3489a53e23b9487b00`
- Oracle: `38f4edde6519a75a671cbca22249364318ebefd5ccf46a878c0dbb02cbaa7adb` → `07a485d955b82d40d73cb633b228753d99d454d90bf151afc871790fab6e07f5`; final blob `a1b4852b92efb3f0a6ee3e233bb3758833375730`
- Final commit/tree: `f5052b75d00954655d953dc4e38f3b7fed19c7d5` / `fe6cb686cee2c39b4c5450f296f7d352afbff04f`

Six-file protected map: only popup changed; P1, tour, elements/assets, base three-products, and mounted-readiness hashes were unchanged.

Ledger paragraph for `deletion-ledger.app.md`:

> `P2-popup-traffic` — Exact read-only Runtime inspect POST classification added for the mounted canonical-head poll, preserving strict sole-film-commit equality, 200-status inspection checks, old-route/unknown-route negatives, and all canonical, identity, receipt, history, reload, undo, raw-field, wait, and timeout assertions. Independent old-RED/new-GREEN predicate review PASS on `f5052b75d0`; no browser/full-suite credit claimed. The popup spec changed `d68b773a…34562` → `ab66f693…a4dea`; six protected-file map shows only the popup delta.