# App2 element final native review

## Verdict

**APPROVE SOURCE** at candidate `01f891ab66a5f27b4b7a9823e6f4ddee83807eaf` (`fix(app): align element PARAM capture with native reads`), compared with base `05b6b488d`.

The consumer/row remains **HOLD** as required. This review does not approve consumer wiring, whole-element-row behavior, or retirement of overlay, transition, apply, remove, fade, entrance, or exit families.

## Scope and source review

- `git diff --name-status 05b6b488d..01f891ab66a5f27b4b7a9823e6f4ddee83807eaf` contains only:
  - `A src/tools/video-editor/commands/elementCapture.ts`
  - `A src/tools/video-editor/commands/elementCapture.test.ts`
- The helper preserves the native literal existing-clip boundary: stable target identity, occurrence/source binding, both `elementRef` and `element_ref` reads, explicit clears, unchanged writes, opaque parameter preservation, and exact recorded claims.
- Asset-backed PARAM capture reads the bound registry leaves in native order: `media_id`, `object_id`, `digest`, `content_digest`; the changed-registry guard is retained.
- Selected project-pack element and PARAM capture refuse without authoritative Agent capture and leave the input draft unchanged. The focused test checks both refusals and snapshot equality.
- No consumer imports/wiring or broader element-operation family appears in this two-file source delta.

## Evidence

1. `./node_modules/.bin/vitest run --no-cache --config config/testing/vitest.config.ts --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/elementCapture.test.ts src/tools/video-editor/commands/clipMoveCapture.test.ts src/tools/video-editor/commands/trackLabelCapture.test.ts`
   - **3 files, 155 tests passed**.
2. `./node_modules/.bin/eslint src/tools/video-editor/commands/elementCapture.ts src/tools/video-editor/commands/elementCapture.test.ts --report-unused-disable-directives --max-warnings 0`
   - **passed**.
3. Actual TypeScript commands were regenerated from this candidate with the frozen Agent `recipe_m2_clip_set_element.json` bundle, using a literal element path and an asset-backed PARAM path. The asset registry included all four guarded leaves.
4. Each generated command was submitted unchanged to Agent 310e5484 using `validate_command` and `execute`, then compared independently against the TypeScript command, full record, and resulting bundle:
   - element: `validate=accepted execute=accepted command_exact=True record_exact=True bundle_exact=True`
   - asset-backed PARAM: `validate=accepted execute=accepted command_exact=True record_exact=True bundle_exact=True`
5. The independent native read sequences included both aliases on both paths. PARAM additionally included all four registry guards before PARAM writes.

Exact parity commands used (temporary probe files were outside the worktree and removed afterward):

```sh
node --import /home/user/work/app/node_modules/tsx/dist/loader.mjs /tmp/element-final-native-probe.mjs > /tmp/element-final-native-probe.json
AG=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-native-parity-environment/agent-ordinary
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$AG" /home/user/work/venv-app2-native/bin/python /tmp/element-final-native-compare.py /tmp/element-final-native-probe.json
```

## Limits

No full, browser, localhost/live-socket, Runtime, consumer, whole-element-row, package/dependency, shared-environment, pin, generated-file, or source mutation was run or made. Targeted TypeScript compilation was not rerun because this final brief requested focused Vitest/ESLint plus independent Agent parity only; the prior repair report recorded its targeted check as passing.

