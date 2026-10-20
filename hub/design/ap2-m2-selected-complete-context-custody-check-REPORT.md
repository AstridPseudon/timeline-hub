# Selected complete-context custody check

## Verdict

**APPROVE** `eee191c1fe5c5bf2625ab640f17923ddabaab000` (`test(app): bind selected Agent credential to issuing Runtime`) for the exact two-file fixture scope.

No App source was changed in this review worktree. The candidate changes only:

- `tests/e2e/local/support/harness.ts`
- `tests/e2e/local/support/selected-param-credential.test.ts`

The selected journey spec and neighboring `tests/e2e/local/support/astrid.ts` are unchanged. Candidate tree: `f091e263dc9367f64117488978f1c19df6c5c295`; integration base: `f54cd98ed91de213763b196e4ed770b557897a8b`.

## Causal custody trace

Frozen Agent `8130a401bf44a518d5a40ae274d398b8c560be55` has the required behavior:

1. `astrid/core/element/project_packs.py:66` calls `AstridClient.open_from_launcher(start_pack_host=False)`.
2. `astrid/sdk/client.py:345-363` consumes the complete all-or-nothing `ASTRID_TIMELINE_EVAL_ENDPOINT`, `..._CREDENTIAL`, `..._REALM_ID`, and `..._ACTOR_ID` quartet and passes it to explicit `AstridClient.open()`.
3. That explicit path resolves the credential file, calls normal Runtime health, then handshake, and validates protocol/schema plus the expected realm and actor (`client.py:277-305`).
4. The original ambient launcher branch instead used the wrapper Runtime selected through its data root/discovery and read the selected file only afterward. Thus token T issued by DirectHarness Runtime A was sent to neutral wrapper Runtime B, whose credential store did not contain T, yielding the observed `401 invalid bearer credential`.

The candidate repairs the binding at `harness.ts:42-53`: the same DirectHarness target supplies ordinary endpoint/file carriers and all four timeline-evaluation carriers. `seedSelectedParamDev()` restarts authoring first, then provisions actor `astrid-selected-param` through the current `runtimeUrl` and uses the resulting file path (`harness.ts:638-651`). The provisioner’s unchanged code sends generated token T to `${runtimeUrl}/v1/credentials` and writes that same T as `{token, actor_id}` with mode `0600` (`harness.ts:566-581`). T is not copied into the child environment; only the file path is.

The new issuer control verifies the provision POST URL is Runtime A, overrides stale wrapper endpoint/credential/realm/actor values, preserves the product `WORKSPACE_RUNTIME_TOKEN_FILE`, and confirms the selected file actor and mode. The frozen resolver rejects non-regular or symlinked credential paths (`workspace_client.py:124-173`); the harness creates the credential under its private `mkdtemp` root with `0600`, and teardown removes that root.

Browser transport remains unchanged at `harness.ts:727-734`: Vite receives `VITE_WORKSPACE_RUNTIME_URL` and `WORKSPACE_RUNTIME_TOKEN_FILE` for the product credential, plus the expected product actor/realm/instance. The selected Agent file is carried only in the child/server environment. No auth bypass, new credential/provider/endpoint, or shim was added, and no token is provisioned into another realm.

## Evidence

Executed against a temporary archive of the candidate branch (shared `node_modules` was symlinked read-only and removed afterward):

- `node --import tsx tests/e2e/local/support/selected-param-credential.test.ts` — **3 passed** (two original file/cleanup controls plus the issuer-binding control).
- Existing App controls via Vitest — **6 files, 71 tests passed**:
  `clipParamsCapture.test.ts`, `selectedParamPort.test.ts`, `selectedParamAuthority.test.ts`, `AstridElementParams.test.tsx`, `AstridElementParams.mounted.test.tsx`, `PropertiesPanel.test.tsx`.
- Targeted ESLint on `harness.ts`, `selected-param-credential.test.ts`, and `three-products.selected-param-dev.spec.ts` — **passed**.
- `tsc --noEmit --pretty false` — **passed**.
- Playwright collection for `three-products.selected-param-dev.spec.ts` — **1 test in 1 file listed**.
- `git diff --check hub/tl/integration...tl/ap2-m2-selected-handshake-authority-binding-source` — **passed**; exactly the two allowed paths differ.
- Selected journey spec tree hash is unchanged: both refs `cb234102db1e913233a6d413024ad0a96947be8e`; SHA-256 `2cd9703de2282282a477f5661d600049c8507fb93df1ef0424a06e7978a8b6a0`.

No browser, live socket, request-test, full suite, or real selected P1/P2 journey was run, per task scope. Those remain the orchestrator’s next qualification step.

