from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import replace
from types import SimpleNamespace

import pytest

from astrid.core.timeline.authoring_bundle import (
    AuthoringBundleError,
    UnsupportedAuthoringEditError,
    approve_authoring_candidate,
    authoring_contract,
    authoring_media_inventory,
    compile_authoring_candidate,
    decode_authoring_bundle_storage,
    diff_authoring_candidate,
    encode_authoring_bundle_storage,
    format_authoring_inspection,
    inspect_authoring_candidate,
    open_authoring_bundle,
    preview_authoring_candidate,
    promote_approved_authoring_candidate,
    publish_authoring_candidate,
    validate_authoring_candidate,
)
from astrid.core.timeline.shot_composition_projection import (
    ShotCompositionProjectionError,
    project_runtime_parent_composition,
)
from astrid.packs.rendering.actions.render.managed_timeline import ManagedRenderSnapshot
from astrid.sdk.authoring_render_preview import (
    candidate_preview_snapshot,
    render_authoring_candidate_preview,
)
from astrid.sdk.invocation import _prepare_managed_render_inputs
from astrid.sdk.timeline_editing import (
    add_track,
    duplicate_authoring_shot,
    move_occurrence_group,
    place_media,
    remove_authoring_shot,
)

OLD = "sha256:" + "1" * 64
NEW = "sha256:" + "2" * 64
AUDIO = "sha256:" + "3" * 64


def _digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return "sha256:" + hashlib.sha256(encoded.encode()).hexdigest()


def _closure(*, shared=True):
    internal_payload = {
        "tracks": [
            {"id": "picture", "kind": "visual", "opaque_track": {"future": True}},
            {"id": "voice", "kind": "audio"},
        ],
        "clips": [
            {
                "id": "picture-1",
                "track": "picture",
                "clipType": "media",
                "asset": "old-picture",
                "at": 0,
                "hold": 1,
                "rect": {"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.4},
                "opaque_clip": {"literal": "item-1"},
            },
            {
                "id": "voice-1",
                "track": "voice",
                "clipType": "media",
                "asset": "voice",
                "at": 0,
                "hold": 1,
            },
        ],
        "effects": [{"type": "opacity", "value": 0.75}],
        "audio": [{"track_id": "voice", "gain": 0.8}],
        "layout": {"width": 1920, "height": 1080},
        "registry": {
            "assets": {
                "old-picture": {"media_id": OLD, "type": "image", "opaque_asset": "keep"},
                "voice": {"media_id": AUDIO, "type": "audio"},
            },
            "opaque_registry": {"keep": [1, 2, 3]},
        },
        "assets": [],
        "opaque_timeline": {"future_schema": 7},
    }
    shot_payload = {
        "name": "Opening",
        "metadata": {"settings": {"look": "warm"}, "opaque": ["keep"]},
        "items": [
            {
                "item_id": "item-1",
                "media_id": OLD,
                "source_frame": None,
                "metadata": {
                    "role": "primary_visual",
                    "source_item_id": "item-1",
                    "opaque_literal": "item-1",
                },
            },
            {
                "item_id": "item-audio",
                "media_id": AUDIO,
                "source_frame": None,
                "metadata": {"role": "voiceover"},
            },
        ],
        "pools": [{"id": "pool-1", "opaque": "keep"}],
        "selected_variants": {"pool-1": "variant-1"},
        "provenance": {"source": "fixture", "shot_id_literal": "shot-shared"},
        "generation_inputs": {"visual": {"object_id": OLD}},
        "audio_bindings": [{"track_id": "voice", "object_id": AUDIO}],
        "text_bindings": [{"slot": "voiceover", "text": "hello"}],
        "internal_timeline_revision_id": "internal-1",
        "opaque_shot": {"future_schema": 9},
    }
    occurrences = [
        {
            "occurrence_id": "occ-1",
            "shot_id": "shot-shared",
            "shot_revision_id": "shot-rev-1",
            "placement": {"start_ms": 0, "track": "picture", "opaque_geometry": "keep"},
            "source_offset": {"start": 0, "end": 1000},
            "duration_ms": 1000,
            "speed": {"numerator": 1, "denominator": 1},
            "track": "picture",
            "transform": {"scale": 1, "opaque_transform": [4, 5]},
            "gain": 1,
            "muted": False,
            "provenance": {"placement": "first"},
            "future_occurrence": {"round_trip": True},
        }
    ]
    if shared:
        second = copy.deepcopy(occurrences[0])
        second["occurrence_id"] = "occ-2"
        second["placement"]["start_ms"] = 1000
        second["provenance"]["placement"] = "second"
        occurrences.append(second)
    parent_payload = {
        "config": {
            # Equal legacy definitions; missing non-app fields would be an
            # initial conflict under the strict film-track resolver.
            "tracks": copy.deepcopy(internal_payload["tracks"]),
            "clips": [{"id": "direct", "track": "picture", "asset": "direct", "at": 3, "hold": 1}],
            "opaque_parent_config": {"keep": True},
        },
        "registry": {"assets": {"direct": {"media_id": OLD}}},
        "clips": [{"id": "direct", "track": "picture", "asset": "direct", "at": 3, "hold": 1}],
        "occurrences": occurrences,
        "opaque_parent": {"keep": ["all", "fields"]},
    }
    parent = {
        "revision_id": "parent-1",
        "project_id": "project-1",
        "timeline_id": "main",
        "content_digest": _digest(parent_payload),
        "payload": parent_payload,
    }
    shot = {
        "revision_id": "shot-rev-1",
        "project_id": "project-1",
        "shot_id": "shot-shared",
        "internal_timeline_revision_id": "internal-1",
        "content_digest": _digest(shot_payload),
        "payload": shot_payload,
    }
    internal = {
        "revision_id": "internal-1",
        "project_id": "project-1",
        "timeline_id": "main",
        "content_digest": _digest(internal_payload),
        "payload": internal_payload,
    }
    return parent, [shot], [internal]


def _replace_selected_media(bundle, shot_id):
    shot = bundle["shots"][shot_id]
    shot["payload"]["items"][0]["media_id"] = NEW
    shot["internal_timeline"]["clips"][0]["asset"] = "new-picture"
    shot["internal_timeline"]["registry"]["assets"]["new-picture"] = {
        "media_id": NEW,
        "type": "image",
        "opaque_asset": "new",
    }


def _replace_values(value, replacements):
    if isinstance(value, dict):
        return {key: _replace_values(child, replacements) for key, child in value.items()}
    if isinstance(value, list):
        return [_replace_values(child, replacements) for child in value]
    return replacements.get(value, value)


def test_open_is_lossless_read_only_and_independent_for_shared_placements():
    parent, shots, timelines = _closure(shared=True)
    before = copy.deepcopy((parent, shots, timelines))

    bundle = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )

    assert (parent, shots, timelines) == before
    assert len(bundle["shots"]) == 2
    assert bundle["placements"][0]["shot_id"] != bundle["placements"][1]["shot_id"]
    first, second = [bundle["shots"][row["shot_id"]] for row in bundle["placements"]]
    assert first["payload"]["items"][0]["item_id"] != second["payload"]["items"][0]["item_id"]
    assert (
        first["payload"]["items"][0]["metadata"]["source_item_id"]
        == first["payload"]["items"][0]["item_id"]
    )
    # Opaque literal strings are not guessed to be references.
    assert first["payload"]["items"][0]["metadata"]["opaque_literal"] == "item-1"
    assert first["payload"]["opaque_shot"] == {"future_schema": 9}
    assert first["internal_timeline"]["opaque_timeline"] == {"future_schema": 7}
    assert bundle["parent"]["opaque_parent"] == {"keep": ["all", "fields"]}
    assert bundle["placements"][0]["future_occurrence"] == {"round_trip": True}

    contract = authoring_contract()
    assert contract["timing"]["intervals"] == "half-open [start,end)"
    assert "source-to-authoring identity mapping" in contract["derived"]
    assert "transform" in contract["capabilities"]["placement"]["editable"]
    assert "source_offset" in contract["capabilities"]["placement"]["guarded"]


