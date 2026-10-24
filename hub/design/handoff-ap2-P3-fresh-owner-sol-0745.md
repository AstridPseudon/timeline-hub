Implemented P3 setup qualification in the three authorized files.

- `openCommandTimeline()` returns the newly claimed scoped owner. Gate5 carries that exact identity through settlement.
- The helper checks exact request/reply keys, source-derived command claims, steps, dependencies, receipt correlation, canonical closure, digest, history records and undo metadata.
- Controls use the real document encoder/save-session request builder. Provider replies and browser events remain offline doubles.

Validation:

```text
/opt/node20/bin/node --import tsx --test tests/e2e/local/support/gate5-reset-precondition.test.mjs
```

Exit 0; direct execution reports **18/18 passing**. Against predecessor source: **14 pass, 4 expected failures**, including demonstrated false acceptance of malformed claims and extra keys.

All exited 0:

```text
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.json
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.app.json
/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit --incremental false -p tsconfig.node.json
/opt/node20/bin/node node_modules/eslint/bin/eslint.js tests/e2e/local/three-products.spec.ts tests/e2e/local/support/gate5-reset-precondition.ts tests/e2e/local/support/gate5-reset-precondition.test.mjs --max-warnings 0
PLAYWRIGHT_OUTPUT_DIR="$TMPDIR/playwright-list" /opt/node20/bin/node node_modules/@playwright/test/cli.js test --config playwright.three-products.config.ts tests/e2e/local/three-products.spec.ts --list
git diff --check
```

TypeScript checks were serialized. Collection found 15 tests.

Integrity:

- Base: `481ed48ead8974b6b3cb639fe7d2198d40d3ad0c`; tree `3fefe21ec9d65bb19e086c84537925fd95b74cd9`.
- Reverse-removing only setup/import and fresh-owner return plumbing reproduces the complete `c0fe889944…` spec byte-for-byte.
- Protected tail remains `f7e7abd9233a332adfeea03155d78af05a5d631ffffbecd64691c7014936bb67`.
- No D50 change imported.

SHA256 values:

| File | Base → final |
|---|---|
| Spec | `fc34128b0e98948cb70bf5c099c680d05ff050896c8c3a1a5ded0762597753a7` → `1b2bad9cd74751f042e6dc7e2aefb5a46d6561924ef43b94429c1712142e0efc` |
| Helper | `a72e32a27824389d54ded1892aee1acbfbaa72ed0a4a292027cd8a94a7ee092c` → `269e9e32962579b219ac32ae6918afbbac6c02de44321d2351dd2110fdebed40` |
| Controls | `657e77f14bfc148fc911d1d5775cc265eda8e0fb5ea3948913c189848088e0ea` → `2c64f97d7324f481c25f35b5b38cead49c8452336efc09342f838ec031849725` |

Gate5 testcase slice, including its header: `4a598f09f0096b89d291925a9af6b7bacd084696e932104d782df736f0839de0` → `31072c3edb2263d96ae3c4b2da44403b3d9632c5258bc27371cf107592d5b3f9`.

Supported inputs are existing outbox `scope/ownerId/accepted.head/value`, canonical pre-gesture data, receipt, authoritative head/revision and `/commits` history. No diagnostic writer changed.

No blocker. No browser/backend/full-suite run occurred; live Gate5 remains unverified. Published 9310 evidence remains one POST/200 with 25 reads each. Next step: independent no-weakening review. Commit message and `DONE` were written.