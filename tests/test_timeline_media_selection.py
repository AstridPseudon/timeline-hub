"""Parity checks for the immutable media-selection read and commit pin."""
from __future__ import annotations

import io
import json
from types import SimpleNamespace

import pytest

from runtime_protocol.errors import ConflictError, NotFoundError, ProtocolError, RuntimeErrorBase
from runtime_protocol.server import RuntimeHandler

from test_generation_publish_v1_settlement import _effect, _fixture, _output, _settle
from test_timeline_commit_port import PreparedProvider, commit, digest, prepared, request


def _selection_effect(project_id):
    effect = _effect(project_id, groups=[{
        "group_key": "main",
        "selectors": [
            {"selector": "first", "ordinal": 0, "variant_key": "first", "output_port": "video"},
            {"selector": "second", "ordinal": 1, "variant_key": "second", "output_port": "video"},
        ],
    }])
    effect["payload"]["metadata"] = {"params": {"duration_seconds": 2.0}}
    return effect


def _settled_media(tmp_path, *, slug="media-selection", include_unmanaged=False):
    service, project, task, attempt, effect = _fixture(
        tmp_path, effect_factory=_selection_effect, slug=slug,
    )
    outputs = [
        _output(b"same video", output_port="video", group_key="main", variant_key="first", ordinal=0,
                filename="clip.mp4", media_type="video/mp4", duration_seconds=2.0),
        _output(b"same video", output_port="video", group_key="main", variant_key="second", ordinal=1,
                filename="clip.mp4", media_type="video/mp4", duration_seconds=2.0),
    ]
    if include_unmanaged:
        outputs.append(_output(
            b"preview", output_port="preview", group_key="preview", variant_key="preview", ordinal=0,
            filename="preview.mp4", media_type="video/mp4", duration_seconds=1.0,
        ))
    _settle(service, attempt, outputs, effect=effect)
    associations = {item["variant_key"]: item for item in service.managed_outputs(task["task"]["id"])}
    return service, project["id"], associations


class _SelectionRouteHandler(RuntimeHandler):
    def _identity(self, scope):
        self.scopes_seen.append(scope)
        return {"actor": "reader", "scopes": ["projects:read"]}

    def _send(self, status, payload=None, **kwargs):
        self.reply = status, payload


def _route_handler(runtime, query):
    handler = object.__new__(_SelectionRouteHandler)
    handler.server = SimpleNamespace(runtime=runtime)
    handler.command = "GET"
    handler.path = "/v1/projects/project%2Fone/media-selection?" + query
    handler.headers = {"Content-Length": "0"}
    handler.rfile = io.BytesIO(b"")
    handler.scopes_seen = []
    return handler


def _capture(service, project, association):
    return service.get_project_media_selection(project, {
        "association_id": association["association_id"],
        "object_id": association["object_id"],
        "version": association["lifecycle"]["version"],
    }, authorize=lambda: None)


def test_media_selection_query_decodes_exact_selector_values():
    calls = []

    def get_selection(project_id, selectors, *, authorize):
        calls.append((project_id, selectors, authorize()["actor"]))
        return {"asset": "picture/cut one&+", "generation_id": "generation/1", "variant_id": "variant?2"}

    handler = _route_handler(
        SimpleNamespace(get_project_media_selection=get_selection),
        "asset=picture%2Fcut+one%26%2B&generation_id=generation%2F1&variant_id=variant%3F2",
    )
    handler._route()
    assert handler.reply[0] == 200
    assert calls == [("project/one", {
        "asset": "picture/cut one&+", "generation_id": "generation/1", "variant_id": "variant?2",
    }, "reader")]
    assert handler.scopes_seen == ["projects:read", "projects:read"]


@pytest.mark.parametrize("query", [
    "asset=a&generation_id=g&variant_id=v&variant_id=duplicate",
    "asset=a&generation_id=g&variant_id=v&association_id=a&object_id=o&version=1",
    "asset=a&generation_id=g",
    "asset=a&generation_id=g&variant_id=v&unknown=x",
    "asset=a&generation_id=g&variant_id=v&bad=%",
    "association_id=a&object_id=o&version=0",
    "association_id=a&object_id=o&version=1.0",
])
def test_media_selection_query_rejects_duplicate_ambiguous_or_malformed_selectors(query):
    def get_selection(*args, **kwargs):
        pytest.fail("invalid selector query reached the service")

    handler = _route_handler(SimpleNamespace(get_project_media_selection=get_selection), query)
    with pytest.raises(ProtocolError):
        handler._route()