def test_compile_materializes_shared_identity_and_keeps_untouched_content():
    parent, shots, timelines = _closure(shared=True)
    bundle = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    first_id = bundle["placements"][0]["shot_id"]
    second_id = bundle["placements"][1]["shot_id"]
    _replace_selected_media(bundle, first_id)

    compiled = compile_authoring_candidate(bundle)
    publication = compiled.publication

    assert {row["shot_id"] for row in publication["shot_revisions"]} == {first_id, second_id}
    by_id = {row["shot_id"]: row for row in publication["shot_revisions"]}
    assert by_id[first_id]["payload"]["items"][0]["media_id"] == NEW
    assert by_id[second_id]["payload"]["items"][0]["media_id"] == OLD
    assert by_id[first_id]["payload"]["metadata"] == by_id[second_id]["payload"]["metadata"]
    assert publication["parent_composition"]["config"] == parent["payload"]["config"]
    assert publication["parent_composition"]["opaque_parent"] == parent["payload"]["opaque_parent"]
    assert publication["parent_composition"]["occurrences"][0]["future_occurrence"] == {
        "round_trip": True
    }
    assert publication["parent_composition"]["occurrences"][0]["duration_ms"] == 1000
    assert {row["media_id"] for row in publication["dependency_manifest"]["media"]} == {
        OLD,
        NEW,
        AUDIO,
    }


def _parent_clear_bundle(*, duplicate):
    parent, _, _ = _closure(shared=False)
    parent["payload"]["occurrences"] = []
    opaque = {"null": None, "false": False, "empty": "", "array": [],
              "object": {}, "literal": {"op": "clear"}}
    clips = [
        {"id": "before", "at": 0, "hold": 2, "track": "picture", "clipType": "hold"},
        {"id": "after", "at": 2, "hold": 2, "track": "picture", "clipType": "hold",
         "opacity": 0.7, "params": {"sibling": copy.deepcopy(opaque)},
         "app": {"sentinel": copy.deepcopy(opaque)}, "opaqueUnknown": copy.deepcopy(opaque),
         "transition": {"type": "cross-fade", "revision": "sha256:transition-r1",
                        "duration": 0.5, "params": {}},
         "elementRef": {"id": "cross-fade", "revision": "sha256:transition-r1",
                        "kind": "transition", "packId": "rendering"}},
    ]
    parent["payload"]["clips"] = clips
    if duplicate:
        parent["payload"]["config"]["clips"] = copy.deepcopy(clips)
    else:
        parent["payload"]["config"].pop("clips")
    parent["content_digest"] = _digest(parent["payload"])
    return open_authoring_bundle(
        parent, shot_revisions=[], internal_timeline_revisions=[]
    )


@pytest.mark.parametrize("duplicate", [True, False], ids=["duplicate-view", "one-view"])
@pytest.mark.parametrize("present", [("transition", "elementRef"), ("transition",),
                                    ("elementRef",), ()])
def test_compile_parent_transition_clear_preserves_exact_siblings(duplicate, present):
    from astrid.sdk.timeline import commands
    from astrid.sdk.timeline.checkout import Checkout

    bundle = _parent_clear_bundle(duplicate=duplicate)
    for parent in (bundle["parent"], bundle["base_parent_payload"]):
        for clips in [parent["clips"], *([parent["config"]["clips"]] if duplicate else [])]:
            for field in {"transition", "elementRef"} - set(present):
                clips[1].pop(field)
    before = copy.deepcopy(bundle)
    baseline = compile_authoring_candidate(bundle).publication["parent_composition"]
    selected = bundle["parent"]["clips"][1]
    # Preserved App request shape, including explicit absent property guards.
    expect = {
        key: {"state": "present", "value": copy.deepcopy(selected[key])}
        if key in selected else {"state": "absent"}
        for key in ("track", "at", "hold", "from", "to", "speed", "clipType",
                    "app.astrid.on", "app.astrid.until", "app.astrid.for",
                    "transition", "elementRef")
    }
    expect["parent/track:picture::kind"] = {"state": "present", "value": "visual"}
    checkout = Checkout(copy.deepcopy(bundle))
    commands.execute(checkout, {
        "op": "clip.set-transition", "select": "parent/clip:after",
        "resolved": ["parent/clip:after"], "args": {"clear": True}, "expect": expect,
    })
    candidate = checkout.document()
    authored = copy.deepcopy(candidate)
    compiled = compile_authoring_candidate(candidate).publication
    expected = copy.deepcopy(baseline)
    for clips in [expected["clips"], *([expected["config"]["clips"]] if duplicate else [])]:
        for field in ("transition", "elementRef"):
            clips[1].pop(field, None)
    assert compiled["parent_composition"] == expected
    assert ("clips" in compiled["parent_composition"]["config"]) is duplicate
    if duplicate:
        actual = compiled["parent_composition"]
        assert actual["clips"] == actual["config"]["clips"]
    assert compiled["content_digest"] == _digest(expected)
    assert compiled["shot_revisions"] == compiled["internal_timeline_revisions"] == []
    assert candidate == authored
    assert bundle == before


@pytest.mark.parametrize("divergence", ["baseline", "alternate", "both", "new-mirror", "scalar-type"])
def test_compile_parent_clip_mirror_refuses_independent_divergence(divergence):
    bundle = _parent_clear_bundle(duplicate=divergence != "new-mirror")
    if divergence == "baseline":
        bundle["base_parent_payload"]["config"]["clips"][0]["opaque"] = "different"
    else:
        alternate = bundle["parent"]["config"].setdefault(
            "clips", copy.deepcopy(bundle["parent"]["clips"])
        )
        if divergence == "scalar-type":
            alternate[0]["at"] = False  # Python equality must not conflate false and 0.
        else:
            alternate[0]["opaque"] = "independent edit"
        if divergence == "both":
            bundle["parent"]["clips"][1].pop("transition")
    before = copy.deepcopy(bundle)
    with pytest.raises(AuthoringBundleError, match="clip.*disagree"):
        compile_authoring_candidate(bundle)
    assert bundle == before


def test_compact_children_hash_the_complete_publication_without_mutating_authored_bytes():
    parent, shots, timelines = _closure(shared=True)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    for shot in candidate["shots"].values():
        shot["internal_timeline"].pop("assets")
        for key in ("generation_inputs", "audio_bindings", "selected_variants"):
            shot["payload"].pop(key, None)
    for placement in candidate["placements"]:
        placement.pop("gain")
        placement.pop("muted")
    before = copy.deepcopy(candidate)
    compact = compile_authoring_candidate(candidate)
    assert candidate == before
    explicit = copy.deepcopy(candidate)
    for shot in explicit["shots"].values():
        shot["internal_timeline"]["assets"] = []
        shot["payload"].update(generation_inputs={}, audio_bindings=[], selected_variants={})
    for placement in explicit["placements"]:
        placement.update(gain=1, muted=False)
    assert compact.publication == compile_authoring_candidate(explicit).publication
    for kind in ("internal_timeline_revisions", "shot_revisions"):
        for row in compact.publication[kind]:
            assert row["content_digest"] == _digest(row["payload"])
    for shot_id, shot in before["shots"].items():
        row = next(r for r in compact.publication["shot_revisions"] if r["shot_id"] == shot_id)
        assert all(row["payload"][key] == value for key, value in shot["payload"].items()
                   if key != "internal_timeline_revision_id")
        internal = next(r for r in compact.publication["internal_timeline_revisions"]
                        if r["revision_id"] == row["internal_timeline_revision_id"])
        assert all(internal["payload"][key] == value for key, value in shot["internal_timeline"].items())


