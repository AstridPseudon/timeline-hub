from __future__ import annotations

from types import SimpleNamespace

import pytest

from astrid.core.contracts.schema import Output
from astrid.sdk.exceptions import CapabilityPreconditionError, CapabilityValidationError
from astrid.sdk.invocation import (
    _generation_publish_effect,
    _kernel_invoke,
    _generation_capability_modality,
    _resolve_generation_variant,
    invoke as public_invoke,
)
from astrid.sdk.results import Capability


DIGEST = "sha256:" + "a" * 64


class _Result:
    def __init__(self, data):
        self.ok = True
        self.data = data
        self.error = None


class _Generations:
    def __init__(self, *, project_id="project-1", version=4, variants=None):
        self.project_id = project_id
        self.version = version
        self._variants = variants if variants is not None else [
            {
                "variant_id": "variant-source",
                "generation_id": "generation-1",
                "object_id": DIGEST,
            }
        ]
        self.calls = []

    def show(self, project, generation_id):
        self.calls.append(("show", project, generation_id))
        return _Result(
            {
                "generation_id": generation_id,
                "project_id": self.project_id,
                "version": self.version,
            }
        )

    def variants(self, project, generation_id):
        self.calls.append(("variants", project, generation_id))
        return _Result([self._variants, None])


class _Projects:
    def show(self, project):
        return _Result({"project_id": "project-1", "slug": project})


def _client(generations=None):
    return SimpleNamespace(
        generations=generations or _Generations(),
        projects=_Projects(),
    )


def _capability(modality: str) -> Capability:
    port = {
        "image": "generated_images",
        "video": "generated_videos",
        "audio": "generated_audio",
    }[modality]
    artifact = {"image": "image", "video": "video/clip", "audio": "audio"}[modality]
    return Capability(
        id=f"generation.generate_{modality}",
        capability_type="executor",
        native_kind="executor",
        handle=SimpleNamespace(),
        outputs=(Output(name=port, type="file", artifact_type=artifact),),
    )


@pytest.mark.parametrize("modality", ["image", "video", "audio"])
@pytest.mark.parametrize("primary", ["preserve", "promote"])
def test_variant_publication_is_shared_across_generation_modalities(modality, primary):
    context = _resolve_generation_variant(
        _client(),
        project="project-1",
        variant_of={"generation_id": "generation-1", "variant_id": "variant-source"},
        primary=primary,
    )
    effect = _generation_publish_effect(
        _capability(modality),
        project="project-1",
        generation_intent={
            "version": 1,
            "modality": modality,
            "partial_success_policy": "reject",
            "groups": [{
                "group_key": "main",
                "selectors": [{
                    "selector": "main-0",
                    "ordinal": 0,
                    "variant_key": "original",
                }],
            }],
        },
        variant_context=context,
    )
    assert effect["effect_type"] == "generation.variant.append"
    assert effect["target_id"] == "generation-1"
    assert effect["expected_version"] == 4
    assert effect["payload"] == {
        "source_variant_id": "variant-source",
        "source_object_id": DIGEST,
        "variant_type": "edit",
        "output_name": {
            "image": "generated_images",
            "video": "generated_videos",
            "audio": "generated_audio",
        }[modality],
        "output_ordinal": 0,
        "primary_policy": primary,
    }


def test_variant_source_is_admitted_and_publication_controls_stay_out_of_executor_inputs():
    calls = []

    class Tasks:
        def create(self, **kwargs):
            calls.append(kwargs)
            return SimpleNamespace(
                ok=True,
                data={"run_id": "run-1", "task_id": "task-1", "attempt_id": "attempt-1"},
            )

    context = _resolve_generation_variant(
        _client(),
        project="project-1",
        variant_of={"generation_id": "generation-1", "variant_id": "variant-source"},
        primary="promote",
    )
    _kernel_invoke(
        _capability("image"),
        kind="executor",
        project="project-1",
        inputs={"prompt": "keep this executor input"},
        outputs={},
        generation_intent={
            "version": 1,
            "modality": "image",
            "partial_success_policy": "reject",
            "groups": [{
                "group_key": "main",
                "selectors": [{
                    "selector": "main-0",
                    "ordinal": 0,
                    "variant_key": "original",
                }],
            }],
        },
        variant_context=context,
        _client=SimpleNamespace(tasks=Tasks()),
    )
    request = calls[0]
    assert request["input_manifest"] == [DIGEST]
    assert "variant_of" not in request["spec"]["inputs"]
    assert "primary" not in request["spec"]["inputs"]
    assert request["settlement_effect"]["effect_type"] == "generation.variant.append"


