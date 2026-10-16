"""Three-occurrence persistence proofs via AstridClient.open and a real daemon.

Fixture provenance: frozen F6705/DF401 retention fixture manifest (SHA-256
 ef7410369bc16f114e23d492741fdc383628942fe7d59e081dad3f08b2aadace).
Only volatile project identity was omitted from the checked-in publication input.
Scene answers below are an explicit synthetic structural capability on the existing
scene client seam, including daemon request threads. No check, evaluation gate,
compiler, publisher or saved verifier is replaced. This is never render evidence.
"""

import copy
import json
import os
from pathlib import Path

import pytest

from astrid.core.execution.remotion_frame_owner import FrameOwnerError
from astrid.core.timeline import scene_answers
from astrid.sdk.client import AstridClient
from astrid.sdk.timeline import commands, journal, saved_publish
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import _digest
from astrid.sdk.timeline.duplicate_fidelity import verify_duplicate
from astrid.sdk.timeline_duplicate import duplicate_timeline
from banodoco_workspace_client.contract_metadata import PROTOCOL

FIXTURE = Path(__file__).parents[1] / "fixtures/timeline_editing/retention_three_occurrences.json"


@pytest.fixture
def daemon_fixture(tmp_path, monkeypatch, request):
    source = os.environ.get("ASTRID_GRAPH_RUNTIME_ROOT")
    if not source:
        pytest.skip("explicit matching Runtime source required")
    monkeypatch.syspath_prepend(source)
    import runtime_protocol
    from runtime_protocol.daemon import RuntimeDaemon
    from runtime_protocol.store import RealmStore

    assert Path(runtime_protocol.__file__).resolve().is_relative_to(Path(source).resolve())
    capabilities = dict(enabled=True, queries=[], saved_before_commit=[])
    proof_root = Path(os.environ.get("ASTRID_DUPLICATE_WITNESS_ROOT", tmp_path))
    proof_root.mkdir(exist_ok=True)

    def record(label, value):
        path = proof_root / (request.node.name + "-" + label + ".json")
        path.write_text(json.dumps(value, sort_keys=True, indent=2))

    capabilities["record"] = record

    class StructuralScene:
        def query_scene(self, *, revision_digest, scene, frames):
            if not capabilities["enabled"]:
                raise FrameOwnerError("structural_fixture_evaluation_unavailable")
            capabilities["queries"].append(dict(digest=revision_digest, frames=list(frames)))
            return [
                dict(frame=f, coverage="COVERED", content="CONTENT", findings=[], layers=[])
                for f in frames
            ]

    monkeypatch.setattr(scene_answers, "_client", lambda: StructuralScene())
    monkeypatch.setenv("BANODOCO_LOCAL_DATA_ROOT", str(tmp_path / "data"))
    monkeypatch.setattr(Checkout, "SAY_SAVED", False)
    realm = tmp_path / "realm"
    RealmStore.initialize(realm).close()
    daemon = RuntimeDaemon(
        realm, support_root=tmp_path / "support", authoring_profile="astrid"
    ).start()
    service = daemon.service
    p = service.create_project(
        dict(slug="retention", name="Structural retention fixture"), idempotency_key="p"
    )["id"]
    service.create_timeline(p, "fixture-source", idempotency_key="source")
    publication = dict(json.loads(FIXTURE.read_text()), project_id=p)
    if getattr(request, "param", None) == "rich":
        media = service.ingest(
            p,
            b"structural metadata item",
            media_type="text/plain",
            original_name="structural.txt",
            idempotency_key="metadata-object",
        )["data"]["object_id"]
        publication["parent_composition"]["config"]["opaque"] = {
            "literal": "fixture-shot-a",
            "null": None,
        }
        publication["parent_composition"]["registry"]["opaque"] = {
            "literal": "fixture-occurrence-a"
        }
        publication["parent_composition"]["clips"] = [
            dict(
                id="parent-picture",
                clipType="media",
                track="video-1",
                at=0,
                hold=1,
                opaque="fixture-shot-a",
            )
        ]
        for shot, internal in zip(
            publication["shot_revisions"], publication["internal_timeline_revisions"]
        ):
            item = "item-" + shot["shot_id"]
            shot["payload"]["items"] = [
                dict(
                    item_id=item,
                    media_id=media,
                    metadata=dict(source_item_id=item, opaque_literal=item),
                )
            ]
            internal["payload"]["clips"][0]["source_item_id"] = item
    service.publish_parent_composition(
        p, "fixture-source", publication, idempotency_key="source-content"
    )
    original_commit = service.commit_timeline

    def observed_commit(project, timeline, body, **kwargs):
        # Observe real saved bytes at receiver entry, before semantic publication.
        from astrid.sdk.timeline import store

        path = store.draft_path(project, timeline, store.current_draft(project, timeline))
        if path.is_file():
            saved_record = dict(
                timeline_id=timeline,
                request_id=body["request_id"],
                draft=json.loads(path.read_text()),
            )
            capabilities["saved_before_commit"].append(saved_record)
            record("saved-before-commit", capabilities["saved_before_commit"])
        return original_commit(project, timeline, body, **kwargs)

    monkeypatch.setattr(service, "commit_timeline", observed_commit)
    try:
        with AstridClient.open(
            endpoint=daemon.endpoint,
            credential=daemon.token,
            realm_id=service.realm["id"],
            actor_id="owner",
            client_name="duplicate-structural-test",
            client_version="1",
            protocol_version=PROTOCOL,
        ) as client:
            yield service, p, client, capabilities
    finally:
        daemon.stop()


