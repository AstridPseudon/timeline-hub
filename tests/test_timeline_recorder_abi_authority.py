"""D61 recorder authority through real provider execution and Runtime history."""
from __future__ import annotations

import copy
import json

import pytest

from runtime_protocol.errors import ProtocolError, RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.store import RealmStore
from runtime_protocol.timeline_commit_port import route_path
from runtime_protocol.timeline_commit_validation import validate_commit_value
from runtime_protocol.util import canonical_json


@pytest.fixture
def recorder(tmp_path, astrid_importable):
    from astrid.sdk.timeline.capture import capture_track_create
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.native_occurrence_create import capture_occurrence_create
    from astrid.sdk.timeline.native_occurrence_fork import capture_occurrence_fork

    from runtime_protocol.timeline_commit_provider import load_timeline_commit_provider

    root = tmp_path / "recorder-realm"
    RealmStore.initialize(root).close()
    runtime = RuntimeService(root)
    project = runtime.create_project({"slug": "recorder", "name": "Recorder"})["id"]
    runtime.create_timeline(project, "film", idempotency_key="bootstrap")
    runtime.register_timeline_commit_provider(load_timeline_commit_provider("astrid"))
    runtime._timeline_commits()[0].bootstrap(project, "film", authorize=lambda: None)

    def document():
        commits = runtime._timeline_commits()[0]
        return commits.revision_closure(project, "film", commits.head(project, "film")["revision_id"])

    def request(command, modern):
        head = runtime._timeline_commits()[0].head(project, "film")
        body = {"api_version": 1, "project_id": project, "timeline_id": "film",
                "base_revision_id": head["revision_id"], "base_publication_id": head["publication_id"],
                "commands": [command], "source": {"via": "python"}, "dry_run": False}
        if modern:
            body.update(label="Fork", merge="fields", reads=[], steps=[{
                "id": "fork", "label": "Fork", "intent": "Fork occurrence", "tags": [],
                "command_ordinals": [0], "patch": [], "reads": []}])
        return body

    def publish(body, key):
        return runtime.commit_timeline(project, "film", body, idempotency_key=key, publisher="editor",
                                       invocation_path=route_path(project, "film"), authorize=lambda: None)

    try:
        track = capture_track_create(bundle_from_document(document()), "parent", {"id": "picture", "kind": "visual"})
        publish(request(track, False), "track")
        birth = capture_occurrence_create(bundle_from_document(document()), "opening", "source-shot",
                                          name="Opening", track="picture", on=0, duration=5)
        publish(request(birth, False), "birth")

        def fork(modern):
            command = capture_occurrence_fork(bundle_from_document(document()), "occurrence:opening", "fork-shot")
            return request(command, modern)

        yield runtime, project, fork, publish
    finally:
        runtime.close()


@pytest.mark.parametrize("abi", [1, 2])
def test_genuine_fork_recorder_authority_history_and_exact_retry(recorder, abi):
    runtime, project, fork, publish = recorder
    submitted = fork(abi == 2)
    result = publish(submitted, "fork")
    entry = runtime._timeline_commits()[0].history_entry(project, "film", result["receipt"]["receipt_id"])
    assert result["data"]["status"] == "accepted"
    assert publish(submitted, "fork") == result
    assert entry.get("recorder_abi", 1) == abi


@pytest.mark.parametrize("value", [1, 2, 0, 3, True, False, None, "2", 2.0, {}, []])
def test_caller_cannot_supply_recorder_authority(recorder, value):
    runtime, _project, fork, publish = recorder
    submitted = fork(True)
    submitted["recorder_abi"] = value
    before = tuple(runtime.store.conn.iterdump())
    with pytest.raises(RuntimeErrorBase):
        publish(submitted, "spoof")
    assert tuple(runtime.store.conn.iterdump()) == before


@pytest.mark.parametrize("value", [1, 0, 3, True, False, None, "2", 2.0, {}, []])
def test_history_authority_requires_accepted_event_commitment(recorder, value):
    runtime, project, fork, publish = recorder
    submitted = fork(True)
    result = publish(submitted, "fork")
    publication = result["receipt"]["receipt_id"]
    metadata = json.loads(runtime.store.conn.execute(
        "SELECT metadata_json FROM timeline_commit_history WHERE publication_id=?", (publication,),
    ).fetchone()[0])
    metadata["recorder_abi"] = copy.deepcopy(value)
    runtime.store.conn.execute("UPDATE timeline_commit_history SET metadata_json=? WHERE publication_id=?",
                               (canonical_json(metadata), publication))
    with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
        runtime._timeline_commits()[0].history_entry(project, "film", publication)


@pytest.mark.parametrize("full_rewrite", [False, True])
def test_v2_recorder_cannot_enter_acceptance_as_legacy_bindings(recorder, monkeypatch, full_rewrite):
    from runtime_protocol.timeline_commit_port import RequestCommitPort

    runtime, _project, fork, publish = recorder
    submitted = fork(True)
    accept = RequestCommitPort.accept
    reached = []

    def attack(port, prepared):
        value = copy.deepcopy(prepared)
        record = value["records"]["commands"][0]
        assert record["command"]["op"] == "occurrence.fork"
        assert any("physical_ref" in binding for binding in record["bindings"])
        legacy_keys = {"key", "ref", "policy", "dependencies"}
        record["bindings"] = [
            {key: item for key, item in binding.items() if key in legacy_keys}
            for binding in record["bindings"]
            if not full_rewrite or binding["key"] != "commit.effect"
        ]
        validate_commit_value(value, "PreparedCommit")
        reached.append(value)
        return accept(port, value)

    monkeypatch.setattr(RequestCommitPort, "accept", attack)
    before = tuple(runtime.store.conn.iterdump())
    with pytest.raises(RuntimeErrorBase):
        publish(submitted, "stripped")
    assert reached
    assert tuple(runtime.store.conn.iterdump()) == before


