## Verdict: PASS — branch-only

Reviewed `81b8d5993773a60e54291d6a7a0bc0cf890974c2` over `73aa558266e04cae80ea23c50a4bd4722abcda6b`. No product files changed.

The review confirms:

- Request key and durable receipt ID are distinct; `receipt.idempotency_key === post.key`, while history/head/inverse/undo use exact `receipt_id` joins.
- Wrong-key, wrong-receipt, head, history, inverse-target, and undo-target cases are rejected by actual helpers.
- Full commands, effects, dependencies, created/reads, fork/raw/opaque/sibling/registry/canonical/reload protections remain strict.
- ADD and SWAP case bodies are byte-identical before/after.
- The `txn-` check is only a current-producer shape assertion; it does not replace concrete identity joins.
- ADD/SWAP browser journeys remain `NOTRUN`; no live/backend claim.

### Evidence

- Popup oracle: Node test runner passed; positive and negative oracle cases passed.
- Semantic oracle: 7/7 passed.
- Three locked TypeScript no-emit checks: all passed.
- Scoped ESLint: passed with `--max-warnings 0`.
- Playwright list-only: exactly 2 tests, ADD and SWAP; no browser execution.
- `git diff --check`: passed.
- Reverse diff apply check: passed.

Commands included:

```text
PATH=/opt/node20/bin:$PATH TSX_DISABLE_CACHE=1 /opt/node20/bin/node --test --test-concurrency=1 --test-reporter=spec tests/e2e/local/support/p2-popup-oracle.test.mjs
```

```text
PATH=/opt/node20/bin:$PATH XDG_CACHE_HOME=/tmp/w-0160613c94/cache NODE_OPTIONS='--import=data:text/javascript,globalThis.__dirname=process.cwd()+String.fromCharCode(47,99,111,110,102,105,103,47,116,101,115,116,105,110,103)' /opt/node20/bin/node node_modules/vitest/vitest.mjs run --config /tmp/w-0160613c94/vitest.popup-review.config.ts --configLoader runner --no-cache --maxWorkers=1 --no-file-parallelism --reporter=dot tests/e2e/local/support/p2-semantic-oracle.test.mjs
```

```text
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.json --noEmit --pretty false --incremental false
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.app.json --noEmit --pretty false --incremental false
flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc -p tsconfig.node.json --noEmit --pretty false --incremental false
```

```text
/opt/node20/bin/node node_modules/eslint/bin/eslint.js tests/e2e/local/three-products.p2-popup.spec.ts tests/e2e/local/support/p2-popup-oracle.test.mjs --max-warnings 0
PATH=/opt/node20/bin:$PATH npm run test:e2e:three-products -- --list --reporter=list tests/e2e/local/three-products.p2-popup.spec.ts
git diff --check 73aa558266e04cae80ea23c50a4bd4722abcda6b 81b8d5993773a60e54291d6a7a0bc0cf890974c2
git diff 73aa558266e04cae80ea23c50a4bd4722abcda6b 81b8d5993773a60e54291d6a7a0bc0cf890974c2 --binary | git apply --reverse --check
```

### Exact hashes

- Review commit: `81b8d5993773a60e54291d6a7a0bc0cf890974c2`
- Parent: `73aa558266e04cae80ea23c50a4bd4722abcda6b`
- Review tree: `65f1a7d3df3fe8d8e409ae8d02ec8cdb69807ee4`
- Popup spec before: `05370adc76b2e8506e812a2c7ce9bde4441868c7c6d97aac7bf0eb8845b64a84`
- Popup spec after: `4292d0b5928e1390c48d0e33876621a2e9b6c7e0616607a72f1b3fa3873d1de9`
- Oracle before: absent
- Oracle after: `38f4edde6519a75a671cbca22249364318ebefd5ccf46a878c0dbb02cbaa7adb`
- Identity helper block: `d14e6f9b9dc90404872a18414250511cf91e2febe6a52ebac3a9203db79e8fbb`
- `assertHistory` before/after: `ca874032964ef18b04f1e353e8fc032340c2b6ce1f6dc6c7d285434499f940bd` / `b817b33ef7fb1d045600e525f3b2b41ec4ad200c3de1fca996d2c19e13ad05ea`
- `assertReloadUndo` before/after: `7a292b995c6ab48f7272e67e919b58867c95337b589be7b724b4bdae7fd2e9df` / `efaa3cf2b7011e529af9e9db807d4a3202d58d8c0dbd9012e975e3ce28172768`
- ADD body before/after: `391605fbbbd8ba7e1c888610661b10e0b52e027a6507d42954d5280d94ebdfb4`
- SWAP body before/after: `e66926998e182b65d877182eda1ab48357c4823abc4f98bd1ada31b92f08c6b0`

### Worker behavior row

| ID | task (short) | model | needs | status | worker | proof | commit |
|---|---|---|---|---|---|---|---|
| APP-P2-SWAP-REVIEW-1257 | Protected P2 popup receipt/publication no-weakening review | Codex | Orchestrator decision; actual ADD/SWAP browser run | PASS — branch-only; ADD/SWAP NOTRUN | app-P2-swap-review-1257 | Popup oracle pass, semantic 7/7, three TS checks, lint, list-only, diff checks | `81b8d5993773a60e54291d6a7a0bc0cf890974c2` |

Required commit message and `DONE` marker were created.