def test_compact_producer_public_http_digests_and_refusals(tmp_path):
    daemon_module = pytest.importorskip("runtime_protocol.daemon")
    runtime_store = pytest.importorskip("runtime_protocol.store")
    from banodoco_workspace_client import ApiError, WorkspaceClient

    root = tmp_path / "realm"
    runtime_store.RealmStore.initialize(root).close()
    (tmp_path / "exports").mkdir()
    daemon = daemon_module.RuntimeDaemon(
        root, support_root=tmp_path / "support", export_root=tmp_path / "exports",
        host="127.0.0.1", port=0,
    ).start()
    try:
        client = WorkspaceClient(daemon.endpoint, daemon.token)
        project = client.create_project("Compact producer", slug="compact", idempotency_key="project")
        project_id = project.get("id") or project["project_id"]
        client.create_timeline(project_id, "main", idempotency_key="timeline")
        parent, shots, timelines = _closure(shared=True)
        for shot in shots:
            shot["payload"]["text_bindings"] = []  # Independent of registered shot text.
        replacements = {"project-1": project_id}
        for label, digest in (("old", OLD), ("new", NEW), ("audio", AUDIO)):
            imported = client.ingest_project_object(
                project_id, label.encode(), media_type="audio/wav" if label == "audio" else "image/png",
                idempotency_key=label,
            )
            replacements[digest] = imported["object_id"]
        parent, shots, timelines = _replace_values([parent, shots, timelines], replacements)
        for row in [parent, *shots, *timelines]:
            row["content_digest"] = _digest(row["payload"])
        candidate = open_authoring_bundle(parent, shot_revisions=shots, internal_timeline_revisions=timelines)
        for shot in candidate["shots"].values():
            shot["internal_timeline"].pop("assets")
            shot["payload"].pop("generation_inputs", None)
        publication = copy.deepcopy(compile_authoring_candidate(candidate).publication)
        publication["expected_head"] = None
        for kind in ("internal_timeline_revisions", "shot_revisions"):
            stale = copy.deepcopy(publication)
            stale[kind][0]["content_digest"] = "sha256:" + "0" * 64
            with pytest.raises(ApiError, match="content digest mismatch"):
                client.publish_parent_composition(project_id, "main", stale, idempotency_key=kind)
            with pytest.raises(ApiError, match="timeline has no parent composition revision"):
                client.inspect_timeline(project_id, "main")
        stale_parent = copy.deepcopy(publication)
        stale_parent["content_digest"] = "sha256:" + "0" * 64
        with pytest.raises(ApiError, match="parent composition content digest mismatch"):
            client.publish_parent_composition(project_id, "main", stale_parent, idempotency_key="parent-digest")
        stale_manifest = copy.deepcopy(publication)
        stale_manifest["dependency_manifest"]["internal_timelines"][0]["content_digest"] = "sha256:" + "0" * 64
        with pytest.raises(ApiError, match="dependency manifest does not match"):
            client.publish_parent_composition(project_id, "main", stale_manifest, idempotency_key="manifest-digest")
        malformed = copy.deepcopy(publication)
        malformed["internal_timeline_revisions"][0]["payload"]["effects"] = {}
        with pytest.raises(ApiError, match="effects must be a list"):
            client.publish_parent_composition(project_id, "main", malformed, idempotency_key="malformed")
        accepted = client.publish_parent_composition(project_id, "main", publication, idempotency_key="accepted")
        fresh = WorkspaceClient(daemon.endpoint, daemon.token)
        assert fresh.inspect_timeline(project_id, "main")["head_revision_id"] == publication["parent_revision_id"]
        assert accepted["content_digest"] == publication["content_digest"]
        for row in publication["internal_timeline_revisions"]:
            read = fresh.get_project_timeline_revision(project_id, row["timeline_id"], row["revision_id"])
            assert (read["payload"], read["content_digest"]) == (row["payload"], row["content_digest"])
        for row in publication["shot_revisions"]:
            read = fresh.get_project_shot_revision(project_id, row["shot_id"], row["revision_id"])
            assert (read["payload"], read["content_digest"]) == (row["payload"], row["content_digest"])
        assert accepted["dependency_manifest"] == publication["dependency_manifest"]
    finally:
        daemon.stop()


def test_independent_unique_shot_reuses_untouched_revision_and_direct_edits_compile_identically():
    parent, shots, timelines = _closure(shared=False)
    helper_candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    direct_candidate = copy.deepcopy(helper_candidate)
    shot_id = helper_candidate["placements"][0]["shot_id"]
    _replace_selected_media(helper_candidate, shot_id)
    _replace_selected_media(direct_candidate, shot_id)

    helper = compile_authoring_candidate(helper_candidate)
    direct = compile_authoring_candidate(direct_candidate)

    assert helper.as_dict() == direct.as_dict()
    assert len(helper.changed_identities) == 1
    unchanged = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    reused = compile_authoring_candidate(unchanged)
    assert reused.publication["shot_revisions"] == []
    assert reused.publication["internal_timeline_revisions"] == []
    assert reused.reused_identities[0]["shot_revision_id"] == "shot-rev-1"


def test_reopen_materialized_candidate_keeps_independent_shot_ids_stable():
    parent, shots, timelines = _closure(shared=True)
    first = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    compiled = compile_authoring_candidate(first)
    publication = compiled.publication
    parent_row = {
        "revision_id": publication["parent_revision_id"],
        "project_id": publication["project_id"],
        "timeline_id": publication["timeline_id"],
        "content_digest": publication["content_digest"],
        "payload": publication["parent_composition"],
    }
    shot_rows = [
        {
            "project_id": publication["project_id"],
            **row,
        }
        for row in publication["shot_revisions"]
    ]
    internal_rows = [
        {
            "project_id": publication["project_id"],
            **row,
        }
        for row in publication["internal_timeline_revisions"]
    ]

    reopened = open_authoring_bundle(
        parent_row,
        shot_revisions=shot_rows,
        internal_timeline_revisions=internal_rows,
    )

    assert [row["shot_id"] for row in reopened["placements"]] == [
        row["shot_id"] for row in first["placements"]
    ]
    assert compile_authoring_candidate(reopened).publication["shot_revisions"] == []


def test_timing_is_admitted_but_competing_selected_media_fails_before_publish():
    parent, shots, timelines = _closure(shared=False)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    shot_id = candidate["placements"][0]["shot_id"]
    candidate["shots"][shot_id]["internal_timeline"]["clips"][0]["hold"] = 2
    compiled = compile_authoring_candidate(candidate)
    assert compiled.publication["shot_revisions"]

    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    candidate["shots"][shot_id]["payload"]["items"][0]["media_id"] = NEW
    with pytest.raises(AuthoringBundleError, match="competing selected media"):
        compile_authoring_candidate(candidate)


def test_target_bound_transport_key_normalizes_digest_prefix_and_punctuation():
    from astrid.sdk.authoring_remote import _transport_idempotency_key

    digest = "sha256:" + "a" * 64
    assert _transport_idempotency_key(digest) == "candidate-" + "a" * 64
    assert _transport_idempotency_key("  edit/key with spaces  ") == "edit-key-with-spaces"
    assert _transport_idempotency_key("!leading") == "candidate--leading"


class _Writer:
    def __init__(self):
        self.calls = []

    def publish_parent_composition(self, project_id, timeline_id, publication, *, idempotency_key):
        self.calls.append((project_id, timeline_id, publication, idempotency_key))
        return {"data": {"new_head": publication["parent_revision_id"]}}


def test_publish_uses_one_compilation_and_returns_complete_mapping():
    parent, shots, timelines = _closure(shared=True)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    writer = _Writer()

    result = publish_authoring_candidate(candidate, writer, idempotency_key="candidate-1")

    assert len(writer.calls) == 1
    assert writer.calls[0][3] == "candidate-1"
    assert result["publication"]["data"]["new_head"] == writer.calls[0][2]["parent_revision_id"]
    assert set(result["identity_mapping"]["placements"]) == {"occ-1", "occ-2"}
    assert result["summary"]["new_head"] == result["publication"]["data"]["new_head"]
    assert isinstance(result["update"], str)
    assert {action["scope"] for action in result["next_actions"]} == {"current_head"}


def test_group_move_compiles_and_uses_existing_publication_boundary():
    parent, shots, timelines = _closure(shared=True)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    move_occurrence_group(candidate, "occ-2", before_occurrence_id="occ-1")
    writer = _Writer()

    result = publish_authoring_candidate(candidate, writer, idempotency_key="a03-group-move")

    assert len(writer.calls) == 1
    assert writer.calls[0][3] == "a03-group-move"
    occurrences = writer.calls[0][2]["parent_composition"]["occurrences"]
    assert [row["occurrence_id"] for row in occurrences] == ["occ-2", "occ-1"]
    assert [row["placement"]["start_ms"] for row in occurrences] == [0, 1000]
    assert [row["duration_ms"] for row in occurrences] == [1000, 1000]
    assert result["publication"]["data"]["new_head"] == writer.calls[0][2]["parent_revision_id"]


def test_approval_is_bound_to_candidate_and_base_revision():
    parent, shots, timelines = _closure(shared=True)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    approval = approve_authoring_candidate(
        candidate, approver="editor-1", approval_id="approval-1"
    )
    writer = _Writer()

    changed = copy.deepcopy(candidate)
    changed["parent"]["config"]["approved-edit"] = True
    with pytest.raises(AuthoringBundleError, match="stale or does not match"):
        promote_approved_authoring_candidate(
            changed, approval, writer, idempotency_key="promote-1"
        )
    assert writer.calls == []

    promoted = promote_approved_authoring_candidate(
        candidate, approval, writer, idempotency_key="promote-1"
    )
    assert promoted["approval"]["approval_id"] == "approval-1"
    assert len(writer.calls) == 1