def test_variant_rejects_primary_promotion_without_variant_source():
    with pytest.raises(CapabilityValidationError, match="requires variant_of"):
        # This is the same public guard used by invoke() before admission.
        from astrid.sdk.invocation import _validate_variant_controls

        _validate_variant_controls(None, "promote", modality="image")


def test_non_generation_capability_cannot_consume_explicit_primary_control():
    from astrid.sdk.invocation import _validate_variant_controls

    with pytest.raises(CapabilityValidationError, match="only accepted for generation"):
        _validate_variant_controls(None, "preserve", modality=None, primary_supplied=True)


def test_variant_rejects_wrong_project_and_raw_media_variant():
    with pytest.raises(CapabilityPreconditionError, match="different project"):
        _resolve_generation_variant(
            _client(_Generations(project_id="project-elsewhere")),
            project="project-1",
            variant_of={"generation_id": "generation-1", "variant_id": "variant-source"},
            primary="preserve",
        )

    raw = _Generations(variants=[{
        "variant_id": "variant-source",
        "generation_id": "generation-1",
        "object_id": None,
    }])
    with pytest.raises(CapabilityPreconditionError, match="managed object"):
        _resolve_generation_variant(
            _client(raw),
            project="project-1",
            variant_of={"generation_id": "generation-1", "variant_id": "variant-source"},
            primary="preserve",
        )


def test_generation_publication_metadata_advertises_opt_in_controls():
    from astrid.sdk.invocation import get_capability

    for modality in ("image", "video", "audio"):
        capability = get_capability(
            f"generation.generate_{modality}", kind="executor", include_elements=False
        )
        publication = capability.definition["metadata"]["generation_publication"]
        assert publication["variant_of"]["type"] == "object"
        assert publication["primary"]["enum"] == ["preserve", "promote"]
        assert publication["primary"]["default"] == "preserve"


def test_new_generation_capability_can_opt_into_shared_publication_contract():
    capability = SimpleNamespace(
        id="custom.generate_storyboard",
        definition={
            "metadata": {
                "generation_publication": {
                    "modality": "image",
                    "variant_of": {"type": "object"},
                    "primary": {"enum": ["preserve", "promote"]},
                }
            }
        },
    )
    assert _generation_capability_modality(capability) == "image"


@pytest.fixture(scope="module")
def registered_h3_finalizer():
    from astrid import sdk
    from astrid.sdk.invocation import get_capability
    registries = sdk._load_registries(include_elements=False)
    capability = get_capability("h3_av.publication_finalizer", kind="executor", include_elements=False,
                                _registries=registries)
    return capability, registries[0].get(capability.id)


def test_registered_h3_publication_selects_declared_port_and_retains_manifest(registered_h3_finalizer):
    from astrid.core.execution.generic_host import _generation_selector_declarations
    capability, definition = registered_h3_finalizer
    intent = {"version": 1, "modality": "video", "partial_success_policy": "reject",
              "groups": [{"group_key": "main", "selectors": [{"selector": "main-0", "ordinal": 0,
                                                             "variant_key": "final-composition"}]}]}
    effect = _generation_publish_effect(capability, project="project-1", generation_intent=intent)
    port, selectors = _generation_selector_declarations(SimpleNamespace(definition=definition), intent)
    assert port == "verified_candidate"
    assert selectors[0]["output_port"] == port
    assert effect["payload"]["groups"][0]["selectors"][0]["output_port"] == port
    assert [output.name for output in capability.outputs] == ["verified_candidate", "manifest"]
    assert capability.definition["metadata"]["generation_publication"] == {
        "version": 1, "modality": "video", "output_port": "verified_candidate"}


