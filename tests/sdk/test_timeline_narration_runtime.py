"""Opt-in joined C producer / D consumer checks on disposable Runtime stores.

ASTRID_NARRATION_RUNTIME_TESTS names the admitted Runtime's existing offline
fixture directory. No copied producer implementation or live provider is used.
"""
# ruff: noqa: E402
import copy
import os
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

fixture_dir = os.environ.get("ASTRID_NARRATION_RUNTIME_TESTS")
if not fixture_dir:
    pytest.skip("requires an explicitly selected narration Runtime fixture source", allow_module_level=True)
sys.path.append(str(Path(fixture_dir)))

from runtime_protocol.errors import ConflictError
from runtime_protocol.narration import narration_projection, validate_artifacts
from test_narration_commit import managed_take
from test_selected_media_commit import snapshot
from test_shot_composition_runtime import _publication, _service
from test_timeline_accept import IDENTITY, SCHEMA, wire
from test_timeline_saved_publish import synthetic_scene_answers  # noqa: F401

from astrid.sdk.contracts import DomainResult
from astrid.sdk.timeline import narration
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline_script import read_composition_script

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")


def valid(value, name):
    import json

    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    opcall = json.loads((Path(__file__).parents[2] / "schemas/change-contract/opcall.schema.json").read_text())
    registry = Registry().with_resource("https://astrid.local/schemas/change-contract/opcall.schema.json", Resource.from_contents(opcall))
    Draft202012Validator({"$ref": "#/$defs/" + name, "$defs": SCHEMA["$defs"]}, registry=registry).validate(value)


class PortProxy:
    def __init__(self, port, **overrides):
        self.port = port
        self.__dict__.update(overrides)

    def __getattr__(self, name):
        return getattr(self.port, name)


@pytest.fixture
def runtime(tmp_path):
    service, project = _service(tmp_path)
    service.publish_parent_composition(project, "main", _publication(project), idempotency_key="initial")
    try:
        yield service, project
    finally:
        service.close()


def script(refs):
    return dict(op="timeline.apply-script", select=None, args=dict(spec=dict(version=1, remove=[], lines=[dict(
        occurrence_id="occurrence-1", clip_id="voice", segment="line-1", text="Hello world!", take=copy.deepcopy(refs))])))


def commit(service, project, body):
    # This exercises the real request-bound port/acceptor. It intentionally does
    # not register a mismatched old generated contract as an installed provider.
    return RuntimeCommitService().commit(body, service._request_commit_port(body, IDENTITY))


def test_actual_request_candidate_acceptance_projection_reload_and_script_read(runtime):
    s, p = runtime
    refs, manifest, words = managed_take(s, p)
    body = wire(p)
    body["change"]["commands"] = [script(refs)]
    valid(body, "CommitRequest")
    before = snapshot(s)
    result = commit(s, p, body)
    assert result["status"] == "accepted", result
    closure = s._commit_revision_closure(p, "main", result["accepted_revision_id"])
    projection = narration_projection(closure)
    assert result["runtime_receipt"]["narration_state"]["projection"] == projection
    assert projection["lines"][0]["take"] == refs
    assert snapshot(s) != before
    assert s.store.conn.execute("select count(*) from shot_text_bindings").fetchone()[0] == 0
    class Timelines:
        def inspect(self, project, timeline, **options):
            return DomainResult.success(s.inspect_timeline(project, timeline, options))
    class Transport:
        def get_project_timeline_revision(self, project, timeline, revision):
            return s.get_project_timeline_revision(project, timeline, revision)
    read = read_composition_script(Timelines(), Transport(), p, "main")
    assert read.ok, read
    assert read.data["occurrences"][0]["text"] == "Hello world!\n"
    assert read.data["occurrences"][0]["bindings"] == []
    assert read.data["occurrences"][0]["provenance"] == "pinned_internal_timeline"
    assert commit(s, p, body) == result
    valid(result, "CommitResult")


def test_current_c_structural_vectors_are_consumed_without_a_second_tokenizer(runtime):
    s, p = runtime
    refs, manifest, words = managed_take(s, p)
    validate_artifacts(refs, manifest, words)
    narration.validate_take(manifest["text"], s._request_commit_port(
        dict(wire(p), change={"commands": [script(refs)]}), IDENTITY).narration_take(refs))
    for value in (.1, True, float("nan"), float("inf")):
        bad = copy.deepcopy(words)
        bad["words"][1]["start_s"] = value
        with pytest.raises(Exception):
            validate_artifacts(refs, manifest, bad)


def test_actual_acceptance_dependency_refusal_rolls_back_head_children_and_journal(runtime):
    s, p = runtime
    refs, manifest, words = managed_take(s, p)
    body = wire(p)
    body["change"]["commands"] = [script(refs)]
    port = s._request_commit_port(body, IDENTITY)
    accept = port.accept
    after_external_change = []
    def corrupt_after_preparation(prepared):
        s.store.conn.execute("UPDATE managed_output_lifecycle SET state='reclaimed'")
        after_external_change.append(snapshot(s))
        return accept(prepared)
    port = PortProxy(port, accept=corrupt_after_preparation)
    with pytest.raises(ConflictError):
        RuntimeCommitService().commit(body, port)
    assert snapshot(s) == after_external_change[0]
    assert s.head(p, "main")["revision_id"] == "parent-1"
    assert s.lookup_request(p, "main", body["request_id"]) is None


