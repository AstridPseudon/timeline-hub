"""One round trip per agent-written visual field: setter -> provider -> installed package.

The case keys and stored values are the ones Runtime publishes and reads back (24 fps), so the App preview
fixture can compare against the same table. Refusals that must happen before publication are listed last.
"""
from __future__ import annotations

import copy
import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

from astrid.core.timeline import clip_fields as cf
from astrid.core.timeline.authoring_bundle import AuthoringBundleError
from astrid.sdk.timeline.commit import bundle_from_document
from astrid.sdk.timeline.validation import validate_final_candidate
from tests.sdk.test_timeline_commit_provider_document import document_fixture

ROOT = Path(__file__).resolve().parents[3]
REMOTION = ROOT / "remotion"
FPS = 24

_FADE = {"id": "fade", "durationFrames": 12}
_SAMPLES = [0, 3, 6, 40, 47]
_OPACITY = [0.0, 0.5, 1.0, 0.6667, 0.0833]

# case_key -> (field, how the agent writes it, stored value, what the installed package draws)
# "written" is the human setter form, or None when the value only arrives as a raw doc.patch.
CASES = {
    "entrance.fade": ("entrance", "fade 0.5s ease=step", {**_FADE, "params": {"easing": "step"}},
                      {"entrance": [{"id": "fade", "durationFrames": 12, "easing": "step"}]}),
    "entrance.fade.linear": ("entrance", "fade 12f ease=linear", {**_FADE, "params": {"easing": "linear"}},
                             {"entrance": [{"id": "fade", "durationFrames": 12, "easing": "linear"}]}),
    "entrance.fade-up": ("entrance", "fade-up 18f", {"id": "fade-up", "durationFrames": 18},
                         {"entrance": [{"id": "fade-up", "durationFrames": 18, "easing": None}]}),
    "entrance.scale-in": ("entrance", "scale-in 18f", {"id": "scale-in", "durationFrames": 18},
                          {"entrance": [{"id": "scale-in", "durationFrames": 18, "easing": None}]}),
    "exit.fade": ("exit", "fade 12f", dict(_FADE), {"exit": [{"id": "fade", "durationFrames": 12, "easing": None}]}),
    "exit.slide-up": ("exit", "slide-up 12f", {"id": "slide-up", "durationFrames": 12},
                      {"exit": [{"id": "slide-up", "durationFrames": 12, "easing": None}]}),
    # The package's own default for an omitted transition duration is 8 frames, and B owns the A -> B span.
    # The setter's word for the stored "fade" transition is "dip" (clip_fields.yaml transition.values).
    "transition.fade.default": ("transition", "dip", {"id": "fade"},
                                {"transition": {"frames": 8, "drawStart": 40, "ownOffset": 8}}),
    "transition.cross-fade.default": ("transition", "crossfade", {"id": "cross-fade"},
                                      {"transition": {"frames": 8, "drawStart": 40, "ownOffset": 8}}),
    "transition.fade.explicit-frames": ("transition", "dip 8f", {"id": "fade", "durationFrames": 8},
                                        {"transition": {"frames": 8, "drawStart": 40, "ownOffset": 8}}),
    "transition.cross-fade.legacy-seconds": ("transition", None, {"type": "crossfade", "duration": 0.5},
                                             {"transition": {"frames": 12, "drawStart": 36, "ownOffset": 12}}),
    "effects.array": ("effects", None, [{"fade_in": 0.25}, {"fade_out": 0.5}], {"opacity": _OPACITY}),
    "effects.object": ("effects", None, {"fade_in": 0.25, "fade_out": 0.5}, {"opacity": _OPACITY}),
}
SETTER_CASES = [key for key, case in CASES.items() if case[1] is not None]
# Raw legacy values the setter normalises to the canonical package reference, so both forms must draw alike.
LEGACY_NORMALISED = {"transition.cross-fade.legacy-seconds": {"id": "cross-fade", "durationFrames": 12}}


def _candidate(owner: str, field: str, value) -> dict:
    bundle = bundle_from_document(document_fixture(shared=False))
    if owner == "parent":
        timeline = bundle["parent"]
        timeline["clips"][0][field] = copy.deepcopy(value)
        timeline["config"]["clips"] = copy.deepcopy(timeline["clips"])
    else:
        bundle["shots"]["chapter-shot"]["internal_timeline"]["clips"][0][field] = copy.deepcopy(value)
    return bundle


