"""Restore preservation with the real Agent; default Runtime never imports it."""
from __future__ import annotations

import copy
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

import test_shot_composition_runtime as host
from test_shot_composition_runtime import restore_provider as real_provider  # noqa: F401 (fixture)
from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import RequestCommitPort, digest, route_path
from test_timeline_commit_input_integration import (
    assert_retained,
    body,
    captured_move,
    commit,
    head,
    history,
    snapshot,
)

from timeline_commit_film_fixture import build_film_fixture

pytestmark = pytest.mark.integration


@pytest.fixture(params=["transcript", "config"])
def retained(request, tmp_path, astrid_importable, monkeypatch):
    # Import Agent only inside this explicitly selected integration fixture.
    from astrid.sdk.timeline import commands as core
    from astrid.sdk.timeline import commit as agent
    from astrid.sdk.timeline.capture import capture_move
    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    assert Path(agent.__file__).resolve().is_relative_to(astrid_importable)
    film = build_film_fixture(tmp_path)
    service = RuntimeService(film.duplicate_root)
    try:
        transcript = service.get_document(film.project_id, film.transcript_document_id)
        config = service.create_document(
            film.project_id, {"document_id": "film.config", "kind": "film.config", "content": {
                "schema": "film.config/v1", "enabled": True, "opaque": [None, {"keep": True}],
                "source": {"media_id": transcript["content"]["media_id"],
                           "source_id": transcript["content"]["source_id"], "word_id": "word-1"},
                "time_map": {"source_offset": 0, "speed": 1},
            }}, idempotency_key="config-v1",
        )["data"]
        sources = [config, transcript]
        captures = [{"pin": {"document_id": source["document_id"], "version": source["version"],
                              "content_digest": digest(source["content"])}, "document": source}
                    for source in sources]
        selected = captures[1 if request.param == "transcript" else 0]
        source, pin = selected["document"], selected["pin"]
        # The captured main backup stays unchanged. Accept only the additional
        # authored anchor/input image through the host boundary, then restart
        # with real Agent for all measured restore, inverse and move operations.
        commits, _ = service._timeline_commits()
        base = commits.install_verified_baseline(film.project_id, film.timeline_id, authorize=lambda: None)
        candidate = commits.revision_closure(film.project_id, film.timeline_id, base["revision_id"])
        parent = candidate["parent_revision"]["payload"]
        parent["clips"][0]["at"] = 0.25
        parent["clips"][0]["app"] = {
            "on": "word:word-1", "astrid": {"on": "word:word-1", "fixed_start": False, "for": 5.5},
        }
        parent["config"]["clips"] = copy.deepcopy(parent["clips"])
        candidate["parent_revision"]["revision_id"] = "input-retained-v1"
        candidate["parent_revision"]["content_digest"] = digest(parent)
        candidate["dependency_manifest"]["documents"] = [capture["pin"] for capture in captures]
        seed = host._accept_restore_document(service, candidate, idempotency_key="initial-input-v1")
        original = seed["data"]["canonical_document"]
        changed = copy.deepcopy(source["content"])
        if request.param == "transcript":
            changed["segments"][0].update(text="producer v2", start=2, end=3)
            changed["segments"][0]["words"] = [{"id": "replacement-word", "text": "v2", "start": 2, "end": 3}]
        else:
            changed.update(enabled=False, opaque=["producer v2"], time_map={"source_offset": 10, "speed": 2})
        current = service.update_document(
            film.project_id, source["document_id"], {"expected_version": 1, "content": changed},
            idempotency_key="producer-v2",
        )["data"]
        assert current["version"] == 2
    finally:
        service.close()

    observed = SimpleNamespace(reads=[], core=[], compiled=[], providers=[])

    def watch_read(method):
        def read(port, value):
            result = method(port, value)
            observed.reads.append(copy.deepcopy(result))
            return result
        return read

    for name in ("transcript_source", "config_source"):
        monkeypatch.setattr(RequestCommitPort, name, watch_read(getattr(RequestCommitPort, name)))
    execute = core.execute
    compile_candidate = agent.compile_authoring_candidate
    provider_type = type(load_timeline_commit_provider("astrid"))
    provider_commit = provider_type.commit

    def observe_execute(bundle, *args, **kwargs):
        observed.core.append(copy.deepcopy(bundle))
        return execute(bundle, *args, **kwargs)

    def observe_compile(bundle):
        result = compile_candidate(bundle)
        observed.compiled.append(copy.deepcopy(bundle))
        return result

    def observe_provider(provider, context, port):
        observed.providers.append(context["idempotency_key"])
        return provider_commit(provider, context, port)

    monkeypatch.setattr(core, "execute", observe_execute)
    monkeypatch.setattr(agent, "compile_authoring_candidate", observe_compile)
    monkeypatch.setattr(provider_type, "commit", observe_provider)
    value = SimpleNamespace(film=film, agent=agent, move=capture_move,
                            source=source, pin=pin, captures=captures,
                            current=current, seed=seed, original=original, observed=observed)

    def restart():
        if getattr(value, "service", None):
            value.service.close()
        value.service = RuntimeService(film.duplicate_root)
        value.service.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))

    value.restart = restart
    restart()
    try:
        yield value
    finally:
        value.service.close()


