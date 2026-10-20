# Runtime / Main Speech SDK admission trace

Date: 2026-10-20T16:44:25Z (UTC)

Scope: read-only trace of the current Agent `generation.generate_speech` and
`video_editing.sync_draft_voiceover` path against Runtime `e2db1e8`. No Agent or
Runtime product source, schema, DTO, or API was changed.

## Finding

The actual normal speech request does **not** currently send the existing
`generation_intent` or `generation.publish_v1` settlement effect.

The SDK does send a normal Runtime task admission with the exact text/settings,
project, capability id/digest, input manifest, and executor authority context.
It is therefore a Runtime-managed task/output path, not a raw local-output path.
However, without the predeclared intent/effect, Runtime's generic settlement
keeps the managed association outside the generation domain: it can carry the
task/attempt/CAS/association identity, but it does not create a generation or
variant association.

This is distinct from the prior Runtime speech-like fixture. That fixture
explicitly supplied `generation_intent` and `generation.publish_v1`; it proved
the Runtime publication path and got the association except intrinsic
`duration_seconds`. It is not evidence that the current normal Agent speech
caller supplies those fields.

The exact normal admission body below is executable SDK evidence. The generic
normal terminal-association consequence is source-traced from Runtime's
settlement/association code; this worker did not run a live speech worker or
external service.

## Exact normal SDK call and admission

The voiceover caller is `astrid/packs/video_editing/shared/draft_voiceover.py`
`runtime_synthesizer` (Agent line 389):

```python
sdk.invoke(
    "generation.generate_speech", kind="executor", project=project,
    inputs={"text": text, **settings}, client=client, wait=True,
    idempotency_context=request_context,
)
```

The typed `generate.audio(mode="tts")` facade also routes to that exact
capability (Agent `astrid/sdk/generation.py:484-513`); it does not add intent or
effect. The direct voiceover path is the relevant one for the original
voiceover/RIPPLE consumer.

The SDK modality resolver recognizes `generation.generate_image*`,
`generation.generate_video*`, and `generation.generate_audio*`, plus explicit
metadata opt-ins; it does not recognize the exact id `generation.generate_speech`
unless the capability metadata supplies `generation_publication`
(`astrid/sdk/invocation.py:2075-2094`). The shipped speech pack has output
manifest metadata, but no `generation_publication` declaration
(`astrid/packs/generation/pack.yaml:1544-1683`). Consequently normal speech has
`intent_modality = None`, no automatic intent, and no effect.

The admission branch only adds `generation_intent` and computes the existing
`generation.publish_v1` effect when `generation_intent` is non-null
(`astrid/sdk/invocation.py:2988-3007`). Runtime's generic task admission then
receives the normal `spec` and no publication fields.

### One captured real SDK submit

I ran the real Agent `sdk.invoke("generation.generate_speech", ...)` against
the existing `tests/sdk/test_execution_request_binding.py` transport fixture,
with only its capability-list response narrowed to the real speech capability.
No speech provider, model service, or Runtime server was contacted. The
captured generated-client admission arguments were:

```json
{
  "capability_id": "generation.generate_speech",
  "capability_digest": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
  "project_id": "speech-fixture",
  "input_object_ids": [],
  "spec": {
    "authority_context": {
      "executor_version": "b5fc8fbf3b6d8fa50155f6cbce83e1610e0833b99a5bea164efa347116743deb"
    },
    "capability_id": "generation.generate_speech",
    "extra_pack_roots": [],
    "inputs": {
      "pitch": "+0Hz",
      "provider": "edge-tts",
      "rate": "+0%",
      "text": "The exact authored words.",
      "voice": "en-US-ChristopherNeural",
      "volume": "+0%"
    },
    "kind": "executor",
    "outputs": {}
  },
  "settlement_effect": null,
  "storage_estimate": null
}
```

The `cccc...` capability digest is the fixture transport's registered digest;
the executor-version digest is resolved from the real Agent pack definition.
The generated transport also supplied a fresh idempotency key. Most
importantly, there was no `generation_intent` key and the effect was null.

## Admission → claim → settlement authority

The existing seams are already sufficient to carry the fields; there is no
need for a speech-specific Runtime DTO:

1. Agent admission composes the existing intent/effect fields in
   `_kernel_invoke` only when an intent exists.
2. Runtime stores intent inside the task spec and exposes it on task/claim
   readback (`runtime_protocol/service.py:5381-5386`, `6238-6262`,
   `6990-7003`). Expected effect is also exposed from the task.
3. Runtime settlement refuses an effect that was not predeclared, and refuses
   to omit one that was declared (`runtime_protocol/service.py:7052-7059`).
4. With `generation.publish_v1`, Runtime creates the generation and variant and
   writes `generation_publish_v1` into the terminal result
   (`runtime_protocol/store.py:5480-5558`). Managed associations receive the
   Runtime-created generation id through the applied effect; generic output
   producer-supplied generation ids are deliberately ignored
   (`runtime_protocol/store.py:5274-5284`).
