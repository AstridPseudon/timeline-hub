# Peer handoff: normal resolved-theme carrier

The existing carrier is Agent's named `theme` file input. Generic host already
materializes an admitted theme as `theme.json`, and Remotion already passes the
resolved value into Composition as `merged_props["theme"]`:

- `astrid/packs/rendering/pack.yaml:902-904`
- `astrid/core/execution/generic_host.py:6894-6903`
- `astrid/packs/rendering/rendering/renderers/remotion/root_preparation.py:167-177`
- `astrid/packs/rendering/shared/rendering_backend/__init__.py:89-123`

The normal gap is before that carrier. App resolves the selected theme from
the output config in
`/home/user/work/app/src/tools/video-editor/compositions/installed-themes.ts:90-105`
and uses it for preview in
`/home/user/work/app/src/tools/video-editor/compositions/TimelineRenderer.tsx:1604-1622`,
but normal render payload construction emits only `theme_id` at
`/home/user/work/app/src/tools/video-editor/lib/renderRouter.ts:852-883`.
`enqueueAstridRuntimeRenderTimeline():940-965` drops even that marker from the
managed task params, and Agent's managed snapshot has no resolved Theme field.

**One request to the admission owner:** bind the exact resolved Theme document
for the selected config/fact/profile to the existing named Agent input `theme`
for both normal saved and candidate preview renders. Preserve
`theme_overrides`; do not pass only the slug, add a DTO/store/public API, or add
another resolver. Once that named handoff exists, the Viewing-side consumer is a
small adapter wiring change at
`astrid/packs/rendering/actions/render/task_adapter.py:365-388` to forward the
existing `materialized_objects["theme"]` path as executor input `theme`.

The current state is not verified parity: with no runtime theme path Agent's
resolver intentionally selects its built-in theme, so a successful render alone
cannot prove the selected App theme survived admission.