@pytest.mark.parametrize("case,admission_seconds", [
    (host.test_parent_composition_history_paginates_and_restores_exact_closure_over_http, None),
    (host.test_parent_composition_history_lists_broken_rows_but_restore_rejects_tampered_dependencies, None),
    (host.test_parent_composition_restore_preserves_payload_and_declared_media_dependency_closure, None),
    (host.test_parent_composition_restore_uses_selected_admission_integrity_budget, 5.0),
    (host.test_parent_composition_restore_uses_selected_admission_integrity_budget, 120.0),
    (host.test_parent_composition_restore_refuses_incomplete_integrity_at_selected_budget, None),
    (host.test_stale_head_conflict_carries_machine_readable_reason_over_http, None),
], ids=["history-http", "tampered-child", "declared-media", "budget-5", "budget-120",
        "incomplete-integrity", "stale-head-http"])
def test_original_restore_behaviour_with_real_agent(case, admission_seconds, tmp_path, monkeypatch, real_provider):
    kwargs = {"tmp_path": tmp_path, "restore_provider": real_provider}
    if admission_seconds is not None:
        kwargs.update(monkeypatch=monkeypatch, admission_seconds=admission_seconds)
    elif case is host.test_parent_composition_restore_refuses_incomplete_integrity_at_selected_budget:
        kwargs["monkeypatch"] = monkeypatch
    case(**kwargs)


def restore(case, source, guards, key):
    return case.service.restore_project_parent_composition_revision(
        case.film.project_id, case.film.timeline_id, source, guards,
        idempotency_key=key, publisher="restore-editor", authorize=lambda: None,
        invocation_path=route_path(case.film.project_id, case.film.timeline_id,
                                   f"composition-revisions/{source}/restore"),
    )


def assert_closure(accepted, expected):
    actual = accepted["data"]["canonical_document"]
    assert actual["parent_revision"]["payload"] == expected["parent_revision"]["payload"]
    assert actual["parent_revision"]["content_digest"] == expected["parent_revision"]["content_digest"]
    for field in ("shot_revisions", "internal_timeline_revisions", "dependency_manifest"):
        assert actual[field] == expected[field]
    assert accepted["receipt"]["result"] == accepted["data"]
    assert accepted["data"]["accepted_revision_id"] == actual["parent_revision"]["revision_id"]


