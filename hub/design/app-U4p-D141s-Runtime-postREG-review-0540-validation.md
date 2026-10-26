# Validation

All Node commands used `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node` (`v20.19.4`).

- `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-95d98f03` — PASS; all 14 Runtime mappings match the pinned producer.
- `node scripts/installer/update-manifest.mjs --runtime-checkout /home/user/work/wt/rt-pin-95d98f03 --agent-checkout /home/user/work/wt/agt-pin-8585ed9c --plan` — PASS; all three planned values are no-ops (`from == to`). Repeated read-only plan remained idempotent.
- `node --test scripts/installer/manifest.test.mjs scripts/installer/update-manifest.test.mjs scripts/runtime-schema-guard.test.mjs` — PASS; 6 tests, 0 failures.
- `node scripts/build/verify-astrid-vendor-sources.mjs` — PASS; 65 pinned closure files, 160 `vendor/astrid-browser` provenance files, and 11 public imports.
- JSON parse of `runtime.lock.json` and `public/install-manifest.json` — PASS.
- `git diff --check` — PASS.
- Direct candidate-vs-base conservation — PASS; only `runtime.lock.json` and `public/install-manifest.json` changed, with only the expected fields.
- Direct producer verification — PASS; Runtime `95d98f...` / tree `78df31...` and Agent `8585ed...` / tree `92a3ff...` are clean and exact. Runtime `6a011d...→95d98f...` has exactly the three documented producer paths, none consumed by App mappings.
- Direct App source/test conservation — PASS; mapped clients, schema, canonical files, test assertions, test inputs, fixtures, scripts, and vendor source are byte-identical to base.

No full Runtime/App suite, browser/journey suite, typecheck, lint, or live service test was rerun. This is applicable because the candidate is metadata-only and all source/test conservation checks passed; prior integrated evidence remains the authoritative behavioral proof.

