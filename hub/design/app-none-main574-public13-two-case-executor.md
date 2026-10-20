# App native-None MAIN574/public13 two-case qualification

## Result

The requested central browser lane passed **2/2 real cases** on the committed
MAIN574/public13 App candidate. No App product source or behavior test was
changed by this worker; the only changes were the ORCH suite registration and
an ORCH-only wrapper around the previously proven native-None executor.

Declared source tuple:

- App: commit `38b41fad9e10a9d33f27f540920f7eb8a8bc67ab`, tree `4054ea8fe15f6a87bfc5169c04a0ab944e0c632c`.
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`; 75 artifact files and the pinned producer manifest were checked.
- App Composition: public13, 77 regular files, SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Agent Composition: retained public12, 77 regular files, SHA-256 `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`.
- Tracked public-source attribution: `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`.
- Browser: Chromium 141 at `/opt/pw-browsers/chromium-1194/chrome-linux/chrome`.

The central snapshot used a synthetic App HEAD
`5e7c71835c4e1eb133f954edd8f2550086349f57`. The wrapper accepted that only
after checking the fixed declared App commit maps to the declared tree, then
held the actual snapshot HEAD/source status stable before and after the run.

## Central evidence

Suite literal:

`e2e-native-none-main574-public13-38b41fad-tree4054ea8-agent8130-runtime2c4-v1-e2e-integration`

TestID:

`app-m2-none-main574-public13-two-case-executor-e2e-native-none-main574-public13-38b41fad-tree4054ea8-agent8130-runtime2c4-v1-e2e-integration-1020162608-28121`

Exact request/wait commands:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  app-m2-none-main574-public13-two-case-executor \
  e2e-native-none-main574-public13-38b41fad-tree4054ea8-agent8130-runtime2c4-v1-e2e-integration
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  app-m2-none-main574-public13-two-case-executor-e2e-native-none-main574-public13-38b41fad-tree4054ea8-agent8130-runtime2c4-v1-e2e-integration-1020162608-28121
```

Central result: **PASS, exit 0, 317 seconds; 2 passed**.

Discovery selected exactly two tests:

1. `tests/e2e/local/three-products.spec.ts:1388` — single native `None`: raw transition absence, reload, lost acknowledgement, Runtime restart, exact retry body/key/receipt, inverse, and zero legacy traffic.
2. `tests/e2e/local/three-products.spec.ts:1464` — bulk native `None`: one original-basis atomic clear, opaque/unknown revision preservation, retry/reload/inverse, real 409 conflict with whole draft retained, and zero legacy traffic.

Preflight and postflight passed the Agent8130/Runtime2c4 tuple, public13
App all77 bytes, public12 Agent all77 bytes, Runtime all75 artifacts, peer
versions, 65 pinned Astrid source files, 155 vendor Astrid-browser files,
20 public-import checks, source cleanliness, private cache isolation, and
Chrome141/no override guards. The browser build completed successfully; the
central log contains only existing Vite/PostCSS/chunk warnings.

Existing source qualification remains as reported by the port worker:

- Core targeted Vitest: 8 files, 216 passed.
- Neighbor Vitest: 13 files, 536 passed.
- TrackInspector prerequisite: 3 files, 120 passed.
- Node contract tests, scoped ESLint, diff check, and frozen-source hash checks passed.

## Cut boundary and remaining callers

The stale report that standalone compatibility fallbacks remain is incorrect.
Comparing the actual `ClipTransitionSection` and `BulkClipPanelBody` handlers
to qualified source `46c15aee5fd08aa71a49b0378eb694491f8482da` shows that both
missing-port paths visibly throw (`Transition clear requires an active
timeline command session.` and `Bulk transition clear requires an active
timeline command session.`); the legacy None callback fallback was cut and
must not be restored.

The production None callers are the single
`src/tools/video-editor/components/PropertiesPanel/ClipTransitionSection.tsx`
control and bulk
`src/tools/video-editor/components/PropertiesPanel/BulkClipPanelBody.tsx`
control, reached through the current `PropertiesPanel`/`PropertiesPanelBody`
hosts. Their clear actions use the native scalar/session ports. Remaining
handlers in those files are transition SET, duration, parameter/reset, and
other effect SET paths (`onChange`/`onChangeDeep`); those are outside this
None-clear qualification and must remain until their own native operations
pass. No compatibility writer was restored.

## Scope and limits

The wrapper reused the proven `1020155632-24451` strict native-None runner,
changing only declared App SHA/tree, App public13 package identity/source
attribution, and the stale public12 setup guard. The two real browser
assertion bodies, discovery count, UI/provider path, and source/cache guards
were preserved. No new checker framework was introduced.

No full suite, TypeScript check, install, frame/PCM lane, or integration merge
was run. Root integration remains frozen for independent full/editing work;
this report is source qualification only.
