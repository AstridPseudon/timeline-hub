# Commands and results

All App commands used `/opt/node20/bin/node` or `PATH=/opt/node20/bin:$PATH`.

- `node scripts/sync-runtime-client.mjs /home/user/work/wt/rt-pin-ab1e4f61` — PASS; lock-only Runtime source refresh.
- `node scripts/installer/update-manifest.mjs --runtime-checkout /home/user/work/wt/rt-pin-ab1e4f61 --agent-checkout /home/user/work/wt/agt-pin-070dfc5e --plan` — PASS; only Runtime SHA changes.
- Same updater with `--write` — PASS; manifest-only write.
- `node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/rt-pin-ab1e4f61` — PASS.
- `node scripts/installer/update-manifest.test.mjs` — PASS, 2/2.
- `node scripts/installer/manifest.test.mjs` — PASS, 2/2.
- `node scripts/runtime-schema-guard.test.mjs` — PASS, 2/2.
- `node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts src/integrations/runtime/installManifestSkew.test.ts src/integrations/runtime/vendorLock.test.ts` — PASS, 2 files and 17/17 tests.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python generators/generate.py --check` — PASS.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/python scripts/artifact_manifest.py --check` — PASS; manifest current.
- `PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-runtime/bin/pytest -q -p no:cacheprovider tests/test_artifact_manifest.py` — PASS, 3/3.
- Node syntax checks for `scripts/sync-runtime-client.mjs`, `scripts/vendor-lock.mjs`, and `scripts/installer/update-manifest.mjs` — PASS, 3/3.
- JSON parse for `runtime.lock.json` and `public/install-manifest.json` — PASS, 2/2.
- `node_modules/.bin/eslint scripts/sync-runtime-client.mjs scripts/vendor-lock.mjs scripts/installer/update-manifest.mjs --max-warnings 0` — PASS; zero warnings/errors.
- `git diff --check` — PASS.
- Exact source comparison — PASS; canonical Runtime files 15/15 vs qualified `42aad0e…`, producer mappings 14/14, protected App files base-to-worktree 8/8.

Not run by instruction: full suite, browser, live service/body, native repeat,
original-four, profile, collector/observer, tour, or D130 held-recovery tests.
