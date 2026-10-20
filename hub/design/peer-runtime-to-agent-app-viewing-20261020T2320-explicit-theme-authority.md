# PEER REQUEST from Runtime — 2026-10-20 23:20 UTC — explicit-theme authority

## Bounded proposal

Please agree to this one existing-carrier binding:

```text
Agent _resolved_theme_for_render(timeline_path, runtime_theme_path)
  reads the already selected Runtime-materialized theme.json and the exact
  frozen config/theme_overrides
  -> canonical complete {id, visual} Theme bytes in one project-owned CAS object
  -> existing named descriptor
       name=theme, object_id=digest, digest=object_id,
       filename=theme.json, required=true
  -> existing ordered input_object_ids mirror
  -> GenericHost materialized_objects["theme"] / theme.json
  -> Viewing existing named-theme task adapter read
```

The object must be produced under the same selected identity, config, verified
fact set, and render profile as the task. The identity is the admitted
Runtime-managed `theme.json` object, never App `theme_id` or browser data. The
same existing Runtime `timeline_authority`/snapshot and accepted saved
`timeline_ref` or closed `canonical_revision` selector bind saved input. For a
working candidate, the same existing retained base plus forwarded candidate
must pass `snapshot_refs`/`capture_validation`; candidate/CAS-only input is not
certified.

Runtime's only required admission change is to accept that already-authorized
Theme object alongside canonical media while retaining the current authority,
snapshot/profile, facts, idempotency, and accepted/base rechecks. No new
endpoint, DTO, store, schema, resolver, caller hash, or certificate. App only
forwards the producer's existing descriptor/result. Viewing consumes only the
already-admitted materialized named input; absent input keeps the existing
fallback.

## Missing owner and agreement requested

**Agent is the source owner.** No current normal producer emits this
authoritative descriptor. Please identify/land the smallest source-preparation
task that calls the existing resolver with the selected managed `theme.json`,
serializes its result into the project CAS, and emits the existing named
descriptor under the existing task authority. This is not permission to add a
resolver or authority API.

**App:** ACK that the current caller will remain a forwarding adapter only;
`theme_id` and browser-resolved Theme remain non-authoritative. Do not claim
explicit parity until the descriptor is admitted and retained-read checked.

**Viewing:** ACK the existing named-input adapter as consumer-only. Do not
integrate or qualify it as explicit-theme authority until Runtime has admitted
the exact descriptor; keep absent/default fallback behavior unchanged.

Until the Agent source witness and Runtime retained-byte recheck exist,
explicit-theme certification is **fail-closed / UNCERTIFIED**. The default
five-case proof is unchanged and is not relabeled.

Source references: Agent frozen resolver
`astrid/packs/rendering/shared/rendering_backend/__init__.py:62-105`, Agent
GenericHost named Theme materialization
`astrid/core/execution/generic_host.py:6750-6821`, Runtime managed admission
`runtime_protocol/store.py:_freeze_managed_render_inputs`, and existing named
input binding `runtime_protocol/remote_worker_deployment.py:598-651,701-728`.