def test_frozen_render_restart_then_approval_promotion_is_single_generation(tmp_path):
    """Exercise the contract, durable replay, and candidate promotion seam together."""
    from astrid.core.execution.reconciler import ExecutionReconciler
    from astrid.core.execution.target_adapter import LocalMachineTargetAdapter

    source = b"deterministically extracted source bytes"
    source_digest = "sha256:" + hashlib.sha256(source).hexdigest()
    contract = {
        "schema_version": 1,
        "workflow": {
            "id": "render.authoring-candidate",
            "contract_digest": "sha256:workflow",
            "required_bindings": ["source_video"],
        },
        "inputs": [
            {
                "name": "source_video",
                "object_id": source_digest,
                "filename": "source.mp4",
                "required": True,
            }
        ],
        "target": {"kind": "machine", "id": "local-1"},
        "retry_policy": {"max_attempts": 2},
        "checks": {"outputs": ["sha256"]},
    }

    class Runtime:
        def __init__(self):
            self.task = None
            self.calls = []

        def create(self, **kwargs):
            self.calls.append(("create", kwargs))
            if self.task is None:
                self.task = {
                    "task_id": "render-task-1",
                    "run_id": "render-run-1",
                    "state": "queued",
                    "idempotency_key": kwargs["idempotency_key"],
                    "capability_id": kwargs["capability"],
                    "spec": {**kwargs["spec"], "execution_request": kwargs["execution_request"]},
                }
            return {"task_id": self.task["task_id"], "run_id": self.task["run_id"]}

        def get_task(self, task_id):
            assert task_id == self.task["task_id"]
            return dict(self.task)

        def claim(self, **kwargs):
            self.calls.append(("claim", kwargs))
            self.task.update({"state": "running", "attempt_id": "render-attempt-1"})
            return {
                "task_id": self.task["task_id"],
                "attempt_id": "render-attempt-1",
                "lease_id": "render-lease-1",
                "fence": 1,
                "runtime_epoch": 1,
                "idempotency_key": "render-request-1",
                "capability_id": "render.authoring-candidate",
                "spec": self.task["spec"],
            }

        def settle(self, attempt_id, **kwargs):
            self.calls.append(("settle", kwargs))
            self.task.update({"state": "completed", "result": {"outputs": kwargs["outputs"]}})
            return {"ok": True}

        def fail(self, *args, **kwargs):
            self.calls.append(("fail", kwargs))
            self.task["state"] = "failed"
            return {"ok": True}

    runtime = Runtime()
    adapter = LocalMachineTargetAdapter(
        {"kind": "machine", "id": "local-1"},
        observer=lambda: {
            "kind": "machine",
            "target_id": "local-1",
            "live": True,
            "runtime_epoch": 1,
            "launch_generation": "launch-1",
            "process_birth_id": "process-1",
            "engine_birth_id": "engine-1",
            "output_root": str(tmp_path),
        },
    )
    render_count = 0

    def execute(_claim, observation):
        nonlocal render_count
        render_count += 1
        output = tmp_path / "render.bin"
        output.write_bytes(source + b"/rendered")
        data = output.read_bytes()
        return {
            "outputs": [
                {
                    "path": output.name,
                    "content_hash": "sha256:" + hashlib.sha256(data).hexdigest(),
                    "bytes": len(data),
                }
            ],
            "source_digest": source_digest,
            "source_filename": "source.mp4",
            "output_root": observation.output_root,
        }

    reconciler = ExecutionReconciler(runtime, adapter)
    first = reconciler.run(
        contract=contract,
        project_id="project-1",
        capability="render.authoring-candidate",
        spec={"inputs": {}},
        executor_id="worker-1",
        execute=execute,
        idempotency_key="render-request-1",
    )
    second = reconciler.run(
        contract=contract,
        project_id="project-1",
        capability="render.authoring-candidate",
        spec={"inputs": {}},
        executor_id="worker-1",
        execute=execute,
        idempotency_key="render-request-1",
    )

    assert first.status == "complete"
    assert second.status == "complete"
    assert second.phase == "recovery"
    assert render_count == 1
    assert [name for name, _ in runtime.calls].count("claim") == 1

    parent, shots, timelines = _closure(shared=True)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    approval = approve_authoring_candidate(candidate, approver="editor-1", approval_id="approval-render-1")
    writer = _Writer()
    promoted = promote_approved_authoring_candidate(
        candidate, approval, writer, idempotency_key="promote-render-1"
    )
    assert promoted["candidate_digest"] == approval["candidate_digest"]
    assert len(writer.calls) == 1


def test_full_authored_field_edits_compile_without_normalizing_opaque_fields():
    parent, shots, timelines = _closure(shared=False)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    shot_id = candidate["placements"][0]["shot_id"]
    candidate["parent"]["config"]["tracks"].append({"id": "effects", "kind": "overlay"})
    placement = candidate["placements"][0]
    placement["placement"]["start_ms"] = 250
    placement["duration_ms"] = 1500
    placement["transform"] = {"x": 100, "y": 0, "width": 960, "height": 540}
    timeline = candidate["shots"][shot_id]["internal_timeline"]
    add_track(candidate["shots"][shot_id], kind="overlay", track_id="overlay")
    timeline["clips"][0]["at"] = 125
    timeline["clips"][0]["hold"] = 3
    timeline["effects"].append({"type": "blur", "value": 0.1})
    timeline["opaque_timeline"]["added"] = {"preserve": True}

    compiled = compile_authoring_candidate(candidate)
    output = compiled.publication["parent_composition"]
    assert output["occurrences"][0]["duration_ms"] == 1500
    child = compiled.publication["shot_revisions"][0]
    assert child["payload"]["opaque_shot"] == {"future_schema": 9}
    assert child["payload"]["internal_timeline_revision_id"]
    internal = compiled.publication["internal_timeline_revisions"][0]["payload"]
    assert internal["opaque_timeline"]["added"] == {"preserve": True}
    assert internal["tracks"] == []
    assert {row["id"] for row in output["config"]["tracks"]} == {"picture", "voice", "overlay", "effects"}


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("source_offset", {"start": 100, "end": 900}),
        ("speed", 1.5),
        ("transform", {"scale": 1.25}),
    ],
)
def test_placement_edits_without_shared_projection_semantics_fail_before_publish(field, value):
    parent, shots, timelines = _closure(shared=False)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    candidate["placements"][0][field] = value
    with pytest.raises(UnsupportedAuthoringEditError, match=field):
        compile_authoring_candidate(candidate)


def test_new_placement_is_checked_even_with_self_pinned_source_mapping():
    parent, shots, timelines = _closure(shared=False)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    added = copy.deepcopy(candidate["placements"][0])
    added["occurrence_id"] = "new-occurrence"
    added["source_offset"] = {"start": 0, "end": 0}
    added["speed"] = 1.5
    candidate["placements"].append(added)
    candidate["source_mapping"]["placements"]["new-occurrence"] = copy.deepcopy(added)

    with pytest.raises(UnsupportedAuthoringEditError, match="speed"):
        compile_authoring_candidate(candidate)


def test_conflicting_parent_registry_locations_rejected_by_compiler():
    parent, shots, timelines = _closure(shared=False)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    candidate["parent"]["config"]["registry"] = {"assets": {"other": {"media_id": NEW}}}

    with pytest.raises(AuthoringBundleError, match="conflicts"):
        compile_authoring_candidate(candidate)

    parent["payload"]["config"]["registry"] = candidate["parent"]["config"]["registry"]
    with pytest.raises(ShotCompositionProjectionError, match="conflicts"):
        project_runtime_parent_composition(
            parent, shot_revisions=shots, internal_timeline_revisions=timelines
        )


def test_live_runtime_bare_item_media_id_is_accepted_without_rewriting_payload():
    parent, shots, timelines = _closure(shared=False)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    shot_id = candidate["placements"][0]["shot_id"]
    candidate["shots"][shot_id]["payload"]["items"][0]["media_id"] = OLD.removeprefix("sha256:")

    compiled = compile_authoring_candidate(candidate)
    item = compiled.publication["shot_revisions"][0]["payload"]["items"][0]
    assert item["media_id"] == OLD.removeprefix("sha256:")
    assert {row["media_id"] for row in compiled.publication["dependency_manifest"]["media"]} == {
        OLD,
        AUDIO,
    }


def test_live_source_asset_authority_resolves_child_selector_without_local_registry():
    parent, shots, timelines = _closure(shared=False)
    parent["payload"]["registry"] = {
        "assets": {
            "old-picture": {"media_id": OLD, "type": "video"},
            "voice": {"media_id": AUDIO, "type": "audio"},
        }
    }
    timelines[0]["payload"].pop("registry")
    timelines[0]["content_digest"] = _digest(timelines[0]["payload"])
    parent["content_digest"] = _digest(parent["payload"])

    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    compiled = compile_authoring_candidate(candidate)

    internal = candidate["shots"][candidate["placements"][0]["shot_id"]]["internal_timeline"]
    assert "registry" not in internal
    assert internal["clips"][0]["asset"] == "old-picture"
    assert compiled.publication["internal_timeline_revisions"] == []
    assert OLD in {row["media_id"] for row in compiled.publication["dependency_manifest"]["media"]}

    candidate["shots"][candidate["placements"][0]["shot_id"]]["internal_timeline"]["clips"][0]["asset"] = "unadmitted-new-asset"
    with pytest.raises(AuthoringBundleError, match="missing registry asset"):
        compile_authoring_candidate(candidate)

    parent["payload"]["registry"]["assets"].pop("old-picture")
    parent["content_digest"] = _digest(parent["payload"])
    parent_fallback_removed = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    with pytest.raises(AuthoringBundleError, match="missing registry asset"):
        compile_authoring_candidate(parent_fallback_removed)

    local_parent, local_shots, local_timelines = _closure(shared=False)
    local_candidate = open_authoring_bundle(
        local_parent, shot_revisions=local_shots, internal_timeline_revisions=local_timelines
    )
    local_shot = local_candidate["shots"][local_candidate["placements"][0]["shot_id"]]
    local_shot["internal_timeline"]["registry"]["assets"].pop("old-picture")
    with pytest.raises(AuthoringBundleError, match="missing registry asset"):
        compile_authoring_candidate(local_candidate)


