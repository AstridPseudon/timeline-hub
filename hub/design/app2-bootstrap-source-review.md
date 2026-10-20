# D01-app-bootstrap source handoff review

Status: source-only handoff; no App product/test changes made. No bootstrap row is live. The App status's live D01 transition-none and shot-graph-settings work is separate; this review does not overlap or claim either row.

## Sources and current seam

- App source reviewed: branch `tl/ap2-m2-bootstrap-source-review`, `dcf52eb3943dffb3554f616f6ecd738717e29d74`.
- Reviewed current root: `b1ef4b9b910ba72375c34cf319692f90d22edc25`. `createDefaultTimeline.ts` and `createDefaultTimeline.test.ts` are unchanged between that root and this source-refresh commit.
- Existing native producer: Agent `487ca1e0d74edf4aecdd2b4e045294ab089fc273`, `native_initialize.py` and pristine-initialize provider tests.
- Current paired consumer baseline: Agent `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` + Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, published App contract/schema `0.2.13` / `8de823011a121359b9ad021e283b45afb6baeabc8a154a02bd086d1260a8b8f4`.
- Runtime source candidate for the scoped empty-state preflight: `708df14c75ef739f9e67b2758a571`. This is source evidence, not a matched registered release.

The local-vs-App seam is `src/integrations/runtime/createDefaultTimeline.ts`. Keep its timeline selection, canonical-ID/alias precedence, concurrent Main reassignment, metadata spread/CAS, and retry behavior. Its current writer is `publishEmptyTimeline` (lines 51–81): it calls `AstridRuntimeClient.publishParentComposition` with a fabricated parent revision and App defaults. First-timeline callers are `VideoEditorPage.tsx:477` and `useProjectCRUD.ts:154`; additional-timeline creation is `VideoEditorPage.tsx:567`. They must all enter the same durable create → verified H0 → native init path. Do not infer browser durability from the current unit tests.

## Reusable source already built

1. `commitOutbox.ts` now has strict `reserveCreate`, project-only owner discovery for a pre-URL/random-ID crash, original create request/default retention, and atomic retention of the original `timeline-init` request/result after later ACKs.
2. `bootstrapInitialization.ts` provides `reserveBootstrapInitialization` and unwired `resumeBootstrapInitialization`. It retries the exact persisted create before recapture, verifies the returned H0 pair, requires the sole original bootstrap history/immutable closure, submits the exact three-command batch, proves the accepted receipt/history/closure, and then loads today’s basis.
3. `bootstrapCapture.ts` matches Agent `487ca1e` for `timeline.init` + sequential V1/A1 `track.create`: raw-parent guard, four absence reads, `registry.assets` ABSENT→`{}`, full records, order and created identities. Fixture SHA256 is `2fe871c23c9b1a38ae44d7c1374c8b7a81128a7b320925bd6e4daef4500dea02`.
4. Generated `WorkspaceClient.createTimeline` already exists at `generated.ts:145`. App’s `AstridRuntimeClient` still lacks the narrow wrapper; existing `commitTimeline`, `listTimelineCommits`, `getProjectParentCompositionRevision`, and `RuntimeDataProvider.loadTimelineCommandBasis` are the available contract seam.

## Exact deletion / replacement list

In the qualified consumer cutover:

- Delete `publishEmptyTimeline` and its direct `client.publishParentComposition` call from `createDefaultTimeline.ts`; remove the now-unused `createDefaultTimelineConfig` import and the deterministic parent-revision UUID generation used only by that publisher.
- Replace the two calls at `createDefaultTimeline.ts:93` and `:121` with the retained outbox-backed create/init producer. Retain `createCanonicalTimeline` as the public additional-timeline operation, but change its implementation to the same producer; do not delete the function or its caller.
- Wire `VideoEditorPage.tsx:477`, `:567`, and `useProjectCRUD.ts:154` through the qualified owner claim/recovery path. Preserve the pending additional-timeline ID/name across reload and use project-scoped recovery.
- Rewrite the old `createDefaultTimeline.test.ts` transport assertions that require `/composition-revisions` to assert the normal create and `/commit` sequence, exact keys/bases, H0 verification, and zero bootstrap publisher traffic. Do not remove or weaken the seven original positive bodies.
- Do not delete `AstridRuntimeClient.publishParentComposition` globally: other legacy App writers still use it. The deletion is the bootstrap consumer in `createDefaultTimeline.ts), followed by direct retired-writer rejection in the qualified central cutover.

## Prerequisites and hold

The current Agent/Runtime pair has no registered semantic `timeline.init`; the generated create operation alone is insufficient. The prerequisite producer is Agent `487ca1e`, which needs a matched additive Agent/Runtime release preserving the current 22-operation contract and registering the init provider. Runtime must also provide the constrained same-ID truly null/no-head repair. Runtime `2c4ac`’s `adopt_empty_shell` path is not proof for the existing null-head positive; it rejects no-row/null-head cases. The `708df14` scoped `timeline_scope_is_empty` source check addresses corrupt same-project orphan content but is not, by itself, a qualified consumer pair.

There is one explicit qualification hold: Agent `487ca1e` records the whole raw parent as an input. The four unrelated-parent-opaque inverse vectors therefore fail with `inverse_dependency_changed`; the existing strict xfails preserve the original successful expectations. Do not call these xfails release evidence, delete them, or add a broad inverse bypass. Agent/owner policy must resolve this before activation.

## Original seven positives to preserve

1. Reuse an existing headed timeline without applying defaults.
2. Fresh project creation with canonical defaults.
3. Same-ID headless/null-head shell repair without a duplicate.
4. Reassigned Main pointer wins over a timeline named `main`.
5. Concurrent metadata/CAS update preserves chat and unrelated metadata.
6. Additional named timeline creation with its own stable idempotency key.
7. Lost-response retry replays the identical publication request.

The current test also retains the opaque-headed no-defaults positive and newer alias/CAS safety cases; those remain required.

## Evidence

Executed:

```sh
node node_modules/vitest/vitest.mjs run --config /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-bootstrap-source-review/vitest.config.mjs --configLoader=runner --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/createDefaultTimeline.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/integrations/runtime/bootstrapInitialization.test.ts
```

Result: exit 0; 3 files passed, 95 tests passed. The first attempt with the repository config stopped before collection because `--configLoader=runner` exposes the existing config’s `__dirname` as undefined; no tests ran in that attempt. The private config changed no shared dependency or cache.

Also executed:

```sh
git diff --check
```

Result: exit 0; repository worktree remains clean.

Not run: full, browser, socket, real Runtime Door, process-restart, or central suite. The prior 27 native/provider passes and four strict opaque-inverse xfails are historical source-refresh evidence, not fresh evidence from this review.

## Acceptance commands after the matched release

1. Re-run the exact targeted Vitest command above after wiring the wrapper/callers, with the original seven assertions retained.
2. Run the qualified Agent native/provider lane against the frozen `487ca1e` successor:
   `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=<qualified-agent-checkout> <agent-venv>/bin/python -m pytest -q tests/editing_conformance/test_pristine_initialize.py tests/sdk/test_timeline_pristine_initialize_provider.py`.
3. Orchestrate the named normal-Door/App journey that proves create/H0/init exact retry, changed-key refusal, null-head repair, restart/reload, later edit/undo/equal-byte restore, and zero `composition-revisions` bootstrap traffic. This worker did not run that browser/socket lane.

Recommendation: keep D01-app-bootstrap OPEN. Merge the reusable source only after the matched Agent/Runtime release and null-head qualification; then perform the single consumer cutover and delete the local publisher in the same change.

