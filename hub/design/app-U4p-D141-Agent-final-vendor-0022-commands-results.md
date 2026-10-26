# U4p/U3 D141 command results

Environment: Node `v20.20.0` via `/opt/node20/bin`; available `/tmp` space was 5.0 GB before checks. The worker tmpdir path supplied by the harness was a regular file, so the private generated destination was `/tmp/app-U4p-D141-final-vendor-private`.

- `node scripts/astrid-landing/refresh-vendor.mjs --astrid-repo /home/user/work/agent --commit 28e56cacb42d3da85b02e5b3543895b44f3d0f70 --destination /tmp/app-U4p-D141-final-vendor-private` — PASS; 160 files; tree `2ebe2ddf5a61f013953ab1e21d51ebaab746e58`.
- Same generator with the default destination — PASS; 160 files; only `vendor/astrid-browser/provenance.json` changed in the App worktree; private/default file sets and payload bytes equal.
- `node scripts/installer/update-manifest.mjs --runtime-checkout /home/user/work/runtime --agent-checkout /home/user/work/agent --plan` — PASS; exact qualified Agent/Runtime SHAs and App schema digest.
- Same command with `--write` — PASS; only `public/install-manifest.json` changed; schema digest unchanged.
- `node scripts/build/verify-astrid-vendor-sources.mjs` — PASS; 65 pinned closure files, 160 browser vendor files, 11 public imports.
- `node scripts/vendor-lock.mjs check config/astrid-cli-surface/vendor.lock.json` — PASS.
- `node --test scripts/installer/manifest.test.mjs scripts/installer/update-manifest.test.mjs scripts/runtime-schema-guard.test.mjs` — PASS; 6/6 tests.
- `node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/integrations/runtime/installManifestSkew.test.ts src/integrations/runtime/vendorLock.test.ts` — PASS; 2 files, 17/17 tests.
- `node_modules/.bin/eslint scripts/astrid-landing/refresh-vendor.mjs scripts/build/verify-astrid-vendor-sources.mjs scripts/installer/update-manifest.mjs scripts/vendor-lock.mjs --max-warnings 0` — PASS.
- `git diff --check` — PASS.
- Direct conservation checks — PASS; Agent provenance source hashes 159/159, Runtime mapped14 exact, manifest pins/schema exact, all outside vendor/manifest equal reviewed db8.

The first direct conservation attempt was rerun with a large `git show` buffer after Node's default 1 MiB buffer rejected a PNG; no source or product state was affected.

Not run by scope: full suite, browser/live socket suites, ZIP/build, app/node TypeScript checks (vendor source payload was unchanged; only provenance metadata changed).