def test_bundle_structure_helpers_duplicate_and_remove_independent_placements():
    parent, shots, timelines = _closure(shared=False)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    source_id = candidate["placements"][0]["shot_id"]
    duplicate = duplicate_authoring_shot(
        candidate, source_id, new_shot_id="shot-copy", occurrence_id="occ-copy", start_ms=2000
    )
    original_items = candidate["shots"][source_id]["payload"]["items"]
    copied_items = duplicate["payload"]["items"]
    assert copied_items[0]["item_id"] != original_items[0]["item_id"]
    assert copied_items[0]["metadata"]["opaque_literal"] == "item-1"
    assert len(candidate["placements"]) == 2
    with pytest.raises(UnsupportedAuthoringEditError, match="source_offset"):
        compile_authoring_candidate(candidate)
    candidate["placements"][1]["source_offset"] = {"start": 0, "end": 0}
    compilation = compile_authoring_candidate(candidate)
    # An actual edit also materializes the admitted source's legacy mirrors
    # into canonical child references; its immutable old revision stays pinned.
    assert {row["shot_id"] for row in compilation.publication["shot_revisions"]} == {source_id, "shot-copy"}
    assert all(row["payload"]["tracks"] == [] for row in compilation.publication["internal_timeline_revisions"])
    remove_authoring_shot(candidate, "shot-copy")
    assert "shot-copy" not in candidate["shots"]
    assert [row["occurrence_id"] for row in candidate["placements"]] == ["occ-1"]
    assert compile_authoring_candidate(candidate).publication["shot_revisions"] == []



def test_diff_baseline_normalizes_placements_and_rejects_malformed_mapping():
    parent, shots, timelines = _closure(shared=True)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    roundtrip = json.loads(json.dumps(candidate))
    assert diff_authoring_candidate(roundtrip)["change_count"] == 0

    candidate["placements"][0]["duration_ms"] += 100
    timed = diff_authoring_candidate(candidate)
    assert timed["change_count"] > 0
    assert any("duration_ms" in row["path"] for row in timed["changed"])

    candidate["placements"][0]["duration_ms"] -= 100
    candidate["placements"].reverse()
    ordered = diff_authoring_candidate(candidate)
    assert ordered["change_count"] > 0
    assert any("placements" in row["path"] for row in ordered["changed"])

    candidate["source_mapping"]["placements"] = []
    with pytest.raises(AuthoringBundleError, match="candidate.source_mapping.placements"):
        diff_authoring_candidate(candidate)


def test_validate_diff_preview_and_media_inventory_are_read_only_and_frozen():
    parent, shots, timelines = _closure(shared=False)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    candidate["placements"][0]["duration_ms"] = 1234
    validation = validate_authoring_candidate(candidate)
    diff = diff_authoring_candidate(candidate)
    inventory = authoring_media_inventory(candidate)
    preview = preview_authoring_candidate(candidate)
    assert validation["valid"] is True
    assert validation["candidate_digest"] == preview["candidate_digest"]
    assert diff["change_count"] > 0
    assert {row["media_id"] for row in inventory["media"]} == {OLD, AUDIO}
    assert inventory["composed_ref"]["candidate_digest"] == inventory["candidate_digest"]
    assert all(
        row["source_ref"]["project_id"] == "project-1"
        and row["source_ref"]["digest"] == row["media_id"]
        for row in inventory["media"]
    )
    frozen_digest = preview["candidate_digest"]
    candidate["placements"][0]["duration_ms"] = 9999
    assert preview["candidate_digest"] == frozen_digest
    assert preview["publication"]["parent_composition"]["occurrences"][0]["duration_ms"] == 1234


def test_frozen_candidate_projects_to_labelled_managed_render_without_publication():
    parent, shots, timelines = _closure(shared=False)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    candidate["placements"][0]["duration_ms"] = 1234
    preview = preview_authoring_candidate(candidate)
    candidate["placements"][0]["duration_ms"] = 9999

    class Runtime:
        media = SimpleNamespace(list=lambda *_args, **_kwargs: SimpleNamespace(
            ok=True, data=[[{"media_id": media_id, "digest": media_id[7:]} for media_id in (OLD, AUDIO)], None]
        ))

        def __init__(self):
            def result(data):
                return SimpleNamespace(ok=True, data=data)

            self.projects = SimpleNamespace(show=lambda _ref: result({"id": "project-1", "slug": "demo"}))
            timeline = {
                "timeline_id": "main", "timeline_ulid": "main", "slug": "main",
                "version": 7, "head_revision_id": "parent-1",
                "config": {"tracks": [], "clips": []}, "registry": {"assets": {}},
            }
            self.timelines = SimpleNamespace(
                show=lambda _project, _ref: result(timeline),
                list=lambda _project, **_kwargs: result([[timeline], None]),
                inspect=lambda _project, _timeline, **_kwargs: result({
                    "representation": "canonical_head",
                    "is_current_head": True,
                    "revision_id": "parent-1",
                    "timeline_id": "main",
                }),
            )

        def get_project_parent_composition_revision(self, _project, _timeline, revision_id):
            assert revision_id == "parent-1"
            return parent

        def get_project_shot_revision(self, _project, shot_id, revision_id):
            return next(row for row in shots if row["shot_id"] == shot_id and row["revision_id"] == revision_id)

        def get_project_timeline_revision(self, _project, _timeline, revision_id):
            return next(row for row in timelines if row["revision_id"] == revision_id)

    snapshot = ManagedRenderSnapshot(
        project_id="project-1", project_slug="demo", timeline_id="main",
        timeline_ulid="main", timeline_slug="main", config_version=7,
        head_event_id="parent-1", head_hash=parent["content_digest"][7:],
        config={"tracks": [], "clips": []}, registry={"assets": {}},
        config_hash="0" * 64, registry_hash="0" * 64,
        materialized_registry_hash="0" * 64,
    )
    projected = candidate_preview_snapshot(preview, snapshot=snapshot, client=Runtime())
    authority = projected.authority()
    assert authority["authority"] == "kernel"
    assert authority["render_mode"] == "authoring_candidate_preview"
    assert authority["authoring_preview"]["label"] == "Unpublished candidate preview"
    assert authority["authoring_preview"]["base_parent"] == preview["head"]
    assert authority["authoring_preview"]["candidate_digest"] == preview["candidate_digest"]
    assert projected.expansion["outputs"][0]["duration_ms"] == 1234
    assert projected.head_event_id == "parent-1"

    render_candidate = copy.deepcopy(preview["candidate"])
    render_candidate["parent"]["config"] = {
        "tracks": [
            {"id": "picture", "kind": "visual", "label": "Picture"},
            {"id": "voice", "kind": "audio", "label": "Voice"},
        ], "clips": [],
    }
    render_candidate["parent"]["clips"] = []
    shot_id = render_candidate["placements"][0]["shot_id"]
    internal = render_candidate["shots"][shot_id]["internal_timeline"]
    internal["tracks"] = copy.deepcopy(render_candidate["parent"]["config"]["tracks"])
    internal["clips"] = []
    picture_clip = place_media(
        internal, OLD, track=internal["tracks"][0], start=0, end=1,
        clip_id="picture-1", fit="cover",
        rect={"x": 0.1, "y": 0.2, "width": 0.3, "height": 0.4},
        clipType="media",
    )
    place_media(
        internal, AUDIO, track=internal["tracks"][1], start=0, end=1,
        clip_id="voice-1", clipType="media",
    )
    assert picture_clip["media_id"] == OLD
    assert picture_clip["fit"] == "cover"
    internal["registry"] = {"assets": {
        "old-picture": {"media_id": OLD, "type": "image", "origin": "managed-local"},
        "voice": {"media_id": AUDIO, "type": "audio", "origin": "managed-local"},
    }}
    render_preview = preview_authoring_candidate(render_candidate)

    class PreviewRuntime(Runtime):
        def get_project_shot_revision(self, *_args):
            raise AssertionError("preview should not project the unrenderable source shot")

        def get_project_timeline_revision(self, *_args):
            raise AssertionError("preview should not project the unrenderable source timeline")

    prepared, admitted = _prepare_managed_render_inputs(
        {"timeline_ref": "main", "authoring_preview": render_preview},
        project="demo", _client=PreviewRuntime(),
    )
    assert "authoring_preview" not in prepared
    assert admitted["authoring_preview"]["candidate_digest"] == render_preview["candidate_digest"]
    assert admitted["authority"] == "kernel"
    assert admitted["render_mode"] == "authoring_candidate_preview"
    assert admitted["config_version"] == 7
    assert admitted["authoring_preview"]["publication_digest"] == render_preview["publication_digest"]
    prepared_config = prepared["timeline_snapshot"]["config"]
    prepared_picture = next(
        clip for clip in prepared_config["clips"] if clip["id"].endswith(":picture-1")
    )
    prepared_track = next(
        track for track in prepared_config["tracks"] if track["id"] == prepared_picture["track"]
    )
    assert prepared_picture["asset"]
    assert "media_id" not in prepared_picture
    assert "fit" not in prepared_picture
    assert "rect" not in prepared_picture
    assert prepared_track["fit"] == "cover"
    assert {key: prepared_picture[key] for key in ("x", "y", "width", "height")} == {
        "x": 0.1, "y": 0.2, "width": 0.3, "height": 0.4,
    }
    projection = prepared_picture["app"]["astrid_authoring_render_projection"]
    assert projection["media_selector"]["media_id"] == OLD
    assert projection["fit"] == {"value": "cover", "projected_to_track": prepared_picture["track"]}
    prepared_asset = prepared["timeline_snapshot"]["registry"]["assets"][prepared_picture["asset"]]
    assert prepared_asset["origin"] == "opaque-foreign"

    stale = copy.deepcopy(preview)
    stale["candidate_digest"] = "sha256:" + "0" * 64
    with pytest.raises(AuthoringBundleError, match="frozen candidate"):
        candidate_preview_snapshot(stale, snapshot=snapshot, client=Runtime())
    with pytest.raises(AuthoringBundleError, match="no longer the exact render head"):
        candidate_preview_snapshot(
            preview, snapshot=replace(snapshot, head_event_id="parent-2"), client=Runtime()
        )

    class RenderClient:
        def invoke_result(self, capability_id, **kwargs):
            assert capability_id == "rendering.render"
            assert kwargs["inputs"]["authoring_preview"]["candidate_digest"]
            assert kwargs["inputs"]["review"] is True
            return {"run_id": "render-run-1", "receipt": "managed"}

    assert render_authoring_candidate_preview(
        preview, RenderClient(), project="demo", timeline_ref="main"
    ) == {"run_id": "render-run-1", "receipt": "managed"}


