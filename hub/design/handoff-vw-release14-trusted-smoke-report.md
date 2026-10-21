# Trusted package-install environment diagnosis and exact smoke

## Result

PASS. Restored the existing trusted CA/proxy configuration only inside the
owned consumer-smoke child and qualified the unchanged archive
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m4-public14-diagnosed-runner-pack-1042/release-output/banodoco-timeline-composition-0.0.14-public14-qualified-1042.tgz`.

- SHA-256: `21fde4d2a5d62a83f97a85d4b8d9f9d3f707a6489c07eb421c6331eccf893e6e`
- Size/members: 72134 bytes / 80
- Source: `df7b86308902fae90eda1dc3080d17d8fc30ea78`, tree `71d8e95edb1bb2d187c3193ef3462d4cfde277fa`
- Package: `@banodoco/timeline-composition@0.0.14`

## Cause and trust repair

The prior smoke used `env -i` without the inherited CA/proxy carriers. npm
therefore failed TLS validation with `SELF_SIGNED_CERT_IN_CHAIN`, and the
subsequent `ERESOLVE` showed `@remotion/layout-utils@undefined` because
registry metadata was unavailable. No smoke assertion had run.

The inherited trusted CA is `/root/.ccr/ca-bundle.crt`, verified as a readable
regular file (187173 bytes, mode 0644, SHA-256
`f2e3619b6f6b3de595df54e3abf341f3f115470345ee4712e80e89a6c7b19127`). The
existing npm-specific proxy carrier is `npm_config_https_proxy`; proxy values
were never printed. The child passed only those existing carriers, plus
`NPM_CONFIG_STRICT_SSL=true`. It omitted `NODE_OPTIONS`, set `NODE_PATH=''`,
used private realpath-checked stage/cache/tmp directories, and left the parent
environment unchanged. No insecure TLS, force, peer workaround, global config
edit, fabricated trust, shared dependency mutation, or archive repack was used.

## Central evidence

Prerequisite suite
`vw-m4-smoke-trust-environment-diagnosis-1056-integration-public14-trust-prerequisite-1056-1021105527-6023`
passed. It verified the source/archive/tool prerequisites, 11280015360 bytes
available against floor 10737418240, measured need 76239977, Node 20.19.4,
npm 10.8.2, strict TLS, the CA identity, and exact metadata for all eight
required package specs:

`@remotion/layout-utils@4.0.509`, `@remotion/media@4.0.509`, `react@18.3.1`,
`react-dom@18.3.1`, `remotion@4.0.509`, `typescript@5.9.3`,
`@types/react@18.3.31`, and `@types/react-dom@18.3.7`.

Smoke suite
`vw-m4-smoke-trust-environment-diagnosis-1056-integration-public14-exact-packed-package-smoke-1056-1021105601-32025`
passed in 6 seconds. The exact existing `npm run test:package` installed 18
packages, then passed plain Node ESM, bundled render/SSR, scoped host
capability/override, shared theme/peer identity, strict NodeNext typecheck,
and installed-integrity checks. The installed package files were unchanged.
The private stage and cache were removed by the command trap.

## Other runs and limits

- `bash -n PREREQUISITE-COMMAND COMMAND` — PASS.
- First prerequisite registration — setup-only exit 127 because the suite
  referenced the original worker path rather than the central snapshot.
- Second prerequisite attempt — harness-only exit 1 because npm returned the
  dotted `dist.integrity` field and the parser initially expected a nested
  object. Neither reached a package assertion or indicates a dependency
  failure; both were corrected before the passing prerequisite.
- No Composition source files were changed. No full suite, browser, physical,
  helper, Runtime, or new source test was run.
