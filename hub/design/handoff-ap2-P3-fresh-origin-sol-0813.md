PASS for bounded source repair and offline checks. Only the three allowed paths changed.

- `openCommandTimeline` now reads durable owners on the existing same-origin `/__blank.html` before mounting the editor. It requires exactly one new matching settled owner and preserves its ID through setup qualification.
- Optional `rationale`/`group_id` require independently captured producer values and exact request/reply/history forwarding. The mounted `appendDocument` request remains strict: source supplies neither annotation (`localSaveSession.ts:304`; `timelineLocalSaveHandoff.ts:570`).
- Added actual-helper controls using real save sessions and durable outboxes. Browser navigation and Runtime replies remain offline doubles.

All final validation commands exited **0**:

```bash
TMPDIR=/tmp/w-da1f955d9d /opt/node20/bin/node --import tsx --test tests/e2e/local/support/gate5-reset-precondition.test.mjs
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json
/opt/node20/bin/node node_modules/eslint/bin/eslint.js tests/e2e/local/three-products.spec.ts tests/e2e/local/support/gate5-reset-precondition.ts tests/e2e/local/support/gate5-reset-precondition.test.mjs --max-warnings 0
PLAYWRIGHT_OUTPUT_DIR=/tmp/w-da1f955d9d/playwright-list /opt/node20/bin/node node_modules/@playwright/test/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts --list
git diff --check
```

Helper controls: **20/20 passed**. TypeScript checks were serialized. Playwright listed **15 tests**.

Predecessor control:

```bash
TMPDIR=/tmp/w-da1f955d9d /opt/node20/bin/node --import tsx --test /tmp/w-da1f955d9d/base-controls.test.mjs
```

Exit **1**, as intended: original **18 passed**; both new controls failed against unchanged `6b208f7…`.

SHA256, base → final:

| File | Before → after |
|---|---|
| Spec | `1b2bad9cd74751f042e6dc7e2aefb5a46d6561924ef43b94429c1712142e0efc` → `a94c315219523ede6710f8ce36f0e9c2b65d2c1dd204c96715fae45b525fcfa6` |
| Helper | `269e9e32962579b219ac32ae6918afbbac6c02de44321d2351dd2110fdebed40` → `94568a9baec294cd6848ad37d01163c057c0c4fb0cea202eafe3838b493c71ab` |
| Controls | `2c64f97d7324f481c25f35b5b38cead49c8452336efc09342f838ec031849725` → `430d75012714c7c183f467bba533f1b2122fa834c9711395de935d8ebef02fee` |

Integrity checks passed:

- Gate5 body unchanged: `c527a321298bef7e3bc7d4c8afc4ee7f24d8f1bdad76c4b0f1969f3dd90ec4d5`.
- Protected 9,648-byte tail unchanged: `f7e7abd9233a332adfeea03155d78af05a5d631ffffbecd64691c7014936bb67`.
- Exact reverse-removal reproduces complete original C0 spec: `0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14`.
- D50 was not imported.

No blocker. No live/browser/backend run or live acceptance credit. Commit message and `DONE` written. Recommended next step: independent cumulative review before clean composition.