@pytest.mark.parametrize("private_capture", [False, True])
@pytest.mark.parametrize("omitted", ["fork.source", "native_bindings", "reads", "selections"])
def test_complete_native_coverage_cannot_be_inferred_from_remaining_physical_bindings(
        recorder, monkeypatch, private_capture, omitted):
    """Keep full physical effect coverage while removing native obligations.

    Raw semantic requests need not carry captured read/selection/binding claims.
    An original/landing carrier copied from the rewritten records cannot supply
    an independent expectation of what the native executor actually observed.
    """
    from runtime_protocol.timeline_commit_port import RequestCommitPort
    from runtime_protocol.timeline_commit_validation import digest

    runtime, _project, fork, publish = recorder
    submitted = fork(True)
    for key in ("resolved", "reads", "selections", "bindings", "expect", "authorship"):
        submitted["commands"][0].pop(key, None)
    validate_commit_value(submitted, "CommitRequest")
    accept = RequestCommitPort.accept
    reached = []

    def attack(port, prepared):
        value = copy.deepcopy(prepared)
        record = value["records"]["commands"][0]
        assert {binding["key"] for binding in record["bindings"] if binding["key"] != "commit.effect"} == {
            "collection.owner:collection.clips", "collection.owner:collection.tracks", "fork.source", "fork.owner"}
        if omitted in {"fork.source", "native_bindings"}:
            record["bindings"] = [binding for binding in record["bindings"]
                                  if binding["key"] != omitted and (
                                      omitted != "native_bindings" or binding["key"] == "commit.effect")]
            if omitted == "native_bindings":
                record["command"]["bindings"] = {}
        else:
            assert record[omitted]
            record[omitted] = []
            record["command"][omitted] = []
        assert record["bindings"] and all("physical_ref" in binding for binding in record["bindings"])
        effects = [binding for binding in record["bindings"] if binding["key"] == "commit.effect"]
        assert len(effects) == sum(
            int(change["before"]["state"] == "present") + int(change["op"] != "remove")
            for change in value["records"]["steps"][0]["patch"])
        validate_commit_value(value, "PreparedCommit")
        if private_capture:
            context = port._provider_context()
            head = value["expected_head"]
            assert head == {"revision_id": submitted["base_revision_id"],
                            "publication_id": submitted["base_publication_id"]}
            execution = {"evaluated_head": head, "records": copy.deepcopy(value["records"]), "commands": [{
                "boundary": {"base_revision_id": submitted["base_revision_id"],
                             "base_publication_id": submitted["base_publication_id"],
                             "evaluated_head": head, "step_id": value["records"]["steps"][0]["id"],
                             "command_ordinal": 0, "phase": "input"},
                "input": port.revision_closure(head["revision_id"]),
                "output": copy.deepcopy(value["canonical_document"])}]}
            port.capture_sequential_execution({
                "schema_version": 1, "context": context,
                "original": copy.deepcopy(execution), "landing": copy.deepcopy(execution),
                "replay_bindings": [], "prepared_digest": digest(value)})
        reached.append(value)
        return accept(port, value)

    monkeypatch.setattr(RequestCommitPort, "accept", attack)
    before = tuple(runtime.store.conn.iterdump())
    with pytest.raises(RuntimeErrorBase):
        publish(submitted, "missing-native-coverage")
    assert reached
    assert tuple(runtime.store.conn.iterdump()) == before


def test_supported_genuine_legacy_acceptance_remains_replayable_after_restart(recorder):
    runtime, project, _fork, _publish = recorder
    commits = runtime._timeline_commits()[0]
    head = commits.head(project, "film")
    before = commits.history(project, "film", head)
    recorded = [entry for entry in before["items"] if entry["intent"] == "recorded"]
    assert [entry["records"]["commands"][0]["command"]["op"] for entry in recorded] == [
        "track.create", "occurrence.create"]
    assert all(entry.get("recorder_abi", 1) == 1 for entry in recorded)
    root = runtime.store.root
    runtime.close()
    restarted = RuntimeService(root)
    try:
        assert restarted._timeline_commits()[0].history(project, "film", head) == before
    finally:
        restarted.close()


def test_legacy_history_cannot_acquire_injected_mode_two(recorder):
    runtime, project, _fork, _publish = recorder
    commits = runtime._timeline_commits()[0]
    publication = commits.head(project, "film")["publication_id"]
    entry = commits.history_entry(project, "film", publication)
    assert entry["records"]["commands"][0]["command"]["op"] == "occurrence.create"
    assert "recorder_abi" not in entry
    metadata = json.loads(runtime.store.conn.execute(
        "SELECT metadata_json FROM timeline_commit_history WHERE publication_id=?", (publication,),
    ).fetchone()[0])
    metadata["recorder_abi"] = 2
    runtime.store.conn.execute("UPDATE timeline_commit_history SET metadata_json=? WHERE publication_id=?",
                               (canonical_json(metadata), publication))
    with pytest.raises(ProtocolError, match="accepted commit record is corrupt"):
        commits.history_entry(project, "film", publication)
