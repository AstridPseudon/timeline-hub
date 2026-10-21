# Agent Main explicit-theme forwarding

## Decision

No Agent source change is needed for the owner ruling. The current Agent
integration tree already preserves Main497's ordinary explicit-theme carrier;
the current managed render adapter also forwards the already-admitted theme
materialization through the existing executor request. The deferred
ThemeDocument/themeSource/private-preparation/delegation proposals remain
unused.

## Exact carrier proof

The normal SDK path is:

1. `astrid/sdk/remote.py:1543` `RemoteMedia.import_file` imports the authored
   `theme.json` through the normal project CAS operation and returns the
   `{digest, object_id, filename}` descriptor.
2. `astrid/sdk/invocation.py:_kernel_invoke` retains the descriptor in the
   admitted `spec.inputs.theme` and adds its digest to `input_object_ids`.
   The direct SDK admission equivalent is `RemoteTasks.prepare_admission` in
   `astrid/sdk/remote.py`; it preserves the same body and ordered manifest.
3. `astrid/core/execution/generic_host.py` verifies the authorized digest,
   fetches the exact CAS bytes, and records the attempt-local
   `materialized_objects["theme"]` path as `theme.json`. Project, CAS,
   candidate, and attempt guards remain in the existing host path.
4. `astrid/packs/rendering/actions/render/task_adapter.py:_admitted_theme_path`
   accepts only that host-admitted file beneath the managed root. When present
   it forwards the exact path as the existing renderer `theme` input; an
   unbound caller `params.theme` is ignored and does not gain authority.
5. `astrid/packs/rendering/shared/rendering_backend/_resolved_theme_for_render`
   loads that one runtime document, applies the authored `theme_overrides`, and
   returns the single resolved theme. Existing Remotion root preparation passes
   that value as `props.theme`.

The SDK import/admission/body/materialization/resolver chain was exercised with
an API-only fixture using a schema-valid, distinguishable JSON theme. It
asserted that imported bytes, the admission descriptor/body, ordered manifest,
materialized `theme.json`, and resolved `{id, visual}` (including an authored
override) all remained identical to the expected Main497 behavior. No MP4,
renderer process, browser, default-only, or physical replay was used.

`origin/main` Main497 (`497714c73531f164082555ec81b61ca5bc8b6554`) has the same
SDK import, GenericHost materialization, and resolver implementations. The
current adapter forwarding is the only relevant current-tree addition, already
present in commit `12e773957` with its focused tests.

## Existing regression coverage

The current tree retains the following adapter tests in
`tests/packs/rendering/test_render_export_task_adapter.py`:

- admitted `materialized_objects["theme"]` reaches the canonical executor;
- a source-only caller `params.theme` cannot override the builtin fallback;
- a theme path outside the host materialization root is refused.

Resolver coverage in `tests/packs/rendering/test_remotion_backend.py` retains
the explicit missing-theme refusal and merged render-props behavior. No tests
were changed or weakened by this worker.

## Callers and App handoff

Agent callers should continue using the documented SDK/CLI ordinary file-input
route (`rendering.render` with the descriptor returned by
`media.import_file`), not a theme slug, inline JSON, browser state, or a new
wire field. The managed adapter consumes only the existing GenericHost named
input materialization.

App's remaining forwarding work is upstream: when App creates the ordinary
managed render invocation, it must preserve the existing `inputs.theme`
descriptor and its CAS identity so GenericHost produces
`materialized_objects["theme"]`. If App uses the managed export adapter, it
must pass through that existing host handoff unchanged. Do not invent
`theme_id` authority, `themeSource`, a second resolver, or a second merge.

Missing theme keeps the intentional builtin default. An invalid, foreign,
tampered, or otherwise unadmitted explicit descriptor must remain a visible
refusal; it must never silently become the default.

## Worker delta

No Agent source or test delta was necessary. This file is the design/handoff
artifact for the already-correct Agent carrier and the App follow-up.
