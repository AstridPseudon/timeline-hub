from __future__ import annotations

import base64
import copy
import json
import os
import subprocess
import sys

import pytest

from runtime_protocol.errors import NotFoundError, ValidationError
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit import CommitRejected
from runtime_protocol.timeline_commit_inputs import capture_document_input, reachable_document_input_pins
from runtime_protocol.timeline_commit_store import digest
from tests.astrid_checkout import astrid_checkout
from timeline_trusted_bootstrap import seed_trusted_legacy_parent

pytestmark = pytest.mark.integration


@pytest.fixture
def legacy(tmp_path, monkeypatch):
    root = tmp_path / "realm"
    RealmStore.initialize(root).close()
    service = RuntimeService(root)
    try:
        project = service.create_project({"slug": "trusted", "name": "Trusted"})["id"]
        service.create_timeline(project, "film", idempotency_key="timeline")
        png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+j1ioAAAAASUVORK5CYII="
        )
        media = service.ingest(project, png, media_type="image/png", original_name="source.png",
                               idempotency_key="image")["data"]["object_id"]
        content = {"schema": "media.transcript/v1", "media_id": media, "source_id": "whisper",
                   "segments": [{"id": "line-1", "start": 4, "end": 5, "text": "original",
                                 "words": [{"id": "word-1", "start": 4, "end": 5, "text": "original"}]}]}
        source = service.create_document(project, {
            "document_id": service._transcript_document_id(project, media, "whisper"),
            "kind": "media.transcript", "content": content,
        }, idempotency_key="transcript")["data"]
        pin = {"document_id": source["document_id"], "version": source["version"],
               "content_digest": digest(content)}
        # Import the actual Agent factory in its own dependency/source stack:
        # Runtime's tests package must not shadow Agent's tests package.
        # Bind real input identities BEFORE factory construction, never JSON
        # replace IDs/times or modify a constructed authored parent afterward.
        script = """
import json, sys
from tests.editing_conformance import test_recipe_m2_group_migration as recipe
from tests.sdk.test_timeline_commit_provider import source_fixture
context = json.load(sys.stdin)
literal = recipe.legacy_document()
source = source_fixture('transcript')
bound = recipe.legacy_document(project_id=context['project'], media_id=context['media'],
                               transcript_pin=context['pin'])
assert literal == json.loads(recipe.FIXTURE.read_text())['input']
print(json.dumps({'literal': literal, 'literal_source': source, 'bound': bound}))
"""
        checkout = astrid_checkout()
        result = subprocess.run(
            [os.environ.get("ASTRID_PYTHON", sys.executable), "-c", script],
            cwd=checkout, env={**os.environ, "PYTHONPATH": str(checkout), "PYTHONDONTWRITEBYTECODE": "1"},
            input=json.dumps({"media": media, "project": project, "pin": pin}),
            capture_output=True, text=True, check=True,
        )
        fixtures = json.loads(result.stdout)

        def unavailable(*args, **kwargs):
            raise AssertionError("trusted setup/readback evaluated a scene")

        monkeypatch.setattr("runtime_protocol.service.evaluate_closure", unavailable)
        monkeypatch.setattr("runtime_protocol.visual_seam.evaluate_closure", unavailable)
        yield service, root, fixtures, source
    finally:
        service.close()


