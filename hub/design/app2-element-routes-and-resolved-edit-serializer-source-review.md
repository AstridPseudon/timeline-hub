# App2 source handoff review: element routes and resolved-edit serializer

## Pins and overlap

Reviewed the settled plan, `hub/status/app.md`, and `design/app2-source-handoff.md`. The reviewed App source is `tl/ap2-m2-elements-serializer-source-review` at `41fff23a29f13bd9aede6343592ffba8adebe1a3` (same tree as `tl/integration`). The current Agent command contract checked is `tl/integration` at `dab91714fc8c1923eb787c83954eb44551d11780`.

No live App2 row was reimplemented. App-owned live rows `transition-none` and `shot-graph-settings` were skipped. `commands/media.ts` and browser replacement/sequence callers also consume the resolved-config path; they are overlap with parent/media or other rows, not deletion targets for this handoff.

## D01-app-element-routes

### Existing path and contract

The direct write path is:

1. `src/tools/video-editor/components/ElementsLibraryPanel.tsx` calls `elementOperationAdapter.execute(...)` for `timeline.apply_element` and `timeline.apply_transition`, passing selected catalog `{id, kind, revision, packId}` but no command or schema pin.
2. `src/tools/video-editor/runtime/element-adapter.ts:createElementTimelineRoutes` loads the whole config/registry and saves it through `saveTimelineAtHead` (immutable-head CAS when available), otherwise numeric `saveTimeline`.
3. `AstridElementOperationAdapter:executeTimelineMutation` checks the captured head and numeric config version, calls local `applyTimelineOperation`, then saves the entire config/registry/bundle.
4. `VideoEditorProvider.tsx` constructs this adapter in the AgentChat bridge and exposes it through `AgentChatEditorContext`. `src/shared/contexts/AgentChatContext.tsx` is therefore a shared type seam.

`applyTimelineOperation` is the dead-end local implementation: it creates overlay IDs, writes `elementRef`/`entrance`/`params`, removes refs, and applies transition/fade fields. This is not the current Agent-native command contract.

At Agent `dab91714`, the reusable native element operation is `clip.set-element` v1 (`astrid/core/timeline/schema/edit-command.schema.json`, `ClipSetElementArgs`; implementation `astrid/sdk/timeline/_clip_scalar_commands.py:clip_set_element`). It replaces an existing clip’s `elementRef` with the same `id`, `kind`, and pack owner. An admitted pack reference requires the exact retained `schema_source` `DocumentPin`; an unqualified ref cannot carry `schema_source`. `clip.set-params` is separate (`_scalar_commands.py`) and accepts literal top-level set/clear keys while preserving unmentioned keys. Neither operation creates/removes an overlay, applies a transition, or changes clip placement. The current panel’s `timeline.apply_element`/`timeline.apply_transition` operations therefore cannot be claimed as native command-backed behavior.

### Minimal replacement and seam

Keep the catalog, authority/editability checks, and provider context. Add a narrow App-owned producer through the existing `useTimelineCommandSession.ts` / `commitSession.ts` path: capture the scoped clip identity, original exact `elementRef`, exact `schema_source` pin when applicable, and literal params; produce Agent `clip.set-element` and/or `clip.set-params`; preview with the same command patch; enqueue through Runtime `/v1` `commitTimeline`. Do not derive the command from the resolved whole document or silently turn unsupported apply/overlay/transition/remove actions into a whole-document save.

The shared seam requires agreement before editing: `VideoEditorProvider.tsx`, `src/shared/contexts/AgentChatContext.tsx`, `useTimelineCommandSession.ts`, `commands/commitSession.ts`, `hooks/useTimelineCommit.ts`, `commands/types.ts`, `data/DataProvider.ts`, and Runtime’s `integrations/runtime/dataProvider.ts`. App owns the session/commit plumbing; Agent owns operation schema, inverse/rebase, and raw reference/parameter semantics. The current adapter route’s `saveTimelineAtHead` CAS is a compatibility fallback, not the one-writer command path required by Gates 5/6.

Frozen R4 App (`origin/codex/handover-timeline-r4-20261019-candidate-app-qualified`, `8f0c2484463e9b666d184a744d52e252984e551a`) contains concrete precedent in `semanticGestures.ts` and its typed element-reference command helpers, including command receipt/retry handling. It is useful as shape only: the current Agent contract and current App source differ, so those helpers must not be copied without aligning to `clip.set-element` and the current session/outbox.

