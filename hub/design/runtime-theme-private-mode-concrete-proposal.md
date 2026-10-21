# Runtime M3 private Theme preparation — concrete proposal

Status: **proposal; no product code changed.** This is the exact shape to ACK
before Runtime coordinates implementation.

## Decision

Use the smallest existing private managed context: a Runtime-admitted delegated
child of the existing managed invocation. `GenericPackHost.run_task()` already
enters its private runtime context when the admitted spec contains
`delegated_parent` (`astrid/core/execution/generic_host.py:8794-8797`), and the
child invocation already uses `invocation="runtime"`, its attempt `run_root`
and private `run_id=None` (`:9456-9473`). The existing private15 host-context
precedent is compatible: identity and output custody come from the host claim
and attempt directory, never from action inputs. No private15 schema, pin, or
public action is imported.

Runtime generates the stage after freezing the saved selector or the closed
candidate plus retained base. A caller cannot set the stage: delegated fields
are Runtime admission authority, and `admit_delegated_child()` already binds
the parent lease/fence/epoch, project, placement, capability digest and stage
order (`runtime_protocol/service.py:5992-6185`).

## Literal internal carrier

At the existing managed parent admission, Runtime selects exactly one captured
Theme member from the trusted pack/host capture associated with the frozen
authority. Let `D` be its already-captured `sha256:<64-hex>` object ID. The
selection is valid only when the capture records the selected frozen
`config.theme` and the same saved revision or candidate/base; a slug, browser
value, caller hash, or arbitrary project object is not a source. If the capture
has no exact member or has changed bytes, refuse before child admission.

Runtime then creates the existing delegated policy/stage with this shape (the
policy is Runtime-generated, not caller supplied):

```json
{
  "child_delegation": {
    "capabilities": [{"capability_id": "rendering.render", "capability_digest": "R"}],
    "targets": [T],
    "input_object_ids": ["D"],
    "stages": [{
      "name": "theme_prepare",
      "capability_id": "rendering.render",
      "capability_digest": "R",
      "target": T,
      "inputs": [{"name": "theme", "root_object_id": "D"}]
    }]
  }
}
```

The one child request uses the existing delegated fields and named input
carrier; Runtime resolves the root input through
`_resolve_delegated_stage_inputs()` and rewrites the descriptor from the
verified object, so the caller cannot choose `D`:

```json
{
  "stage": "theme_prepare",
  "input_refs": [{"name": "theme", "root_object_id": "D"}],
  "spec": {
    "inputs": {
      "theme": {"object_id": "D", "digest": "D", "filename": "theme.json", "required": true}
    }
  },
  "execution_request": {
    "target": T,
    "inputs": [{"name": "theme", "object_id": "D", "digest": "D", "filename": "theme.json", "required": true}]
  }
}
```

This is the existing `execution_request.inputs` / `spec.inputs` / ordered
`input_object_ids` contract (`runtime_protocol/store.py:428-480`,
`runtime_protocol/remote_worker_deployment.py:598-728`). GenericHost
materializes the admitted bytes as its existing attempt-local `theme.json` and
the Agent side calls exactly
`_resolved_theme_for_render(timeline_path, runtime_theme_path)` at
`astrid/packs/rendering/shared/rendering_backend/__init__.py:89-123`.

## Private dispatch and result

The internal mode is the existing delegated stage value
`delegated_stage == "theme_prepare"`; it is not a new public entrypoint or
DTO. The bounded Agent dispatch belongs beside the existing render command at
`astrid/packs/rendering/actions/render/run.py`, reached only from the admitted
private GenericHost path. It writes one canonical complete `{id, visual}` JSON
value after the one resolver call to the already-declared `provenance` output
path. It does not invoke the renderer and does not fabricate video.

The existing harvest/typed-output path remains in force:
`generic_host.py:_typed_outputs()` validates declared-port membership,
containment, hash, size and result identity (`:6970-7170`). The only bounded
host change is at the later media check (`:9665-9686`): for the exact admitted
`rendering.render` child whose `delegated_stage` is `theme_prepare`, require
the existing `provenance` result and do not require `video`; for every other
render, retain the current `video` requirement. `outputs_required()` still
requires a typed settled output. No normal output is exempted and no Theme
port is added.

The child therefore settles through the existing result shape as one ordinary
output association with `output_port == "provenance"`; its bytes are `D2`, the
canonical resolved Theme object. Runtime retains `D2` through the existing
`settle_attempt()` staging/publication and `_associate_managed_outputs()`
project/task/attempt custody (`runtime_protocol/service.py:7372-7504`,
`runtime_protocol/store.py:5312+`). The final ordinary render is then admitted
with the existing named input, unchanged public shape:

```text
execution_request.inputs += {
  name: "theme", object_id: D2, digest: D2,
  filename: "theme.json", required: true
}
spec.inputs.theme = the same descriptor
input_object_ids = existing ordered media IDs, then D2
```

Final admission repeats the existing project association, exact saved/candidate
authority, frozen config/facts/profile, digest/bytes, idempotency and ordered
binding checks. The final render still must produce its declared `video`.

## Authority and proof

Keep `_freeze_managed_render_inputs()` and its exact config/registry/media
freeze, candidate/base checks, snapshot publication and replay identity;
`capture_validation.validate_capture()` and `snapshot_refs` remain the source
of candidate authority. Keep delegated parent lease/fence/epoch/placement and
stage-order checks, GenericHost source-root recheck, input hash/materialization
guards, typed-output validation, and Runtime CAS settlement unchanged.

Smallest positive: the private child consumes the Runtime-selected captured
`D`, settles only `provenance` as `D2`, and the following ordinary render
materializes `D2` as `theme.json`; assert `D2` is canonical complete
`{id,visual}` and the final task still settles `video`.

Smallest negative: (1) a child with `theme_prepare` but no `provenance` result
refuses at the private result check; (2) an ordinary `rendering.render` with no
`video` still refuses at the unchanged media check. Also refuse a foreign or
changed captured `D` before child admission.

## ACK requested from Agent

Please ACK this exact internal contract in the Agent design/inbox: delegated
stage `theme_prepare`; existing named input `theme` bound by Runtime to the
captured `D`; one `_resolved_theme_for_render()` call; canonical `{id,visual}`
bytes through the existing declared `provenance` result; and private-only
omission of `video` at the host’s existing media check. Confirm the Agent
dispatch can distinguish this host-admitted delegated stage without a public
field, caller authority, new Theme port, second resolver, or schema/pin change.
If Agent cannot carry the stage through the existing host command boundary,
name that exact call/type; do not substitute provenance semantics for ordinary
renders.

No implementation, test run, render, browser, MP4, schema, client, or pin
change is part of this proposal.
