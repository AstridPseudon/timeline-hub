# App2 M2 selected final95 owned runner

## Result

Prepared the owned runner at:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-final95-owned-driver-source-0658/run-owned-selected-final95.sh
```

Runner SHA-256:

```text
159c1fa4ba6ed4d8b13d33d8230319b923d930a5b61dddb543a0bbe3d93c061a
```

The runner defaults to an offline CHEAP preflight. `SELECTED_FINAL95_MODE=run`
is required to enter the later central actual path. The private worker record
also contains an empty `KEEP` marker. No App source file, shared helper, shared
graph, lock, generated file, package, or dependency was modified.

## Final App source custody

The App source supplied to the runner is the harness commit:

```text
HEAD:       ba02c8f246ec61cd65d178a1ada686788df3fdab
HEAD tree:  7fe8c15b56da9944ae31e8273d41d3ceb21b3677
base:       42b0c6c8434e2c491f8dbdf00a210ed755e41a95
base tree:  fa887b5689d7ad44957021080f74d13a9d0c4e30
```

The current HEAD is a clean descendant of the base. The selected source and
unchanged normal-DEV controls are:

```text
tests/e2e/local/three-products.selected-param-dev.spec.ts
  10250fa44db4e2d4423f8d06258105df267e3ba4e29700d700bb1d3182a6def1
tests/e2e/local/support/harness.ts
  af61e605e1930ae061506a317008d670c7c1be01511c7c1a57188a6a91cc0465
config/vite/vite.config.ts
  5f26c8fa9beae5691c7c94ae11d008eb6c548eb28aaa2b66887b7512efe6c70d
scripts/runtime-discovery-proxy.mjs
  93989e634008d1c9a6aaeddbca7b0aa0f97c40a7ce232860157d04bc6b2155c0
```

The selected spec remains the approved byte-identical source. The runner
checks the exact title, `20_000` mount budget, `90_000` semantic ceiling,
`240_000` worker fixture budget, original timeline/project identity checks,
P1/P2 admission and source removal, refusal, lost acknowledgement, exact
retry body and idempotency key, two reloads, inverse/undo, and zero legacy
POST assertions.

## Final95 cohort and graph

The runner carries the qualified normal014 controls without relabelling the
old013 driver result:

```text
Agent:       6efc81500a0e0688c2bb41e736503f0fc3e04abb
Agent tree:  2ed2b8a12b5b3391ca221ba6ff05390f71a73556
Runtime:     95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
Runtime tree:d3a290b407fa61e6ab2d476f50c068073f70df00
Producer:    95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c
Artifacts:   sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac
Manifest:    a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d
Count:       76
Schema:      6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
Wire:        sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816
App lock:    770352eaf1d015e90fca0ed2f1893749b73b69356ca82a7223b2573276fe485e
```

The approved selected graph remains Composition `0.0.13`, 77 archive members,
nested tarball SHA-256
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, and
graph archive SHA-256
`895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.
The private graph resolves Node `v22.22.0`, Vite `5.4.21`, Vitest `4.1.5`,
Playwright `1.60.0`, and `@banodoco/timeline-composition` `0.0.13`.

Compared with the old013 Runtime manifest (75 artifacts, manifest SHA
`129abdbbf1f8776436183b5290b39a5dd9225ba95b4c8fe8f2bb005ea4cf85497`, version
`sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`),
final95 has 15 changed or added artifact entries:

```text
contract/schemas/edit-command.json
contract/schemas/health.json
contract/schemas/services.json                 (added)
generators/release.json
packages/python/astrid_runtime_client/__init__.py
packages/python/astrid_runtime_client/contract_metadata.py
packages/python/astrid_runtime_client/generated.py
packages/python/astrid_runtime_client/timeline_commit_types.py
packages/python/pyproject.toml
packages/typescript/package-lock.json
packages/typescript/package.json
packages/typescript/src/contract-metadata.ts
packages/typescript/src/generated.ts
packages/typescript/src/timeline-commit-types.ts
runtime_protocol/schemas/timeline-commit-bundle.json
```

The exact old013-to-final95 artifact hashes are:

