# Diagnosis: exact d971 materializer call contract

## Verdict

This is fixture plumbing, not a proven product forwarding regression. No SDK,
Runtime, host-dispatch, renderer, central, or retry run was performed. The
selected Agent source is exactly `d971d4584c86a85a17d083d033c2049d83d6ef47`.

The first cause is the direct fixture call at
`tests/integrations/test_generic_host_remotion_render.py:615-621`. The normal
Runtime task value in `task.spec` is already the admission envelope. The
fixture wraps it again as `{"spec": task.spec, "input_object_ids": ...}`.
`_admitted_spec_envelope` intentionally unwraps exactly one layer, so the
materializer receives the Runtime outer envelope as its `input_spec`. That
outer envelope has `spec`, `input_object_ids`, `schema_version`, and
`capability_digest`, but no top-level `inputs`. The materializer therefore
starts with `{}` at `generic_host.py:6511-6516`, never enters the per-input
loop, and never takes the `theme` branch at `generic_host.py:6894-6904`.
The later `values["theme"]` read is consequently a fixture-side `KeyError`,
not evidence that Runtime admission dropped the theme descriptor.

The current selected d971 fixture also contains the earlier stale envelope
reads at lines 602-603 and 657. The already-approved correction from the
0839 investigation (use `task.spec["spec"]["inputs"]`) is included in the
unapplied proposal so the proposal is complete against this exact selected
source. No part of that proposal was applied here.

## Source trace

| Boundary | Exact source and contract |
| --- | --- |
| Agent envelope decoder | `astrid/core/execution/generic_host.py:2254-2286` documents `task.spec = admission envelope`, `task.spec.spec = capability request`, and `task.spec.spec.inputs`; it unwraps only one `spec` mapping. |
| Agent materializer | `generic_host.py:6460-6474` accepts the task envelope and authorization carrier; `6483-6512` selects authorized IDs and the one-layer admitted input spec; `6511-6516` copies `input_spec["inputs"]`; `6888-6904` authorizes and fetches the managed `theme` object to `theme.json`. |
| Normal host caller | `generic_host.py:9179-9199` passes `spec` directly, passes `authorized_input_object_ids`, metadata-derived parameter/CAS-port arguments, storage policy values, continuation ID, and file input names. It does not construct another `{"spec": ...}` wrapper. |
| Normal claim-to-dispatch path | `generic_host.py:10284-10291` preserves the claim’s immutable `spec`; `10329-10336` calls `run_task` with the task snapshot and lease/attempt/fence identity. The claim data is built from the Runtime response at the surrounding `10110-10283` path. |
| Frozen Runtime envelope | Runtime `8f105c26e3b62f9c2683f717a9773a12bc775a8e`, `runtime_protocol/service.py:5466-5492` stores `task_spec` with outer `input_object_ids`, schema/digest metadata, and nested `spec = body["spec"]`; `6383-6388` exposes that shape; `7125-7132` returns the same admitted outer shape from claim. |
| Fixture call | Exact d971 fixture lines `601-603` read the task identity (but line 603 is stale); `615-621` makes the extra wrapper; `622-626` reads the expected managed theme carrier; `631-648` probes prepared Root props; `650-653` checks built-in fallback; `655-665` checks local-source rejection. |

## Argument-by-argument comparison

- **Envelope versus capability spec:** normal `run_task` receives the Runtime
  outer envelope as `spec` and passes it unchanged. The fixture receives the
  same `task.spec` but wraps it once more. The smallest correction is to pass
  `task.spec` directly.
- **Authorization/input IDs:** normal dispatch passes the claim’s
  `authorized_input_object_ids` explicitly (`task_data["input_object_ids"]`),
  while the fixture puts the IDs in its extra wrapper and relies on the
  fallback. The correction passes
  `authorized_input_object_ids=task.input_object_ids`, preserving the same
  authority boundary.
