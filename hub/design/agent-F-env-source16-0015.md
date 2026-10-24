Implemented and qualified the source-mode harness.

- Added `tools/run-env-source16-0015.sh`.
- Added one named central test-service row: `agent env-source16-0015-targeted`.
- No product code, test bodies, profiles, registries, or shared dependencies changed.
- Harness pins Agent parent `c36ca8c...`, Runtime `8ea0766...`, Node `v20.19.4`, and records origins, hashes, environment bindings, and before/after profile state.
- `external_pkg` remains excluded as separately owned.

Evidence:

- `bash -n tools/run-env-source16-0015.sh` — passed.
- `git diff --check` — passed.
- Final central run:
  `request-test agt-F-env-source16-0015 env-source16-0015-targeted`
  followed by `wait-test ...1024002042-19627` — passed.
- Results: private-import case `1 passed`; source bootstrap/polling cases `15 passed`; total `16 passed`, no skips/errors.

The final run preserved source-mode execution, used the existing managed Runtime installation only where required by the private child-process contract, and unset unrelated Remotion globals. Profile inventory and registry hashes were identical before and after.

Two preflight-only attempts and one earlier 15-pass/1-fail invocation were retained diagnostically; the failure was corrected by the case-specific invocation. The broader full suite remains unrun per instructions and its prior known FAIL267 result is preserved.

Completion marker and commit message were written.