@pytest.mark.parametrize("key", SETTER_CASES)
def test_setter_writes_the_runtime_published_value(key):
    field, written, stored, _ = CASES[key]
    clip: dict = {}
    cf.write(clip, field, written, fps=FPS)
    assert clip[field] == stored
    assert cf.read(clip, field) == stored
    # What the agent reads back is what it can write again.
    again: dict = {}
    cf.write(again, field, cf.describe(clip, fps=FPS)[field], fps=FPS)
    assert again == clip


@pytest.mark.parametrize("owner", ["parent", "child"])
@pytest.mark.parametrize("key", list(CASES))
def test_provider_accepts_every_published_value(key, owner):
    field, _, stored, _ = CASES[key]
    validate_final_candidate(_candidate(owner, field, stored))


@pytest.mark.parametrize("key", list(LEGACY_NORMALISED))
def test_legacy_value_normalises_to_the_canonical_reference(key):
    field, _, stored, _ = CASES[key]
    assert cf.coerce(field, stored, fps=FPS)[1] == LEGACY_NORMALISED[key]


@pytest.mark.integration
def test_installed_package_draws_what_the_table_says(tmp_path):
    # Needs the locked Remotion install (the render-proof lane provides it), like test_composition_package.py.
    peers = Path(os.environ.get("ASTRID_TEST_NODE_MODULES", str(REMOTION / "node_modules"))).resolve()
    host = tmp_path / "module-host"
    host.mkdir()
    (host / "node_modules").symlink_to(peers, target_is_directory=True)
    script = host / "visual-field-round-trip.mjs"
    shutil.copyfile(REMOTION / "tests/visual-field-round-trip.mjs", script)
    rows = [{"key": key, "clip": {field: stored}} for key, (field, _, stored, _) in CASES.items()]
    rows += [{"key": f"{key}.canonical", "clip": {CASES[key][0]: canonical}} for key, canonical in LEGACY_NORMALISED.items()]
    request = host / "rows.json"
    request.write_text(json.dumps({"fps": FPS, "rows": rows}))
    done = subprocess.run([os.environ.get("ASTRID_NODE_EXECUTABLE", "node"), str(script), str(request)],
                          cwd=host, check=True, capture_output=True, text=True, timeout=120)
    drawn = json.loads(done.stdout)
    for key, (_, _, _, expected) in CASES.items():
        assert drawn[key] == expected, key
    for key in LEGACY_NORMALISED:
        assert drawn[f"{key}.canonical"] == drawn[key], key


# Refused before publication: the setter or the provider stops what the package cannot draw.
# Neighbouring tests already pin the full lists (test_clip_fields.py, test_commit_v2_validation.py); these are the
# per-field cases of this table.
@pytest.mark.parametrize("field,raw", [
    ("entrance", "type-on 18f"),
    ("entrance", "slide-up 12f"),
    ("exit", "fade-up 12f"),
    ("entrance", {"type": "fade-up", "params": {"distance": 60}}),
    ("entrance", "swirl 12f"),
    ("transition", {"id": "cross-fade", "params": {"easing": "out"}}),
    ("entrance", {"id": "fade", "durationFrames": 8.5}),
])
def test_setter_refuses_what_the_package_cannot_draw(field, raw):
    with pytest.raises(cf.ClipFieldError):
        cf.coerce(field, raw, fps=FPS)


@pytest.mark.parametrize("owner", ["parent", "child"])
@pytest.mark.parametrize("field,raw", [
    ("entrance", {"id": "type-on", "durationFrames": 18}),
    ("exit", {"id": "fade", "params": {"easing": "bounce"}}),
    ("entrance", {"id": "unknown-animation"}),
    ("entrance", {"id": "fade", "params": {"ignored": 1}}),
    ("transition", {"id": "fade", "params": {"easing": "out"}}),
    ("transition", {"id": "unknown-transition"}),
])
def test_provider_refuses_raw_values_the_package_cannot_draw(owner, field, raw):
    with pytest.raises(AuthoringBundleError):
        validate_final_candidate(_candidate(owner, field, raw))
