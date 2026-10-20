"""Pure capture projection on the existing semantic provider; no save dependency."""
import builtins
import copy
import io
import json
import socket
import subprocess
from pathlib import Path

import pytest

from astrid.core.timeline.authoring_bundle import AuthoringBundleError, preview_authoring_candidate
from astrid.sdk.timeline.commit import RuntimeCommitService, bundle_from_document
from tests.sdk.test_timeline_commit_provider_document import document_fixture


def project(document, preview=None):
    return RuntimeCommitService("unused-by-pure-capture").project_capture(
        document, authoring_preview=preview)


def draft(document):
    bundle = bundle_from_document(document)
    bundle["parent"]["config"]["opaque_draft"] = [None, False, 0, 2.0]
    first = next(iter(bundle["shots"].values()))
    first["internal_timeline"]["clips"][0]["at"] = 2.002
    return bundle


@pytest.mark.parametrize("candidate", [False, True])
def test_projection_is_detached_json_deterministic_without_io(monkeypatch, candidate):
    document = document_fixture()
    preview = preview_authoring_candidate(draft(document)) if candidate else None
    before = copy.deepcopy((document, preview))
    expected = project(document, preview)

    def forbidden(*args, **kwargs):
        raise AssertionError("pure capture projection attempted IO")

    import astrid.core.timeline.shot_composition_projection as projector
    original = projector.project_runtime_parent_composition
    calls = []

    def one_projector(*args, **kwargs):
        calls.append(True)
        return original(*args, **kwargs)

    monkeypatch.setattr(projector, "project_runtime_parent_composition", one_projector)
    with monkeypatch.context() as no_io:
        for target, name in ((builtins, "open"), (io, "open"), (Path, "open"),
                             (socket, "socket"), (socket, "create_connection"),
                             (subprocess, "Popen"), (subprocess, "run")):
            no_io.setattr(target, name, forbidden)
        for _ in range(3):
            result = project(copy.deepcopy(document), copy.deepcopy(preview))
            assert json.dumps(result, sort_keys=True, allow_nan=False) == json.dumps(
                expected, sort_keys=True, allow_nan=False)
            result["config"]["opaque"]["v"].append("caller change")
    assert len(calls) == 3
    assert (document, preview) == before
    assert expected["config"]["output"]["fps"] == {"numerator": 30000, "denominator": 1001}
    assert expected["config"]["clips"][0]["app"]["org.example"]["clear"] is None
    assert set(expected) == {"config", "registry", "expansion"}
    if candidate:
        marker = expected["expansion"]["working_copy"]
        assert marker["base_parent"] == preview["head"]
        assert marker["candidate_digest"] == preview["candidate_digest"]
        assert marker["publication_digest"] == preview["publication_digest"]
        assert marker["candidate_parent_revision_id"] != document["parent_revision"]["revision_id"]


@pytest.mark.parametrize("damage", ["parent_digest", "shot_digest", "internal_digest", "missing_shot",
                                    "missing_internal", "orphan", "link", "scope", "manifest"])
def test_inconsistent_saved_closure_refuses(damage):
    document = document_fixture()
    if damage.endswith("_digest"):
        family = {"parent_digest": "parent_revision", "shot_digest": "shot_revisions",
                  "internal_digest": "internal_timeline_revisions"}[damage]
        row = document[family] if family == "parent_revision" else document[family][0]
        row["content_digest"] = "sha256:" + "0" * 64
    elif damage == "missing_shot":
        document["shot_revisions"] = []
    elif damage == "missing_internal":
        document["internal_timeline_revisions"] = []
    elif damage == "orphan":
        document["shot_revisions"].append(copy.deepcopy(document["shot_revisions"][0]))
    elif damage == "link":
        document["shot_revisions"][0]["internal_timeline_revision_id"] = "foreign"
    elif damage == "scope":
        document["shot_revisions"][0]["project_id"] = "foreign"
    else:
        document["dependency_manifest"]["shots"][0]["content_digest"] = "sha256:" + "0" * 64
    with pytest.raises(AuthoringBundleError):
        project(document)


@pytest.mark.parametrize("damage", ["kind", "head", "candidate_digest", "publication_digest", "publication",
                                    "project_id", "timeline_id", "base_parent", "base_parent_payload",
                                    "base_placements", "source", "child_base", "internal_base", "embedded_base",
                                    "retained_pin", "missing_candidate", "candidate_after_freeze"])