@pytest.mark.parametrize("fault", ["unknown", "duplicate", "non-file", "manifest", "blank", "null",
                                  "boolean-version", "unsupported-version", "modality", "not-mapping"])
def test_explicit_publication_invalid_metadata_rejects_without_fallback(registered_h3_finalizer, fault):
    from copy import deepcopy
    from dataclasses import replace
    from astrid.core.execution.generic_host import HostError, _generation_output_port
    from astrid.sdk.invocation import _generation_primary_output_port
    capability, definition = registered_h3_finalizer
    metadata = deepcopy(capability.definition["metadata"])
    declaration = metadata["generation_publication"]
    outputs = capability.outputs
    if fault == "unknown": declaration["output_port"] = "missing"
    elif fault == "duplicate": outputs = outputs + (outputs[0],)
    elif fault == "non-file": outputs = (replace(outputs[0], type="json"), outputs[1])
    elif fault == "manifest": declaration["output_port"] = "manifest"
    elif fault == "blank": declaration["output_port"] = " "
    elif fault == "null": declaration["output_port"] = None
    elif fault == "boolean-version": declaration["version"] = True
    elif fault == "unsupported-version": declaration["version"] = 2
    elif fault == "modality": declaration["modality"] = "image"
    else: metadata["generation_publication"] = "invalid"
    sdk_capability = replace(capability, outputs=outputs, definition={**capability.definition, "metadata": metadata})
    host_definition = replace(definition, outputs=outputs, metadata=metadata)
    with pytest.raises(CapabilityValidationError):
        _generation_primary_output_port(sdk_capability, "video")
    with pytest.raises(HostError):
        _generation_output_port(SimpleNamespace(definition=host_definition), {"modality": "video"})


def test_absent_explicit_port_keeps_legacy_ambiguous_rejection(registered_h3_finalizer):
    from copy import deepcopy
    from dataclasses import replace
    from astrid.core.execution.generic_host import HostError, _generation_output_port
    from astrid.sdk.invocation import _generation_primary_output_port
    capability, definition = registered_h3_finalizer
    metadata = deepcopy(capability.definition["metadata"])
    del metadata["generation_publication"]["output_port"]
    with pytest.raises(CapabilityValidationError, match="exactly one primary"):
        _generation_primary_output_port(replace(capability, definition={**capability.definition, "metadata": metadata}), "video")
    with pytest.raises(HostError, match="exactly one primary"):
        _generation_output_port(SimpleNamespace(definition=replace(definition, metadata=metadata)), {"modality": "video"})


@pytest.fixture(scope="module")
def registered_speech_generator():
    from astrid import sdk
    from astrid.sdk.invocation import get_capability

    registries = sdk._load_registries(include_elements=False)
    capability = get_capability(
        "generation.generate_speech",
        kind="executor",
        include_elements=False,
        _registries=registries,
    )
    return capability, registries[0].get(capability.id)


def _speech_publication_intent():
    return {
        "version": 1,
        "modality": "audio",
        "partial_success_policy": "reject",
        "groups": [{
            "group_key": "main",
            "selectors": [{
                "selector": "main-0",
                "ordinal": 0,
                "variant_key": "original",
                "required": True,
            }],
        }],
    }


