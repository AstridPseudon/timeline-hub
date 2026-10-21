# Runtime speech primary-WAV duration safety review

Verdict: FINDING — test assertion-preservation gap; do not approve until the
legacy audio-positive assertion is restored alongside the genuine speech case.

Scope reviewed:

- Source commit `d7597d5440d5ed5d5912235d547cb4380d226980`, tree
  `e1663a36fb6400af2a32479574fbe60d16d86443` (the requested review tree).
- Design: `design/runtime-speech-primary-wav-duration.md`.
- Changed source: `runtime_protocol/store.py` and
  `tests/test_generation_publish_v1_settlement.py`.
- Baseline parent: `30413e3`, tree `2c5a5088c90cddfb38fba6dadcad899b28fb2c59`.

## Finding

`tests/test_generation_publish_v1_settlement.py:_speech_effect` changed its
declared primary selector from `output_port: "audio"` to `output_port:
"speech"` (line 112). The existing exact positive settlement/selection/read
test then changed its output from `audio` to `speech` (line 510), and every
other former speech-capability case in this file was changed the same way
(invalid WAV, zero-rate WAV, explicit null/value, and authenticated read).
Thus the patch adds genuine `generation.generate_speech`/`speech` coverage but
silently removes the old positive `generation.generate_speech`/`audio`-
primary behavior. The remaining `audio` outputs in this file belong to
generic `generation.publish.v1` shape/fixture tests, not this duration
fallback, so they do not preserve that assertion.

The smallest one-to-one preservation fix is to retain the current positive
speech test and add an equivalent positive audio-port case, preferably by
making `_speech_effect` accept an `output_port` argument and parameterizing
`test_speech_settlement_derives_wav_duration_for_exact_media_selection` over
`["audio", "speech"]`. Keep the malformed-WAV/rate, explicit metadata/null,
authenticated-read, and exact-replay controls as speech cases as they are;
they are not the missing positive compatibility assertion.

## Implementation review

The production change is otherwise narrowly scoped: in
`runtime_protocol/store.py:4923-4935`, the existing condition now accepts
`output_port in {"audio", "speech"}`. The task capability remains exactly
`generation.generate_speech`; the settlement effect remains modality
`audio`; selector matching and primary selection remain Runtime-owned; MIME
remains limited to `audio/wav` and `audio/x-wav`; inference still requires
`duration_seconds` to be absent both from the output/variant metadata and
from the effect metadata; and `wav_duration` still reads the CAS object using
the output digest and declared size. No sidecar, client/source-window
authority, old-row normalization, new generation, or canonical timeline write
was added.

## Evidence

Reused handoff evidence from the design:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_generation_publish_v1_settlement.py -k 'not authenticated_http' \
  tests/test_imported_media_catalog.py tests/test_timeline_media_selection.py
36 passed, 1 deselected

request-test rt-m2-speech-primary-wav-duration-0336 targeted \
  --files "tests/test_generation_publish_v1_settlement.py"
16 passed in 2.34s
```

Bounded discriminator for the concrete preservation concern (inline fixture,
no repository changes): the pre-patch `generation.generate_speech` effect and
primary `audio` output still derive `duration_seconds == 1.0` under this
source tree.

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:$PWD/tests:$PWD/packages/python" \
  /home/user/work/venv-runtime/bin/python - <<'PY'
import tempfile
from pathlib import Path
from test_generation_publish_v1_settlement import _fixture, _output, _settle, _speech_effect, _wav_bytes

with tempfile.TemporaryDirectory() as root:
    def old_audio_effect(project_id):
        effect = _speech_effect(project_id)
        effect["payload"]["groups"][0]["selectors"][0]["output_port"] = "audio"
        return effect

    service, _project, task, attempt, effect = _fixture(
        Path(root), effect_factory=old_audio_effect,
        slug="speech-old-audio", capability="generation.generate_speech",
    )
    try:
        _settle(
            service, attempt,
            [_output(
                _wav_bytes(), output_port="audio", group_key="main",
                variant_key="original", ordinal=0, filename="speech.wav",
                media_type="audio/wav",
            )],
            effect=effect, key="old-audio-discriminator",
        )
        association = service.managed_outputs(task["task"]["id"])[0]
        variant = service.list_variants(association["generation_id"])["items"][0]
        assert variant["metadata"]["duration_seconds"] == 1.0
    finally:
        service.close()
print("old audio-port speech-capability discriminator: PASS")
PY
old audio-port speech-capability discriminator: PASS
```

No full suite, browser, render, model, or socket-capable duplicate was run.
