"""Fresh history authentication walks a dependency graph, not recursive paths."""
from __future__ import annotations

from collections import Counter

import pytest
import test_timeline_commit_integration as real

from runtime_protocol.errors import RuntimeErrorBase
from runtime_protocol.service import RuntimeService
from runtime_protocol.timeline_commit_port import RequestCommitPort

film = real.film
agent = real.agent
editing = real.editing
pytestmark = pytest.mark.integration


def inverse_chain(editing, count):
    change = {"op": "set", "ref": "parent", "path": ["meta"],
              "before": {"state": "absent"}, "value": {"org.example.note": {"text": "Note"}}}
    command = {"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
               "args": {"changes": [change]}}
    accepted = []
    for ordinal in range(count):
        if accepted:
            command = real.inverse(accepted[-1]["receipt"]["receipt_id"])
        body = editing.body([command])
        if not accepted:
            body["steps"][0]["patch"] = [change]
        accepted.append(editing.commit(body, f"assembly-{ordinal}"))
    return accepted


def note_curve(editing, count):
    change = {"op": "set", "ref": "parent", "path": ["meta"],
              "before": {"state": "absent"}, "value": {"org.example.note": {}}}
    command = {"schema_version": 1, "op": "doc.patch", "version": "1", "select": None,
               "args": {"changes": [change]}}
    body = editing.body([command])
    body["steps"][0]["patch"] = [change]
    seed = editing.commit(body, "notes-seed")
    base = {"revision_id": seed["data"]["accepted_revision_id"],
            "publication_id": seed["receipt"]["receipt_id"]}
    accepted = []
    for ordinal in range(count):
        change = {"op": "set", "ref": "parent", "path": ["meta", "org.example.note", f"note-{ordinal}"],
                  "before": {"state": "absent"}, "value": f"Note {ordinal}"}
        command = {**command, "args": {"changes": [change]}}
        body = editing.body([command], base=base)
        body["steps"][0]["patch"] = [change]
        accepted.append(editing.commit(body, f"note-{ordinal}"))
    return accepted


@pytest.mark.parametrize("count", [2, 4, 8])
def test_provider_history_lookup_authenticates_each_graph_node_once(editing, monkeypatch, count):
    accepted = note_curve(editing, count)
    commits, _ = editing.service._timeline_commits()
    calls = Counter()
    verify = commits._verify_accepted_record

    def counted(row, edge, **kwargs):
        calls[edge["publication_id"]] += 1
        return verify(row, edge, **kwargs)

    monkeypatch.setattr(commits, "_verify_accepted_record", counted)
    target = accepted[-1]["receipt"]["receipt_id"]
    # Exercise the supported provider port inside real commit execution. Stop
    # before acceptance so only the history read contributes to the bound.
    observed = []
    provider_type = type(editing.service._timeline_commit_provider)

    class ReadComplete(RuntimeErrorBase):
        pass

    def read_only(self, context, port):
        assert isinstance(port, RequestCommitPort)
        calls.clear()
        entry = port.history_entry(target)
        observed.append(entry)
        assert set(calls) == {value["receipt"]["receipt_id"] for value in accepted}
        assert max(calls.values()) == 1
        raise ReadComplete("history read complete")

    monkeypatch.setattr(provider_type, "commit", read_only)
    with pytest.raises(ReadComplete):
        editing.commit(editing.body([real.inverse(target)]), "assembly-read")
    assert observed[0]["receipt"] == accepted[-1]["receipt"]


