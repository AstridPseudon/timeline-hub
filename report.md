# Normal resolved-theme carrier: source-backed result

## Result

There is no complete, verified normal saved/candidate carrier from the selected
App config to the Agent render today. The exact existing render carrier to
reuse is already present in Agent:

`theme` input file -> generic-host `theme.json` materialization -> Remotion
`theme_path` -> `_resolved_theme_for_render()` -> Composition props
`merged_props["theme"]`.

The missing handoff is upstream of the final resolver. App currently computes
the theme identity, but the normal Runtime admission does not bind the
resolved theme document to Agent's existing `theme` input. Agent then falls
back to its built-in theme when `theme_path` is absent. Forwarding only the
theme slug would not fix this and would violate the current Agent contract,
which explicitly forbids resolving a historical slug from a worker checkout.

## Current source identities and exact lines

### App preview and normal saved render

- App preview preserves the canonical command projection as `pairedConfig` at
  `/home/user/work/app/src/tools/video-editor/components/PreviewPanel/useVideoEditorPreviewComposition.ts:53-84`.
  It carries the selected config plus the projection fact; it does not carry a
  resolved Theme document.
- App's one existing theme authority is
  `/home/user/work/app/src/tools/video-editor/compositions/installed-themes.ts:90-105`:
  `resolveTimelineRenderTheme(config)` selects the installed theme and deep-
  merges `theme_overrides`.
- The actual App preview consumes that authority at
  `/home/user/work/app/src/tools/video-editor/compositions/TimelineRenderer.tsx:1604-1622`.
  `renderConfig` is the projected output config and `runtimeTheme` is derived
  from the resolved Theme.
- Normal saved render flushes the acknowledged version and uses its selected
  `renderConfig` at
  `/home/user/work/app/src/tools/video-editor/hooks/useRenderState.ts:869-916`.
- `buildRenderTimelinePayload()` creates the existing `theme_id` marker from
  the projected output config at
  `/home/user/work/app/src/tools/video-editor/lib/renderRouter.ts:852-883`.
  This is only a slug (`defaultThemeId(outputConfig)` at lines 734-739), not
  the resolved Theme content.
- The concrete drop is
  `/home/user/work/app/src/tools/video-editor/lib/renderRouter.ts:940-965`:
  `enqueueAstridRuntimeRenderTimeline()` writes `timeline_ref`, selector,
  output name, and canonical metadata, but no theme input. Its deliberate
  `input_object_ids: []` at lines 953-957 means the browser is not currently
  admitting a theme object either.

### Agent normal saved snapshot and candidate preparation

- Normal snapshot preparation projects the exact parent and stores only
  `config`, `registry`, expansion, and graph at
  `astrid/packs/rendering/actions/render/managed_timeline.py:1123-1165`.
  `ManagedRenderSnapshot` itself has no resolved-theme field at lines 694-711.
- Snapshot materialization writes only `timeline.json`, `assets.json`, and
  `authority.json` at
  `astrid/packs/rendering/actions/render/managed_timeline.py:1168-1189`.
- Candidate preparation validates the frozen candidate, exact base head, and
  pinned child revisions, then calls the same composition projector at
  `astrid/sdk/authoring_render_preview.py:91-172`. The returned candidate
  snapshot replaces `config` and `registry` but still has no Theme document at
  lines 191-213.
- Candidate invocation preserves the preview authority and timeline reference
  at `astrid/sdk/authoring_render_preview.py:216-233`; it does not create a
  separate theme transport.

### Existing Agent carrier and final consumer

- The rendering capability already declares the existing optional `theme` file
  input at `astrid/packs/rendering/pack.yaml:891-904`.
- The generic host already has the exact named carrier: when input `theme` is
  admitted, it fetches `theme.json`, exposes `values["theme"]`, and records
  `materialized_objects["theme"]` at
  `astrid/core/execution/generic_host.py:6888-6903` and
  `astrid/core/execution/generic_host.py:6970-6972`.
- The normal managed task adapter currently constructs executor inputs without
  that name at `astrid/packs/rendering/actions/render/task_adapter.py:365-388`.
  It forwards the timeline, assets, authority identity, and materialized
  object map only.
- The Remotion preparation path already consumes the carrier. At
  `astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:167-177`,
  `theme_path` is passed to `backend._resolved_theme_for_render()` and the
  resulting resolved value is placed in `merged_props["theme"]`.
- The resolver's contract is explicit at
  `astrid/packs/rendering/shared/rendering_backend/__init__.py:89-123`: a
  runtime-pinned theme document is authoritative, authored
  `theme_overrides` are merged, and the timeline's historical slug is never
  used to search a checkout or filesystem. With no runtime theme path it uses
  the built-in theme at lines 101-105.

## One precise peer request

**PEER REQUEST — normal render admission owner:** preserve the full resolved
Theme selected from the same output config/fact/profile used for the normal
saved render and candidate preview, and bind it through the already-declared
Agent input named `theme` before the managed task reaches the Agent task
adapter. The existing App `theme_id` at
`/home/user/work/app/src/tools/video-editor/lib/renderRouter.ts:878` may remain
the identity/lookup marker, but forwarding that slug alone is insufficient;
the named input must resolve to the exact `theme.json` document whose visual
values include the selected `theme_overrides`.

Do not add a DTO, store, public API, second resolver, or duplicate theme
literals. Do not make Agent look up `config.theme` in its checkout. The owning
area should close the existing admission gap at
`enqueueAstridRuntimeRenderTimeline():959-965` and/or its existing Runtime
binding so generic-host materialization can use the already-existing
`theme` path. The Agent consumer then needs only the bounded existing-input
forwarding described below.

## Bounded Viewing-side patch (not applied)

If the owning change lands as the existing named host materialization
`materialized_objects["theme"]`, the only Agent-side correction needed is in
`astrid/packs/rendering/actions/render/task_adapter.py:365-388`: validate the
admitted `theme` materialization and pass that existing path as executor input
`theme`, alongside the current `materialized_root` and
`materialized_objects`. This is a consumer wiring change only. It must not
derive a theme from the snapshot slug or introduce another source of truth.

The patch is intentionally not applied here because the current normal
App/Runtime admission supplies no named theme materialization for it to
consume; changing the Agent adapter alone would leave the carrier empty.

## Controls required when the peer request is implemented

- The selected config, projection fact, and render profile must remain one
  paired input. The candidate path must retain the exact base-head and frozen
  candidate checks at `authoring_render_preview.py:104-116` and
  `:156-172`.
- The theme document identity and bytes must be admitted together. Its visual
  values must equal the single App resolution of the selected config, including
  `theme_overrides`; no slug-only fallback is acceptable.
- Agent's final `merged_props["theme"]` must come from the named runtime theme
  input, then use the existing resolver's override merge. A missing carrier
  must remain observable as the intentional built-in fallback, not be silently
  treated as proof of parity.
- The normal saved path and candidate preview must use the same carrier and
  preserve the existing `timeline_ref`, acknowledged version, canonical
  metadata, and preview authority.
- Acceptance evidence should compare the App resolved Theme with Agent
  `merged_props["theme"]` for the selected config/fact/profile. No new parity
  harness or second full run is requested by this handoff.

## Verification status

This report is source tracing only. No product code was changed and no live
App/Runtime/Agent normal render was run. The prior theme compatibility report
(`vw-m3-theme-compat`) likewise recorded Composition/App source equivalence but
no Agent-resolved Theme paired with the selected config. The peer request is
therefore required before claiming the normal carrier is verified.
