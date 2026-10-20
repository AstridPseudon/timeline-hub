# D08 normal-render explicit-theme producer blocker

Status: source-backed blocker recovered from the completed
`vw-m3-normal-render-admitted-theme-producer-packet`. No App product patch is
possible on the current source: the normal App/Runtime admission has no
retained immutable `theme.json` bound to Agent's existing named `theme` input.
The Agent consumer-side carrier already exists.

This report is based on the prior worker's `COMMAND` and source-inspection
output in its `log.txt`, not on that worker's short `report.md` summary.

## Exact source identities

The prior trace inspected these source trees:

| Area | Source SHA | Owner-relevant source |
| --- | --- | --- |
| App | `a12b19be56816112da9b16cd8db4c48f9c5c399b` | `src/tools/video-editor/lib/renderRouter.ts` and normal preview/render callers |
| Agent | `384918908aa8c75229c2b6ccdd8fda03b7ce24a1` | `astrid/packs/rendering/actions/render/task_adapter.py`, rendering backend, Remotion preparation |
| Runtime | `e8a24e301c2d5fed7ac5a9d10c7ec226e11199d8` | `runtime_protocol/store.py` managed render admission |

The exact commits were verified read-only with `git show -s --format='%H %s'`.

## Existing boundary, with source evidence

1. App preview has the selected config/fact, but no retained theme artifact.

   - `src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.ts:53-84`
     chooses the projection fact and returns the paired projected config.
   - `src/tools/video-editor/hooks/useRenderState.ts:582-599` makes the
     selected composition resolution the render config and derives render
     metadata from it.
   - `src/tools/video-editor/compositions/installed-themes.ts:90-105`
     resolves the installed theme over `DEFAULT_THEME` and deep-merges
     `theme_overrides`. This is a local preview value, not a retained Runtime
     object.

2. App's normal render producer emits only a theme slug and media identities.

   - `src/tools/video-editor/lib/renderRouter.ts:709-718` defines
     `AstridRuntimeRenderTimelinePayload.theme_id` but no theme bytes or theme
     object identity.
   - `src/tools/video-editor/lib/renderRouter.ts:852-883` sets
     `theme_id: defaultThemeId(outputConfig)` and derives
     `input_object_ids` from managed timeline media only.
   - `src/tools/video-editor/lib/renderRouter.ts:940-977` builds the Runtime
     admission with `input_object_ids: []`; its params contain `timeline_ref`,
     selector, output name, and canonical metadata, but no named theme input.
   - `src/tools/video-editor/hooks/useRenderState.ts:900-916,934-938` passes
     the selected `renderConfig` to this producer and enqueues the resulting
     request.

   `theme_id` is therefore metadata only. It cannot identify the resolved
   nested theme document that preview used.

3. Runtime freezes the canonical timeline closure, but no theme document.

   - `runtime_protocol/store.py:1709-1773` resolves the project-scoped
     `timeline_ref`, rejects caller-supplied `timeline`, `assets_registry`,
     `materialized_root`, `materialized_objects`, snapshot, and authority
     fields, and establishes Runtime ownership of those inputs.
   - `runtime_protocol/store.py:1935-1955` loads the retained parent payload's
     `config` and `registry`.
   - `runtime_protocol/store.py:2003-2065` derives only registry asset media
     identities and prepared scene objects for the managed input closure.
   - `runtime_protocol/store.py:2103-2140` records timeline authority,
     `timeline_ref`, and `timeline_authority`; the only copied parameter
     bindings are `selector`, `profile`, and `output_name`. There is no
     retained resolved-theme document or `theme` materialization binding.

4. Agent already has the exact existing named carrier.

   - `astrid/packs/rendering/actions/render/task_adapter.py:215-247`
     reads `materialized_objects["theme"]`, requires an admitted regular file
     named `theme.json` beneath the host materialization root, and returns the
     host-admitted path unchanged. It refuses symlinks, outside-root paths, and
     other filenames.
   - `astrid/packs/rendering/actions/render/task_adapter.py:332-366` reads the
     host materialization map and obtains the admitted theme path before
     staging the registry.
   - `astrid/packs/rendering/shared/rendering_backend/__init__.py:89-123`
     uses the runtime-materialized theme as the base, merges authored nested
     overrides, and uses the Agent builtin only when no runtime theme path is
     supplied. The timeline slug is not a filesystem lookup authority.
   - `astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:167-177`
     passes `theme_path` to `_resolved_theme_for_render()` and places the
     resulting value in `merged_props["theme"]`.

The missing link is upstream of this existing Agent consumer: no current
normal App/Runtime source produces the immutable `theme.json` object and binds
it to the named `theme` materialization.

## Ownership and smallest existing-carrier action

Owner: the normal App/Runtime render-admission producer, coordinated at the
App call site `enqueueAstridRuntimeRenderTimeline()` and Runtime's
`_freeze_managed_render_inputs()`. Agent is the downstream consumer and does
not need a new resolver or DTO for this blocker.

Smallest action: from the same selected config/fact/profile/revision that the
preview uses, bind the resolved Theme document to the existing immutable
Runtime-managed object path under the existing named input `theme`, so the
host receives `materialized_objects["theme"]` pointing to that exact admitted
`theme.json`. Preserve the existing `timeline_ref`, canonical authority,
revision pairing, and materialization validation. Once that carrier exists,
Agent's current task adapter and Remotion preparation consume it unchanged.

This does not authorize a new DTO, Runtime endpoint, store, resolver, slug
lookup, mutable-latest read, caller-supplied path, copied `DEFAULT_THEME`, or
an invented retained-object field. Adding only `theme_id` to the current App
request would not close the boundary and would lose explicit runtime-pinned
themes and nested overrides. The implicit no-pin path remains Agent's builtin
authority.

## Evidence and limits

Recovered prior worker evidence:

- `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 src/tools/video-editor/lib/renderRouter.test.tsx src/tools/video-editor/compositions/TimelineRenderer.sequence.test.tsx`
  — 2 files passed, 121 tests passed.
- `git diff --check` passed and the prior App worktree was clean before its
  report artifacts.

This worker did not repeat tests or broad source investigation. Full,
browser/e2e, live render, network/socket admission, Runtime/Agent suites,
install, and positive retained-theme/forged-source acceptance were not run.
No product source was changed.