def test_real_restore_retained_inputs_inverse_redo_and_restart_retry(retained, monkeypatch):
    case = retained
    source_files = {path.relative_to(case.film.source_root): path.read_bytes()
                    for path in case.film.source_root.rglob("*") if path.is_file()}

    # The neutral fixture is already seeded. Every measured edit uses Agent,
    # with evaluation unavailable and the mutable producer already at v2.
    import runtime_protocol.service as service_module
    import runtime_protocol.visual_seam as visual_seam

    def unavailable(*args, **kwargs):
        raise AssertionError("restore invoked the renderer or recomputed a retry")

    class RendererUnavailable:
        def find_spec(self, fullname, path=None, target=None):
            if fullname.startswith(("astrid.packs.rendering", "astrid.core.rendering",
                                    "astrid.sdk.authoring_render_preview",
                                    "astrid.core.timeline.compatibility", "composition", "remotion")):
                raise AssertionError("restore imported renderer: " + fullname)

    monkeypatch.setattr(sys, "meta_path", [RendererUnavailable(), *sys.meta_path])
    monkeypatch.setattr(service_module, "evaluate_closure", unavailable)
    monkeypatch.setattr(visual_seam, "evaluate_closure", unavailable)
    initial = copy.deepcopy(case.original)
    moved = commit(case.service, case.film,
                   body(case.film, head(case.service, case.film), [captured_move(case)]), "before-restore")
    assert_retained(case, moved)
    assert moved["data"]["canonical_document"]["parent_revision"]["payload"] != initial["parent_revision"]["payload"]
    current = head(case.service, case.film)
    guards = {"expected_head": current["revision_id"], "expected_publication_id": current["publication_id"]}
    source = initial["parent_revision"]["revision_id"]
    immutable = {table: [tuple(row) for row in case.service.store.conn.execute(
        f"SELECT id, payload_json, content_digest FROM {table} ORDER BY id")]
        for table in ("parent_composition_revisions", "shot_revisions", "internal_timeline_revisions")}
    restored = restore(case, source, guards, "real-restore")
    assert_closure(restored, initial)
    assert_retained(case, restored)
    entry = history(case.service, case.film)[-1]
    assert entry["records"]["restored_from"] == {
        "revision_id": source, "content_digest": initial["parent_revision"]["content_digest"],
    }
    assert entry["records"]["commands"][0]["writes"]
    assert entry["receipt"] == restored["receipt"]
    assert restored["receipt"]["receipt_id"] not in {
        case.seed["receipt"]["receipt_id"], moved["receipt"]["receipt_id"],
    }
    for table, rows in immutable.items():
        for row in rows:
            assert tuple(case.service.store.conn.execute(
                f"SELECT id, payload_json, content_digest FROM {table} WHERE id=?", (row[0],),
            ).fetchone()) == row

    def inverse(publication, key):
        return commit(case.service, case.film, body(case.film, head(case.service, case.film), [{
            "schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
            "args": {"publications": [publication["receipt"]["receipt_id"]]},
        }]), key)

    undone = inverse(restored, "undo-restore")
    assert_closure(undone, moved["data"]["canonical_document"])
    assert_retained(case, undone)
    assert history(case.service, case.film)[-1]["records"]["undo_of"] == [restored["receipt"]["receipt_id"]]
    redone = inverse(undone, "redo-restore")
    assert_closure(redone, initial)
    assert_retained(case, redone)
    assert history(case.service, case.film)[-1]["records"]["undo_of"] == [undone["receipt"]["receipt_id"]]

    # The exact restore flight survives a service restart and newer history.
    case.restart()
    before, observed = snapshot(case.service), copy.deepcopy(vars(case.observed))
    with monkeypatch.context() as retry:
        retry.setattr(type(case.service._timeline_commit_provider), "commit", unavailable)
        retry.setattr(RealmStore, "integrity_report", unavailable)
        assert restore(case, source, guards, "real-restore") == restored
    assert snapshot(case.service) == before
    assert vars(case.observed) == observed
    assert head(case.service, case.film)["publication_id"] == redone["receipt"]["receipt_id"]
    changed = dict(guards, expected_publication_id=redone["receipt"]["receipt_id"])
    with pytest.raises(RuntimeErrorBase) as error:
        restore(case, source, changed, "real-restore")
    assert error.value.status == 409
    assert error.value.details["reason"] == "idempotency_mismatch"
    assert snapshot(case.service) == before
    assert case.observed.reads and all(value in case.captures for value in case.observed.reads)
    assert all(capture in case.observed.reads for capture in case.captures)
    assert case.service.get_document(case.film.project_id, case.source["document_id"]) == case.current
    assert {path.relative_to(case.film.source_root): path.read_bytes()
            for path in case.film.source_root.rglob("*") if path.is_file()} == source_files
