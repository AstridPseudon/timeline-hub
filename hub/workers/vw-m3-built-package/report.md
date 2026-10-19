Built Composition **0.0.8** with all 13 approved defaults, scoped registries, compiled ESM/declarations, and exact React/Remotion peers. Removed workspace shims and external theme discovery. No consumer edits.

[Tarball](/home/user/work/wt/vw-m3-built-package/banodoco-timeline-composition-0.0.8.tgz) — 51,083 bytes; two clean build/pack runs produced identical integrity:

```text
sha512-Pr+RFouHJVbKNfncRGFUCsxiPMy7PGSkRPdVHtoPg2rzdu7x1JDHsvpiMjw4nBU2GnAE55FpsTQpvsCZJ1Mvaw==
```

Passed:

```sh
npm_config_cache=/tmp/vw-m3-npm-cache npm ci
npm run gen-registry:check
npm run build
npm run build:test
node --import ./typescript/tests/register-extensionless.mjs --test \
  typescript/test-dist/tests/registries.test.js \
  typescript/test-dist/tests/scene-evaluation.test.js scripts/gen-registry.test.mjs
npm_config_cache=/tmp/vw-m3-npm-cache npm pack --json
git diff --check
```

Focused tests: **11 passed, zero skipped**. A planted builtin type error correctly failed the build with TS2322; restored afterward.

Fresh-consumer smoke passed. Reproduce from this worktree:

```sh
npm_config_cache=/tmp/vw-m3-npm-cache npm run test:package -- \
  "$PWD/banodoco-timeline-composition-0.0.8.tgz"
```

It verifies plain Node imports, bundled rendering, scoped overrides/capabilities, declaration consumption, shared ThemeContext, deduplicated peers, and unchanged installed files. The declaration probe uses `skipLibCheck` for upstream Remotion’s legacy `Timer` declaration.

Decisions followed the design: supplied registry members replace complete category maps; bundled 2rp remains **0.1.0**.

No blockers. Commit message written; build output removed. Next: manager review/full suite, consumer migrations, and host/film frame/audio parity—all still unverified.