def test_inconsistent_candidate_refuses_even_with_recomputed_preview(damage):
    document = document_fixture()
    bundle = draft(document)
    identity = next(iter(bundle["shots"]))
    if damage in {"project_id", "timeline_id"}:
        bundle[damage] = "foreign"
    elif damage == "base_parent":
        bundle[damage]["revision_id"] = "other-parent"
    elif damage in {"base_parent_payload", "base_placements"}:
        bundle[damage]["forged"] = True
    elif damage == "source":
        bundle["source_mapping"]["placements"] = {}
    elif damage in {"child_base", "internal_base"}:
        key = "base_payload" if damage == "child_base" else "base_internal_timeline"
        bundle["shots"][identity][key]["forged"] = True
    elif damage == "embedded_base":
        bundle["source_mapping"]["_runtime_document"]["project_id"] = "foreign"
    elif damage == "retained_pin":
        bundle["source_mapping"]["shots"][identity]["internal_timeline_content_digest"] = "sha256:" + "0" * 64
    preview = preview_authoring_candidate(bundle)
    if damage in {"kind", "candidate_digest", "publication_digest", "head", "publication"}:
        preview[damage] = {} if damage in {"head", "publication"} else "forged"
    elif damage == "missing_candidate":
        preview.pop("candidate")
    elif damage == "candidate_after_freeze":
        preview["candidate"]["parent"]["config"]["opaque_draft"] = "changed after freezing"
    with pytest.raises(AuthoringBundleError):
        project(document, preview)


@pytest.mark.parametrize("value", [True, 2.0])
def test_json_distinct_base_values_are_not_equal(value):
    document = document_fixture()
    preview = preview_authoring_candidate(draft(document))
    # JSON bool/int and float/int comparisons must preserve encoded identity.
    preview["candidate"]["base_parent_payload"]["config"]["clips"][0]["hold"] = value
    with pytest.raises(AuthoringBundleError, match="exact base"):
        project(document, preview)


def test_reused_candidate_pin_is_compared_with_verified_image():
    document = document_fixture(shared=False)
    bundle = bundle_from_document(document)
    bundle["source_mapping"]["shots"]["chapter-shot"]["content_digest"] = "sha256:" + "0" * 64
    preview = preview_authoring_candidate(bundle)
    with pytest.raises(AuthoringBundleError, match="child source"):
        project(document, preview)


