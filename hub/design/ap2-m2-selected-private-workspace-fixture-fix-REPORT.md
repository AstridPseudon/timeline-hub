# app2-m2 selected private-workspace fixture repair report

## Result

Ported the exact reviewed selected DEV source from `tl/ap2-m2-selected-reviewed-current-delivery-and-gate` onto `hub/tl/integration`, including the existing aliases/settings/trim/shared5a behavior and the reviewed selected-param fixture. No product API, provider, store, schema, pin, or shared-dependency changes were made.

Added the app2-owned `run-central-selected-p1.sh` wrapper and synchronized the central named-gate driver. Its private per-run setup now:

- clones the frozen Agent and Runtime sources into the run root;
- creates an isolated Runtime data root and ephemeral realm;
- writes a source manifest for those private checkouts;
- runs the frozen Runtime `workspace create` followed by `workspace inspect`, asserting configured state, realm identity, and readiness;
- uses a per-run door port to avoid unrelated stale Runtime instances;
- leaves the existing graph/archive, tuple, source, credential, cleanliness, and admission guards intact.

The exact preflight command passed twice:

```text
SELECTED_WORKSPACE_PREFLIGHT_ONLY=1 sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh /home/user/work/composition
selected DEV private workspace preflight: ready
```

The preflight used the same frozen Runtime/Agent checkout, Python, source manifest, and workspace create/inspect path as the selected gate. The initial neutral “No workspace is configured” refusal is therefore repaired.

## Verification

Passed:

- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipParamsCapture.test.ts src/tools/video-editor/commands/selectedParamPort.test.ts src/tools/video-editor/commands/selectedParamAuthority.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx`: **6 files, 71 tests passed**.
- `./node_modules/.bin/eslint --no-cache --max-warnings 0 playwright.three-products.config.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx src/tools/video-editor/components/PropertiesPanel/ClipPanelBody.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.tsx tests/e2e/local/support/harness.ts tests/e2e/local/three-products.selected-param-dev.spec.ts`: **passed**.
- `./node_modules/.bin/tsc --noEmit --pretty false`: **passed**.
- `git diff --check`: **passed**.
- `sh -n run-central-selected-p1.sh`: **passed**.
- `git diff --check`: **passed**.
- `sh -n run-central-selected-p1.sh`: **passed**.

The final post-repair named gate was requested once after the final workspace preflight:

```text
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-selected-private-workspace-fixture-fix ap2-m2-selected-real-p1-history-fixture-fix --no-cache) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
result: ap2-m2-selected-private-workspace-fixture-fix-ap2-m2-selected-real-p1-history-fixture-fix-1020232241-8979
app snapshot: 8f0b9b4...
```

It reported **build PASS / list 1**, then started one selected Playwright test. The test reached the real selected fixture `project-pack init`, but no P1 was admitted. The retained sanitized log is:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-selected-private-workspace-fixture-fix-ap2-m2-selected-real-p1-history-fixture-fix-1020232241-8979/log.txt`

The failure is the frozen Agent `workspace_client` attempting to open the reviewed harness token as a credential-file path, then reporting `runtime credential is unavailable`. The source causality is visible in `tests/e2e/local/support/harness.ts`: `selectedParamEnv` sets `ASTRID_RUNTIME_CREDENTIAL` to the provisioned token, while the frozen Agent interprets that variable as a path. This is before P1 admission, so the requested original P1/history, P2/removal/refusal/retry/reload/undo, zeroLegacy, and original post-P2 pin assertions remain unverified.

Two earlier central probes were not unchanged retries: the first exposed a malformed launcher value and the second exposed the default door-port collision. Both were corrected before the final post-repair gate. No full suite, local browser suite, or local socket suite was run directly.

## Decision / blocker

I stopped at the pre-P1 credential failure. Fixing it would require changing the reviewed App harness or introducing an Agent shim, which exceeds this task’s wrapper-only scope and would risk changing the original admission/provenance behavior. No physical fallback cut was prepared because the gate did not pass. The retained central log is the failure trace for the orchestrator’s next decision.

Frozen tuple used by the wrapper:

- Agent commit `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Graph archive SHA `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.
- Composition tarball SHA `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
