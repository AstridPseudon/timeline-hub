# U4p D141v validation

## Result

PASS. Authorized metadata-only adoption completed from the exact final Agent and Runtime producer checkouts.

## Commands and results

- Supported Node v20.19.4 — PASS.
- Private refresh-vendor.mjs to TMPDIR — PASS: all 160 payload names and bytes matched the App baseline.
- Normal refresh-vendor.mjs with final Agent — PASS: 160 files; provenance updated.
- sync-runtime-client.mjs with final Runtime — PASS; Runtime lock remained byte-identical because it already pinned 95d98f038320d5d46bd679ac000ab3e15825c935.
- vendor-lock.mjs check — PASS.
- update-manifest.mjs plan, write, repeat plan — PASS; repeat plan idempotent.
- node --test scripts/installer/manifest.test.mjs scripts/installer/update-manifest.test.mjs scripts/runtime-schema-guard.test.mjs — PASS: 6 tests, 0 failures, 0 skipped.
- node scripts/build/verify-astrid-vendor-sources.mjs — PASS: 65 pinned source files, 160 vendor files, 11 public imports.
- JSON parse of the three metadata files — PASS.
- git diff --check HEAD — PASS.
- Outside-conservation check excluding the three authorized metadata paths — PASS; all other tree entries exact.
- Final producer identity checks — PASS; Agent ec0a9f5baef2c31bc5179087b83f044524575182/83b84c79941917fde535ee3ddba5533a776cace3 and Runtime 95d98f038320d5d46bd679ac000ab3e15825c935/78df31d62c5b9ba4c84dee4ea346e43a767718c1, both clean.

## Final delta

- public/install-manifest.json: agent.sha advanced from 8585ed9c0404d0187b2ce70242d25114a32747c2 to ec0a9f5baef2c31bc5179087b83f044524575182.
- vendor/astrid-browser/provenance.json: Agent commit/tree and refresh command advanced to the final producer.
- runtime.lock.json: no final diff; Runtime pin was already current.

No full suite, typecheck, lint, browser, journey, service, build, ZIP, or global GO reproof was run, per scope.

A first ad hoc conservation probe used CommonJS require in an ES-module stdin script and failed before checking files; the corrected ESM probe passed and no product state was affected.