def test_compact_inspection_pins_head_and_reports_bounded_structure_without_opaque_payloads():
    parent, shots, timelines = _closure(shared=True)
    candidate = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    before = copy.deepcopy(candidate)
    inspection = inspect_authoring_candidate(candidate, offset=1, limit=1)

    assert candidate == before
    assert inspection["kind"] == "authoring-candidate-inspection"
    assert inspection["head"] == candidate["base_parent"]
    assert inspection["page"] == {
        "offset": 1,
        "limit": 1,
        "returned": 1,
        "total": 2,
        "next_offset": None,
    }
    assert inspection["placements"][0]["occurrence_id"] == "occ-2"
    assert inspection["counts"] == {
        "placements": 2,
        "shots": 2,
        "changed_shots": 2,
        "media": 2,
        "unresolved": 0,
    }
    assert {row["media_id"] for row in inspection["media"]} == {OLD, AUDIO}
    assert inspection["omissions"] == {"placements": 1}
    assert "opaque_parent" not in json.dumps(inspection)
    text = format_authoring_inspection(inspection)
    assert "head=parent-1" in text
    assert "placement occ-2" in text


def test_candidate_compiler_integrates_with_runtime_atomic_publication(tmp_path):
    runtime_service = pytest.importorskip("runtime_protocol.service")
    runtime_store = pytest.importorskip("runtime_protocol.store")
    root = tmp_path / "realm"
    runtime_store.RealmStore.initialize(root).close()
    service = runtime_service.RuntimeService(root)
    try:
        project = service.create_project(
            {"slug": "authoring", "name": "Authoring"}, idempotency_key="project"
        )
        project_id = project["id"]
        service.create_timeline(project_id, "main", idempotency_key="timeline")
        old = service.ingest(
            project_id, b"old-picture", media_type="image/png", idempotency_key="old"
        )["data"]["object_id"]
        new = service.ingest(
            project_id, b"new-picture", media_type="image/png", idempotency_key="new"
        )["data"]["object_id"]
        audio = service.ingest(
            project_id, b"voiceover", media_type="audio/wav", idempotency_key="audio"
        )["data"]["object_id"]
        parent, shots, timelines = _closure(shared=True)
        # Runtime now requires authored shot text to pin a registered binding;
        # this atomic compiler fixture is not testing text registration.
        shots[0]["payload"]["text_bindings"] = []
        replacements = {OLD: old, NEW: new, AUDIO: audio, "project-1": project_id}
        parent = _replace_values(parent, replacements)
        shots = _replace_values(shots, replacements)
        timelines = _replace_values(timelines, replacements)
        timelines[0]["content_digest"] = _digest(timelines[0]["payload"])
        shots[0]["content_digest"] = _digest(shots[0]["payload"])
        parent["content_digest"] = _digest(parent["payload"])
        seed = {
            "project_id": project_id,
            "timeline_id": "main",
            "expected_head": None,
            "parent_revision_id": "parent-1",
            "parent_composition": parent["payload"],
            "internal_timeline_revisions": timelines,
            "shot_revisions": shots,
        }
        service.publish_parent_composition(project_id, "main", seed, idempotency_key="seed-parent")
        exact_parent = service.get_project_parent_composition_revision(
            project_id, "main", "parent-1"
        )
        exact_shot = service.get_project_shot_revision(project_id, "shot-shared", "shot-rev-1")
        exact_internal = service.get_project_timeline_revision(project_id, "main", "internal-1")
        candidate = open_authoring_bundle(
            exact_parent,
            shot_revisions=[exact_shot],
            internal_timeline_revisions=[exact_internal],
        )
        first_shot = candidate["placements"][0]["shot_id"]
        candidate["shots"][first_shot]["payload"]["items"][0]["media_id"] = new
        candidate["shots"][first_shot]["internal_timeline"]["clips"][0]["asset"] = "new-picture"
        candidate["shots"][first_shot]["internal_timeline"]["registry"]["assets"]["new-picture"] = {
            "media_id": new,
            "type": "image",
        }

        committed = publish_authoring_candidate(
            candidate, service, idempotency_key="complete-candidate"
        )
        new_head = committed["publication"]["data"]["new_head"]
        assert committed["summary"]["new_head"] == new_head
        assert committed["summary"]["catalog_media"] is None
        assert committed["summary"]["media_selections"]["image"]["replaced"] == 1
        assert any(row["scope"] == "saved_revision_pair" for row in committed["next_actions"])
        assert f"Saved revision {new_head}" in committed["update"]
        reread = service.get_project_parent_composition_revision(project_id, "main", new_head)

        assert new_head == committed["publication"]["data"]["parent_revision_id"]
        assert new_head != committed["identity_mapping"]["placements"]["occ-1"]["shot_revision_id"]
        assert [row["shot_id"] for row in reread["payload"]["occurrences"]] == [
            row["shot_id"] for row in candidate["placements"]
        ]
        assert reread["payload"]["opaque_parent"] == {"keep": ["all", "fields"]}
        newer_payload = copy.deepcopy(reread["payload"])
        newer_payload["opaque_parent"]["writer"] = "later"
        service.publish_parent_composition(
            project_id,
            "main",
            {
                "project_id": project_id,
                "timeline_id": "main",
                "expected_head": new_head,
                "parent_revision_id": "newer-head",
                "parent_composition": newer_payload,
            },
            idempotency_key="later-writer",
        )
        replay = publish_authoring_candidate(
            candidate, service, idempotency_key="complete-candidate"
        )
        assert replay == committed
        assert service._timeline_resource("main")["head_revision_id"] == "newer-head"
    finally:
        service.close()


