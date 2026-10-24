---
name: vibecomfy
description: >
  Import, inspect, edit, validate, and run ComfyUI workflows through VibeComfy's
  canonical Python/companion/source bundle and Astrid task history.
---

# VibeComfy

Use this pack for ComfyUI workflows that need graph inspection or edits beyond
the standard `generation` contracts, including LoRAs, IP-adapter, ControlNet,
custom samplers, and graph composition. The canonical bundle contains three
separate members: editable `workflow.py`, its `workflow.vibe.json` revision and
UI companion, and byte-identical original `source.json`.

## Windows with NVIDIA

ComfyUI on Windows with NVIDIA is untested, but runs by default. Please tell us
how it went, including the GPU model and driver from `nvidia-smi`. For
`vibecomfy.*`, Astrid's GPU detection is informational; the local server uses
your own ComfyUI and its GPU.

The candidate environment pins are in `environment.windows-nvidia.json` and
`requirements.windows-nvidia.txt`. They select Python 3.12.10, PyTorch CUDA
13.0 wheels, the existing ComfyUI/VibeComfy source pins, and the H3 and
VideoHelperSuite custom-node source/dependency pins. Other custom nodes need
their own reviewed pins before being added to this candidate.

Supply clean, already admitted checkouts with those nodes under
`ComfyUI\custom_nodes`, and keep the selected VibeComfy `custom_nodes.lock`:

```powershell
python -m astrid.core.generation.gpu_environment vibecomfy --checkout C:\Astrid\ComfyUI --vibecomfy-checkout C:\Astrid\VibeComfy --plan
python -m astrid.core.generation.gpu_environment vibecomfy --checkout C:\Astrid\ComfyUI --vibecomfy-checkout C:\Astrid\VibeComfy
```

This uses user-local uv 0.11.32 and needs a network connection on the tester's
computer. It creates the environment under
`%LOCALAPPDATA%\Astrid GPU\vibecomfy\<identity>`, without administrator access or a
system CUDA toolkit. The shared provisioner verifies source/node pins,
combines the CUDA pins with ComfyUI's requirements, VibeComfy's declared
dependencies/build tools and each selected node's requirements, then resolves
with the recorded upload cutoff. It writes and syncs a fully versioned,
hash-bound `requirements.lock`, installs the selected VibeComfy source without
changing that closure, checks dependencies and probes CUDA. A resolver,
dependency or CUDA failure produces no success receipt.

Keep the lock and `astrid-gpu-environment.json` with test evidence. Replay the
lock with `uv pip sync --require-hashes` to reproduce the resolved environment,
including its exact PyTorch wheel URLs. Use the printed interpreter path as the existing
warm server's engine interpreter; source, model and readiness-profile
admission still apply. Provisioning does not start another server or download
models. A repair uses a new `--destination` so a warm interpreter is never
overwritten. macOS and Linux retain their existing path.

## Executors

| Executor | Inputs and result |
|---|---|
| `vibecomfy.import` | Admitted raw `source` JSON plus a stable `workflow_id`; emits `python`, `companion`, `source`, and an origin `report`. |
| `vibecomfy.inspect` | One UI `workflow` JSON or the complete `python`/`companion`/`source` trio; emits only a read-only `projection` and `inspection`. Canonical Python requires `python_execution_consent="confirmed"`; UI JSON is inspected statically without it. |
| `vibecomfy.edit` | A canonical parent trio plus required `python_execution_consent="confirmed"`, and `operations` for one atomic typed batch or one separate `capture_python`/`capture_graph` candidate; emits the full successor trio and audited `report`. |
| `vibecomfy.validate` | A UI `workflow` JSON or the canonical trio; checks structure offline. Canonical Python requires `python_execution_consent="confirmed"`; UI JSON is validated statically without it. Runtime and target-schema validation are deferred to `vibecomfy.run`. |
| `vibecomfy.run` | A UI `workflow` JSON or the canonical trio; executes the workflow and settles its result artifacts. |

Canonical bundle members are immutable Astrid artifacts. Each edit or capture
consumes the exact prior trio and reports its `workflow_id`, `transition_kind`,
`parent_revision`, `parent_task_id`, and `origin_task_id`. Astrid's existing
task lifecycle records admission, completion/failure, and output digests. Read
the detailed import → inspect → edit/capture → validate → run journey in
[`docs/guides/cli-journeys.md`](../../../../docs/guides/cli-journeys.md).

`vibecomfy.inspect` is read-only: it does not create a revision or canonical
bundle. Its Python-like projection is for reading, never for mutation input.
`vibecomfy.edit` is the accepted mutation path. Typed edits and manual captures
produce a successor and a structured transition report. A ComfyUI canvas Apply
does not enter Astrid task history; use explicit project-bound capture to
record a candidate.

For canonical Python bundles, include the scalar input
`python_execution_consent: "confirmed"` in `spec.inputs` for inspect, edit,
and validate. It has no default, is validated as an exact literal, and must be
explicitly present on every task that loads canonical Python. The adapter maps
it to VibeComfy's existing audited non-interactive `--yes` GateContext; task
admission and `authority_context` do not stand in for this input. Inspect,
edit, and validation artifacts include the consent value and gate audit. UI
JSON inspection and validation stay on the static ingestion path and need no
consent. `vibecomfy.run` is a separate generation capability.

Canonical validation uses `--no-schema` and reports
`validation_mode="canonical_bundle_structural"`, with `runtime_validation.status`
set to `deferred` and its executor set to `vibecomfy.run`. It preserves canonical
bundle and structural graph checks without contacting or managing Comfy. Passing
this step does not establish runtime readiness: the run adapter must attest its
session and compile against fresh target schemas before queueing generation.

## Typed edit document

The `operations` input is JSON with one ordered list of leaf operations. The
executor lowers the list to one VibeComfy `edit_batch`, so any rejected leaf
rejects the whole batch and no successor artifacts are published.

```json
{
  "schema_version": 1,
  "expected_revision": 0,
  "ops": [
    {"op": "edit_node", "target": "ksampler", "field": "steps", "value": 24}
  ]
}
```

The supported leaf tools are `edit_node`, `add_node`, `remove_node`,
`upsert_link`, `remove_link`, and `set_node_mode`. Node targets may be rendered
bindings or stable UIDs. Explicitly named new-node UIDs can be referenced by a
later operation in the same batch. For field names, node classes, and tool
schemas, use the installed `vibecomfy node` command before editing.

For task invocation, place scalar ports under `spec.inputs`; name each
immutable file port in `spec.input_digests` and authorize its media object in
`input_manifest`. Keep the same `workflow_id`, `transition_kind`,
`parent_revision`, `parent_task_id`, and `origin_task_id` in the task spec so
the report and task history describe one lineage. Import, edit, capture,
validation, and execution are separate tasks when using Astrid. Do not pass a
`--project` option to an Astrid-native executor: its admitted task already
supplies project context.

## When not to use

- Use `generation.generate_image` for standard image generation contracts.
- Use `understanding` to explain existing media.
- Use `video_editing` to cut or render timelines.