def source_state(service, project):
    head = service.head(project, "fixture-source")
    return dict(
        head=head,
        history=service.list_project_parent_composition_revisions(
            project, "fixture-source", limit=200
        ),
        closure=service._commit_revision_closure(project, "fixture-source", head["revision_id"]),
    )


def assert_published(result):
    # The caller cannot infer publication from a non-throwing helper return.
    assert result["status"] in {"accepted", "no_change"} and result["copy_verified"], result
    assert result["new_head"] and result["draft_path"]


def test_real_daemon_three_occurrence_fidelity_changed_shot_and_undo(daemon_fixture):
    s, p, client, capability = daemon_fixture
    before = source_state(s, p)
    assert _digest(before["closure"]["parent_revision"]["payload"]) == "sha256:eeb6a23d5b7d25c45baffb8dfec53bea12a5c00fa06db34d4d5b5ab19d032654"
    result = duplicate_timeline(p, "fixture-source", slug="copy", client=client)
    assert_published(result)
    draft = Checkout.load(result["draft_path"])
    rows = [json.loads(row) for row in journal.journal_path(p, "copy").read_text().splitlines()]
    saved = [
        row
        for row in rows
        if row["kind"] == "save" and any(c["op"] == "timeline.duplicate" for c in row["calls"])
    ]
    assert len(saved) == 1 and len(saved[0]["calls"]) == 1
    # This pre-publication journal save is still a three-placement/three-shot document.
    assert len(saved[0]["calls"][0]["args"]["identities"]) == 3
    intent = next(
        e for row in rows for e in row["evidence"] if e.get("kind") == "publish-intent-v1"
    )
    persisted = saved_publish._exact(
        saved_publish._workspace(client), intent["body"], result["new_head"]
    )
    assert len(persisted["immutable_closure"]["parent"]["payload"]["occurrences"]) == 3
    assert (
        len(persisted["immutable_closure"]["shots"])
        == len(persisted["immutable_closure"]["internal_timelines"])
        == 3
    )
    verify_duplicate(
        saved_publish._workspace(client),
        intent["body"],
        next(
            e["result"]["canonical_document"]
            for row in rows
            for e in row["evidence"]
            if e.get("kind") == "publish-result-v1"
        ),
        persisted,
    )
    assert len(s.list_project_parent_composition_revisions(p, "copy", limit=200)["items"]) == 2
    assert (
        s.store.conn.execute(
            "SELECT count(*) FROM command_idempotency WHERE command_kind='timeline.commit'"
        ).fetchone()[0]
        == 1
    )
    assert source_state(s, p) == before and capability["queries"]
    capability["record"]("verified-copy", dict(source=before, result=result, persisted=persisted,
                                                saved_before_commit=capability["saved_before_commit"]))
    # Undo the one content transaction, then redo the exact duplicate in a new owned timeline for independence.
    assert len(draft.undo(client=client)) == 1
    undone = draft.publish("undo copy", client=client)
    assert undone["status"] == "accepted"
    assert (
        s.get_project_parent_composition_revision(p, "copy", undone["accepted_revision_id"])[
            "payload"
        ]["occurrences"]
        == []
    )
    independent = duplicate_timeline(p, "fixture-source", slug="changed", client=client)
    assert_published(independent)
    draft = Checkout.load(independent["draft_path"])
    row = draft.bundle["placements"][0]
    pin = draft.bundle["source_mapping"]["shots"][row["shot_id"]]
    commands.run(
        draft,
        dict(
            op="shot.set",
            select="occurrence:" + row["occurrence_id"] + "/shot",
            args=dict(
                source=dict(
                    parent_revision_id=draft.base_revision,
                    occurrence_id=row["occurrence_id"],
                    shot_id=pin["shot_id"],
                    shot_revision_id=pin["revision_id"],
                    internal_revision_id=pin["internal_timeline_revision_id"],
                ),
                values=dict(name="Changed destination only"),
            ),
        ),
    )
    assert draft.publish("changed destination", client=client)["status"] == "accepted"
    assert source_state(s, p) == before


