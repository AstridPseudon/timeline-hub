# A2 D141 REG — blocked at exact reader contract seam

No candidate or source diff. Frozen base and all test assertions/mocks remain byte-exact. The finite productREG classification is accepted and reproduced: 2 expected, 3 observed. This report does not relitigate that decision and does not assert duplicate-output corruption.

## Why no safe scoped patch was authored

The real editor calls `duplicateShotGroup` with its selected timeline/configVersion (`AstridTimelineEditor.tsx:348-363`). The byte-identical production caller (`015ce2d5f182ed711ba51ea8f8bb44af7edd2d0a`) then:

1. Calls `loadTimelineDocument` (`shot-group-pack-commands.ts:388`), checks the actual numeric `expectedVersion`, resolves final-video media, and optionally awaits a pack task.
2. Calls `mutateTimelineDocument` (`:410`) with the same explicit target. Placement loads the verified canonical command basis (`placementService.ts:252`), validates the complete pinned closure (`:256`), and freshly observes both revision/publication (`:259-263`) before creating a durable owner/intent.
3. Captures through `createPlacementLocalSaveHandoff`, persists through `LocalSaveSession`, and sends via `provider.commitTimeline` (`placementService.ts:278`). Accepted/recovered canonical closure remains the authority. No old writer is involved.

The original caller read cannot substitute for a basis: `LoadedTimeline` supplies display config, provider-local numeric configVersion and an optional head, but no full canonical closure/history. The original test's head has no publication pin. The basis reader supplies canonical closure and exact pair but no numeric display version. `loadTimelineCommandBasis` itself reads history before immutable closure assembly; it does not observe the live head after asynchronous authoring validation. Thus merely keeping one basis call does not preserve the existing local staleness gate.

With the currently exposed and immutable mocked reader contracts, preserving the numeric caller preflight + complete closure validation + fresh revision/publication comparison requires the three observed counted loads. The registry read has no head/closure to reuse. Neither target configVersion nor history length may be invented as the actual numeric version. Reconstructing an empty canonical closure from display config is forbidden. A module cache would offer no cold-call or cross-await freshness proof. Moving the gate into Runtime rejection changes the existing pre-intent retry/no-owner behavior; it is not equivalent.

The existing Workspace v1 suite passed all 16 cases, including two stable-read pairs on bounded retry, no durable intent on repeated local staleness, exact original request/key recovery, definitive dependency/binding/value/selection/atomic/stale-head refusal, and adoption of recovered closure before later placement. No guard was weakened or test changed.

## Exact seam to allocate

An orchestrator decision is needed on a reader-interface change **outside this brief**:

- `src/integrations/runtime/dataProvider.ts:886-991` (`loadTimelineCommandBasis`) and `:996-1016,1442-1522` (`loadTimeline`/`readTimelineInOrder`): expose one authenticated read result that ties the complete canonical basis to the same provider-local display/version observation, with an explicit fresh post-validation pair observation or a caller-owned checked continuation. Do not infer version from commit count or publication text, and do not manufacture pins.
- Corresponding public read result types in `src/tools/video-editor/data/DataProvider.ts:60-65,95-106` if required. Both files are outside allowed scope.
- The protected original mock currently implements only separate display and basis readers (`shot-group-pack-commands.test.ts:33-67`). A real combined read/cheap current-pair API cannot be invoked through that mock without an interface-support addition to its setup. Its byte-exact requirement currently forbids even that addition. Preserve its original input, every assertion, and loads=2; any exception must come from the orchestrator, not this worker.

This is an allocation seam, not a speculative patch proposal or an authorization to broaden source work. A future author must prove the ordering and cold-call caller wiring, then obtain independent review. The reviewer may find a smaller safe design; none was established here.

## Proof and handoff status

See `validation.md`: actual targeted run 21/22 PASS with exact D141 RED; app/node types, lint and diff check PASS. No full, browser, profile or unrelated own-failure investigation. `source-manifest.json` records base parents/tree and exact unchanged blobs. `guard-map.json` identifies preserved guards; `affected-proofs.json` records finite controlling receipts and contingent P1/P2/P3 reproof requirements.

No candidate head/tree exists, so no proof receipt is invalidated by this worker and no merge/review request is filed. Harness must record final Git identity only if it creates a future candidate; no direct Git write was attempted. All private/raw evidence is unchanged. D130 remains an absolute hold; D141 B022/Element/SWAP/profiling/other-own-failure stops remain.
