# P3 environment repair handoff

Status: environment repair completed; the one authorized successor was submitted and stopped at App setup preflight. No Gate-5 browser/body result is claimed.

## Source and installed graph

- App worktree: /home/user/work/wt/ap2-P3-env-repair-0355, base 7116a8e2898585fb1e685322a397fd6f0f641f9a; no product/source files changed.
- Shared snapshot install before repair: /home/user/work/app/node_modules; installed Composition realpath /home/user/work/app/node_modules/@banodoco/timeline-composition, version 0.0.8.
- Approved pinned archive: /home/user/work/app/vendor/artifacts/banodoco-timeline-composition-635f4de06fda22a85fc2e4cfc764d0153a4c9f40.tgz, 73,451 bytes, SHA-256 819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234, package version 0.0.14.
- Private owned graph: /tmp/w-2b901599a5/ap2-P3-env-repair-0355/private/node_modules. It was created with the existing prepareNodeModulesOverlay tool from scripts/testing/auto-real-proxy-main95.mjs; ordinary dependencies remain links to /home/user/work/app/node_modules, while the Composition entry is a physical extraction of the approved archive.
- Private Composition realpath: /tmp/w-2b901599a5/ap2-P3-env-repair-0355/private/node_modules/@banodoco/timeline-composition, version 0.0.14. Operational links expose effects.generated, animations.generated, and transitions.generated at package root to existing dist/*.js files, and typescript to /home/user/work/app/vendor/timeline-composition/typescript; no archive, package, lock, or product bytes were edited.

## Runtime Python lookup

- Exact Runtime checkout: /home/user/work/wt/rt-pin-34eac004, HEAD 34eac0041b0891e9011966b39bcbd26053fde5bc; it originally had no .venv.
- Existing supported interpreter: /home/user/work/venv-app2-native/bin/python (realpath /usr/bin/python3.12).
- Operational ignored link added at /home/user/work/wt/rt-pin-34eac004/.venv/bin/python to that interpreter. This satisfies the existing runtimePython() lookup while preserving the exact Runtime checkout used by revisionSet().
- Agent checkout/head: /home/user/work/agent, f894c3c9dda25ab03527eeb7f52da5da31d627c1; Agent and Runtime Python variables both use /home/user/work/venv-app2-native/bin/python.

## Exact suite-row change

Only the existing app ap2-P3-gate5-h6-0348 row in /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf changed. It now:

1. verifies the test-service-created $PWD/node_modules link resolves to /home/user/work/app/node_modules;
2. replaces only that snapshot-owned link with /tmp/w-2b901599a5/ap2-P3-env-repair-0355/private/node_modules;
3. verifies Composition 0.0.14;
4. sets NODE_OPTIONS=--max-old-space-size=4096;
5. sets ASTRID_CHECKOUT=/home/user/work/agent, ASTRID_PYTHON=/home/user/work/venv-app2-native/bin/python, ASTRID_RUNTIME_CHECKOUT=/home/user/work/wt/rt-pin-34eac004, ASTRID_RUNTIME_PYTHON=/home/user/work/venv-app2-native/bin/python, TIMELINE_BUNDLE_AGENT_HEAD=f894c3c9dda25ab03527eeb7f52da5da31d627c1, TIMELINE_BUNDLE_RUNTIME_HEAD=34eac0041b0891e9011966b39bcbd26053fde5bc, and PYTHONPATH=$PWD:/home/user/work/wt/rt-pin-34eac004:/home/user/work/agent;
6. retains the exact original Gate-5 title selector: M2 real gate 5 (M1 real mounted path): Agent edit, lost ACK, newer local gesture, exact retry, restart and undo preserve intent.

## Checks

- Exact selector collection with the original title selector → PASS, exactly 1 test.
- Pinned registry imports from the private package (effects.generated, animations.generated, transitions.generated) → PASS.
- Final harness lookup probe with exact Runtime checkout → PASS: runtimePython() returned /home/user/work/wt/rt-pin-34eac004/.venv/bin/python; revisionSet() returned Agent f894c3c9... and Runtime 34eac004....
- Hosted build with the private graph and NODE_OPTIONS=--max-old-space-size=4096: npm run build:hosted → PASS locally; the central successor also completed npm run build:hosted (5272 modules transformed, built in 53.28s).
- git diff --check and App worktree status → PASS/clean.

## Single central successor

- Requested exactly once: ap2-P3-env-repair-0355-ap2-P3-gate5-h6-0348-1023040206-29980.
- Log: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-P3-env-repair-0355-ap2-P3-gate5-h6-0348-1023040206-29980/log.txt.
- Result: FAIL, exit 1, 60s. Hosted bundle setup passed; Playwright started one selected test but failed at tests/e2e/local/three-products.spec.ts:79 because the pre-repair row omitted required full-SHA TIMELINE_BUNDLE_AGENT_HEAD and TIMELINE_BUNDLE_RUNTIME_HEAD. The afterAll source-tuple mismatch was a consequence of that setup failure (runtimeHead was null under the temporary fixture). No browser journey assertion or Runtime/Agent acceptance ran.
- Setup owner: App Gate-5 harness preflight (three-products.spec.ts:72-87) and the suite row environment. The final row now supplies the exact heads and exact Runtime checkout; no second service run was submitted.

The final row is ready for the manager's next authorized same-case run.