@pytest.mark.parametrize("daemon_fixture", ["rich"], indirect=True)
def test_real_daemon_preserves_opaque_fields_and_defined_item_references(daemon_fixture):
    s, p, client, capability = daemon_fixture
    before = source_state(s, p)
    result = duplicate_timeline(p, "fixture-source", slug="rich-copy", client=client)
    assert_published(result)
    pre = capability["saved_before_commit"][0]["draft"]
    assert len(pre["placements"]) == len(pre["shots"]) == 3
    accepted = s._commit_revision_closure(p, "rich-copy", result["new_head"])
    for field in ("config", "registry", "clips"):
        assert (
            accepted["parent_revision"]["payload"][field]
            == before["closure"]["parent_revision"]["payload"][field]
        )
    for row, old in zip(
        accepted["parent_revision"]["payload"]["occurrences"],
        before["closure"]["parent_revision"]["payload"]["occurrences"],
    ):
        shot = s.get_project_shot_revision(p, row["shot_id"], row["shot_revision_id"])
        internal = s.get_project_timeline_revision(
            p, shot["internal_timeline_id"], shot["internal_timeline_revision_id"]
        )
        item = shot["payload"]["items"][0]
        assert item["item_id"] != "item-" + old["shot_id"]
        assert (
            item["metadata"]["source_item_id"]
            == item["item_id"]
            == internal["payload"]["clips"][0]["source_item_id"]
        )
        assert item["metadata"]["opaque_literal"] == "item-" + old["shot_id"]
    assert source_state(s, p) == before
    capability["record"]("verified-rich-copy", dict(source=before, result=result, persisted=accepted,
                                                     saved_before_commit=capability["saved_before_commit"]))


