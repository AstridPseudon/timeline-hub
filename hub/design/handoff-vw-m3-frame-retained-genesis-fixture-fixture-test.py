"""Pure input witnesses. No realm, provider, acceptance, capture or renderer."""
import base64
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

from runtime_protocol.errors import ValidationError
from runtime_protocol.service import RuntimeService
from runtime_protocol.snapshot_refs import snapshot_bytes, snapshot_digest
from runtime_protocol.timeline_commit_validation import digest, validate_commit_value

PREFIX = Path(__file__).with_name("handoff-vw-m3-frame-retained-genesis-fixture-")
spec = importlib.util.spec_from_file_location("retained_fixture", str(PREFIX) + "fixture.py")
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


def test_canonical_input_uses_packaged_runtime_schema_and_codec():
    value = fixture.build_fixture()
    document = value["canonical_document"]
    before = copy.deepcopy(document)
    validate_commit_value(document, "CanonicalDocument")
    for image in [document["parent_revision"], *document["shot_revisions"], *document["internal_timeline_revisions"]]:
        assert RuntimeService._revision_digest(image["payload"]) == image["content_digest"]
    assert document == before
    assert value["document_digest"] == digest(document)
    assert snapshot_digest(document) == digest(document)
    assert json.loads(snapshot_bytes(document)) == document


def test_exact_main_image_input_and_owned_media_manifest():
    value = fixture.build_fixture()
    document = value["canonical_document"]
    old = json.loads(PREFIX.with_name("handoff-vw-m3-main-image-cap-source-vector-raw-closure.json").read_text())
    # S2's RawTimelinePayload requires a list; MAIN's old source fixture used
    # the older single effect-map spelling. Retain that exact fade declaration.
    expected = copy.deepcopy(old["internal_timeline_revisions"][0]["payload"])
    expected["clips"][0]["effects"] = [expected["clips"][0]["effects"]]
    assert document["internal_timeline_revisions"][0]["payload"] == expected
    parent = document["parent_revision"]["payload"]
    assert parent["config"] == old["parent_revision"]["payload"]["config"]
    assert len(parent["occurrences"]) == 1
    assert parent["occurrences"][0]["duration_ms"] == 4000
    media, = value["media"]
    data = base64.b64decode(media["bytes_base64"], validate=True)
    assert data == PREFIX.with_name("handoff-vw-m3-main-image-cap-source-vector-image.png").read_bytes()
    assert hashlib.sha256(data).hexdigest() == "ec19e1c7d1d247d56db54f73e6514c92a82147a1b6ab59eaa30edeebca2e82b6"
    assert len(data) == media["size"]
    assert media["object_id"] == media["digest"] == "sha256:" + hashlib.sha256(data).hexdigest()
    assert document["dependency_manifest"]["media"] == [{"media_id": media["object_id"], "content_digest": media["digest"]}]


def test_scope_rebinding_changes_document_identity_without_changing_media_or_child():
    a, b = fixture.build_fixture(), fixture.build_fixture("fresh-project", "fresh-timeline")
    assert a["document_digest"] != b["document_digest"]
    assert a["media"] == b["media"]
    assert a["canonical_document"]["internal_timeline_revisions"][0]["payload"] == b["canonical_document"]["internal_timeline_revisions"][0]["payload"]


def test_published_agent_pure_capture_projector_consumes_this_canonical_input():
    from astrid.sdk.timeline.commit import create_runtime_commit_service

    document = fixture.build_fixture()["canonical_document"]
    before = copy.deepcopy(document)
    projection = create_runtime_commit_service().project_capture(document)
    clip, = projection["config"]["clips"]
    assert clip["hold"] == 4
    assert clip["effects"] == [{"fade_out": 1}]
    assert projection["expansion"]["parent_revision_id"] == document["parent_revision"]["revision_id"]
    assert projection["expansion"]["parent_content_digest"] == document["parent_revision"]["content_digest"]
    asset, = projection["registry"]["assets"].values()
    assert asset["media_id"] == document["dependency_manifest"]["media"][0]["media_id"]
    assert document == before
    assert document["internal_timeline_revisions"][0]["payload"]["clips"][0]["hold"] == 5


@pytest.mark.parametrize("field", ["track", "duration_ms"])
def test_packaged_canonical_schema_rejects_missing_occurrence_field(field):
    document = fixture.build_fixture()["canonical_document"]
    del document["parent_revision"]["payload"]["occurrences"][0][field]
    with pytest.raises(ValidationError):
        validate_commit_value(document, "CanonicalDocument")


def test_existing_restore_request_uses_real_head_pair_and_target_payload_digest():
    document = fixture.build_fixture()["canonical_document"]
    head = {"revision_id": "server-created-empty-head", "publication_id": "server-created-empty-receipt"}
    request = fixture.restore_request(document, head)
    assert request["base_revision_id"] == head["revision_id"]
    assert request["base_publication_id"] == head["publication_id"]
    assert request["commands"][0]["args"] == {"revision_id": document["parent_revision"]["revision_id"],
        "content_digest": RuntimeService._revision_digest(document["parent_revision"]["payload"])}
    assert request["commands"][0]["op"] == "timeline.restore"
    assert "capture_snapshot_ref" not in request