5. In either case, Runtime creates the managed association with task/attempt,
   output port/group/variant key, CAS digest, manifest reference, lifecycle,
   producer, and attempt-bound provenance (`runtime_protocol/store.py:5301-5338`).

For a normal speech request with no effect, the association's
`generation_id` is null. Its existing `association_id`, `task_id`,
`attempt_id`, object/digest, manifest reference, output port, and lifecycle are
still authoritative. This is not a raw-object-only result.

## Settled public SDK wrapper and reachability

For `sdk.invoke(..., wait=True)`, the existing observer reads terminal task
state and the managed-output page, then returns `InvocationResult`. The public
`outputs["managed_outputs"]` rows preserve Runtime-owned association fields
(`association_id`, task/attempt ids, object/digest, manifest reference,
producer/provenance, lifecycle, and `generation_id` when present). The public
DTO also exposes `kernel_task_id` and `kernel_attempt_id`
(`astrid/sdk/invocation.py:3396-3545`, `1824-1855`; `astrid/sdk/results.py:158-180`).

Reachability from the current normal result is therefore:

| Identity | Normal speech result | With explicit existing intent/effect |
|---|---|---|
| task id | `InvocationResult.kernel_task_id`, task readback, managed row | same |
| attempt id | `InvocationResult.kernel_attempt_id` after wait, task readback, managed row | same |
| object id / CAS | managed output row; manifest/audio rows are readable by digest | same |
| association id | managed output row | same |
| generation id | absent/null: no publication effect | terminal `generation_publish_v1` and managed row |
| variant id | absent: no variant exists; generic row has only `variant_key` | terminal `generation_publish_v1.publications[].variants[].variant_id` |
| exact five-field MediaSelection | not derivable from this normal result | reachable only after the existing Runtime generation/variant/catalog read path succeeds; the fixture still lacked intrinsic duration |

The `generate.audio(mode="tts")` facade can reconstruct the existing
`GenerationResult` from the invocation payload/managed rows, but the original
voiceover caller does not use that facade: it uses direct `sdk.invoke`, so its
authoritative terminal context is `InvocationResult` plus the managed-output
rows.

## Original voiceover / RIPPLE consumer

`runtime_synthesizer` selects the existing managed `speech_manifest` and
`speech` rows, reads both objects by their exact digest, verifies the WAV hash,
manifest audio hash, and manifest text hash, and returns only:

```text
text, settings, audio_media_id, duration_seconds, run_id, task_id
```

It drops `attempt_id`, `association_id`, generation/variant identity, catalog
identity, manifest reference, producer provenance, and lifecycle context
(`astrid/packs/video_editing/shared/draft_voiceover.py:382-414`).

`prepare_draft_voiceover` then binds the verified audio into the existing shot
asset/clip registry, applies the existing `preserve` or `ripple` retime policy,
and publishes through the existing authoring target. The old readable-audio
and RIPPLE positive behavior must remain unchanged. This trace does not turn
that positive into a refusal or `proposal_open` result.

## Bounded Agent recommendation before implementation

If the managed-output path is to produce a generation-backed speech selection,
the narrow Agent-owned adapter should be limited to the exact
`generation.generate_speech` capability used by `runtime_synthesizer`:

- classify that capability as the existing audio publication modality;
- construct the existing v1 opaque intent with one `audio`/`speech`/`main`/
  `original`/ordinal-0 selector and existing text/settings provenance;
- pass the existing `generation_intent` and the matching
  `generation.publish_v1` effect through the current `_kernel_invoke` →
  `RemoteTasks` admission, with no new DTO, endpoint, schema, producer pin, or
  raw-object adoption path;
- retain the terminal `InvocationResult`/managed-row context until the exact
  existing Runtime generation/variant/catalog read has returned a valid
  five-field `MediaSelection`. Never manufacture `generation_id`,
  `variant_id`, catalog digest, or duration from the task id, latest/gallery
  output, client input, or a raw CAS digest;
- only then hand the existing selection/verified audio into the current
  voiceover preparation path. If the exact selection is unavailable, preserve
  the current visible held/refusal behavior while preserving the old
  readable-audio/RIPPLE positive path.

Runtime remains the authority for generation/variant creation, managed-output
association, CAS bytes, attempt provenance, lifecycle, and settlement-effect
matching. Agent remains the authority for the bounded speech admission
adapter and for retaining result context until the consumer can make its
existing selection read. No new producer guard is assumed here.

## Evidence commands

Agent source head inspected: `79b33f8a1e69b27fd53f3cd5230301b84d0d4ef1`.
Runtime worker base: `e2db1e8cc7c176fafa1e4e651da3639b6e3a89dd`.

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_generation_publish_v1_settlement.py \
  tests/test_managed_output_public_api.py \
  tests/test_timeline_media_selection.py
# 25 passed in 4.56s
```

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_generate_audio_tts_routing.py \
  tests/sdk/test_invoke_settlement_and_replay.py
# 17 passed in 1.42s; 2 existing pytest-config warnings (unknown timeout options)
```

No full/broad suite, render, browser, live socket, external speech/model
service, package install, or shared dependency write was performed.
