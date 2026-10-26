# D141l validation

Result: the single normal service row was installed; no product or test body was run.

## Read-only source checks

- `git -C /home/user/banodoco/reigh-app show -s --format='commit=%H%nparents=%P%ntree=%T' 5344c53e3063001bb3255bd0c9cd32cc5e77967f` returned qualified App `5344c53e3063001bb3255bd0c9cd32cc5e77967f`, tree `dd989783046aeff652486a1ba39db42aea86e201`.
- The same command for `d822d2f5d2bd05187b4ff5b6071c3e13945d4747` returned pristine tree `2af40a015057779ceb4e4b37cad62e1469aa7e36`.
- `git ls-tree <source> package.json` returned package blobs `70a005c2c3a4f1c59373ef1c4a404de4b225c37c` and `5bdc5b0aaab190884feea72120b3d9d12ab9264f4`; `jq empty` passed for both package blobs.
- Exact `jq -j '.scripts["test:node"]'` extraction produced 1,709 bytes / SHA-256 `74e219373befd25b92f85eb21e84d685c4bf767b0ab969a1e464097766d5363a` for qualified App and 1,666 bytes / SHA-256 `cfe43a224171922de49fe96c4b7647554c63263a090477137430ad4596099455` for pristine upstream.
- Exact script comparison found the qualified-only `scripts/installer/update-manifest.test.mjs` at the specified position. Import, concurrency, reporters, guard, and all other selectors/order match.
- Both source snapshots have `test = npm run test:app && npm run test:node`; both `test:app` scripts retain no-smoke, known-failures, no-raw-skips, and skip-registry checks.

## Allow-list CAS and conservation checks

- Before mutation: `suites.conf` SHA-256 `5ce57b6ee789de40c6d25874a29af37c4fff3d477b913219617eff8b1d01f072`, 733149 bytes, mode 600, LF terminated.
- Mutation used `flock -x` on the absolute config, verified that preimage SHA, rejected any mismatching or duplicate suite-name row, copied with mode preservation, appended one LF-terminated row, and installed with same-filesystem atomic `mv -T`.
- Installed raw row: `app full-d141-node-phase npm run test:node`; 43 bytes including LF, SHA-256 `ca72c9edfe37e73855c5165802f8213ab5693628f6778da0791c827579383b47`; exact count 1 at line 416.
- After mutation: SHA-256 `e100f177f029aedc17b5e4ad3fb697e1c9e98142ca88e6c91101c5f0046ac5f7`, 733192 bytes, mode 600, LF terminated. The first 733149 bytes retain the preimage SHA exactly.
- Existing normal App full row remains byte-identical: `app         full              npm test -- --maxWorkers=3` (raw LF SHA-256 `ea65e55ed5233e5bc335fe7ac6f632ad0fcd0d855449176d5ada293fd2c45bb5`).

## Documentary host check

- Composition host remains commit `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`; `git status --short` was empty and `git diff --check` passed.

No test, full/body, request-test, wait-test, browser, provider import, Node test, TypeScript, lint, or collection command was run.
