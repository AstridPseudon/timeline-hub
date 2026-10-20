# ap2-m2-selected-current-record-parity-fix

## Result

PASS for the requested App repair. The existing `clip.set-params` carrier is unchanged. The App session now retains the exact schema-source pin used by the selected PARAM retained read and refuses a changed pin during either prefetch or finish, preserving the draft.

## Implementation

- Changed only `src/tools/video-editor/commands/commitSession.ts`.
- Captured the exact `DocumentPin` after the generation-checked retained read.
- Added visible refusal when a later prefetch or finish supplies a different source pin.
- Preserved original P1, opaque/unmentioned parameters, existing guards, and the App-owned provider join. No new op, wire field, DTO, public pin, catalog lookup, or activation claim was added.

## Fresh parity evidence

Generated fresh `selectedParamsCommand` values from the current App TypeScript source for both fixture cases, then exercised them against the frozen Agent `8130a401bf44a518d5a40ae274d398b8c560be55` provider implementation. The diagnostic harness used fresh command-core fields rather than stale recorder claims.

- Authoritative read paths were exactly: `id`, `clipType`, `clip_type`, `asset`, `asset_id`, `media_id`, `object_id`, `elementRef`, `element_ref`, in that order.
- Fresh record bindings retained the existing `scalar.target` and `params.element` bindings, including `params.schema` and `params.snapshot` dependencies.
- Original P1 was retained; opaque/unmentioned data was preserved while the selected value changed.
- Inverse and redo reproduced the expected post-command document.
- Wrong original pin and same-target stale-head races were visibly refused.
- This is an Agent in-memory diagnostic, not a live Runtime acceptance or browser/socket run.

## Tests

Targeted App tests:

```text
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-transport-assertion-repair/notes/vitest-runner.cjs node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/clipParamsCapture.test.ts src/tools/video-editor/commands/selectedParamAuthority.test.ts src/tools/video-editor/commands/selectedParamPort.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.test.tsx
PASS — 5 test files, 96 tests.
```

Lint, diff validation, and strict island typecheck:

```text
node_modules/.bin/eslint src/tools/video-editor/commands/commitSession.ts src/tools/video-editor/commands/clipParamsCapture.ts src/tools/video-editor/commands/clipParamsGesture.ts src/tools/video-editor/commands/selectedParamAuthority.ts src/tools/video-editor/commands/selectedParamPort.ts src/tools/video-editor/components/PropertiesPanel/AstridElementParams.tsx --report-unused-disable-directives --max-warnings 0 && git diff --check && node_modules/.bin/tsc -p tsconfig.strict-islands.json --noEmit --pretty false
PASS — exit 0.
```

No full, browser, localhost, socket, or live Runtime suite was run, per the task constraints.

## Notes and next steps

The old portable probe was treated as stale evidence and was not relaxed or used as the acceptance record. A private probe was refreshed from the current App command generation and frozen Agent provider behavior. The temporary extracted probe material was cleaned; the final worktree contains only the intended source modification.

The orchestrator should run the cross-repo Runtime acceptance gate when the AppProvider final join is available. This worker makes no activation claim.