def test_capture_method_imports_and_runs_without_renderer_or_runtime():
    import os
    import sys

    script = r'''
import sys
class Blocked:
    def find_spec(self, fullname, *args):
        if fullname.startswith(('runtime_protocol', 'astrid.packs.rendering',
                                'astrid.core.rendering', 'astrid.sdk.authoring_render_preview',
                                'astrid.core.timeline.compatibility', 'composition')) or 'scene' in fullname:
            raise AssertionError('forbidden dependency: ' + fullname)
sys.meta_path.insert(0, Blocked())
from tests.sdk.test_timeline_capture_projection import project, draft
from tests.sdk.test_timeline_commit_provider_document import document_fixture
from astrid.core.timeline.authoring_bundle import preview_authoring_candidate
document = document_fixture()
assert project(document)['expansion']['canonical'] is True
assert project(document, preview_authoring_candidate(draft(document)))['expansion']['working_copy']
'''
    result = subprocess.run([sys.executable, "-c", script], capture_output=True, text=True,
                            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    assert result.returncode == 0, result.stderr


@pytest.fixture
def saved_runtime(tmp_path):
    from tests.helpers.runtime import use_runtime
    from tests.sdk import test_capture_source_runtime as captures

    use_runtime(commit="4bb1d0f7efd2972d7b027fd9f458dbe8dabd0136")
    yield from captures.open_source_runtime(tmp_path, before_provider=publish_golden)


def publish_golden(runtime):
    """Untracked saved chain, published before the provider; reference order differs from canonical sort order."""
    project_id = runtime.project_id
    parent = runtime.get_project_parent_composition_revision(project_id, "main", "parent-1")
    shot = runtime.get_project_shot_revision(project_id, "shot-shared", "shot-rev-1")
    internal = runtime.get_project_timeline_revision(project_id, "main", "internal-1")
    shots, internals, occurrences = [], [], []
    for name in ("z", "a"):
        child = {**copy.deepcopy(internal), "revision_id": f"internal-{name}"}
        child.pop("created_at")
        child.pop("content_digest")
        child["payload"]["opaque_timeline"]["source"] = name
        child["payload"]["created_at"] = f"authored internal {name}"
        child["payload"]["dependency_manifest"] = {"opaque": [None, False, 0, {"created_at": name}]}
        image = {**copy.deepcopy(shot), "shot_id": f"shot-{name}", "revision_id": f"shot-{name}-r1",
                 "internal_timeline_revision_id": child["revision_id"]}
        image.pop("created_at")
        image.pop("content_digest")
        image["payload"]["internal_timeline_revision_id"] = child["revision_id"]
        image["payload"]["created_at"] = f"authored shot {name}"
        image["payload"]["metadata"]["dependency_manifest"] = {"opaque": [name, None]}
        for item in image["payload"]["items"]:
            item["item_id"] += "-" + name
        occurrence = copy.deepcopy(parent["payload"]["occurrences"][0])
        occurrence.update(occurrence_id=f"occ-{name}", shot_id=image["shot_id"],
                          shot_revision_id=image["revision_id"], ordinal=len(occurrences), source_offset=0)
        occurrence["placement"]["start_ms"] = len(occurrences) * 1000
        shots.append(image)
        internals.append(child)
        occurrences.append(occurrence)
    payload = copy.deepcopy(parent["payload"])
    payload["occurrences"] = occurrences
    payload["created_at"] = "authored parent"
    payload["dependency_manifest"] = {"opaque": {"created_at": [None, False, 0]}}
    payload["config"]["theme_overrides"] = {"visual": {"canvas": {"fps": [30000, 1001]}}}
    runtime.service.publish_parent_composition(project_id, "main", {
        "project_id": project_id, "timeline_id": "main", "expected_head": "parent-1",
        "parent_revision_id": "parent-golden", "parent_composition": payload,
        "shot_revisions": shots, "internal_timeline_revisions": internals,
    }, idempotency_key="golden")


@pytest.fixture
def saved_closure(saved_runtime):
    commits, _ = saved_runtime.service._timeline_commits()
    document = commits.revision_closure(saved_runtime.project_id, "main", "parent-golden")
    return saved_runtime, document


@pytest.mark.integration
def test_real_saved_projection_config_registry_and_full_pins_golden(saved_closure):
    from astrid.packs.rendering.actions.render.managed_timeline import _project_exact_parent_head

    runtime, document = saved_closure
    parent, expected, expansion = _project_exact_parent_head(
        client=runtime, project_id=runtime.project_id, timeline_id="main", parent_revision_id="parent-golden")
    result = project(document)
    assert result["config"] == expected.config
    assert result["registry"] == expected.registry
    assert result["expansion"]["parent_content_digest"] == parent["content_digest"]
    for key in ("canonical", "parent_revision_id", "children", "shots", "occurrences", "outputs"):
        assert result["expansion"][key] == expansion[key]
    assert [row["shot_id"] for row in result["expansion"]["shots"]] == ["shot-z", "shot-a"]
    assert result["expansion"]["shots"][0]["content_digest"] == next(
        row["content_digest"] for row in document["shot_revisions"] if row["shot_id"] == "shot-z")
    assert result["expansion"]["children"][0]["config_hash"] == next(
        row["content_digest"] for row in document["internal_timeline_revisions"] if row["revision_id"] == "internal-z")


@pytest.mark.integration
def test_real_saved_entire_expansion_golden(saved_closure):
    from astrid.packs.rendering.actions.render.managed_timeline import _project_exact_parent_head

    runtime, document = saved_closure
    parent, projected, expansion = _project_exact_parent_head(
        client=runtime, project_id=runtime.project_id, timeline_id="main", parent_revision_id="parent-golden")
    assert project(document) == {
        "config": projected.config, "registry": projected.registry,
        "expansion": {**expansion, "parent_content_digest": parent["content_digest"]},
    }


@pytest.mark.integration
def test_saved_canonical_images_preserve_authored_fields_pins_order_and_read_rows(saved_closure, monkeypatch):
    from astrid.packs.rendering.actions.render.managed_timeline import _project_exact_parent_head

    runtime, document = saved_closure
    parent = runtime.get_project_parent_composition_revision(runtime.project_id, "main", "parent-golden")
    shots = {(row["shot_id"], row["revision_id"]): runtime.get_project_shot_revision(
        runtime.project_id, row["shot_id"], row["revision_id"]) for row in document["shot_revisions"]}
    internals = {row["revision_id"]: runtime.get_project_timeline_revision(
        runtime.project_id, "main", row["revision_id"]) for row in document["internal_timeline_revisions"]}
    # Exercise the duplicated read-envelope manifest, including a retained document pin.
    manifest = copy.deepcopy(document["dependency_manifest"])
    manifest["documents"] = [{"document_id": "retained-transcript", "version": 7,
                              "content_digest": "sha256:" + "1" * 64}]
    parent["dependency_manifest"] = manifest
    before = copy.deepcopy((parent, shots, internals, document))
    monkeypatch.setattr(runtime, "get_project_parent_composition_revision", lambda *args: parent)
    monkeypatch.setattr(runtime, "get_project_shot_revision", lambda p, s, r: shots[s, r])
    monkeypatch.setattr(runtime, "get_project_timeline_revision", lambda p, t, r: internals[r])
    returned, projected, expansion = _project_exact_parent_head(
        client=runtime, project_id=runtime.project_id, timeline_id="main", parent_revision_id="parent-golden")
    graph = expansion["graph"]
    assert graph == project(document)["expansion"]["graph"]
    assert returned["dependency_manifest"] == manifest
    assert manifest["shots"] == document["dependency_manifest"]["shots"]
    assert manifest["internal_timelines"] == document["dependency_manifest"]["internal_timelines"]
    assert manifest["media"] == document["dependency_manifest"]["media"]
    assert manifest["media"] and manifest["documents"]
    assert graph["parent_revision"]["content_digest"] == document["parent_revision"]["content_digest"]
    assert "dependency_manifest" not in graph["parent_revision"]
    assert [row["shot_id"] for row in graph["shot_revisions"]] == ["shot-z", "shot-a"]
    assert [row["revision_id"] for row in graph["internal_timeline_revisions"]] == ["internal-z", "internal-a"]
    images = [graph["parent_revision"], *graph["shot_revisions"], *graph["internal_timeline_revisions"]]
    for row in images:
        assert "created_at" not in row
        assert row["payload"]["created_at"].startswith("authored ")
    assert graph["parent_revision"]["payload"] == parent["payload"]
    for row in graph["shot_revisions"]:
        assert row["payload"] == shots[row["shot_id"], row["revision_id"]]["payload"]
    for row in graph["internal_timeline_revisions"]:
        assert row["payload"] == internals[row["revision_id"]]["payload"]
    assert all("created_at" in row for row in [parent, *shots.values(), *internals.values()])
    assert (parent, shots, internals, document) == before
    projected.graph["parent_revision"]["payload"]["created_at"] = "caller mutation"
    assert (parent, shots, internals, document) == before
    assert runtime.service.get_project_parent_composition_revision(
        runtime.project_id, "main", "parent-golden")["payload"] == before[0]["payload"]


@pytest.mark.integration
@pytest.mark.parametrize("change", ["parent", "child", "new_shot", "duplicate", "remove", "sdk_bundle"])
def test_real_candidate_matches_sdk_opener_exactly(saved_closure, change):
    from astrid.core.timeline.authoring_bundle import open_authoring_bundle
    from astrid.sdk.timeline_editing import (
        add_authoring_shot,
        duplicate_authoring_shot,
        remove_authoring_shot,
    )
    from astrid.sdk.timeline_filmstrip import _open_candidate_input_closure

    runtime, document = saved_closure
    bundle = bundle_from_document(document)
    if change == "sdk_bundle":
        bundle = open_authoring_bundle(
            runtime.get_project_parent_composition_revision(runtime.project_id, "main", "parent-golden"),
            shot_revisions=[runtime.get_project_shot_revision(runtime.project_id, row["shot_id"], row["revision_id"])
                            for row in document["shot_revisions"]],
            internal_timeline_revisions=[runtime.get_project_timeline_revision(runtime.project_id, "main", row["revision_id"])
                                         for row in document["internal_timeline_revisions"]])
        bundle["parent"]["config"]["opaque_draft"] = {"sdk": True}
    elif change == "parent":
        bundle["parent"]["config"]["opaque_draft"] = {"keep": [False, None, 0]}
    elif change == "child":
        next(iter(bundle["shots"].values()))["internal_timeline"]["clips"][0]["hold"] = 0.5
    elif change == "new_shot":
        add_authoring_shot(bundle, shot_id="new-shot", occurrence_id="new-occ", start_ms=2000)
    elif change == "duplicate":
        duplicate_authoring_shot(bundle, "shot-a", new_shot_id="duplicate-shot", occurrence_id="duplicate-occ", start_ms=2000)
    else:
        remove_authoring_shot(bundle, "shot-a")
    preview = preview_authoring_candidate(bundle)
    config, registry, expansion = _open_candidate_input_closure(
        runtime, project_id=runtime.project_id, timeline_id="main", preview=preview)
    assert project(document, preview) == {"config": config, "registry": registry, "expansion": expansion}
    assert runtime.service.get_project_timeline(runtime.project_id, "main")["head_revision_id"] == "parent-golden"