@pytest.mark.parametrize("missing", ["evaluation", "provider"])
def test_real_daemon_unavailable_capability_is_pending_and_recoverable(daemon_fixture, missing):
    s, p, client, capability = daemon_fixture
    provider = s._timeline_commit_provider
    if missing == "evaluation":
        capability["enabled"] = False
    else:
        s._timeline_commit_provider = None
    result = duplicate_timeline(p, "fixture-source", slug="pending", client=client)
    assert result["status"] == "pending" and result["copy_verified"] is False
    assert result["expected_shots"] == 3 and Path(result["draft_path"]).is_file()
    assert len(Checkout.load(result["draft_path"]).bundle["placements"]) == 3
    assert not s._timeline_resource("pending")["archived"]
    assert (
        s.store.conn.execute(
            "SELECT count(*) FROM command_idempotency WHERE command_kind='timeline.commit'"
        ).fetchone()[0]
        == 0
    )
    assert len(s.list_project_parent_composition_revisions(p, "pending", limit=200)["items"]) == 1
    capability["record"]("pending", dict(result=result, draft=Checkout.load(result["draft_path"]).bundle,
                                         bootstrap=s.head(p,"pending")))
    if missing == "evaluation":
        assert "evaluation" in result["error"] and result["diagnostics"]
        assert result["request_id"] is None  # preparation never reached durable intent
    else:
        assert (
            result["publication_result"]["error"]["code"] == "runtime_unavailable"
            and result["request_id"]
        )
    capability["enabled"] = True
    s._timeline_commit_provider = provider
    recovery = Checkout.load(result["draft_path"]).publish("same saved copy", client=client)
    assert recovery["status"] == "accepted"
    if result["request_id"]:
        assert recovery["request_id"] == result["request_id"]
    assert len(s.list_project_parent_composition_revisions(p, "pending", limit=200)["items"]) == 2


@pytest.mark.parametrize("damage", ["empty", "child", "parent"])
def test_source_bound_fidelity_rejects_matching_wrong_canonical_and_closure(daemon_fixture, damage):
    s, p, client, capability = daemon_fixture
    result = duplicate_timeline(p, "fixture-source", slug="wrong", client=client)
    assert_published(result)
    rows = [json.loads(r) for r in journal.journal_path(p, "wrong").read_text().splitlines()]
    intent = next(
        e for row in rows for e in row["evidence"] if e.get("kind") == "publish-intent-v1"
    )
    accepted = next(
        e["result"] for row in rows for e in row["evidence"] if e.get("kind") == "publish-result-v1"
    )
    exact = saved_publish._exact(
        saved_publish._workspace(client), intent["body"], result["new_head"]
    )
    canonical = copy.deepcopy(accepted["canonical_document"])
    if damage == "empty":
        canonical.update(placements=[], shots={})
        exact["immutable_closure"]["parent"]["payload"]["occurrences"] = []
        exact["immutable_closure"].update(shots={}, internal_timelines={})
    elif damage == "parent":
        canonical["parent"]["config"]["opaque"] = "forged"
        exact["immutable_closure"]["parent"]["payload"]["config"]["opaque"] = "forged"
    else:
        sid = next(iter(canonical["shots"]))
        canonical["shots"][sid]["payload"]["name"] = "forged"
        next(iter(exact["immutable_closure"]["shots"].values()))["payload"]["name"] = "forged"
    # Identical faulty compiler projections cannot serve as proof against the source.
    with pytest.raises(Exception, match="duplicate fidelity mismatch"):
        verify_duplicate(saved_publish._workspace(client), intent["body"], canonical, exact)


def test_saved_acceptance_cannot_use_empty_bootstrap_as_no_change(daemon_fixture):
    s, p, client, capability = daemon_fixture
    result = duplicate_timeline(p, "fixture-source", slug="false-nochange", client=client)
    assert_published(result)
    rows = [
        json.loads(r) for r in journal.journal_path(p, "false-nochange").read_text().splitlines()
    ]
    intent = next(
        e for row in rows for e in row["evidence"] if e.get("kind") == "publish-intent-v1"
    )
    accepted = next(
        e["result"] for row in rows for e in row["evidence"] if e.get("kind") == "publish-result-v1"
    )
    workspace = saved_publish._workspace(client)
    bootstrap = saved_publish._exact(workspace, intent["body"], result["old_head"])
    forged = dict(
        accepted,
        status="no_change",
        canonical_document=bootstrap,
        document_digest=_digest(bootstrap),
    )
    # Both old compiler projections would be the same empty bootstrap. The
    # source-bound seam must instead require the three requested reserved outputs.
    with pytest.raises(Exception, match="duplicate fidelity mismatch"):
        saved_publish._verify_result(workspace, intent, forged)
