# U4p D141v independent validation

## Result

PASS for the requested metadata-only qualification. The author sampler custody limitation is recorded as a finding and is not credited.

## Exact commands and results

- `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --test scripts/installer/manifest.test.mjs scripts/installer/update-manifest.test.mjs scripts/runtime-schema-guard.test.mjs` — PASS: 6 tests, 0 failures, 0 skipped.
- `node scripts/build/verify-astrid-vendor-sources.mjs` using the same Node 20.19.4 — PASS: 65 pinned source files, 160 vendor files, 11 public imports.
- `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-95d98f03` — PASS.
- `node scripts/installer/update-manifest.mjs --runtime-checkout /home/user/work/wt/rt-pin-95d98f03 --agent-checkout /home/user/work/wt/agt-pin-ec0a9f5b --plan` twice — PASS; textual plan diff is empty and all three proposed values equal current values.
- Independent Git identity check — PASS: candidate `beee9d3110fbb4fae73eb2998e1dac5e12f0d1dc` / tree `e2632a4fbe63cadbd03b03edc5d34196a37304fd`, sole parent base `82e9e13ddf1d7ec6c736521b2eb091dca9877598`.
- Independent JSON parse of `public/install-manifest.json`, `runtime.lock.json`, and `vendor/astrid-browser/provenance.json` — PASS.
- `git diff --check 82e9e13ddf1d7ec6c736521b2eb091dca9877598 HEAD` — PASS.
- Independent byte audit — PASS: exactly 160 vendor payloads conserved; all 14 Runtime mappings conserved and hash-valid; no tracked entry outside the three allowed metadata paths changed.

## Scope exclusions

No typecheck, lint, full suite, browser journey, service, build, ZIP, or semantic/product review was run, per the metadata-only brief. Existing prior lint findings remain unchanged and are not requalified here.