def _chapter_bundle():
    parent, shots, timelines = _closure(shared=True)
    # Inherited occurrence clocks are immutable source provenance, not new
    # placement edits. The storage adapter must not normalize or rebase them.
    parent["payload"]["occurrences"][0]["source_offset"] = {"start": 125, "end": 875}
    parent["payload"]["occurrences"][0]["speed"] = {"numerator": 3, "denominator": 2}
    parent["content_digest"] = _digest(parent["payload"])
    bundle = open_authoring_bundle(
        parent, shot_revisions=shots, internal_timeline_revisions=timelines
    )
    tracks = copy.deepcopy(timelines[0]["payload"]["tracks"])
    tracks[0]["app"] = {
        "scaleAppliesToPositionedClips": True,
        "foreign": {"v": 9, "_opaque": [None, {"keep": True}]},
    }
    bundle["parent"]["config"]["tracks"] = copy.deepcopy(tracks)
    bundle["parent"]["config"]["fps"] = 24
    for shot in bundle["shots"].values():
        shot["internal_timeline"]["tracks"] = copy.deepcopy(tracks)
        # These are source-clock values, never chapter-local offsets.
        shot["internal_timeline"]["clips"][0].update({"from": 2.25, "to": 4.25, "speed": 2})
        shot["internal_timeline"]["clips"][0].pop("hold")
    bundle["chapter_layout"] = [
        {"id": "chapter-b", "label": "First stored chapter", "start_ms": 1000,
         "end_ms": 2000, "occurrence_ids": ["occ-2"], "_opaque": {"future": None}},
        {"id": "empty", "label": "Empty boundary", "start_ms": 2000,
         "end_ms": 2000, "occurrence_ids": []},
        {"id": "chapter-a", "label": "Last stored chapter", "start_ms": 0,
         "end_ms": 1000, "occurrence_ids": ["occ-1"]},
    ]
    bundle["opt_in"] = {"chapter_storage": True, "provenance": {"source": "synthetic"}}
    bundle["future_bundle"] = {"unknown": ["preserve", None]}
    return bundle


def _stored_internal(storage, chapter_index=0):
    return next(iter(storage["chapters"][chapter_index]["shots"].values()))["internal_timeline"]


def _chapter_projection(bundle):
    from astrid.core.timeline.duration import (
        clip_end_frame,
        clip_start_frame,
        timeline_duration_frames,
        timeline_render_duration_frames,
    )

    publication = compile_authoring_candidate(bundle).publication
    projection = project_runtime_parent_composition(
        {"project_id": publication["project_id"], "timeline_id": publication["timeline_id"],
         "revision_id": publication["parent_revision_id"], "payload": publication["parent_composition"]},
        shot_revisions=publication["shot_revisions"],
        internal_timeline_revisions=publication["internal_timeline_revisions"],
    )
    config = projection.config
    fps = config["fps"]
    return {
        "projection": projection.as_dict(),
        "frames": [(clip["id"], clip_start_frame(clip, fps), clip_end_frame(clip, fps))
                   for clip in config["clips"]],
        "duration_frames": timeline_duration_frames(config, fps),
        "render_duration_frames": timeline_render_duration_frames(config, fps),
    }


def test_chapter_storage_round_trip_is_detached_deterministic_and_renderer_equivalent():
    bundle = _chapter_bundle()
    before = copy.deepcopy(bundle)
    compilation = compile_authoring_candidate(bundle).as_dict()
    projection = _chapter_projection(bundle)
    storage = encode_authoring_bundle_storage(bundle)
    assert bundle == before
    assert storage == encode_authoring_bundle_storage(bundle)
    stored_before = copy.deepcopy(storage)
    # Exercise actual JSON serialization, including opaque nulls and arrays.
    reopened = decode_authoring_bundle_storage(json.loads(json.dumps(storage)))
    assert reopened == before
    assert storage == stored_before
    assert encode_authoring_bundle_storage(reopened) == storage
    assert compile_authoring_candidate(reopened).as_dict() == compilation
    assert _chapter_projection(reopened) == projection
    assert projection["duration_frames"] == projection["render_duration_frames"] == 96
    assert [row["layout"]["id"] for row in storage["chapters"]] == ["chapter-b", "empty", "chapter-a"]
    assert [row["occurrence_id"] for row in reopened["placements"]] == ["occ-1", "occ-2"]
    assert reopened["chapter_layout"] == before["chapter_layout"]
    assert reopened["source_mapping"] == before["source_mapping"]
    assert reopened["base_parent_payload"] == before["base_parent_payload"]
    assert reopened["base_placements"] == before["base_placements"]
    reopened["shots"][reopened["placements"][0]["shot_id"]]["internal_timeline"]["clips"][0]["id"] = "changed"
    assert bundle == before
    assert storage == stored_before


def test_chapter_storage_has_one_film_track_owner_and_exact_child_references():
    bundle = _chapter_bundle()
    storage = encode_authoring_bundle_storage(bundle)
    assert storage["film"]["tracks"] == bundle["parent"]["config"]["tracks"]
    assert "tracks" not in storage["film"]["bundle"]["parent"]["config"]
    assert storage["film"]["bundle"]["parent"]["config"]["track_ids"] == ["picture", "voice"]
    # Historical definitions are immutable, content-addressed film snapshots.
    for digest, track in storage["film"]["baseline_tracks"].items():
        assert digest == _digest(track)
        assert track not in storage["film"]["tracks"]
    for chapter in storage["chapters"]:
        for placement in chapter["placements"]:
            original = next(row for row in bundle["placements"] if row["occurrence_id"] == placement["occurrence_id"])
            assert placement == original
            shot_id = placement["shot_id"]
            stored = chapter["shots"][shot_id]
            original_shot = bundle["shots"][shot_id]
            assert stored["internal_timeline"]["track_ids"] == ["picture", "voice"]
            assert stored["internal_timeline"]["clips"] == original_shot["internal_timeline"]["clips"]
            assert stored["payload"] == original_shot["payload"]
            assert "tracks" not in stored["internal_timeline"]
            assert "tracks" not in stored["base_internal_timeline"]
            assert "track_refs" in stored["base_internal_timeline"]


@pytest.mark.parametrize("film_label,child_label", [(True, False), (False, True), (False, False)])
def test_chapter_codec_reconciles_optional_labels_without_changing_immutable_bases(film_label, child_label):
    bundle = _chapter_bundle()
    if film_label:
        bundle["parent"]["config"]["tracks"][0]["label"] = " Video · exact "
    if child_label:
        for shot in bundle["shots"].values():
            shot["internal_timeline"]["tracks"][0]["label"] = " Video · exact "
    before = copy.deepcopy(bundle)
    storage = encode_authoring_bundle_storage(bundle)
    # Read a legacy serialized child mirror, not just canonical references.
    internal = _stored_internal(storage)
    internal.pop("track_ids")
    internal["tracks"] = copy.deepcopy(bundle["shots"][bundle["placements"][1]["shot_id"]]["internal_timeline"]["tracks"])
    encoded = json.dumps(storage, sort_keys=True)
    reopened = decode_authoring_bundle_storage(json.loads(encoded))
    track = reopened["parent"]["config"]["tracks"][0]
    assert ("label" in track) == (film_label or child_label)
    if film_label or child_label:
        assert track["label"] == " Video · exact "
    assert bundle == before and json.dumps(storage, sort_keys=True) == encoded
    assert reopened["base_parent_payload"] == bundle["base_parent_payload"]
    for sid, shot in reopened["shots"].items():
        assert shot["base_internal_timeline"] == bundle["shots"][sid]["base_internal_timeline"]
        assert shot["internal_timeline"]["audio"] == bundle["shots"][sid]["internal_timeline"]["audio"]
        assert shot["internal_timeline"]["opaque_timeline"] == bundle["shots"][sid]["internal_timeline"]["opaque_timeline"]
    canonical = encode_authoring_bundle_storage(reopened)
    assert encode_authoring_bundle_storage(decode_authoring_bundle_storage(canonical)) == canonical


def test_chapter_storage_equal_legacy_rows_and_disjoint_app_metadata_merge_losslessly():
    bundle = _chapter_bundle()
    storage = encode_authoring_bundle_storage(bundle)
    for index in (0, 2):
        internal = _stored_internal(storage, index)
        internal.pop("track_ids")
        internal["tracks"] = copy.deepcopy(storage["film"]["tracks"])
    untouched = copy.deepcopy(storage)
    assert decode_authoring_bundle_storage(storage) == bundle
    assert storage == untouched
    _stored_internal(storage)["tracks"][0]["app"]["foreign"]["new_annotation"] = {"opaque": [1, 2]}
    _stored_internal(storage, 2)["tracks"][0]["app"]["other_owner"] = {"future": None}
    untouched = copy.deepcopy(storage)
    merged = decode_authoring_bundle_storage(storage)
    assert storage == untouched
    app = merged["parent"]["config"]["tracks"][0]["app"]
    assert app["scaleAppliesToPositionedClips"] is True
    assert app["foreign"] == {**bundle["parent"]["config"]["tracks"][0]["app"]["foreign"],
                              "new_annotation": {"opaque": [1, 2]}}
    assert app["other_owner"] == {"future": None}
    assert merged["base_parent_payload"] == bundle["base_parent_payload"]
    for shot_id, shot in merged["shots"].items():
        assert shot["internal_timeline"]["tracks"][0]["app"] == app
        assert shot["base_internal_timeline"] == bundle["shots"][shot_id]["base_internal_timeline"]
    canonical = encode_authoring_bundle_storage(merged)
    assert decode_authoring_bundle_storage(canonical) == merged
    assert encode_authoring_bundle_storage(decode_authoring_bundle_storage(canonical)) == canonical


