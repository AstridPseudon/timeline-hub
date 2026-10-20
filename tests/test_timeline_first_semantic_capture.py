"""M1 blocker diagnostic, NOT a first semantic input capture qualification.

The genuine legacy film has a word anchor and readable main-v1 sources, but
the admitted move is fixed numeric timing. Source hydration/dependencies alone
must not be presented as word-follow or config-driven semantic calculation.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest

from precut_realm_fixture import load_precut_realm_fixture
from runtime_protocol.errors import ValidationError
from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit_inputs import capture_document_input
from runtime_protocol.timeline_commit_port import RequestCommitPort, digest
from runtime_protocol.timeline_commit_validation import validate_commit_value
from test_timeline_commit_input_integration import body, commit, document, head, history, snapshot
from timeline_commit_film_fixture import FilmFixture


def test_official_move_dto_cannot_express_first_source_semantics():
    command = {"schema_version": 1, "op": "clip.move", "version": "1",
               "select": "parent/clip:music-bed", "args": {"on": 1}}
    validate_commit_value(command, "EditCommand")
    for args in ({"on": "word:word-1"}, {"on": 1, "pin": {
            "document_id": "film.config", "version": 1,
            "content_digest": "sha256:" + "0" * 64}}):
        with pytest.raises(ValidationError, match="invalid EditCommand"):
            validate_commit_value({**command, "args": args}, "EditCommand")


@pytest.mark.integration
def test_m1_fixed_move_is_not_first_semantic_capture(tmp_path, astrid_importable, monkeypatch):
    captured = load_precut_realm_fixture(tmp_path, variant="anchor")
    pins = captured.pins
    film = FilmFixture(
        source_root=captured.copy_roots[0], duplicate_root=captured.copy_roots[1],
        project_id=pins["project_id"], timeline_id=pins["timeline_id"],
        parent_revision_id=pins["parent_revision_id"], media_ids=pins["media_ids"],
        transcript_document_id=pins["transcript_document_id"], text_binding_id=pins["text_binding_id"],
    )

    def unavailable(*args, **kwargs):
        raise AssertionError("fixed move/retry/inverse reached forbidden work")

    class RendererUnavailable:
        def find_spec(self, fullname, path=None, target=None):
            if fullname.startswith(("astrid.packs.rendering", "astrid.core.rendering",
                                    "astrid.sdk.authoring_render_preview",
                                    "astrid.core.timeline.compatibility", "composition", "remotion")):
                raise AssertionError("save imported renderer: " + fullname)

    monkeypatch.setattr(sys, "meta_path", [RendererUnavailable(), *sys.meta_path])
    import runtime_protocol.service as service_module
    import runtime_protocol.visual_seam as visual_seam
    monkeypatch.setattr(service_module, "evaluate_closure", unavailable)
    monkeypatch.setattr(visual_seam, "evaluate_closure", unavailable)
    from astrid.sdk.timeline import commit as agent
    from astrid.sdk.timeline.capture import capture_move
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    assert Path(agent.__file__).resolve().is_relative_to(astrid_importable)
    reads = []

    def watch_read(method):
        def read(port, pin):
            result = method(port, pin)
            reads.append(copy.deepcopy(result))
            return result
        return read

    for name in ("transcript_source", "config_source"):
        monkeypatch.setattr(RequestCommitPort, name, watch_read(getattr(RequestCommitPort, name)))

    service = RuntimeService(film.duplicate_root)
    try:
        service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
        original = document(service, film)
        sources = [service.get_document(film.project_id, name)
                   for name in (film.transcript_document_id, "film.config")]
        assert sources[0]["content"]["schema"] == "media.transcript/v1"
        assert sources[0]["content"]["segments"][0]["words"][0]["id"] == "word-1"
        assert sources[1]["kind"].endswith(".config")
        assert original["dependency_manifest"]["documents"] == []
        initial_parent = original["parent_revision"]["payload"]
        assert initial_parent["clips"][0]["app"]["astrid"]["on"] == "word:word-1"
        for source in sources:
            pin = {"document_id": source["document_id"], "version": source["version"],
                   "content_digest": digest(source["content"])}
            # Read-only fixture feasibility check, outside Agent execution.
            capture = capture_document_input(service.store.conn, film.project_id, pin,
                                             expected_kind=source["kind"])
            assert capture.document == source and not capture.retained

        def assert_unretained():
            for table in ("timeline_document_input_contents", "timeline_document_input_bindings",
                          "timeline_document_input_links"):
                assert service.store.conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0] == 0

        assert_unretained()
        command = capture_move(agent.bundle_from_document(original), "parent/clip:music-bed", 1)
        request = body(film, head(service, film), [command])
        moved = commit(service, film, request, "fixed-move-not-word-follow")
        parent = moved["data"]["canonical_document"]["parent_revision"]["payload"]
        assert parent["clips"][0]["at"] == 1
        assert parent["clips"][0]["app"]["astrid"]["fixed_start"] is True
        record = history(service, film)[-1]["records"]["commands"][0]
        assert {"ref": "parent", "path": ["config", "output", "fps"],
                "state": {"state": "present", "value": 24}} in record["reads"]
        assert not [dep for dep in record["dependencies"] if dep["kind"] in {"source", "transcript"}]
        assert reads == []
        assert_unretained()

        for index, source in enumerate(sources):
            changed = copy.deepcopy(source["content"])
            if source["kind"] == "media.transcript":
                changed["segments"][0].update(text="producer v2", start=2, end=3)
                changed["segments"][0]["words"] = [
                    {"id": "replacement-word", "text": "v2", "start": 2, "end": 3}]
            else:
                changed["enabled"] = False
            updated = service.update_document(
                film.project_id, source["document_id"],
                {"expected_version": source["version"], "content": changed},
                idempotency_key=f"diagnostic-source-v2-{index}",
            )["data"]
            assert updated["version"] == 2
        service.close()
        service = RuntimeService(film.duplicate_root)
        provider = load_timeline_commit_provider("astrid")
        service.register_timeline_commit_provider(provider)
        before = snapshot(service)
        with monkeypatch.context() as retry:
            retry.setattr(type(provider), "commit", unavailable)
            assert commit(service, film, request, "fixed-move-not-word-follow") == moved
        assert snapshot(service) == before
        undo = {"schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
                "args": {"publications": [moved["receipt"]["receipt_id"]]}}
        undone = commit(service, film, body(film, head(service, film), [undo]), "fixed-move-inverse")
        assert undone["data"]["canonical_document"]["parent_revision"]["payload"] == initial_parent
        assert reads == []
        assert_unretained()
    finally:
        service.close()
