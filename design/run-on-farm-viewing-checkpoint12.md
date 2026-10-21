Status: HOLD

# Composition 12Z checkpoint — farm request

This is the 12:00 UTC M3/M4 checkpoint for the Composition repository. It is
heavy-farm work only. The farm lead may mark this request READY after checking
the identities and prerequisites below, then runs it once with a Luna worker.

## Source identity

- Repository: Composition
- Hub/integration branch: `timeline/composition/tl/integration`
- Farm checkout: `/home/user/work/composition`
- Commit: `df7b86308902fae90eda1dc3080d17d8fc30ea78`
- Tree: `71d8e95edb1bb2d187c3193ef3462d4cfde277fa`
- Package: `@banodoco/timeline-composition@0.0.14`
- The checkout must be clean and must match both 40-hex identities before the
  command starts. Do not substitute a release, private candidate, or another
  Composition head.

## Exact command

From the exact checkout, after the preflight, run these commands once. The
explicit `env -i` is part of the command; do not add `|| true`, skip flags, an
expected-failure wrapper, or a retry.

```sh
cd /home/user/work/composition

env -i \
  HOME=/root \
  LANG=C.UTF-8 \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  TMPDIR=/tmp/vw-c12 \
  /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/npm run build

env -i \
  HOME=/root \
  LANG=C.UTF-8 \
  PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin \
  TMPDIR=/tmp/vw-c12 \
  /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/npm test
```

`npm run build` is intentionally separate from `npm test`: it is the real
package build and begins with `npm run gen-registry:check`, so stale generated
registries fail the run. `npm test` is the repository's current own suite; it
builds the test output and runs `typescript/test-dist/tests/*.test.js` and
`scripts/*.test.mjs` through the package's existing script. No extra test
framework, browser, socket, install, pack, or archive step is requested.

The expected test result is TAP `# tests 85`, `# pass 85`, `# fail 0`,
`# cancelled 0`, `# skipped 0`, and `# todo 0`. Any zero-test condition is a
failure even if the process exits zero: `No tests found`, `No test files found`,
`collected 0 items`, `# tests 0`, or an absent test-count summary must be recorded
as FAIL. A changed count must be reported, not masked.

## Immutable prerequisites and preflight

The farm lead must list every failed prerequisite before stopping. Verify:

1. `/home/user/work/composition` is the clean checkout of the commit and tree
   above, and the hub branch still names that head.
2. The required immutable Node toolchain exists and is read-only:
   `/home/user/work/toolchain/node-v20.19.4-linux-x64`, Node `v20.19.4`, npm
   `10.8.2`; the observed executable hashes are Node
   `43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490` and npm
   `8e5f6f3429f8cdbe693cdc29904e9d5a7b127a494bd15c804bd54c7403bfcbe7`.
3. The shared dependency tree is already present at
   `/home/user/work/composition/node_modules`, resolves to that immutable
   install, and is read-only. Verify the root and representative leaves with
   `realpath` before starting; no leaf may resolve into a worker checkout or
   another borrowed install. Do not run npm install/ci or modify shared
   dependencies. `package-lock.json` must remain byte-identical with SHA-256
   `b0c1a911648538219cdded4eeb4f76544af85e09366168966240246e54f8d1dd`.
4. `/tmp/vw-c12` is a fresh private mode-0700 run directory owned by this run,
   with the machine's normal disk-floor policy passing. Keep all temporary
   paths short; remove only this exact run directory after the farm has retained
   its log. `env -i` must leave `NODE_OPTIONS`, `NODE_PATH`, `PYTHONHOME`, and
   every `LD_*` variable unset.
5. The command is executed from the requested checkout with no network or
   borrowed worktree. Registry freshness is checked by the unmodified
   `gen-registry:check` step in `npm run build`.

The farm result belongs at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run-on-farm-result-viewing-checkpoint12.md`.
It must include the exact source identities, both command outcomes, the final
TAP counts, and the log path. This request makes no M4 gate or hard-stop claim.

## Prior evidence read for this request

These results were inspected once and are not being rerun locally:

- Source full result
  `composition-full-1021073946-21820`: `npm test` passed 85, failed 0,
  skipped 0 on tree `71d8e95edb1bb2d187c3193ef3462d4cfde277fa`.
  Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/composition-full-1021073946-21820/log.txt`.
- Package smoke result
  `vw-m4-smoke-trust-environment-diagnosis-1056-integration-public14-exact-packed-package-smoke-1056-1021105601-32025` passed the qualified 0.0.14 archive's plain Node ESM, bundled render, scoped host capability/override, peer identity, and installed-integrity checks. It is prior package evidence, not a replacement for this exact checkpoint source run.
  Log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m4-smoke-trust-environment-diagnosis-1056-integration-public14-exact-packed-package-smoke-1056-1021105601-32025/log.txt`.