@pytest.mark.parametrize("field,value", [
    ("label", ""), ("label", None), ("label", False),
    ("kind", "audio"), ("opaque_track", {"future": False}), ("gain", 0.5),
    ("app", {"scaleAppliesToPositionedClips": False}),
    ("app", {"scaleAppliesToPositionedClips": 1}),
    ("app", {"foreign": {"_opaque": [None]}}),
    ("app", None),
])
def test_chapter_storage_legacy_conflicts_refuse_without_mutation(field, value):
    storage = encode_authoring_bundle_storage(_chapter_bundle())
    # Put the conflict in the last nonempty chapter: earlier input must survive.
    internal = _stored_internal(storage, 2)
    internal.pop("track_ids")
    internal["tracks"] = copy.deepcopy(storage["film"]["tracks"])
    internal["tracks"][0][field] = value
    before = copy.deepcopy(storage)
    with pytest.raises(AuthoringBundleError, match="conflicting track"):
        decode_authoring_bundle_storage(storage)
    assert storage == before


@pytest.mark.parametrize("field,value", [
    ("label", "Other"), ("label", None), ("label", ""), ("label", False),
    ("kind", "audio"), ("gain", .5), ("volume", 0), ("muted", False),
    ("mute", False), ("timing", {"offset": 0}), ("routing", []),
    ("opaque_track", {"future": 1}),
])
def test_optional_label_codec_refuses_present_label_and_semantic_conflicts(field, value):
    bundle = _chapter_bundle()
    bundle["parent"]["config"]["tracks"][0]["label"] = "Video"
    storage = encode_authoring_bundle_storage(bundle)
    internal = _stored_internal(storage, 2)
    internal.pop("track_ids")
    internal["tracks"] = copy.deepcopy(bundle["shots"][bundle["placements"][0]["shot_id"]]["internal_timeline"]["tracks"])
    internal["tracks"][0][field] = value
    before = copy.deepcopy(storage)
    with pytest.raises(AuthoringBundleError, match="conflicting track"):
        decode_authoring_bundle_storage(json.loads(json.dumps(storage)))
    assert storage == before


@pytest.mark.parametrize("fault", [
    "duplicate_track", "invalid_track", "missing_track", "competing_tracks",
    "missing_occurrence", "duplicate_occurrence", "shared_shot", "unowned_shot",
    "duplicate_chapter", "invalid_chapter", "unsupported_transform", "missing_clip_track",
    "duplicate_clip", "duplicate_item", "conflicting_parent_tracks", "conflicting_clip_owner",
    "conflicting_occurrence_track", "missing_layout", "reserved_track_field", "missing_film_owner",
    "scale_transform", "malformed_transform",
])
def test_chapter_storage_flat_refusals_are_read_only(fault):
    bundle = _chapter_bundle()
    first = bundle["placements"][0]
    shot = bundle["shots"][first["shot_id"]]
    internal = shot["internal_timeline"]
    if fault == "duplicate_track":
        internal["tracks"].append(copy.deepcopy(internal["tracks"][0]))
    elif fault == "invalid_track":
        internal["tracks"][0]["id"] = " "
    elif fault == "missing_track":
        internal["tracks"] = internal["tracks"][:1]
    elif fault == "competing_tracks":
        internal["tracks"][0]["opacity"] = 0.25
    elif fault == "missing_occurrence":
        bundle["chapter_layout"][0]["occurrence_ids"] = ["absent"]
    elif fault == "duplicate_occurrence":
        bundle["placements"].append(copy.deepcopy(first))
    elif fault == "shared_shot":
        bundle["placements"][1]["shot_id"] = first["shot_id"]
    elif fault == "unowned_shot":
        bundle["shots"]["extra"] = copy.deepcopy(shot)
    elif fault == "duplicate_chapter":
        bundle["chapter_layout"][1]["id"] = bundle["chapter_layout"][0]["id"]
    elif fault == "invalid_chapter":
        bundle["chapter_layout"][0]["id"] = ""
    elif fault == "unsupported_transform":
        first["transform"]["rotate"] = 15
    elif fault == "missing_clip_track":
        internal["clips"][0]["track"] = "absent"
    elif fault == "duplicate_clip":
        internal["clips"].append(copy.deepcopy(internal["clips"][0]))
    elif fault == "duplicate_item":
        second = bundle["shots"][bundle["placements"][1]["shot_id"]]
        second["payload"]["items"][0]["item_id"] = shot["payload"]["items"][0]["item_id"]
    elif fault == "conflicting_parent_tracks":
        bundle["parent"]["tracks"] = []
    elif fault == "conflicting_clip_owner":
        bundle["parent"]["clips"][0]["at"] = 4
    elif fault == "conflicting_occurrence_track":
        first["track"] = "voice"
    elif fault == "missing_layout":
        bundle.pop("chapter_layout")
    elif fault == "reserved_track_field":
        internal["track_ids"] = ["picture"]
    elif fault == "missing_film_owner":
        bundle["parent"]["config"]["tracks"].pop()
    elif fault == "scale_transform":
        first["transform"]["scale"] = 2
    elif fault == "malformed_transform":
        first["transform"] = ["unsupported"]
    before = copy.deepcopy(bundle)
    with pytest.raises(AuthoringBundleError):
        encode_authoring_bundle_storage(bundle)
    assert bundle == before


@pytest.mark.parametrize("fault", [
    "missing_track", "duplicate_track", "missing_shot", "duplicate_chapter", "duplicate_order",
    "competing_tracks", "unknown_envelope", "layout_change", "unsupported_format",
    "baseline_digest", "baseline_reference", "unowned_snapshot", "duplicate_clip", "film_track_order",
    "missing_film_owner", "unsupported_transform",
])
def test_chapter_storage_decode_refusals_are_read_only(fault):
    storage = encode_authoring_bundle_storage(_chapter_bundle())
    internal = _stored_internal(storage)
    if fault == "missing_track":
        internal["track_ids"].append("absent")
    elif fault == "duplicate_track":
        storage["film"]["tracks"].append(copy.deepcopy(storage["film"]["tracks"][0]))
    elif fault == "missing_shot":
        storage["chapters"][0]["shots"].clear()
    elif fault == "duplicate_chapter":
        storage["chapters"].append(copy.deepcopy(storage["chapters"][0]))
    elif fault == "duplicate_order":
        storage["film"]["placement_order"].append("occ-1")
    elif fault == "competing_tracks":
        internal["tracks"] = copy.deepcopy(storage["film"]["tracks"])
    elif fault == "unknown_envelope":
        storage["unknown"] = {"must_not_drop": True}
    elif fault == "layout_change":
        storage["chapters"][0]["layout"]["label"] = "conflicting label"
    elif fault == "unsupported_format":
        storage["format"] = "future/v99"
    elif fault == "baseline_digest":
        next(iter(storage["film"]["baseline_tracks"].values()))["kind"] = "changed"
    elif fault == "baseline_reference":
        baseline = next(iter(storage["chapters"][0]["shots"].values()))["base_internal_timeline"]
        baseline["track_refs"][0] = "sha256:" + "0" * 64
    elif fault == "unowned_snapshot":
        row = {"id": "unused", "kind": "audio"}
        storage["film"]["baseline_tracks"][_digest(row)] = row
    elif fault == "duplicate_clip":
        internal["clips"].append(copy.deepcopy(internal["clips"][0]))
    elif fault == "film_track_order":
        storage["film"]["bundle"]["parent"]["config"]["track_ids"].reverse()
    elif fault == "missing_film_owner":
        internal.pop("track_ids")
        internal["tracks"] = copy.deepcopy(storage["film"]["tracks"])
        internal["tracks"].append({"id": "unowned", "kind": "audio"})
    elif fault == "unsupported_transform":
        storage["chapters"][0]["placements"][0]["transform"]["rotate"] = 5
    before = copy.deepcopy(storage)
    with pytest.raises(AuthoringBundleError):
        decode_authoring_bundle_storage(storage)
    assert storage == before
