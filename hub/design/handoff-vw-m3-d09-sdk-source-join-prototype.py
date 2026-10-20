"""Unapplied D09 contract probe. One positive intentionally remains red.

Uses the real candidate projector and final Root staging. Runtime admission,
toolchain checks and the asset-free port selection are explicit test doubles.
The callback aborts before any render, browser or socket can start.
"""
import copy
import json
from types import SimpleNamespace

import pytest

from astrid.core.timeline import Timeline, onscreen, scene_answers
from astrid.core.timeline.authoring_bundle import (
    _digest, open_authoring_bundle, preview_authoring_candidate,
)
from astrid.packs.rendering.actions.render import managed_timeline
from astrid.packs.rendering.rendering.renderers.remotion import run
from astrid.sdk.timeline_checkout import Checkout
from astrid.sdk.timeline_filmstrip import prepare_filmstrip
from tests.packs.rendering.test_capture_scene_labels import host, native  # noqa: F401
from tests.packs.rendering.test_scene_source_carry import Revisions


@pytest.fixture
def prepared_candidate(host, native, tmp_path, monkeypatch):
    client = Revisions("am-snap-plate")
    client.internal["payload"]["clips"] = [{
        "id": "opaque:source:field", "track": "picture", "clipType": "am-snap-plate",
        "at": 0, "hold": 1, "params": {"fill": "#F7F4ED"},
        "app": {"astrid": {"cut": "c08", "layer": "field"}},
    }]
    parent = client.get_project_parent_composition_revision("p", "tl", "parent:old")
    parent["payload"]["occurrences"] = parent["payload"]["occurrences"][:1]
    shot = client.get_project_shot_revision("p", "s", "shot:old")
    shot["project_id"] = "p"
    internal = copy.deepcopy(client.internal)
    for row in (parent, shot, internal):
        row["content_digest"] = _digest(row["payload"])
    checkout = Checkout(open_authoring_bundle(
        parent, shot_revisions=[shot], internal_timeline_revisions=[internal]))
    checkout.clips()[0].set(fill="#123456")
    report = checkout.check()  # freeze the actual post-resolve document
    assert report.valid and any("EMPTY" in line and "c08" in line for line in report.problems)
    preview = preview_authoring_candidate(checkout.document())
    monkeypatch.setattr(managed_timeline, "_runtime_snapshot_registry", lambda registry, **kw: registry)
    snapshot = prepare_filmstrip(
        {"composed_capture": True, "timeline_ref": "tl", "authoring_preview": preview},
        project="demo", client=client)["capture_snapshot"]
    assert snapshot["metadata"]["working_copy"]["candidate_digest"] == preview["candidate_digest"]
    timeline = tmp_path / "timeline.json"
    assets = tmp_path / "assets.json"
    Timeline.from_config(snapshot["config"]).dump(timeline)
    assets.write_text(json.dumps(snapshot["registry"]))
    monkeypatch.setattr(run, "_regenerate_element_registries", lambda *a: None)
    monkeypatch.setattr(run, "_validate_project_dir", lambda _: SimpleNamespace(
        node_executable="unused", remotion_cli="unused"))
    monkeypatch.setattr(run, "_available_remotion_port", lambda: 32101)
    observed = []

    class Observed(Exception):
        pass

    def observe(props, frames):
        assert json.loads((tmp_path / ".remotion-props.json").read_text()) == props
        observed.append(copy.deepcopy(props))
        raise Observed

    with pytest.raises(Observed):
        run._execute_remotion_locked(
            timeline, assets, tmp_path / "unused.mp4", provenance_out_path=tmp_path / "unused.mp4",
            project_dir=host, composition_id=run.DEFAULT_COMPOSITION_ID, theme_path=None,
            min_free_gb=None, frame_numbers=(0, 24), frame_output_dir=tmp_path / "unused-frames",
            on_scene_props=observe)
    assert not (tmp_path / ".remotion-props.json").exists()
    profile = run._canonical_profile(timeline, snapshot["registry"], None)
    basis = {"width": profile.width, "height": profile.height,
             "fps": profile.fps_rational[0] / profile.fps_rational[1]}
    rows = scene_answers.host_frames_at(observed[0], basis, range(24))
    print(json.dumps({"basis": basis, "clips": observed[0]["timeline"]["clips"],
                      "rows": [[r["frame"], r["coverage"], r["content"]] for r in rows]}))
    return checkout, preview, snapshot, rows


def test_exact_resolved_candidate_has_public_empty_and_opaque_address_join(prepared_candidate):
    checkout, preview, snapshot, rows = prepared_candidate
    assert preview["candidate"] == checkout.document()
    assert {(row["coverage"], row["content"]) for row in rows} == {("COVERED", "EMPTY")}
    identities = snapshot["metadata"]["scene_clips"]
    assert {row["layers"][0]["clipId"] for row in rows} == set(identities)
    assert {entry["address"] for entry in identities.values()} == {"c08.field"}
    assert {entry["occurrence_id"] for entry in identities.values()} == {"opaque:occ:A"}


def test_explicit_check_preserves_public_empty_without_private_coverage(prepared_candidate, monkeypatch):
    checkout, _, _, rows = prepared_candidate
    assert all(row["coverage"] == "COVERED" and row["content"] == "EMPTY" for row in rows)

    def forbidden(*a, **kw):
        raise AssertionError("D09 seam: exact prepared candidate exists, check still calls private coverage")

    monkeypatch.setattr(onscreen, "coverage", forbidden)
    # No existing check API consumes the prepared candidate/Root/rows above.
    # Keep the real positive expectation red; do not replace it with refusal.
    report = checkout.check()
    assert report.valid and any("EMPTY" in line and "c08.field" in line for line in report.problems)