@pytest.mark.parametrize("explicit", [False, True], ids=["automatic", "explicit"])
def test_registered_speech_public_invocation_admits_project_bound_publication(
    registered_speech_generator, explicit
):
    capability, _ = registered_speech_generator
    assert capability.definition["metadata"]["generation_publication"] == {
        "version": 1,
        "modality": "audio",
        "output_port": "speech",
    }
    calls = []

    class Tasks:
        def create(self, **kwargs):
            calls.append(kwargs)
            return _Result({
                "run_id": "speech-run",
                "task_id": "speech-task",
                "attempt_id": "speech-attempt",
            })

    inputs = {"text": "Hello from the registered speech capability."}
    if explicit:
        inputs["generation_intent"] = _speech_publication_intent()
    public_invoke(
        "generation.generate_speech",
        kind="executor",
        project="project-1",
        inputs=inputs,
        client=SimpleNamespace(tasks=Tasks()),
    )

    assert len(calls) == 1
    admission = calls[0]
    intent = admission["generation_intent"]
    assert intent["version"] == 1
    assert intent["modality"] == "audio"
    if not explicit:
        assert "metadata" not in intent
    selector = intent["groups"][0]["selectors"][0]
    assert (selector["selector"], selector["ordinal"]) == ("main-0", 0)
    assert admission["project_id"] == "project-1"
    assert admission["settlement_effect"]["effect_type"] == "generation.publish_v1"
    assert admission["settlement_effect"]["target_id"] == "project-1"
    published_selector = admission["settlement_effect"]["payload"]["groups"][0]["selectors"][0]
    assert published_selector["ordinal"] == 0
    assert published_selector["output_port"] == "speech"
    assert admission["spec"]["inputs"] == {"text": "Hello from the registered speech capability."}
    assert "generation_intent" not in admission["spec"]["inputs"]


def test_registered_speech_host_uses_speech_port_and_keeps_provenance_outputs(
    registered_speech_generator,
):
    from astrid.core.execution.generic_host import _generation_selector_declarations

    capability, definition = registered_speech_generator
    intent = _speech_publication_intent()
    port, selectors = _generation_selector_declarations(
        SimpleNamespace(definition=definition), intent
    )

    assert port == "speech"
    assert selectors[0]["output_port"] == "speech"
    assert [
        (output.name, output.type, output.path_template, output.artifact_type)
        for output in capability.outputs
    ] == [
        ("speech", "file", "{out}/audio/speech.wav", "audio"),
        ("speech_manifest", "file", "{out}/speech-provenance.json", None),
        ("speech_words", "file", "{out}/speech-words.json", "application/json"),
    ]
    assert capability.definition["metadata"]["generation_publication"] == {
        "version": 1,
        "modality": "audio",
        "output_port": "speech",
    }


@pytest.mark.parametrize("fault", ["modality", "port", "version", "ambiguous"])
def test_registered_speech_invalid_or_ambiguous_publication_declaration_refuses(
    registered_speech_generator, fault
):
    from copy import deepcopy
    from dataclasses import replace

    from astrid.core.execution.generic_host import HostError, _generation_output_port
    from astrid.sdk.invocation import _generation_primary_output_port

    capability, definition = registered_speech_generator
    metadata = deepcopy(capability.definition["metadata"])
    declaration = metadata["generation_publication"]
    if fault == "modality":
        declaration["modality"] = "video"
    elif fault == "port":
        declaration["output_port"] = "speech_manifest"
    elif fault == "version":
        declaration["version"] = 2
    else:
        del declaration["output_port"]
    sdk_capability = replace(
        capability,
        definition={**capability.definition, "metadata": metadata},
    )
    host_definition = replace(definition, metadata=metadata)

    with pytest.raises(CapabilityValidationError):
        _generation_primary_output_port(sdk_capability, "audio")
    with pytest.raises(HostError):
        _generation_output_port(
            SimpleNamespace(definition=host_definition), {"modality": "audio"}
        )


def test_registered_speech_publication_requires_a_project_before_admission(
    registered_speech_generator,
):
    calls = []

    class Tasks:
        def create(self, **kwargs):
            calls.append(kwargs)
            return _Result({"run_id": "speech-run", "task_id": "speech-task"})

    class Projects:
        def current(self):
            return SimpleNamespace(
                ok=False,
                error=SimpleNamespace(code="not_found"),
            )

    with pytest.raises(CapabilityPreconditionError):
        public_invoke(
            "generation.generate_speech",
            kind="executor",
            inputs={
                "text": "This request has no project.",
                "generation_intent": _speech_publication_intent(),
            },
            client=SimpleNamespace(tasks=Tasks(), projects=Projects()),
        )
    assert calls == []