def test_actual_lost_response_replay_before_any_dependency_consultation(runtime):
    s, p = runtime
    refs, manifest, words = managed_take(s, p)
    body = wire(p)
    body["change"]["commands"] = [script(refs)]
    port = s._request_commit_port(body, IDENTITY)
    accept = port.accept
    def lose(prepared):
        accept(prepared)
        raise TimeoutError("durable acceptance then crash")
    port = PortProxy(port, accept=lose)
    with pytest.raises(TimeoutError):
        RuntimeCommitService().commit(body, port)
    stored = s.lookup_request(p, "main", body["request_id"])["result"]
    port.narration_take = lambda *_: pytest.fail("dependency read before replay")
    assert RuntimeCommitService().commit(body, port) == stored


def test_offline_capability_preparation_reads_actual_managed_bytes_then_commits(runtime, monkeypatch):
    from astrid.sdk.timeline.checkout import Checkout
    s, p = runtime
    refs, manifest, words = managed_take(s, p)
    class Client:
        def get_managed_output(self, association):
            return s.managed_output(association)
        def get_object(self, object_id):
            return {"data": s.cas.path_for(object_id[7:]).read_bytes()}
    invokes = []
    def offline(capability, **kwargs):
        assert capability == "generation.generate_speech"
        assert kwargs["inputs"]["voice"] == "fixture-voice" and kwargs["inputs"]["rate"] == "+0%"
        invokes.append(kwargs)
        return SimpleNamespace(ok=True, outputs={"managed_outputs": [dict(ref, output_port=port) for port, ref in refs.items()]})
    monkeypatch.setattr("astrid.sdk.invocation.invoke", offline)
    body = wire(p)
    base = RuntimeCommitService._load_revision(s._request_commit_port(body, IDENTITY), body, "parent-1")
    raw = dict(version=1, remove=[], voice="fixture-voice", lines=[dict(occurrence_id="occurrence-1",
        clip_id="voice", segment="line-1", text="Hello world!")])
    command, verified = narration.prepare_script(Checkout(base), raw, client=Client(), preparation_id=body["request_id"])
    assert len(invokes) == 1 and len(verified) == 1
    body["change"]["commands"] = [command]
    assert commit(s, p, body)["status"] == "accepted"


def test_actual_timing_edit_inverse_and_empty_projection_restore_without_generation(runtime, monkeypatch):
    from astrid.sdk.timeline.checkout import Checkout
    from astrid.sdk.timeline.inverse import inverse_command
    s, p = runtime
    refs, manifest, words = managed_take(s, p)
    body = wire(p)
    body["change"]["commands"] = [script(refs)]
    first = commit(s, p, body)
    assert first["status"] == "accepted"
    body = wire(p, key="timing-edit")
    body["base_revision_id"] = first["accepted_revision_id"]
    body["base_publication_id"] = first["accepted_publication_id"]
    base = RuntimeCommitService._load_revision(s._request_commit_port(body, IDENTITY), body, body["base_revision_id"])
    timing = script(refs)
    timing["args"]["spec"]["lines"][0]["gap_after_s"] = .8
    body["change"]["commands"] = [timing]
    second = commit(s, p, body)
    assert second["status"] == "accepted", second
    inverse = inverse_command(second["change"]["commands"], base, second["canonical_document"],
        second["accepted_publication_id"], consequences=second["change"]["consequences"])
    undo = wire(p, key="undo")
    undo.update(base_revision_id=second["accepted_revision_id"], base_publication_id=second["accepted_publication_id"])
    undo["change"]["commands"] = [inverse]
    monkeypatch.setattr("astrid.sdk.invocation.invoke", lambda *_a, **_k: pytest.fail("undo generated speech"))
    restored = commit(s, p, undo)
    assert restored["status"] == "accepted", restored
    assert narration.line_clips(Checkout(base))["occurrence:occurrence-1/clip:voice"].data == narration.line_clips(
        Checkout(restored["canonical_document"]))["occurrence:occurrence-1/clip:voice"].data
    delete = wire(p, key="remove-all")
    delete.update(base_revision_id=restored["accepted_revision_id"], base_publication_id=restored["accepted_publication_id"])
    delete["change"]["commands"] = [dict(op="timeline.apply-script", select=None,
        args=dict(spec=dict(version=1, lines=[], remove=["occurrence:occurrence-1/clip:voice"])))]
    empty = commit(s, p, delete)
    assert empty["status"] == "accepted", empty
    assert empty["runtime_receipt"]["narration_state"]["projection"] == {"version": 1, "lines": []}