```text
contract/schemas/edit-command.json: a6f1aaa9dfcc31828bd04c908158fd7fd9a825df6c9f88f79b81779273a190ef => 6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
contract/schemas/health.json: e88960225448e1f7b17bc47a50ce2931205aa6a82175da7e8b98c665a6600221 => dcaec4238eec1633683b3bc223c039f78e7f9066effb18d80667a4a903f4510e
contract/schemas/services.json: added 10614b9c5a8f044b4c6727701147197b91410ddaf4230b8fa990b78255574018
generators/release.json: 1088179f2bc01644c3de734a77485a59282691cd45776eca12b24b12bde2fcea => bc2e426715c604f06e1e286470eb4bbb58238b6518cecb4bb400f101f26986ce
packages/python/astrid_runtime_client/__init__.py: e2525b02f113d46db5380a70cc23567de8ac721fce487338c37c7c34b5d4b45f => 78a69901f7c68d67b152410732f1c42dd30954ca07e7b4b9a319d4ddbd9035e6
packages/python/astrid_runtime_client/contract_metadata.py: b8f40f1b36e0b2113da2521f04a2a431f4edfd6f9ade7b4dc156e098aa0b3cca => cdedeb72880102ff6557320d908eac9068470b5088256c4441514e9d7db40514
packages/python/astrid_runtime_client/generated.py: 2db50f1b36e0b2113da2521f04a2a431f4edfd6f9ade7b4dc156e098aa0b215f => e2e66babca52a7ff95b8387dd6b36a5e46b4a4085bc9082ea664ab8d054bd468
packages/python/astrid_runtime_client/timeline_commit_types.py: a3c9ce015dff4cfbbc669b42ff44f2f12aec012745d6ea7421804a350384b473 => 4b23c46311210f5fa3a5684eceeab2772b30c40b61c623eacf0fcd1183d45457
packages/python/pyproject.toml: b74a3c7e6d816125ed167cfa9b9f41b14843ff08f1a57592a81f9845fa889f8f => 6c15723214b1d240f1e9fbea6692019da4893acc486dabcb74ab28e2efaf879f
packages/typescript/package-lock.json: 937e106a608c535d6a5de37eaabb9902f216378a96b445f0a5390a461bd46288 => bb5b79bd79ddd6c780a16e658763f7d534718a739703abcf809b75b664957d66
packages/typescript/package.json: 90d3e1c9eda7b26ff887fcd31a2c97f21b0ddda2c5766f8c3ee8bae80c3e9dea => 8510b0cb8e15630ef999539e697b4f480e6b640d8c9b56c121fa58b66fb451f3
packages/typescript/src/contract-metadata.ts: 0829f42a52fd74e596f5925814766cb87d60919203991b22f07f6869ab6ace44 => 4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044
packages/typescript/src/generated.ts: dd542c8c04ceec1af3d21413cf82ac6316879c0f3d2dacae5f88754c3b395ee8 => c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d
packages/typescript/src/timeline-commit-types.ts: e3d625cea11e5e0318c1a3020b1baba62c3726c4d7fe4b3d03d810d48743331d => f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
runtime_protocol/schemas/timeline-commit-bundle.json: e0cc63576c17f73d6d5855d0ef6ab2e441f3db67b5e07596e8ed7c0ff4f0e4c9 => 6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3
```

The final95 Agent and Runtime edit-command schema bytes are identical at
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`. The App
generated metadata, generated client, types, and timeline schema hashes are
respectively:

```text
4cd934d868eafd5ab82578da2232f1ee13f04d83c9314b3473b75bd951570044
c575f183b6486dd07e8ec798f5a46bff4c9ffc0918892b189c1a433b9f80762d
f8cbbbbc48713a308c2ac2e2e977d08525c4280ef4dc93cd3e8d842245394564
f52b82024ecd44a5e6c9c68d5cb326d50d70efe9aaad6f8ac6352ea1c87b97b1
```

## Literal selected recipe and controls

The selected title and source are unchanged:

```text
local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo
tests/e2e/local/three-products.selected-param-dev.spec.ts
```

The runner preserves the original selected argv exactly:

```sh
node node_modules/playwright/cli.js test --config playwright.three-products.config.ts --grep "$TEST_TITLE" --list
npm run build:hosted
flock -w 600 /home/user/work/.app-m1-browser.lock npm run test:e2e:three-products -- --grep "$TEST_TITLE"
```

The normal-DEV lifecycle remains the existing harness lifecycle: the selected
Agent credential is passed as `ASTRID_RUNTIME_CREDENTIAL` file path; the App
uses `WORKSPACE_RUNTIME_TOKEN_FILE`; Runtime discovery is through
`ASTRID_WORKSPACE_DISCOVERY`; and both proxy and Vite use
`ASTRID_RUNTIME_OPERATION_ORIGIN` from the actual `devOrigin`. The runner uses
one private `mktemp` run root, one private App overlay, private graph links
back to the read-only locked graph, private caches, and private source clones
for a future actual. It never writes the shared graph or source repositories.

## Preflight evidence

Command:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-final95-owned-driver-source-0658/run-owned-selected-final95.sh \
  /home/user/work/wt/ap2-m2-selected-final95-owned-driver-source-0658
```

Result: **PASS**. It reported all of the following together: final source,
ancestry, selected spec, KEEP and clean normal link; final95 source refs,
trees, artifacts, manifest, schema, and graph; Node/Vite/Vitest/Playwright
resolution; helper/driver hashes and syntax; DEV proxy/origin/credential
scope; exact selected contract and budgets; local lock, disk floor, and copy
controls; private overlay; and exactly one test in one file from Playwright
`--list`.

The offline planted wrong role, Agent tree, App pin, graph path, argv, and
zero-test probes all refused as required. `sh -n` passed for the owned runner,
the old selected driver, and `normal014-source-common.sh`; `node --check`
passed for the discovery proxy. App `git status --short --untracked-files=all`
and `git diff --check` are clean.

Shared control hashes were unchanged:

```text
old selected driver:       a959de6e0041f0d8ee28b949a19f5add97d7fb5de27714da6beaad15abd6ce4f
normal014 parent media:    1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd
normal014 source common:   d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848
```

No browser, build, daemon, socket, startup, central actual, full suite, or
dependency install was run. The private Playwright collection is module/test
listing only and does not start product processes.

## Decisions and remaining prerequisite

No shared-helper role patch was needed. The existing helper's final95 source
roles are closed to its qualified parent/bootstrap App roots; this owned
runner therefore performs a local collision-resistant exact check for the
selected harness HEAD/tree and uses the shared helper only for its existing
read-only final95 source/artifact/private-graph functions. No shared file was
patched, and no new source authority was introduced.

The remaining prerequisite is the later central test-service actual using the
owned runner's explicit `SELECTED_FINAL95_MODE=run` path. That actual must
re-check the clean source/tree and final95 tuple, acquire the existing browser
lock, and execute the literal recipe above. Until that run passes, this report
claims runner/preflight readiness only, not selected-case behavioral
qualification.
