# AP2 M2 duplicate current joined deletion gate

## Result

Ported the reviewed duplicate dead-writer deletion and durable real-UI journey onto current App integration 20ea14c26. The candidate is ready for harness commit. The deletion row remains OPEN/PENDING: no central actual-journey result or qualified deletion merge SHA exists.

Changed exactly five App files:

- removed duplicateIndependentShot and its obsolete graph-writer test assertions;
- retained/extended native occurrence-duplicate capture assertions for parent config, copied immutable shot/internal closure, linked reuse, and distinct destination roots;
- added the reviewed real canonical shot-group duplicate journey covering lost ACK, disjoint Agent edit, newer local edit, reload, Runtime restart, exact retry, opaque preservation, guarded undo, and zero legacy traffic.

No commitSession, VideoEditorProvider, recovery implementation, schema/API, dependency, public pin, or shared packet was changed.

## Validation

All commands ran against the dirty candidate worktree with Vitest cache disabled.

- ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/data/shotCompositionEditor.test.ts src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx — 5 files, 70 passed.
- ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts src/tools/video-editor/hooks/useTimelineCommandSession.test.tsx — 5 files, 74 passed.
- ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/data/shotCompositionEditor.test.ts src/integrations/runtime/shotCompositionRuntime.test.ts src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts src/tools/video-editor/commands/occurrenceDuplicateGesture.test.ts src/tools/video-editor/commands/commitSession.occurrenceDuplicate.test.ts src/tools/video-editor/components/AstridTimelineEditor.document-shots.test.tsx — 87 passed, 3 failed in existing popup provider/runtime neighbor cases. First failure: popup add keeps raw child roots... received The shot draft has no unambiguous raw clip counterpart instead of the expected lost-ACK error. The other two fail on existing storedOccurrenceDurationMs draft-shape differences. These are outside the changed duplicate files and App-owned provider/recovery scope; tests were preserved.
- ./node_modules/.bin/eslint src/tools/video-editor/data/shotCompositionEditor.ts src/tools/video-editor/data/shotCompositionEditor.test.ts src/integrations/runtime/shotCompositionRuntime.test.ts src/tools/video-editor/commands/occurrenceDuplicateCapture.test.ts tests/e2e/local/three-products.spec.ts --ext ts,tsx --max-warnings 0 — passed.
- npm run typecheck:strict-probe — passed.
- ./node_modules/.bin/playwright test --config playwright.three-products.config.ts --list --grep 'M2 native occurrence duplicate' — 1 test collected; no browser/socket run.
- git diff --check — passed.
- rg -n 'duplicateIndependentShot' src --glob '!**/*.test.*' — zero production references.

No full suite, localhost/browser/socket execution, or central test was run.

## Central handoff

After the harness commits this clean candidate, run exactly once:

    R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-duplicate-current-joined-deletion-gate e2e-m2-duplicate-three-products) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"

The configured runner uses the reviewed public13 graph, Agent 8130a401bf44a518d5a40ae274d398b8c560be55, Runtime 2c4ac180c2220bdad966bc01e95ad230e99ce26a2, Composition 0.0.13, private caches, and the actual UI grep. Do not run it against this dirty tree or substitute pins. Classify the first failure before any rerun. Only a passing result on the committed candidate permits changing D01-app-duplicate from open/pending to qualified/deleted.