def test_bound_factory_parent_with_runtime_supported_source_reads_back_exactly(legacy, monkeypatch):
    # This qualifies the raw-parent/storage seam with an ordinary Runtime
    # transcript. It does NOT qualify Agent's detached lines-shaped source;
    # its separate exact-source refusal below remains a handoff blocker.
    service, root, fixtures, source = legacy
    document = fixtures["bound"]
    original = copy.deepcopy(document)
    literal_payload = fixtures["literal"]["parent_revision"]["payload"]
    # The factory's authored parent differs only in its pre-bound media input.
    expected_payload = copy.deepcopy(literal_payload)
    expected_payload["registry"]["assets"]["image"]["media_id"] = source["content"]["media_id"]
    assert document["parent_revision"]["payload"] == expected_payload
    from timeline_trusted_bootstrap import request_identity

    def captured_request_identity(context):
        assert context["request"]["commands"][0]["created"] == []
        assert context["invocation"]["body"] == context["request"]
        return request_identity(context)

    monkeypatch.setattr("timeline_trusted_bootstrap.request_identity", captured_request_identity)
    result = seed_trusted_legacy_parent(service, document, idempotency_key="legacy-setup")
    assert document == original
    assert result["data"]["canonical_document"] == original
    assert result["data"]["document_digest"] == digest(original)
    project, timeline = document["project_id"], document["timeline_id"]
    parent = document["parent_revision"]
    pin = document["dependency_manifest"]["documents"][0]

    def readback(runtime):
        head = runtime.get_project_timeline(project, timeline)
        assert head["head_revision_id"] == parent["revision_id"]
        assert head["head_publication_id"] == result["receipt"]["receipt_id"]
        revision = runtime.get_project_parent_composition_revision(project, timeline, parent["revision_id"])
        assert revision["payload"] == parent["payload"]
        assert revision["content_digest"] == digest(parent["payload"]) == parent["content_digest"]
        assert revision["dependency_manifest"] == document["dependency_manifest"]
        commits, _ = runtime._timeline_commits()
        assert commits.revision_closure(project, timeline, parent["revision_id"]) == original
        pins = reachable_document_input_pins(runtime.store.conn, project, timeline,
                                             revision_ids=[parent["revision_id"]])
        assert pins == [pin]
        captured = capture_document_input(runtime.store.conn, project, pin, reachable_pins=pins,
                                          expected_kind="media.transcript", expected_schema="media.transcript/v1")
        assert captured.document == source
        history = runtime.list_timeline_commits(project, timeline, authorize=lambda: None)
        assert len(history["items"]) == 2
        setup = history["items"][-1]
        assert setup["receipt"] == result["receipt"]
        assert setup["provider_version"] == "test-only-trusted-bootstrap"
        record = setup["records"]["commands"][0]
        assert record["command"]["op"] == "test.trusted-legacy-bootstrap"
        assert record["command"]["created"] == record["created"] == []
        assert record["writes"][0]["after"]["value"] == parent["payload"]
        assert record["dependencies"][0]["pin"] == pin
        inspected = runtime.inspect_timeline(project, timeline, {"detail": True})
        assert inspected["revision_id"] == parent["revision_id"]
        assert inspected["parent_content_digest"] == parent["content_digest"]
        assert inspected["render_requested"] is False
        assert inspected["render_timing_context"]["fps"] == {"numerator": 30000, "denominator": 1001}
        assert [(row["clip_id"], row["start"], row["duration"]) for row in inspected["selected_parent_clips"]] == [
            ("before", [10, 1], [1, 1]), ("c1", [0, 1], [2, 1]),
            ("c2", [2, 1], [2, 1]), ("after", [12, 1], [1, 1]),
        ]
        return inspected

    inspected = readback(service)
    service.update_document(project, source["document_id"], {"expected_version": 1,
                            "content": {**source["content"], "segments": []}}, idempotency_key="overwrite-source")
    service.close()
    reopened = RuntimeService(root)
    try:
        assert readback(reopened) == inspected
        assert seed_trusted_legacy_parent(reopened, document, idempotency_key="legacy-setup") == result
        assert reopened.store.integrity_report()["ok"]
    finally:
        reopened.close()


@pytest.mark.parametrize("damage", ["digest", "media", "pin", "second-setup", "changed-retry"])
def test_invalid_or_repeated_setup_refuses_without_rewriting_input(legacy, damage):
    service, _, fixtures, _ = legacy
    document = copy.deepcopy(fixtures["bound"])
    project, timeline = document["project_id"], document["timeline_id"]
    if damage in {"second-setup", "changed-retry"}:
        seed_trusted_legacy_parent(service, document, idempotency_key="first")
    commits, _ = service._timeline_commits()
    commits.bootstrap(project, timeline, authorize=lambda: None)
    before = service.get_project_timeline(project, timeline)
    if damage == "digest":
        document["parent_revision"]["payload"]["opaque"] = None
    elif damage == "media":
        document["dependency_manifest"]["media"][0]["media_id"] = "sha256:" + "1" * 64
        document["dependency_manifest"]["media"][0]["content_digest"] = "sha256:" + "1" * 64
    elif damage == "pin":
        document["dependency_manifest"]["documents"][0]["content_digest"] = "sha256:" + "0" * 64
    elif damage == "changed-retry":
        document["parent_revision"]["payload"]["opaque"] = None
        document["parent_revision"]["content_digest"] = digest(document["parent_revision"]["payload"])
    supplied = copy.deepcopy(document)
    expected = NotFoundError if damage == "pin" else (ValidationError, CommitRejected)
    with pytest.raises(expected):
        seed_trusted_legacy_parent(service, document,
                                   idempotency_key="first" if damage == "changed-retry" else "refused")
    assert document == supplied
    assert service.get_project_timeline(project, timeline) == before


def test_literal_agent_transcript_source_is_not_an_allowed_runtime_document(legacy):
    service, _, fixtures, source = legacy
    # Exact counterexample, not a fabricated evaluation or a repaired source:
    # Agent's detached source fixture uses lines; ordinary Runtime API requires
    # segments. Keep this incompatibility visible for the Agent handoff.
    literal = fixtures["literal_source"]["document"]
    assert "lines" in literal["content"] and "segments" not in literal["content"]
    project = source["project_id"]
    with pytest.raises(ValidationError, match="transcript content must have the canonical media.transcript/v1 fields"):
        service.create_document(project, {"document_id": literal["document_id"],
                                "kind": literal["kind"], "content": literal["content"]},
                                idempotency_key="literal-source")
