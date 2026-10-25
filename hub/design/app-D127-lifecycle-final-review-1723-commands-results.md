# D127 commands and results

Source and review branch both resolved to `54c91d77fa51cb8d21dd86a76d8297d13d8d19e9` / tree `7be73e2cbbcf89d627bf7b9da940b4ce17968c20`. Normal base was `d4e5284dfcc20801977cef12253b12f9cc8798fd` / tree `5efca939546f30b039cb9cacba7a29d7db690f2a`.

| Command | Result |
|---|---|
| `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python NODE_COMPILE_CACHE=/tmp/w-c593aa576a/node-cache /opt/node20/bin/node --import tsx --test --test-name-pattern='D127|D105 launch ownership' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` | PASS: 3 passed, 2 skipped; D105 and both D127 source/matrix tests. |
| `ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python D66_P2_COMMIT_PHASE_CAPTURE_HELPER=/tmp/w-d127-combined-Ntc0E0/p2_commit_phase_capture.py D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256=4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e NODE_COMPILE_CACHE=/tmp/w-c593aa576a/node-cache /opt/node20/bin/node --import tsx --test --test-name-pattern='D78 bootstrap' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts` | PASS: 1 passed, 4 skipped; admission `5,032,046,592` bytes. |
| Same qualified tuple and hash hook with `--test-name-pattern='P2 Runtime observer bootstrap'` | NOTRUN_AFTER_SETUP_REFUSAL: one run exited before observer bootstrap because `/home/user/work/wt/agt-pin-070dfc5e/.venv/bin/python` is absent; admission `5,031,952,384` bytes. |
| `/opt/node20/bin/node node_modules/eslint/bin/eslint.js tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts --report-unused-disable-directives --max-warnings 0` | PASS. |
| `flock -w 60 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json --pretty false` | PASS. |
| `/opt/node20/bin/node node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json --pretty false` | PASS. |
| `git diff --check` | PASS. |
| `git status --porcelain=v1` | Clean. |
| `git diff --name-status d4e5284dfcc20801977cef12253b12f9cc8798fd HEAD` | Exactly one modified path: assigned test file. |
| `git -C /home/user/work/runtime show 231ddb5a6605b535d26172d34439ebe7b90804de:tests/helpers/p2_commit_phase_capture.py | sha256sum` | `4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e`. |
| Prior independent Runtime custody `1630` / central `28551` | Reused: 160 original predicates and PASS23; not duplicated. |

No full suite, browser/original tour, native, family, P2/P4, SWAP, new collector, service replay or integration run was performed.
