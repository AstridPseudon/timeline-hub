# U4p/D141 command results

Working tree: `/home/user/work/wt/app-U4p-D141-Runtime-adoption-0011`

Available space at acceptance: `5147197440` bytes (>= 5 GB).

- `PATH=/opt/node20/bin:$PATH /opt/node20/bin/node scripts/sync-runtime-client.mjs /home/user/work/runtime` — PASS; updated only `runtime.lock.json` source pointer.
- `PATH=/opt/node20/bin:$PATH /opt/node20/bin/node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/runtime` — PASS; `ok runtime.lock.json (matches pinned producer commit)`.
- `PATH=/opt/node20/bin:$PATH node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/integrations/runtime/installManifestSkew.test.ts src/integrations/runtime/vendorLock.test.ts` — PASS; 2 files, 17 tests.
- `PATH=/opt/node20/bin:$PATH /opt/node20/bin/node --test scripts/runtime-schema-guard.test.mjs` — PASS; 2 tests.
- `PATH=/opt/node20/bin:$PATH node_modules/.bin/eslint scripts/sync-runtime-client.mjs scripts/vendor-lock.mjs --max-warnings 0` — PASS; no diagnostics.
- `git diff --check` — PASS.
- Producer `git status --porcelain=v1` — PASS; clean.
- Required producer SHA-256 checks — PASS; artifacts, version, manifest, and timeline-commit schema matched the task values.
- Exact 14 mapping SHA-256 comparison — PASS; every consumer, producer, and lock digest matched.

Node: `v20.20.0`; npm: `10.8.2`.

No full suite, browser, live socket, or redundant Runtime producer test was run.
