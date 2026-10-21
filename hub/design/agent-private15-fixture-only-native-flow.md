# private15 fixture-only native flow

Status: **BLOCKED**. No production source, caller, TLS setting, capability source/digest, or test was changed.

## Exact source and first trace

The intended production inner call is real and distinct: `astrid/packs/video_editing/shared/draft_voiceover.py:536-548` (`runtime_synthesizer`) calls `sdk.invoke("generation.generate_speech", kind="executor", project=..., inputs={..., "generation_intent": _speech_generation_intent(...)}, wait=True)`. The intent is the existing v1 audio/main/speech/original/ordinal-0 publication shape at `draft_voiceover.py:385-410`.

SDK admission composes `generation.publish_v1` in `astrid/sdk/invocation.py:2211-2259`, but the current capability lookup does not classify `generation.generate_speech` as a generation capability. `_generation_capability_modality()` at `astrid/sdk/invocation.py:2077-2096` recognizes image/video/audio IDs or `metadata.generation_publication`; the speech definition at `astrid/packs/generation/pack.yaml:1601-1631` has no `generation_publication` metadata. The first actual failure is `astrid/sdk/invocation.py:4140-4144`: the normal request containing the production v1 intent raises `CapabilityValidationError("generation_intent is only accepted for generation capabilities")` before Runtime admission.

Therefore this current path is neither a local Edge fallback nor an admitted Runtime task: it fails before a Runtime task/attempt, v1 effect, claim, settlement, managed output, or selection exists. The Edge command is not reached in this trace. Adding the missing production metadata or bypassing the admission check in a test would be a production/source-authority change outside this assignment.

## Fixture boundary considered

The valid boundary, if the existing source gap is repaired by the owning production work, is the normal registered production `generation.generate_speech` capability with its real source/digest, real SDK admission, Runtime `claim_next`, real lease/fence/attempt settlement, and the existing `generation.publish_v1` effect. Only the authorized worker computation would read the committed `tests/fixtures/storyboard-assets/idea-1.wav` and submit the WAV plus matching manifest/word outputs. CAS, hash, project association, generation, variant, catalog, outer producer, proposal, requester outbox, retry, undo, provenance, and history would remain real. The live `GenericPackHost.run` path would be guarded so accidental Edge TTS/network use fails visibly.

That fixture route was not retained because the current normal request cannot create the required admitted task. No local output was presented as managed speech and no Runtime response was mocked.

Exact live-caller change: **none**.

## Evidence

Central named run (the one permitted run) failed at the pre-admission source gap, before any Edge/TLS call:

```text
R=$(.../request-test agt-m2-private15-fixture-only-native-flow agt-m2-private15-requester-restart-prep) && .../wait-test ...
test ...: fail exit=1 in 17s
CapabilityValidationError: generation_intent is only accepted for generation capabilities
astrid/sdk/invocation.py:4142
```

Local checks on the unchanged baseline test file:

- `PYTHONDONTWRITEBYTECODE=1 python3 -m py_compile tests/packs/video_editing/test_outer_voiceover_native.py`: passed.
- `git diff --check`: passed.
- Ruff reports pre-existing issues in that baseline file: unsorted imports and unused `target_duration`/`result` locals; no task patch was kept to alter unrelated baseline code.
