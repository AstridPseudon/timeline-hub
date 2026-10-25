# D127 commands and results

- `/opt/node20/bin/node --version`: `v20.20.0`
- `/opt/node20/bin/npm --version`: `10.8.2`
- `git diff --check`: PASS.
- `./node_modules/.bin/eslint tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts --report-unused-disable-directives --max-warnings 0`: PASS.
- `/opt/node20/bin/node --import tsx --test --test-name-pattern='D127 reviewed-new validator' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`: PASS, 1 passed, 3 skipped.
- `/opt/node20/bin/node --import tsx --test --test-name-pattern='D105 launch ownership|D78 bootstrap' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`: FAIL overall: D105 passed; D78 failed before validator execution because the selected Runtime checkout lacks `tests/helpers/p2_commit_phase_capture.py` and reported `P2 Runtime phase helper is unavailable at the selected Runtime source`.
- `/opt/node20/bin/npm run typecheck:strict-islands`: FAIL baseline/environment outside the assigned file: missing `@astrid/packs/*` and `virtual:astrid-element-admissions` modules plus existing implicit-any errors.
- `./node_modules/.bin/tsc --noEmit --target ES2022 --module NodeNext --moduleResolution NodeNext --allowImportingTsExtensions --skipLibCheck tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`: FAIL on pre-existing target/harness `unknown` narrowing errors and one harness missing property; no syntax parse failure.
- `git -C /home/user/banodoco/banodoco-workspace-runtime show b81c0ab26df66c7e6f4656104a02e001224b3ffd:tests/helpers/p2_commit_phase_capture.py | sha256sum`: PASS, exact `4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e`.

Not run: actual P2/endpoint activation, candidate helper activation, browser/native/service replay, full suite, or central full request.
