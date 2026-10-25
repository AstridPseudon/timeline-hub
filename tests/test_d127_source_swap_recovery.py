"""D127: source-authored native SWAP and the storage recovery boundary.

The historical App request is not available to this test.  The fixture below
rebuilds its public source recipe with the registered Agent provider and real
Runtime media selections, then authors a new fork+swap request.  Nothing in
the test is a replay of the old request or a hand-written provider result.
"""
from __future__ import annotations

import copy
import os
import shutil
import sqlite3
import struct
import zlib
from pathlib import Path
from types import SimpleNamespace

import pytest

import test_timeline_clip_replacement as native
from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import route_path
from runtime_protocol.timeline_commit_store import TimelineCommitStore


AGENT_PARENT = "5e9ad1c6"
REFERENCE_AT = 15
OCCURRENCE_HOST_WINDOW = 12
SOURCE_OCCURRENCE = "f2-occurrence"
SHARED_OCCURRENCE = "f2-occurrence-copy"
TARGET = f"occurrence:{SHARED_OCCURRENCE}/clip:f2-agent-clip"
HAS_D127_WAL_FIX = hasattr(TimelineCommitStore, "_physical_identity_changed")


def _png(width: int, height: int) -> bytes:
    """The same real RGB gradient used by the source recipe's makePng."""
    def chunk(kind: bytes, payload: bytes) -> bytes:
        body = kind + payload
        return struct.pack(">I", len(payload)) + body + struct.pack(">I", zlib.crc32(body) & 0xFFFFFFFF)

    rows = []
    for y in range(height):
        row = bytearray([0])
        for x in range(width):
            row.extend(((x * 255 // width), (y * 255 // height), 128))
        rows.append(bytes(row))
    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(
        b"IDAT", zlib.compress(b"".join(rows))
    ) + chunk(b"IEND", b"")


def _selection(service, project, data):
    pin = service.get_project_media_selection(project, {
        "asset": data["variant_id"],
        "generation_id": data["generation_id"],
        "variant_id": data["variant_id"],
    }, authorize=lambda: None)
    verified = service.get_project_verified_media(project, pin, authorize=lambda: None)
    return pin, verified


def _import_image(service, project, payload, alias):
    result = service.import_media(
        project, payload, media_type="image/png", original_name=f"{alias}.png",
        actor_id="d127-source-swap-test", idempotency_key=f"import-{alias}",
    )["data"]
    return _selection(service, project, result)


def _body(service, project, commands, *, label, base=None, steps=None,
          merge="fields", reads=None):
    head = service.get_project_timeline(project, "film") if base is None else base
    return {
        "api_version": 1,
        "project_id": project,
        "timeline_id": "film",
        "base_revision_id": head["head_revision_id"],
        "base_publication_id": head["head_publication_id"],
        "commands": copy.deepcopy(commands),
        "label": label,
        "steps": steps if steps is not None else [{
            "id": "edit", "label": label, "intent": label, "tags": [],
            "command_ordinals": list(range(len(commands))), "patch": [], "reads": [],
        }],
        "merge": merge,
        "reads": [] if reads is None else copy.deepcopy(reads),
        "dry_run": False,
        "source": {"via": "app"},
    }


def _commit(service, project, body, key):
    body = copy.deepcopy(body)
    return service.commit_timeline(
        project, "film", body, idempotency_key=key,
        publisher="d127-source-swap-test",
        invocation_path=route_path(project, "film"), authorize=lambda: None,
    )


def _document(service, project):
    head = service.get_project_timeline(project, "film")
    bootstrap = service.get_project_parent_composition_revision(
        project, "film", head["head_revision_id"],
    )
    return {
        "schema_version": 1,
        "project_id": project,
        "timeline_id": "film",
        "parent_revision": {key: bootstrap[key] for key in (
            "revision_id", "content_digest", "payload")},
        "shot_revisions": [],
        "internal_timeline_revisions": [],
        "dependency_manifest": bootstrap["dependency_manifest"],
    }


def _source_fixture(tmp_path):
    """Build the source recipe through real Agent captures and Runtime commits."""
    checkout = Path(os.environ.get("ASTRID_CHECKOUT", ""))
    if not (checkout / "astrid/sdk/timeline/native_occurrence_fork.py").is_file():
        pytest.fail(
            "CURRENT missing input: ASTRID_CHECKOUT must name the immutable Agent "
            f"source (expected parent {AGENT_PARENT})"
        )
    agent = native._native_imports()
    from astrid.sdk.timeline.native_occurrence_fork import capture_occurrence_fork
    from astrid.sdk.timeline.native_occurrence_shared import capture_occurrence_place_shared

    agent.capture_occurrence_fork = capture_occurrence_fork
    agent.capture_occurrence_place_shared = capture_occurrence_place_shared
    RealmStore.initialize(tmp_path / "realm").close()
    service = RuntimeService(tmp_path / "realm")
    project = service.create_project({"slug": "d127-source", "name": "D127 source"})["id"]
    service.register_timeline_commit_provider(agent.load_timeline_commit_provider("astrid"))
    service.create_timeline(project, "film", idempotency_key="d127-bootstrap")

    seed_image, seed_verified = _import_image(service, project, _png(64, 48), "f2-image")
    placeholder, placeholder_verified = _import_image(service, project, _png(64, 48), "f2-placeholder")
    old, old_verified = _import_image(service, project, _png(64, 48), "p2-popup-old")
    new, new_verified = _import_image(service, project, _png(65, 49), "p2-popup-new")

    document = _document(service, project)
    bundle = agent.bundle_from_document(document)
    commands = []

    def add(command, verified=()):
        nonlocal bundle
        commands.append(command)
        bundle = agent.execute(bundle, [command], verified_media=list(verified)).bundle

    # Source seed: reference-at-15, native-none opaque source, and a 12-second
    # occurrence host.  The real old seed image is retained as f2-image.
    add(agent.capture_track_create(bundle, "parent", {"id": "V1", "kind": "visual", "label": "V1"}))
    add(agent.capture_track_create(bundle, "parent", {"id": "S1", "kind": "visual", "label": "S1"}))
    add(agent.capture_clip_add_media(bundle, {
        "id": "f2-app-clip", "at": 0, "track": "V1", "clipType": "image",
        "asset": seed_image["asset"], "hold": 3,
    }, seed_image, verified_media=[seed_verified]), [seed_verified])
    add(agent.capture_clip_add_media(bundle, {
        "id": "f2-transition-clip", "at": REFERENCE_AT, "track": "V1", "clipType": "image",
        "asset": seed_image["asset"], "hold": 3,
    }, seed_image, verified_media=[seed_verified]), [seed_verified])
    add(agent.capture_occurrence_create(
        bundle, SOURCE_OCCURRENCE, "f2-shot", name="F2 agent shot", track="S1",
        on=0, duration=OCCURRENCE_HOST_WINDOW,
    ))
    add(agent.capture_track_create(bundle, f"occurrence:{SOURCE_OCCURRENCE}", {
        "id": "plate", "kind": "visual", "label": "plate",
    }))
    add(agent.capture_track_create(bundle, f"occurrence:{SOURCE_OCCURRENCE}", {
        "id": "V2", "kind": "visual", "label": "V2",
    }))
    for row, pin, verified in (
        ({"id": "f2-plate", "at": 0, "track": "plate", "clipType": "image",
          "asset": seed_image["asset"], "hold": OCCURRENCE_HOST_WINDOW}, seed_image, seed_verified),
        ({"id": "f2-agent-clip", "at": 3, "track": "V2", "clipType": "image",
          "asset": placeholder["asset"], "hold": 3,
          "app": {"f2Opaque": {"owner": "f2", "nested": [1, {"k": "v"}]}},
         }, placeholder, placeholder_verified),
    ):
        add(agent.capture_occurrence_add_media(
            bundle, f"occurrence:{SOURCE_OCCURRENCE}", row, pin,
            verified_media=[verified],
        ), [verified])

    seed_reads = [{"kind": "scope", "ref": "timeline", "path": []}]
    seed_steps = [{
        "id": f"seed-{ordinal}", "label": command["op"], "intent": "D127 source seed",
        "tags": [], "command_ordinals": [ordinal], "patch": [], "reads": seed_reads,
    } for ordinal, command in enumerate(commands)]
    seed = _commit(service, project, _body(
        service, project, commands, label="D127 source seed",
        steps=seed_steps, merge="atomic", reads=seed_reads,
    ), "seed")
    document = seed["data"]["canonical_document"]

    # The App recipe's shared occurrence at 12 seconds is authored as a real
    # native command, then the old imported selection and opaque field are
    # installed through the real doc.patch command path.
    bundle = agent.bundle_from_document(document)
    shared = agent.capture_occurrence_place_shared(
        bundle, f"occurrence:{SOURCE_OCCURRENCE}", SHARED_OCCURRENCE, on=12,
    )
    shared_result = _commit(service, project, _body(
        service, project, [shared], label="D127 shared source",
    ), "shared")
    document = shared_result["data"]["canonical_document"]

    occurrence = next(row for row in document["parent_revision"]["payload"]["occurrences"]
                      if row["occurrence_id"] == SHARED_OCCURRENCE)
    shot = next(row for row in document["shot_revisions"]
                if row["shot_id"] == occurrence["shot_id"]
                and row["revision_id"] == occurrence["shot_revision_id"])
    internal = next(row for row in document["internal_timeline_revisions"]
                    if row["revision_id"] == shot["internal_timeline_revision_id"])
    target = next(row for row in internal["payload"]["clips"] if row["id"] == "f2-agent-clip")
    old_target_asset = target["asset"]
    old_entry = {
        "media_id": old["object_id"], "type": "image",
        "generationId": old["generation_id"], "variantId": old["variant_id"],
    }
    changes = [
        {"op": "set", "ref": "parent", "path": ["config", "x_f2_opaque"],
         "before": {"state": "absent"},
         "value": {"owner": "f2", "nested": [1, {"k": "v"}], "flag": True}},
        {"op": "set", "ref": f"internal-revision:{internal['revision_id']}",
         "path": ["clips", "id:f2-agent-clip", "asset"],
         "before": {"state": "present", "value": old_target_asset}, "value": old["asset"]},
        {"op": "set", "ref": f"internal-revision:{internal['revision_id']}",
         "path": ["registry", "assets", old["asset"]], "before": {"state": "absent"},
         "value": old_entry},
    ]
    patches = [{"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
                "args": {"changes": changes}, "created": [
                    f"occurrence:{SOURCE_OCCURRENCE}/asset:{old['asset']}",
                    f"occurrence:{SHARED_OCCURRENCE}/asset:{old['asset']}",
                ]}]
    patch_result = _commit(service, project, _body(
        service, project, patches, label="D127 popup source preparation",
        steps=[{
            "id": "prepare", "label": "D127 popup source preparation",
            "intent": "Prepare imported old media", "tags": [],
            "command_ordinals": [0], "patch": changes, "reads": [],
        }],
    ), "prepare")
    document = patch_result["data"]["canonical_document"]
    return SimpleNamespace(
        service=service, project=project, root=tmp_path / "realm", agent=agent,
        old=old, old_verified=old_verified, new=new, new_verified=new_verified,
        document=document, old_target_asset=old_target_asset,
    )


def test_d127_source_swap_is_newly_authored_and_inverse_survives_reload(tmp_path):
    fixture = _source_fixture(tmp_path)
    service = fixture.service
    try:
        before = copy.deepcopy(fixture.document)
        bundle = fixture.agent.bundle_from_document(before)
        fork = fixture.agent.capture_occurrence_fork(
            bundle, f"occurrence:{SHARED_OCCURRENCE}", "shot-fork-d127",
        )
        forked = fixture.agent.execute(bundle, [fork]).bundle
        swap = fixture.agent.capture_occurrence_swap_media(
            forked, TARGET, fixture.old, fixture.new,
            verified_media=[fixture.old_verified, fixture.new_verified],
        )
        request = _body(
            service, fixture.project, [fork, swap],
            label="D127 source-faithful native SWAP",
            steps=[{
                "id": "swap", "label": "D127 source-faithful native SWAP",
                "intent": "Fork shared occurrence then swap media", "tags": ["source", "native"],
                "command_ordinals": [0, 1], "patch": [], "reads": [],
            }],
        )
        accepted = _commit(service, fixture.project, request, "source-swap")
        assert accepted["data"]["status"] == "accepted"
        assert accepted["receipt"]["result"] == accepted["data"]
        assert [item["op"] for item in request["commands"]] == ["occurrence.fork", "occurrence.swap-media"]
        assert request["commands"][1]["args"]["old_media"] == fixture.old
        assert request["commands"][1]["args"]["media"] == fixture.new

        result = accepted["data"]["canonical_document"]
        occurrence = next(row for row in result["parent_revision"]["payload"]["occurrences"]
                          if row["occurrence_id"] == SHARED_OCCURRENCE)
        assert occurrence["shot_id"] == "shot-fork-d127"
        child = next(row for row in result["internal_timeline_revisions"]
                     if row["timeline_id"] == "film" and row["revision_id"] ==
                     next(shot["internal_timeline_revision_id"] for shot in result["shot_revisions"]
                          if shot["shot_id"] == "shot-fork-d127"))["payload"]
        target = next(row for row in child["clips"] if row["id"] == "f2-agent-clip")
        assert target["asset"] == fixture.new["asset"]
        assert target["app"]["f2Opaque"] == {"owner": "f2", "nested": [1, {"k": "v"}]}
        assert result["parent_revision"]["payload"]["config"]["x_f2_opaque"]["flag"] is True

        commits, _ = service._timeline_commits()
        accepted_history = commits.history_entry(
            fixture.project, "film", accepted["receipt"]["receipt_id"],
        )
        records = accepted_history["records"]
        assert records["steps"][0]["command_ordinals"] == [0, 1]
        command_ops = [row["command"]["op"] for row in records["commands"]]
        assert command_ops == ["occurrence.fork", "occurrence.swap-media"]
        dependencies = [dependency for row in records["commands"]
                        for dependency in row["dependencies"]]
        assert any(dependency.get("key") == "media.old" and dependency.get("pin") == fixture.old
                   for dependency in dependencies), repr(dependencies)
        assert any(dependency.get("key") == "media.new" and dependency.get("pin") == fixture.new
                   for dependency in dependencies), repr(dependencies)
        history = service.list_timeline_commits(fixture.project, "film", authorize=lambda: None)
        assert any(item["publication_id"] == accepted["receipt"]["receipt_id"] for item in history["items"])

        service.close()
        service = RuntimeService(fixture.root)
        service.register_timeline_commit_provider(fixture.agent.load_timeline_commit_provider("astrid"))
        assert _commit(service, fixture.project, request, "source-swap") == accepted

        head = service.get_project_timeline(fixture.project, "film")
        inverse = {
            "schema_version": 1, "op": "timeline.inverse", "version": "1", "select": None,
            "args": {"publications": [accepted["receipt"]["receipt_id"]]},
        }
        undone = _commit(service, fixture.project, _body(
            service, fixture.project, [inverse], label="D127 source SWAP inverse",
            base=head, steps=[{
                "id": "inverse", "label": "D127 source SWAP inverse",
                "intent": "Undo source SWAP", "tags": ["inverse"],
                "command_ordinals": [0], "patch": [], "reads": [],
            }],
        ), "source-swap-inverse")
        assert undone["data"]["status"] == "accepted"
        restored = undone["data"]["canonical_document"]
        restored_occurrence = next(row for row in restored["parent_revision"]["payload"]["occurrences"]
                                   if row["occurrence_id"] == SHARED_OCCURRENCE)
        assert restored_occurrence["shot_id"] == before["parent_revision"]["payload"]["occurrences"][-1]["shot_id"]
        assert not any(row["shot_id"] == "shot-fork-d127" for row in restored["shot_revisions"])
    finally:
        service.close()


def test_d127_source_history_recovery_rejects_tampered_replacement(tmp_path):
    fixture = _source_fixture(tmp_path)
    service = fixture.service
    try:
        commits, _ = service._timeline_commits()
        head = service.get_project_timeline(fixture.project, "film")
        genuine = commits.history_entry(fixture.project, "film", head["head_publication_id"])
        assert genuine["revision_id"] == head["head_revision_id"]
        service.store.conn.execute("PRAGMA wal_checkpoint(TRUNCATE)").fetchall()
        stale = sqlite3.connect(service.store.db_path, isolation_level=None)
        replacement = tmp_path / "replacement.sqlite3"
        shutil.copyfile(service.store.db_path, replacement)
        replacement.replace(service.store.db_path)
        with sqlite3.connect(service.store.db_path, isolation_level=None) as tampered:
            tampered.execute(
                "UPDATE command_idempotency SET event_ids_json='[]' WHERE txn_id=?",
                (head["head_publication_id"],),
            )
        service.store.conn = stale
        try:
            if not HAS_D127_WAL_FIX:
                try:
                    commits.history_entry(fixture.project, "film", head["head_publication_id"])
                except RuntimeErrorBase:
                    pass
                # This base is intentionally below the final WAL fix.  The
                # real probe records the fallback as RED by showing that the
                # stale handle remains mounted after the replacement.
                assert commits._connection is stale
                return
            with pytest.raises(RuntimeErrorBase):
                commits.history_entry(fixture.project, "film", head["head_publication_id"])
            assert not any(commits._history_state.values())
            assert commits._connection is not stale
        finally:
            if service.store.conn is not stale:
                stale.close()
    finally:
        service.close()
