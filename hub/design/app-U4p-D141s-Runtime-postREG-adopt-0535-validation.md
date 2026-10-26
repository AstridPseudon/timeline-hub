# Validation

All commands used Node `v20.19.4` from `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin`.

- `node scripts/sync-runtime-client.mjs /home/user/work/wt/rt-pin-95d98f03` — pass; updated only the Runtime source pin.
- `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-95d98f03` — pass.
- `node scripts/installer/update-manifest.mjs --runtime-checkout /home/user/work/wt/rt-pin-95d98f03 --agent-checkout /home/user/work/wt/agt-pin-8585ed9c --plan` — pass.
- Same installer command with `--write` — pass; Runtime SHA updated, Agent/schema unchanged.
- Same installer command with `--plan` after write — pass; idempotent pins.
- `node --test scripts/installer/manifest.test.mjs scripts/installer/update-manifest.test.mjs scripts/runtime-schema-guard.test.mjs` — pass, 6 tests, 0 failures.
- `node scripts/build/verify-astrid-vendor-sources.mjs` — pass; 65 pinned source files, 160 Agent browser vendor files, 11 public imports.
- JSON parse of `runtime.lock.json` and `public/install-manifest.json` — pass.
- `git diff --check` — pass.
- Direct `git diff --quiet HEAD -- . ':(exclude)runtime.lock.json' ':(exclude)public/install-manifest.json'` — pass; no outside-allowlist changes.
- Direct producer/consumer SHA comparison for all 14 Runtime lock mappings — pass.

No full/browser/journey suite was rerun; this adoption is metadata-only and prior integrated evidence is retained by the plan.
