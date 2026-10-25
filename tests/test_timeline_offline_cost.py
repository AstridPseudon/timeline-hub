from __future__ import annotations

import copy
import json

import pytest

from runtime_protocol import timeline_commit_auth as auth
from runtime_protocol.errors import ValidationError
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_validation import detached, digest
from tools.benchmark_timeline_commit_cost import CAPTURE, element_document, verify_retained


@pytest.mark.parametrize("scale", [1, 4, 16])
def test_synthetic_element_shapes_keep_validated_document_images(scale):
    document = element_document(scale)
    before = copy.deepcopy(document)
    images = auth._capture_document_images(document)
    assert len(images) == 3
    assert len(document["parent_revision"]["payload"]["clips"]) == 2 * scale
    assert len(document["internal_timeline_revisions"][0]["payload"]["clips"]) == 3 * scale
    assert all(image["content_digest"] == digest(image["payload"]) for image in images.values())
    result = detached(document)
    result["parent_revision"]["payload"]["clips"][0]["hold"] = 99
    assert document == before
    auth._capture_document_images(document)


@pytest.mark.parametrize("damage", ["schema", "nonfinite", "digest", "duplicate"])
def test_offline_shapes_recheck_security_guards_after_success(damage):
    document = element_document()
    auth._capture_document_images(document)
    if damage == "schema":
        document["parent_revision"]["revision_id"] = None
    elif damage == "nonfinite":
        document["parent_revision"]["payload"]["opaque"] = float("inf")
    elif damage == "digest":
        document["parent_revision"]["payload"]["clips"][0]["hold"] = 99
    else:
        document["shot_revisions"].append(copy.deepcopy(document["shot_revisions"][0]))
    before = copy.deepcopy(document)
    with pytest.raises((ValidationError, CommitRejected)):
        auth._capture_document_images(document)
    assert document == before


def test_offline_reproducer_keeps_authentic_capture_and_checks_both_stages():
    packet = json.loads(CAPTURE.read_text(encoding="utf-8"))
    before = copy.deepcopy(packet)
    verify_retained(packet)
    assert packet == before
    packet["capture"]["landing"]["commands"][0]["input"]["unexpected"] = True
    with pytest.raises((ValidationError, CommitRejected)):
        verify_retained(packet)