@pytest.mark.parametrize("mutation", ["ancestor", "parent", "event", "metadata", "file", "rewind", "fork", "aba"])
def test_dependency_graph_is_fresh_between_provider_lookups(editing, monkeypatch, mutation):
    accepted = inverse_chain(editing, 4)
    commits, _ = editing.service._timeline_commits()
    conn = editing.service.store.conn
    target = accepted[-1]["receipt"]["receipt_id"]
    project, timeline = editing.project, editing.timeline
    provider_type = type(editing.service._timeline_commit_provider)
    reached = []

    def read_then_mutate(self, context, port):
        assert port.history_entry(target)["receipt"] == accepted[-1]["receipt"]
        publication = accepted[0]["receipt"]["receipt_id"]
        if mutation in {"ancestor", "parent"}:
            column = "revision_id" if mutation == "ancestor" else "previous_revision_id"
            conn.execute(f"UPDATE timeline_commit_history SET {column}=? WHERE publication_id=?",
                         (accepted[-1 if mutation == "ancestor" else 0]["data"]["accepted_revision_id"], publication))
        elif mutation == "event":
            conn.execute("UPDATE timeline_events SET payload_json='{}' WHERE id=?",
                         (accepted[0]["receipt"]["event_ids"][-1],))
        elif mutation in {"metadata", "aba"}:
            head = commits.head(project, timeline)
            conn.execute("UPDATE timeline_commit_history SET metadata_json='{}' WHERE publication_id=?",
                         (publication,))
            if mutation == "aba":
                conn.execute("UPDATE parent_composition_heads SET publication_id=? WHERE project_id=? AND timeline_id=?",
                             (publication, project, timeline))
                conn.execute("UPDATE parent_composition_heads SET publication_id=? WHERE project_id=? AND timeline_id=?",
                             (head["publication_id"], project, timeline))
        elif mutation == "file":
            media = accepted[0]["data"]["canonical_document"]["dependency_manifest"]["media"][0]["media_id"]
            path = editing.service.cas.path_for(media.removeprefix("sha256:"))
            path.write_bytes(b"corrupt physical media")
        else:
            conn.execute("UPDATE timeline_commit_history SET previous_publication_id=? WHERE publication_id=?",
                         (publication if mutation == "rewind" else target, target))
        before = real.rows(editing.service)
        with pytest.raises(RuntimeErrorBase):
            port.history_entry(target)
        assert real.rows(editing.service) == before
        reached.append(True)
        raise ReadComplete("history read complete")

    class ReadComplete(RuntimeErrorBase):
        pass

    monkeypatch.setattr(provider_type, "commit", read_then_mutate)
    with pytest.raises(ReadComplete):
        editing.commit(editing.body([real.inverse(target)]), "mutated-read")
    assert reached == [True]
    with pytest.raises(RuntimeErrorBase):
        commits.history_entry(project, timeline, target)


@pytest.mark.parametrize("attack", ["queued-row", "indirect-cycle"])
def test_unverified_dependencies_cannot_escape_the_graph(editing, monkeypatch, attack):
    accepted = inverse_chain(editing, 2)
    commits, _ = editing.service._timeline_commits()
    target = accepted[-1]["receipt"]["receipt_id"]
    seed = accepted[0]["receipt"]["receipt_id"]
    original = commits._inverse_stage_history

    def attacked(project, timeline, records, **kwargs):
        history = original(project, timeline, records, **kwargs)
        if history and attack == "queued-row":
            # The dependency has been read but not yet authenticated. Its live
            # row must still match when the worklist reaches it.
            editing.service.store.conn.execute(
                "UPDATE timeline_commit_history SET metadata_json='{}' WHERE publication_id=?", (seed,))
        elif not history and attack == "indirect-cycle":
            commits.history_entry(project, timeline, target)
        return history

    monkeypatch.setattr(commits, "_inverse_stage_history", attacked)
    with commits.verification_scope():
        with pytest.raises(RuntimeErrorBase):
            commits.history_entry(editing.project, editing.timeline, target)
        assert commits._verification.current["traversal"] is None
        assert not commits._verification.current["active"]
        assert not commits._verification.current["verified"]


def test_reopened_runtime_rechecks_ancestors_before_exact_retry(editing, monkeypatch):
    accepted = inverse_chain(editing, 2)
    seed, undone = accepted
    base = {"revision_id": seed["data"]["accepted_revision_id"],
            "publication_id": seed["receipt"]["receipt_id"]}
    body = editing.body([real.inverse(seed["receipt"]["receipt_id"])], base=base)
    root = editing.service.store.root
    editing.service.close()
    runtime = RuntimeService(root)
    try:
        runtime.register_timeline_commit_provider(editing.agent.provider())
        reopened = real.Editing(runtime, editing.film, editing.agent)

        def forbidden(*args):
            raise AssertionError("exact retry executed provider")

        monkeypatch.setattr(type(runtime._timeline_commit_provider), "commit", forbidden)
        assert reopened.commit(body, "assembly-1") == undone
        conn = runtime.store.conn
        assert conn is not None
        conn.execute("UPDATE timeline_commit_history SET metadata_json='{}' WHERE publication_id=?",
                     (seed["receipt"]["receipt_id"],))
        before = real.rows(runtime)
        with pytest.raises(RuntimeErrorBase):
            reopened.commit(body, "assembly-1")
        assert real.rows(runtime) == before
    finally:
        runtime.close()