def test_media_selection_denies_unmanaged_uncompleted_and_foreign_outputs(tmp_path):
    service, project, associations = _settled_media(tmp_path, include_unmanaged=True)
    try:
        selected = associations["first"]
        selected_pin = _capture(service, project, selected)
        selected_query = {
            key: selected_pin[key] for key in ("asset", "generation_id", "variant_id")
        }
        # A generic managed output has no authoritative generation/variant binding.
        preview = associations["preview"]
        with pytest.raises(NotFoundError):
            service.get_project_media_selection(project, {
                "association_id": preview["association_id"],
                "object_id": preview["object_id"],
                "version": 1,
            }, authorize=lambda: None)

        foreign = service.create_project({"slug": "foreign", "name": "Foreign"})["id"]
        with pytest.raises(NotFoundError):
            service.get_project_media_selection(foreign, selected_query, authorize=lambda: None)

        service.store.conn.execute(
            "UPDATE generations SET status='failed' WHERE id=?", (selected["generation_id"],)
        )
        service.store.conn.commit()
        with pytest.raises(ConflictError):
            service.get_project_media_selection(project, selected_query, authorize=lambda: None)
    finally:
        service.close()


def test_unrelated_catalogue_change_does_not_invalidate_exact_selected_pin(tmp_path):
    service, project, associations = _settled_media(tmp_path, slug="unrelated-catalogue")
    try:
        selected = _capture(service, project, associations["first"])
        other = associations["second"]
        other_pin = _capture(service, project, other)
        metadata = service.get_variant(other_pin["variant_id"])["metadata"]
        metadata["is_primary"] = True
        service.store.conn.execute(
            "UPDATE generation_variants SET metadata_json=? WHERE id=?",
            (json.dumps(metadata, separators=(",", ":"), sort_keys=True), other_pin["variant_id"]),
        )
        service.store.conn.commit()
        assert service.get_project_media_selection(project, {
            "asset": selected["asset"],
            "generation_id": selected["generation_id"],
            "variant_id": selected["variant_id"],
        }, authorize=lambda: None) == selected
    finally:
        service.close()


def _selection_acceptance_snapshot(service, project):
    return {
        "head": tuple(service.store.conn.execute(
            "SELECT * FROM parent_composition_heads WHERE project_id=? AND timeline_id=?", (project, "main")
        ).fetchone() or ()),
        "history": [tuple(row) for row in service.store.conn.execute(
            "SELECT * FROM timeline_commit_history WHERE project_id=? AND timeline_id=? ORDER BY publication_id",
            (project, "main"),
        )],
        "receipts": [tuple(row) for row in service.store.conn.execute(
            "SELECT * FROM command_idempotency WHERE command_kind='timeline.commit' ORDER BY txn_id",
        )],
        "rows": list(service.store.conn.iterdump()),
    }


@pytest.mark.parametrize("mutation", ["lifecycle", "identity"])
def test_selected_media_mutation_between_capture_and_accept_is_atomic(tmp_path, mutation):
    service, project, associations = _settled_media(tmp_path, slug="accept-" + mutation)
    try:
        association = associations["first"]
        selection = service.get_project_media_selection(project, {
            "association_id": association["association_id"],
            "object_id": association["object_id"],
            "version": 1,
        }, authorize=lambda: None)
        assert set(selection) == {"asset", "generation_id", "variant_id", "object_id", "catalog_digest"}
        before_accept = None

        def action(context, port):
            nonlocal before_accept
            port.selected_media(selection)
            candidate = prepared(context, port)
            candidate["canonical_document"]["dependency_manifest"]["media"] = [{
                "media_id": selection["object_id"], "content_digest": selection["object_id"],
            }]
            candidate["records"]["commands"][0]["dependencies"] = [{
                "key": "media:selected", "kind": "media", "pin": selection, "policy": "exact",
            }]
            candidate["document_digest"] = digest(candidate["canonical_document"])
            if mutation == "lifecycle":
                service.store.conn.execute(
                    "UPDATE managed_output_lifecycle SET state='reclaimed', version=version+1 WHERE association_id=?",
                    (association["association_id"],),
                )
            else:
                service.store.conn.execute(
                        "UPDATE managed_output_associations SET variant_key=? WHERE association_id=?",
                        ("changed", association["association_id"]),
                )
            service.store.conn.commit()
            before_accept = _selection_acceptance_snapshot(service, project)
            return port.accept(candidate)

        provider = PreparedProvider(action)
        service.register_timeline_commit_provider(provider)
        service.test_project = project
        service.create_timeline(project, "main", idempotency_key="create-main")
        body = request(service)
        body["commands"][0]["op"] = "fixture.inspect"
        body["commands"][0]["args"]["selection"] = selection
        with pytest.raises(RuntimeErrorBase):
            commit(service, body, key="mutated-" + mutation)
        assert provider.calls == 1
        assert before_accept == _selection_acceptance_snapshot(service, project)
        assert service.store.conn.execute(
            "SELECT COUNT(*) FROM timeline_commit_history WHERE intent='recorded'"
        ).fetchone()[0] == 0
    finally:
        service.close()
