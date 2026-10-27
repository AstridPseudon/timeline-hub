import copy

import pytest

from runtime_protocol.errors import ValidationError
from runtime_protocol.timeline_visual_fields import validate_timeline_visual_fields


@pytest.mark.parametrize("phase,ref", [
    ("entrance", {"id": "fade", "durationFrames": 12, "params": {"easing": " EASE-OUT "}}),
    ("entrance", {"id": "fade-up", "durationFrames": 18}),
    ("entrance", {"id": "scale-in", "durationFrames": 18}),
    ("entrance", {"id": "slide-left", "durationFrames": 18}),
    ("entrance", {"id": "type-on", "durationFrames": 60,
                   "params": {"durationFraction": 0.55, "showCaret": True, "startFrame": 18}}),
    ("exit", {"id": "fade", "durationFrames": 12}),
    ("exit", {"id": "slide-up", "durationFrames": 12}),
])
def test_supported_builtin_animation_references_are_admitted(phase, ref):
    validate_timeline_visual_fields({"clips": [{phase: ref}]})


@pytest.mark.parametrize("phase,ref", [
    ("entrance", {"id": "slide-up", "durationFrames": 12}),
    ("exit", {"id": "fade-up", "durationFrames": 12}),
    ("entrance", {"id": "not-installed", "durationFrames": 12}),
    ("entrance", {"type": "fade", "duration": 0.4}),
    ("entrance", {"id": "fade", "durationFrames": 12, "duration": 0.4}),
    ("entrance", {"id": "fade", "durationFrames": 12, "params": {"easing": "bounce"}}),
    ("entrance", {"id": "fade", "durationFrames": 12, "params": {"amplitude": 2}}),
    ("entrance", {"id": "type-on", "durationFrames": 60, "params": {"showCaret": "yes"}}),
    ("entrance", {"id": "type-on", "durationFrames": 60, "params": {"startFrame": "soon"}}),
    ("entrance", {"id": "fade", "durationFrames": 0}),
])
def test_unsupported_animation_refs_are_refused(phase, ref):
    with pytest.raises(ValidationError):
        validate_timeline_visual_fields({"clips": [{phase: ref}]})


@pytest.mark.parametrize("ref", [
    {"id": "cross-fade", "durationFrames": 12},
    {"id": "fade", "durationFrames": 12},
    {"type": "crossfade", "duration": 0.2},
])
def test_supported_canonical_transition_references_are_admitted(ref):
    validate_timeline_visual_fields({"clips": [{"transition": ref}]})


@pytest.mark.parametrize("ref", [
    {"type": "wipe", "duration": 0.4},
    {"id": "wipe", "durationFrames": 12},
    {"id": "fade", "durationFrames": 12, "duration": 0.4},
    {"id": "fade", "durationFrames": 12, "params": {"easing": "out"}},
])
def test_unsupported_transition_refs_are_refused(ref):
    with pytest.raises(ValidationError):
        validate_timeline_visual_fields({"clips": [{"transition": ref}]})


@pytest.mark.parametrize("effects", [
    {"fade_in": 0.2, "fade_out": 0.3},
    [{"fade_in": 0.2}, {"fade_out": 0.3}],
])
def test_effects_collection_forms_and_scoped_elements_are_preserved(effects):
    document = {"clips": [{"effects": effects,
                           "params": {"entrance": "custom-element-setting"},
                           "elementRef": {"kind": "effect", "id": "project-custom/glow",
                                          "revision": "sha256:" + "a" * 64}}]}
    original = copy.deepcopy(document)

    validate_timeline_visual_fields(document)

    assert document == original
