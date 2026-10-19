Implemented registration-owned `supportsEasing` metadata and ordinary progress/easing props. Removed default-ID and component-identity routing; deleted the private adapters. Type-on now owns its reveal window. No dependency or consumer changes.

Validation passed:

```sh
npm run build:test
node --import ./typescript/tests/register-extensionless.mjs --test \
  typescript/test-dist/tests/animations.test.js \
  typescript/test-dist/tests/registries.test.js \
  typescript/test-dist/tests/scene-evaluation.test.js \
  scripts/gen-registry.test.mjs
npm run gen-registry:check
npm run build
git diff ed89754 --check
```

All **18 tests passed**. Also compared **1,030 default-output samples** against the base: unchanged.

With `W="$ORCH/workers/vw-m3-package-progress"`:

```sh
npm_config_cache="$W/npm-cache" npm pack --json --pack-destination "$W"
npm_config_cache="$W/npm-cache" npm run test:package -- \
  "$W/banodoco-timeline-composition-0.0.8.tgz"
```

Fresh-consumer smoke passed. Repeating the clean pack produced identical bytes.

[New 0.0.8 tarball](丿tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-package-progress/banodoco-timeline-composition-0.0.8.tgz), 50,664 bytes:

```text
sha512-dzRWuIgeSjKt6ko64AJ7F8aaiSBBxtEzwS0WBFkVi7XB+z2wHLKArlA9fWle/KlwZlXjFDzq2oBi9QJLy1HHUw==
```

Commit message written to the assigned path; build output and temporary files removed. No blockers. Manager review/merge and central full suite are next; browser/frame/audio/film parity remains unverified. The old tarball remains unapproved.