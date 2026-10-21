# Agent M3 Theme concrete source/carrier answer

Status: **NO-CARRIER** (read-only source trace, 2026-10-21).

## Concrete answers

- **Captured pack/host Theme selector before final admission: NO.** No existing
  path selects one project-authorized `theme.json` before the final managed
  task. `astrid/packs/rendering/shared/rendering_backend/__init__.py:62-71`
  accepts only an already materialized absolute `theme.json`; the resolver at
  `:89-123` merges that file with frozen timeline overrides and never resolves
  the timeline slug. `active_theme` is only an SDK argument; it does not bind a
  source. `source_root`/`_verify_admitted_source` only fence an admitted source.

- **Existing final-input carrier: YES, but post-admission only.** The render
  pack declares file input `theme` (`astrid/packs/rendering/pack.yaml:904-907`)
  and maps it to `--theme` (`:1062-1064`). GenericHost materializes an already
  Runtime-admitted named object as `theme.json` and
  `materialized_objects["theme"]` (`astrid/core/execution/generic_host.py:6888-6903`).
  This cannot be the first source; using it as preparation input is circular.

- **Existing private invocation/custody mode: YES.** Use the existing
  `_invoke_internal_result(..., kind="executor", inputs=...)` wrapper
  (`astrid/sdk/invocation.py:4654-4661`), which authorizes the existing
  `_include_internal` registry path (`:4025-4026,4062-4069`). On the host, the
  already-existing private runtime context is triggered by
  `child_delegation`, `delegated_parent`, or
  `delegated_recoverable_outputs` in the admitted spec
  (`astrid/core/execution/generic_host.py:8882-8884`). It carries the normal
  request `inputs`, `out`, `run_root`, and `invocation="runtime"`; private
  dispatch uses `run_id=None` (`:9555-9567`), and the child returns existing
  `outputs`/`payload`/`error` via `.astrid-capability-result.json`
  (`:8261-8272`; `generic_host_worker.py:157-170`). This is execution and
  result custody, not a Theme selector.

- **Existing declared output port: YES as a byte/result carrier, not as Theme
  authority.** `rendering.render` declares `provenance` at
  `astrid/packs/rendering/pack.yaml:1030-1035`, with type `file` and artifact
  type `metadata/provenance`. The normal manifest names it at
  `astrid/packs/rendering/actions/render/run.py:278-289`; GenericHost's normal
  declared-port validator still checks port membership, attempt containment,
  SHA-256, and byte count (`generic_host.py:7087-7160`). Thus a private
  preparation result may carry canonical JSON bytes there without bypassing
  transport validators; Agent's existing Theme document validator is
  `astrid/core/theme/_schema.py:237-264`. The port itself supplies no Theme
  selection.
  The normal render action still writes renderer provenance and expects its
  video path, so this is not an existing Theme-preparation mode today.

## Smallest already-approved proposal

Reuse that private managed invocation context and existing `inputs`/`out`/
`outputs[]` carriers. Runtime must first expose one real, already-authorized
pack/host Theme source selected from the same frozen saved selector or
candidate-plus-retained-base, config/registry, facts, profile, and idempotency
authority. It must then admit the exact named input:

```text
theme = {name: "theme", object_id: D, digest: D,
         filename: "theme.json", required: true}
```

Agent performs exactly one `_resolved_theme_for_render(timeline_path,
runtime_theme_path)` call, validates/canonicalizes the complete `{id, visual}`
document with the existing Theme validator, and emits those bytes through the
existing declared `provenance` result carrier. Runtime settles the ordinary
output, rechecks bytes/authority, and forwards the resulting `D` unchanged to
the final named `theme` input. App forwards; Viewing consumes
`materialized_objects["theme"]`. No slug, browser value, arbitrary descriptor,
new API/store/provider/whitelist/permission, or second resolver is authorized.
