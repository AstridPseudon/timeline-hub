# Handoff report — Composition checkpoint 12 farm request

Prepared `design/run-on-farm-viewing-checkpoint12.md` for the exact Composition
integration head:

- commit `df7b86308902fae90eda1dc3080d17d8fc30ea78`
- tree `71d8e95edb1bb2d187c3193ef3462d4cfde277fa`
- hub branch `timeline/composition/tl/integration`

The request remains `Status: HOLD` until the manager checks it. It specifies one
farm run with explicit `env -i` Node 20.19.4/npm 10.8.2 build and test commands,
read-only shared dependencies, the package-lock and toolchain hashes, registry
freshness through `npm run build`, and a zero-tests-fail guard. It deliberately
does not request local execution, installation, packaging, browser work, or
artifact machinery.

Exact farm commands from `/home/user/work/composition`:

```sh
env -i HOME=/root LANG=C.UTF-8 PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/tmp/vw-c12 /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/npm run build
env -i HOME=/root LANG=C.UTF-8 PATH=/home/user/work/toolchain/node-v20.19.4-linux-x64/bin:/usr/local/bin:/usr/bin:/bin TMPDIR=/tmp/vw-c12 /home/user/work/toolchain/node-v20.19.4-linux-x64/bin/npm test
```

Prior evidence read once, not rerun locally:

- source full21820: `npm test`, 85 passed / 0 failed / 0 skipped on tree
  `71d8e95edb1bb2d187c3193ef3462d4cfde277fa`; log at
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/composition-full-1021073946-21820/log.txt`;
- package32025: qualified 0.0.14 package smoke passed; log at
  `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/vw-m4-smoke-trust-environment-diagnosis-1056-integration-public14-exact-packed-package-smoke-1056-1021105601-32025/log.txt`.

No tests were run locally by instruction. The farm result is expected at
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/run-on-farm-result-viewing-checkpoint12.md`.
