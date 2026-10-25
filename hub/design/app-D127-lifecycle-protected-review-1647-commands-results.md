# D127 command results

All commands were read-only against the App worktree. Scratch/cache state used `/tmp/w-dcff93892a`; no repository files, shared dependencies, generated files, pins, or Git refs were written.

| Command | Result |
|---|---|
| `NODE_COMPILE_CACHE=/tmp/w-dcff93892a/node-cache /opt/node20/bin/node --import tsx --test --test-name-pattern='D127 reviewed-new validator|D105 launch ownership' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` | PASS: 2 passed, 2 skipped |
| `./node_modules/.bin/eslint tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts --report-unused-disable-directives --max-warnings 0` | PASS |
| `flock -w 600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 ./node_modules/.bin/tsc --noEmit -p tsconfig.app.json --pretty false` | PASS |
| `./node_modules/.bin/tsc --noEmit -p tsconfig.node.json --pretty false` | PASS |
| `git diff --check HEAD^ HEAD` | PASS |
| `git diff --name-only d4e5284dfc HEAD` | PASS: only `tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` |
| in-memory execution of actual App validator against baseline and lifecycle/phase mutants | FINDING: baseline pending accepted; pending+raised dispatch accepted; pending+ended dispatch accepted; completed+raised dispatch accepted; returned_without_response+raised dispatch accepted |
| `git show HEAD:tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts \| sha256sum` | `1855a9c9b68818f27bbfb420a9c6c1b97312bd30a52f21fbab76c2b4e5a177de` |
| `git diff HEAD^ HEAD --binary -- tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts \| sha256sum` | `d8d1f5846ae9c198cd41c0364cd887f2591d2308de3b9ac7e5195575576148b3` |
| frozen helper hash: `git -C /home/user/banodoco/banodoco-workspace-runtime show 231ddb5a6605b535d26172d34439ebe7b90804de:tests/helpers/p2_commit_phase_capture.py \| sha256sum` | `4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e` |

## Gated proof

Not run because the source verdict is FAIL and the brief requires focused D78/reviewed-new bootstrap controls only after SOURCE PASS. The existing central unchanged Runtime evidence (`23 passed in 3.46s`) and prior focused observer proof were not duplicated. No full, browser, native, collector, family/P2/P4, original tour, service replay, or held SWAP work was run.

The known strict-islands baseline was not rerun: the brief explicitly retains its missing generated/virtual modules and unrelated implicit-any diagnostics and says no repeat is needed.