### Deletion order / closure

1. Agree and qualify the command producer for existing element references and params; separately decide the missing Agent operations for apply/overlay/transition/remove.
2. Migrate panel ingress and AgentChat callers to command preview/commit/reload, preserving the existing adapter tests until equivalent command tests exist.
3. Remove the corresponding branches from `applyTimelineOperation`; then remove `AstridElementOperationAdapter:executeTimelineMutation`.
4. Remove `createElementTimelineRoutes`, `ElementTimelineRoutes`, and the adapter-only error/types/imports from `element-adapter.ts`; then remove the direct adapter field/type from the AgentChat context and provider only after no callers remain.
5. Verify Gate 5 retry/reload/undo behavior and Gate 6 zero element-path `saveTimelineAtHead` traffic before deleting the old route tests. Do not infer browser durability from these unit tests.

The actual closure blocker is Agent capability coverage: current native commands close revision replacement and params only, not the full panel operation set. A full row handoff needs a qualified producer revision for the remaining operations or an explicit supported/refused boundary; it must not retain a whole-document fallback while claiming Gate 6 closure.

## D01-app-resolved-edit-serializer

### Existing path and callers

`src/tools/video-editor/lib/serialize.ts:serializeResolvedTimelineEdit` takes a resolved projection, removes its resolved registry, preserves authored opaque roots and an authored registry root when present, then delegates to `serializeForDisk`. It is a compatibility serializer for a whole resolved document, not an EditCommand.

There are three direct callers:

- `src/tools/video-editor/commands/runner.ts:applyTimelineCommandEffect`, the `resolved-config` mutation branch;
- `src/tools/video-editor/hooks/useTimelineCommit.ts:applyEdit`, the `config` mutation branch that schedules the actual save;
- `src/tools/video-editor/lib/timeline-mutation-engine.ts:previewTimelineMutation`, the `config` preview/apply branch.

The current tests intentionally cover authored registry and opaque-root preservation in `serialize.test.ts`; those expectations are compatibility evidence and must not be weakened into refusal tests.

### Minimal replacement and deletion order

Each producer should emit a command plus a local projection from that command. The runner and mutation engine should consume that projection rather than reserialize an arbitrary resolved config. `useTimelineCommit` should enqueue the command through the existing commit session and stop scheduling a whole-document save from the resolved projection. Keep `serializeForDisk` and other domain serializers if still used.

Convert all `config`/`resolved-config` producers first, explicitly inventorying the media swap and browser replacement/sequence overlap. Then remove the three imports/calls above. Only after no producer or preview depends on the old mutation unions should App remove the `resolved-config`/resolved-`config` mutation variants from `commands/types.ts` and `useTimelineCommit.ts`; delete `serializeResolvedTimelineEdit` last. Preserve the existing opaque-root/registry behavior in command-equivalent authored-document tests.

The local-vs-App seam is exact: Agent supplies command schema, raw base/revision, inverse, and rebase; App’s command session supplies preview, outbox, retry, and Runtime `/v1` commit. The resolved serializer cannot be the payload for that writer. `useTimelineCommandSession.ts`, `commands/commitSession.ts`, and `DataProvider.ts` are shared App-owned seams and require agreement before this row changes them.

## Acceptance commands

These are the smallest useful checks for the eventual implementation; the Agent command checks are prerequisite producer evidence, not evidence of browser durability:

```sh
npx vitest run --no-cache --config config/testing/vitest.config.ts \
  src/tools/video-editor/runtime/element-adapter.test.ts \
  src/tools/video-editor/components/ElementsLibraryPanel.test.tsx \
  src/tools/video-editor/lib/serialize.test.ts
```

```sh
PYTHONPATH=/home/user/work/agent /home/user/work/venv-agent/bin/python -m pytest -q \
  /home/user/work/agent/tests/editing_conformance/test_recipe_clip_set_element.py \
  /home/user/work/agent/tests/sdk/test_timeline_clip_scalar_provider.py
```

The Vitest command passed here: 3 files, 49 tests passed. The requested runner form (`--configLoader=runner`) was also attempted but cannot load this repo config because `__dirname` is undefined in the runner’s ESM evaluation; no config or dependency was changed. The Agent command was not run by this source-only review. No full, browser, socket, or live-runtime suite was run.
