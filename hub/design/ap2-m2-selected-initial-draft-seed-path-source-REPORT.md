# AP2 M2 selected initial-draft seed path source

## Result

Fixed the selected fixture's setup order in `tests/e2e/local/support/harness.ts`.
The existing `compositionPublication` initial draft is now accepted before the
authoring-profile restart. The selected credential is issued and bound to the
current Runtime only after that restart, then the existing project-pack
admission and native Agent producer establish accepted P1.

No production writer, endpoint, profile-at-save change, tracked-publication
guard bypass, synthetic history, fake success, or new source pin was added.

## Normal source proof and old/new setup map

The ordinary harness path is `DirectHarness.start()` → `seedRuntime()` at
`tests/e2e/local/support/harness.ts:473`, followed by callers' explicit
`enableTimelineAuthoring()` (for example the existing ordinary three-products
journey). `seedRuntime()` uses the shared `compositionPublication()` helper
against the normal Runtime publication route.

Before this change, `seedSelectedParamDev()` called
`enableTimelineAuthoring()` first, then posted its initial selected draft to
`composition-revisions`. That made the initial raw fixture a tracked-profile
publication and produced the expected `timeline_commit_required` refusal before
P1.

The new causal order is:

| Stage | Before | After |
| --- | --- | --- |
| Initial selected draft | authoring restart, then raw publication | raw `compositionPublication` publication at lines 656–661 |
| Initial carrier | `draft-1`, no `packId` | unchanged: `draft-1`, no `packId`, no P1 history |
| Authoring profile | first operation | restart at line 665, after initial draft acceptance |
| Selected issuer | before fixture setup | provisioned at line 666 through the post-restart `runtimeUrl`; existing all-carrier binding remains unchanged |
| Pack/P1 | after credential, but after the refused draft | after restart and credential: `project-pack init`/admit at lines 676–687, then existing Agent `update-element` at lines 690–692 |
| Accepted P1 provenance | native `clip.set-element` + `clip.set-params` assertion unchanged | unchanged; history is still read only after the real Agent command |

The initial payload, raw clip/config/registry shape, order, and downstream
P1/P2/refusal/retry/reload/undo assertions were preserved. P1's exact
`DocumentPin` is still resolved only after accepted P1 history; no phantom pin
is introduced in the initial draft.

## Checks

Passed:

- Offline causal/provenance control: verified source order
  `initial draft → authoring restart → selected issuer → project-pack admission → P1`
  and verified the initial carrier is `draft-1` without `packId`.
- `node --import tsx tests/e2e/local/support/selected-param-credential.test.ts` — 3 passed.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipParamsCapture.test.ts src/tools/video-editor/commands/selectedParamPort.test.ts src/tools/video-editor/commands/selectedParamAuthority.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx` — 6 files, 71 passed.
- `./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/support/harness.ts tests/e2e/local/support/selected-param-credential.test.ts tests/e2e/local/three-products.selected-param-dev.spec.ts` — passed.
- `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- `./node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list` — exactly 1 test collected.
- `git diff --check` — passed.

Not run by instruction: browser execution, localhost/live sockets, request-test,
full suite, or the real selected P1/P2 journey. Those require the custody
review/central qualification step.