- **Inputs and params:** rendering’s capability definition has file inputs
  `timeline`, `assets_registry`, and `theme` at
  `astrid/packs/rendering/pack.yaml:865-907`, plus scalar/config inputs such
  as `selector` at `908-920`; it declares no `params` or HC04 parameter/CAS
  metadata. The normal caller still supplies the metadata keyword arguments,
  which resolve to `None` for this capability. The fixture’s omission of
  those optional metadata values is not the cause of the missing theme.
- **Role and lifecycle:** SDK admission is the owner-side request; the normal
  host path is a claimed worker execution with lease ID, attempt ID, fence,
  runtime epoch, and heartbeat. `generic_host.py:9003` defines the normal
  cancellation callback; `9111-9123` heartbeats the lease, and the callback
  is carried through materialization/process monitoring. The fixture calls
  `_materialize_inputs` directly after `sdk.invoke`; it has no claim, lease,
  heartbeat, fence, or cancellation callback. This is acceptable for a pure
  materialization/root-prefix probe, but it is not normal task qualification.
- **Materialized result carrier:** `_materialize_inputs` returns the
  pre-command-binding `PreparedTimelineInputs` mapping, including a path for
  `theme` and a mapping for `materialized_objects`. The fixture reads those
  values directly and passes the mapping to `_prepared_remotion_root`, which
  is explicitly a no-render, read-only props probe at
  `renderers/remotion/root_preparation.py:89-93`. The normal command path at
  `generic_host.py:7927-7992` adds host values, binds the command, and serializes
  a mapping-valued `materialized_objects` into
  `attempt/inputs/materialized-objects.json` at `7943-7953`; the child then
  receives that path through the manifest command inputs. Thus the fixture’s
  direct mapping is an intentional pre-binding probe, not the normal child
  carrier, and it cannot be used to qualify renderer forwarding.
- **Theme path after materialization:** the rendering command manifest forwards
  `theme` as `--theme` and host-owned materialized values as
  `--materialized-root`/`--materialized-objects` at
  `astrid/packs/rendering/pack.yaml:1043-1091`. Root preparation consumes the
  materialized path at `root_preparation.py:143-177`; `_resolved_theme_for_render`
  uses that path or the intentional built-in fallback at
  `rendering/shared/rendering_backend/__init__.py:89-123`.

## All remaining fixture calls/reads

The fixture’s `discover`, `preflight`, and `register` calls are setup and
capability registration. `sdk.invoke` is the real admission boundary and was
already observed to pass admission and corrected descriptor identity in the
0839 evidence. `generated.get_task` is a convenience task read; its input IDs
are valid, but its nested descriptor assertion must use
`task.spec["spec"]["inputs"]`. The direct `_materialize_inputs` call is the
only call with the extra envelope layer and is the first failure. The Root
preparation call and `_resolved_theme_for_render(..., None)` are local probes;
the forged-source call intentionally verifies that a local theme path is not
accepted as a managed Runtime object. Its input map should reuse the corrected
admitted input mapping. No remaining external call or read explains the
missing `theme` before line 622/623.

The success, identity, `theme.json`, one-resolver, props, local-source-negative,
and credential assertions remain preserved by the proposed fixture-only
correction. No new Theme contract, DTO, store, resolver, or authority is
needed.

## Smallest unapplied correction

See the unified diff in the companion `-PATCH.md`. It makes the two stale
nested-input reads match the already-approved 0839 correction, and changes
only the direct materializer call from a double-wrapped argument to:

```python
host._materialize_inputs(
    task.spec,
    attempt,
    authorized_input_object_ids=task.input_object_ids,
    file_input_names=...,
)
```

No product or test edit was made in this diagnosis worktree. If the owner
applies this proposal, the next step is one authorized central run through the
normal caller. A failure after this boundary should be diagnosed separately;
this report does not claim that unrun qualification.

## Verification and hashes

The only execution performed was the pure `_admitted_spec_envelope` probe;
it passed and reproduced the one-layer/double-layer distinction. No pytest,
SDK, Runtime, host, render, browser, socket, central, or full suite was run,
as required by the task. The exact commands and final readback hashes are in
the worker `COMMAND` artifact.

