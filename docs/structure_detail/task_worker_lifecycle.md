# Task & Worker Lifecycle

> **Current boundary (2026-10-19).** Runtime owns task admission, execution
> receipts, settlement, event history, and canonical timeline publication.
> App producers use the Runtime task and timeline contracts; they do not write
> legacy task rows or publish whole timeline configurations.

## Supported execution path

Generation work follows one supported path:

```text
UI producer
  -> App createTask
  -> Runtime admission (project, inputs, idempotency)
  -> Worker GenericPackHost execution
  -> Runtime settlement and receipts
  -> CAS/gallery/timeline readback
```

Runtime carries input identity, ordered inputs, output validation,
idempotency, and the publication fence. Workers execute the admitted work and
return results to Runtime; they do not become a second task or timeline
authority.

See [`unified_task_creation.md`](unified_task_creation.md) for the admission
contract and [`realtime_system.md`](realtime_system.md) for client updates.

## Retained `complete_task` boundary

`supabase/functions/complete_task` remains a narrowly retained completion
adapter for supported worker outputs and existing settlement callers. It
performs the following work after authentication and task-ownership checks:

1. Validates task and storage references, then stores the completed output and
   thumbnail.
2. Creates or updates the ordinary generation/variant result and its
   relational shot metadata where the completion contract requires it.
3. Marks the task complete, cleans materialized inputs, records orchestrator
   follow-up state, and preserves service-role cost calculation and billing.
4. Returns the output URLs plus any follow-up warnings.

Completion does not publish a canonical timeline document, append a timeline
configuration, update the canonical asset registry, or automatically place a
completed asset on a timeline. A placement-shaped input is therefore not a
second authoring route; the completion result remains available for a normal
timeline command to reference.

## Timeline authoring

Timeline edits use the normal Runtime command path:

```text
App gesture or authoring client
  -> EditCommand capture with reads/selections/bindings
  -> crash-safe App outbox
  -> POST /v1/projects/{project}/timelines/{timeline}/commit
  -> Agent command provider and Runtime acceptance
  -> accepted revision and timeline readback
```

Retired edge authoring handlers, append helpers, and whole-configuration
publication paths are not authoring routes. Producers that need to affect a
timeline must emit the published command contract and use
the Runtime commit door; completion and media preparation alone do not grant a
canonical write.

## Worker responsibilities

Workers may process image, video, prompt, and related generation work through
Runtime's admitted task. They may upload immutable output artifacts and report
completion. They must not:

- insert or complete legacy task rows outside the retained completion
  contract;
- replace a canonical timeline document or append a timeline configuration;
- infer a timeline placement from a display ID or refresh authoring guards; or
- bypass Runtime with a hosted append/publish relay.

When a result should appear in a timeline, the client or another supported
authoring producer reads the immutable result and submits a guarded command
through Runtime.

## Debugging

Trace a generation from App task admission through Runtime settlement and
readback. For retained completion failures, inspect the `complete_task`
response's typed error or follow-up warnings and the task's persisted result
data. For timeline edits, inspect the command request, accepted revision, and
Runtime history; do not diagnose a deleted append/import route as a supported
path.
