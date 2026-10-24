Implemented `scripts/testing/d66-plain-stack.mjs` and three service rows; retained older rows and unchanged originals.

Validation passed:

- `node --check scripts/testing/d66-plain-stack.mjs`
- `node node_modules/eslint/bin/eslint.js scripts/testing/d66-plain-stack.mjs`
- Launcher `--collect`: P1 **2**, P2 **8**, P3 **1**
- Launcher `p1 --launch`: normal boot, native seed, Agent identity and authoritative history **PASS**
- JSON parsing, six original spec hashes, service-command `bash -n`, and `git diff --check` **PASS**

Used Node 20/npm 10 with a 6 GB heap. Preserved six externally staged adoption files, verified identical to App integration `95cfbf216f`. Commit message and `DONE` written.

**One P1 submitted and running; verdict pending:**

```bash
$ORCH/bin/wait-test app-D66-plain-stack-sol-1528-d66-plain-p1-three-products-1024154715-13564
```

When that same ID is green, submit these immediately in parallel:

```bash
$ORCH/bin/request-test app-D66-plain-stack-sol-1528 d66-plain-p2-three-products
$ORCH/bin/request-test app-D66-plain-stack-sol-1528 d66-plain-p3-three-products
```

Each result writes `$ORCH/tests/<ID>/d66/manifest.json`, `readiness.xml`, and `p1.xml`/`p2.xml`/`p3.xml`. Local startup proof is retained in `launch-manifest.json` and `launch.log`.

No browser journey ran locally. P2/P3 remain unsubmitted; no full suite requested.