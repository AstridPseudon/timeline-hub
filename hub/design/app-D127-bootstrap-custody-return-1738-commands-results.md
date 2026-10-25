# D127 retained custody commands and results

## Current worker read-only checks

- `git rev-parse 9bf465285ccf57be31570c800d4a1f86855ebc4e^{tree}` → `7be73e2cbbcf89d627bf7b9da940b4ce17968c20`.
- `git rev-parse 54c91d77fa51cb8d21dd86a76d8297d13d8d19e9^{tree}` → `7be73e2cbbcf89d627bf7b9da940b4ce17968c20`.
- `git show 9bf465285ccf57be31570c800d4a1f86855ebc4e:tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts | sha256sum` → `92586e7fb9603bec32b6fbee03aeb0fff9176d7cf16a35534ae8a2287e4ad48c`.
- `git show 54c91d77fa51cb8d21dd86a76d8297d13d8d19e9:tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts | sha256sum` → same SHA256; both blobs are 49,511 bytes.
- `git -C /home/user/banodoco/banodoco-workspace-runtime show 231ddb5a6605b535d26172d34439ebe7b90804de:tests/helpers/p2_commit_phase_capture.py | sha256sum` → `4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e`.
- Exact Agent/Runtime commit and tree objects were present and matched the retained source-custody values: Agent `070dfc5e…` / `60564143…`; Runtime `ab1e4f61…` / `7d8e77b2…`.
- Exact retained private paths were checked read-only and are absent: `/tmp/w-52d29f4d54/app-D127-p2-selector.log`, `/tmp/w-52d29f4d54/p2-runtime-cli-smoke-LTLcBf/p2-commit-phase.jsonl`, and `/tmp/w-52d29f4d54/app-D127-p2-helper/p2_commit_phase_capture.py`.
- The promised prior directory is absent: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127-reviewed-clean-bootstrap-1731/evidence`.
- No tests, sockets, services, browsers, full suites, or source edits were run by this worker.

## Retained 1731 execution (not rerun)

- Exact command: `TMPDIR=/tmp/w-52d29f4d54 NODE_COMPILE_CACHE=/tmp/w-52d29f4d54/app-D127-node-cache-selector ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-ab1e4f61 ASTRID_RUNTIME_PYTHON=/home/user/work/venv-runtime/bin/python ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-070dfc5e ASTRID_PYTHON=/home/user/work/venv-agent/bin/python D66_P2_COMMIT_PHASE_CAPTURE_HELPER=/tmp/w-52d29f4d54/app-D127-p2-helper/p2_commit_phase_capture.py D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256=4ee0424b63f1f9847995a605dc1050ad7cb8ca75f4d64b8c36d851cfe723f41e /opt/node20/bin/node --import tsx --test --test-name-pattern='P2 Runtime observer bootstrap' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`.
- Retained TAP result: `1..5`, `# tests 5`, `# pass 1`, `# fail 0`, `# skipped 4`, `# duration_ms 14606.499108`; the named test passed and the four other names were skipped by the selector.
- Retained capture validator result: all JSON objects; 102 events; 10 phases; two `completed` summaries; 34,670 bytes; mode `0600`; checked private markers absent. Capture SHA256 recorded as `51cd6d3ba29707d2d6e88d605861757fc3608b459f9f1fd999f502a3884a1f3e`.
- These capture facts are retained-log assertions only. The capture bytes, selector log bytes, and helper copy are no longer present, so this report does not claim raw capture custody or independently recompute those claims.
- Retained scoped controls: ESLint PASS; D127 offline validators `2 passed, 3 skipped, 0 failed`; no D78 rerun; no full/family/browser/native/service suite.
