# AP2 M2 selected complete-context real gate

## Result

Blocked: the single authorized central DEV gate did not reach P1 admission.
No App source changes were made in this worker; the approved custody source was
already present at `eee191c1f` and the effective harness uses its exact
`selectedParamCliEnv` helper.

The helper binds `ASTRID_RUNTIME_ENDPOINT`, `ASTRID_RUNTIME_CREDENTIAL`, and
all existing `ASTRID_TIMELINE_EVAL_*` carriers to the same `DirectHarness`
Runtime endpoint, realm, actor, and 0600 credential file. The browser product
transport remains on its existing product credential file. Selected fallback
writers remain absent.

## Evidence

Passed:

- `node --import tsx tests/e2e/local/support/selected-param-credential.test.ts`
  — 3 passed.
- `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipParamsCapture.test.ts src/tools/video-editor/commands/selectedParamPort.test.ts src/tools/video-editor/commands/selectedParamAuthority.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx src/tools/video-editor/components/PropertiesPanel/AstridElementParams.mounted.test.tsx src/tools/video-editor/components/PropertiesPanel/PropertiesPanel.test.tsx`
  — 6 files, 71 passed.
- Targeted `eslint --no-cache --max-warnings 0` over the selected harness,
  journey, command, and PropertiesPanel paths — passed.
- `./node_modules/.bin/tsc --noEmit --pretty false` — passed.
- `git diff --check` — passed.
- `node_modules/.bin/playwright test --config playwright.three-products.config.ts tests/e2e/local/three-products.selected-param-dev.spec.ts --list`
  — exactly 1 test selected.
- `SELECTED_WORKSPACE_PREFLIGHT_ONLY=1 sh .../run-central-selected-p1.sh "$PWD"`
  — private workspace preflight ready.

The one requested cache-disabled central run was:

```text
request-test ap2-m2-selected-complete-context-real-gate ap2-m2-selected-real-p1-history-fixture-fix --no-cache
```

Result ID:
`ap2-m2-selected-complete-context-real-gate-ap2-m2-selected-real-p1-history-fixture-fix-1021000131-494`

The hosted build passed and collection selected one test. The test then failed
while `seedSelectedParamDev` tried to publish the initial draft fixture through
`POST /v1/projects/{project}/timelines/{timeline}/composition-revisions`:

```text
409 conflict: timeline_commit_required
tracked timeline publication requires a timeline command
```

Therefore the real project-pack init/admit, accepted P1 set-element/set-params,
P2/removal/refusal, lost-ack/restart/exact-retry/reload/undo, and zero-legacy
checks are unverified. The failure is before browser editing and does not test
selected authority behavior.

Bounded sanitized evidence retained by the central wrapper:

- result log: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-selected-complete-context-real-gate-ap2-m2-selected-real-p1-history-fixture-fix-1021000131-494/log.txt`
- trace directory: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/central-trace`

The wrapper removed its temporary run root. No secrets were copied into the
report. No retry, code change, full suite, local browser/socket run, new pin,
schema, provider, or shim was added.

## Decision and next step

Per the brief, I did not retry or change the fixture after the gate failure and
did not perform a fallback cut. The central fixture and the frozen Runtime
currently disagree on the accepted write path; the orchestrator should resolve
that prerequisite before authorizing another selected DEV gate.
