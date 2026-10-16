import copy
import hashlib

import pytest

from astrid.sdk.contracts import DomainResult
from astrid.sdk.timeline.narration import digest
from astrid.sdk.timeline_script import read_composition_script


def projected_script_fixture():
    """Wire data at the real reader boundary; no current/head reads exist."""
    take = {port: {"association_id": port, "object_id": "sha256:" + "a" * 64}
            for port in ("speech", "speech_words", "speech_manifest")}
    clips = [dict(id=cid, at=at, app=dict(astrid=dict(text=text, segment=cid, take=take)))
             for cid, at, text in (("z", 0, "Last."), ("a", 5, "First."))]
    payload = dict(clips=clips)
    rows = [dict(occurrence_id="o", shot_id="s", shot_revision_id="sr", internal_timeline_id="child",
                 internal_revision_id="ir", clip_id=c["id"], segment=c["id"], take=take,
                 line_digest="sha256:" + digest(c)) for c in reversed(clips)]
    state = dict(parent_revision_id="origin-parent", projection=dict(version=1, lines=rows))
    state["digest"] = "sha256:" + digest(state["projection"])
    record = dict(project_id="p", timeline_id="child", revision_id="ir", payload=payload,
                  content_digest="sha256:" + digest(payload), narration_state=state)
    placed = dict(occurrence_id="o", shot_id="s", shot_revision_id="sr", internal_timeline_revision_id="ir",
                  internal_timeline_digest=record["content_digest"], text_bindings=[binding("stale")])
    return record, placed


def read_projected_fixture(record, placed, *, legacy=False):
    class Timeline:
        def inspect(self, *args, **kwargs):
            return DomainResult.success(dict(project_id="p", timeline_id="child", revision_id="later-parent",
                snapshot_digest="snapshot", selected=[dict(role="target", occurrence=placed)], next_cursor=None))

    class Transport:
        def get_project_timeline_revision(self, *args):
            assert args == ("p", "child", "ir")
            return record

        def get_object(self, ref):
            assert legacy, "present narration must never consult legacy text"
            assert ref == binding("stale")["media_id"]
            return {"data": b"stale"}

    return read_composition_script(Timeline(), Transport(), "p", "child", revision_id="later-parent")


def test_present_projection_uses_exact_payload_in_projection_order():
    record, placed = projected_script_fixture()
    before = copy.deepcopy(record)
    result = read_projected_fixture(record, placed)
    assert result.ok, result
    row = result.data["occurrences"][0]
    assert row["text"] == "First. Last.\n"  # projection order, not clip time
    assert [line["clip_id"] for line in row["lines"]] == ["a", "z"]
    assert row["bindings"] == [] and row["provenance"] == "pinned_internal_timeline"
    assert record == before


def test_full_projection_scopes_multiple_occurrences_and_child_revisions():
    first, first_placed = projected_script_fixture()
    second, second_placed = copy.deepcopy((first, first_placed))
    second["revision_id"] = second_placed["internal_timeline_revision_id"] = "ir-2"
    second_placed.update(occurrence_id="o-2", shot_id="s-2", shot_revision_id="sr-2")
    for clip in second["payload"]["clips"]:
        clip["app"]["astrid"]["text"] = "Other " + clip["app"]["astrid"]["text"]
    second["content_digest"] = second_placed["internal_timeline_digest"] = "sha256:" + digest(second["payload"])
    rows = second["narration_state"]["projection"]["lines"]
    for line in rows:
        line.update(occurrence_id="o-2", shot_id="s-2", shot_revision_id="sr-2", internal_revision_id="ir-2")
        line["line_digest"] = "sha256:" + digest(next(c for c in second["payload"]["clips"] if c["id"] == line["clip_id"]))
    parent = dict(first["narration_state"]["projection"]["lines"][0])
    for key in ("occurrence_id", "shot_id", "shot_revision_id", "internal_timeline_id", "internal_revision_id"):
        parent[key] = None
    first["narration_state"]["projection"]["lines"] = [parent, *first["narration_state"]["projection"]["lines"], *rows]
    first["narration_state"]["digest"] = "sha256:" + digest(first["narration_state"]["projection"])
    second["narration_state"] = copy.deepcopy(first["narration_state"])

    class Timeline:
        def inspect(self, *args, **kwargs):
            return DomainResult.success(dict(revision_id="later-parent", snapshot_digest="snapshot",
                selected=[dict(role="target", occurrence=p) for p in (second_placed, first_placed)], next_cursor=None))

    calls = []

    class Transport:
        def get_project_timeline_revision(self, project, timeline, revision):
            calls.append((project, timeline, revision))
            return {"ir": first, "ir-2": second}[revision]

        def get_object(self, *_):
            pytest.fail("projection must override stale text")

    result = read_composition_script(Timeline(), Transport(), "p", "child")
    assert result.ok, result
    assert {r["occurrence_id"]: r["text"] for r in result.data["occurrences"]} == {
        "o": "First. Last.\n", "o-2": "Other First. Other Last.\n"}
    assert calls == [("p", "child", "ir-2"), ("p", "child", "ir")]


@pytest.mark.parametrize("scope", ["globally-empty", "different-occurrence", "different-child"])
def test_present_projection_without_selected_rows_is_explicit_empty(scope):
    record, placed = projected_script_fixture()
    projection = record["narration_state"]["projection"]
    if scope == "globally-empty":
        projection["lines"] = []
    else:
        for line in projection["lines"]:
            line["occurrence_id"] = "another"
            if scope == "different-child":
                line.update(shot_id="other-shot", shot_revision_id="other-sr", internal_revision_id="other-ir")
    record["narration_state"]["digest"] = "sha256:" + digest(projection)
    result = read_projected_fixture(record, placed)
    assert result.ok, result
    row = result.data["occurrences"][0]
    assert row["status"] == "empty" and row["text"] == "" and row["lines"] == []
    assert row["bindings"] == []


def test_genuine_state_absence_preserves_legacy_text_and_old_take_paths():
    record, placed = projected_script_fixture()
    del record["narration_state"]
    old = read_projected_fixture(record, placed)
    assert old.ok and old.data["occurrences"][0]["text"] == "Last. First.\n"
    record["payload"]["clips"] = []
    record["content_digest"] = placed["internal_timeline_digest"] = "sha256:" + digest(record["payload"])
    legacy = read_projected_fixture(record, placed, legacy=True)
    assert legacy.ok and legacy.data["occurrences"][0]["text"] == "stale"


@pytest.mark.parametrize("fault", [
    "null-state", "missing-parent", "null-parent", "empty-parent", "extra-state", "digest",
    "projection-null", "version", "boolean-version", "lines-null", "line-null", "missing-pin",
    "occurrence-null", "shot_id", "shot_revision_id", "internal_timeline_id", "internal_revision_id",
    "duplicate", "unordered", "clip_id", "segment", "take", "line_digest", "payload-digest",
])
def test_present_corrupt_narration_refuses_without_legacy_fallback(fault):
    record, placed = projected_script_fixture()
    state = record["narration_state"]
    projection = state["projection"]
    line = projection["lines"][0]
    if fault == "null-state":
        record["narration_state"] = None
    elif fault == "missing-parent":
        del state["parent_revision_id"]
    elif fault in ("null-parent", "empty-parent"):
        state["parent_revision_id"] = None if fault == "null-parent" else ""
    elif fault == "extra-state":
        state["extra"] = True
    elif fault == "projection-null":
        state["projection"] = None
    elif fault in ("version", "boolean-version"):
        projection["version"] = 2 if fault == "version" else True
    elif fault == "lines-null":
        projection["lines"] = None
    elif fault == "line-null":
        projection["lines"][0] = None
    elif fault == "missing-pin":
        del line["internal_revision_id"]
    elif fault == "occurrence-null":
        line["occurrence_id"] = None
    elif fault == "duplicate":
        projection["lines"].append(copy.deepcopy(line))
    elif fault == "unordered":
        projection["lines"].reverse()
    elif fault == "take":
        line["take"] = {**line["take"], "speech": {"association_id": "different", "object_id": "sha256:" + "b" * 64}}
    elif fault == "payload-digest":
        record["payload"]["clips"][0]["at"] = 99
    elif fault != "digest":
        line[fault] = "wrong" if fault != "line_digest" else "sha256:" + "b" * 64
    state["digest"] = "sha256:" + digest(state["projection"])
    if fault == "digest":
        state["digest"] = "sha256:" + "0" * 64
    result = read_projected_fixture(record, placed)
    assert not result.ok and result.error.code == "integrity_error", result


def test_missing_pinned_internal_revision_returns_typed_transport_error():
    from astrid.sdk.workspace_client import WorkspaceClientError

    class Timelines:
        def inspect(self, *args, **kwargs):
            return DomainResult.success(dict(revision_id="parent", snapshot_digest="pinned", selected=[
                dict(role="target", occurrence=dict(occurrence_id="o", internal_timeline_revision_id="ir",
                                                    text_bindings=[]))], next_cursor=None))

    class Transport:
        def get_project_timeline_revision(self, *args):
            raise WorkspaceClientError(404, "not_found", "missing pinned internal", {})

    result = read_composition_script(Timelines(), Transport(), "p", "t")
    assert not result.ok and result.error.code == "not_found"


def binding(text, head=1):
    raw = text.encode()
    return {"binding_id": "binding", "kind": "voiceover_script", "head": head,
            "media_id": "sha256:" + hashlib.sha256(raw).hexdigest(),
            "content_hash": "sha256:" + hashlib.sha256(raw).hexdigest(),
            "byte_size": len(raw), "event_stream_id": "binding:shot.text_binding"}


def test_pinned_script_order_missing_empty_and_no_latest_read():
    old, empty = binding("Pinned wording"), binding("")
    def placed(oid, start, bindings):
        return {"role": "target", "occurrence": {"occurrence_id": oid, "shot_id": "s",
            "shot_revision_id": "shot-old", "start": [start, 1], "duration": [2, 1],
            "name": oid, "text_bindings": bindings}}
    class Timeline:
        calls = []
        def inspect(self, *args, **kwargs):
            self.calls.append(kwargs)
            return DomainResult.success({"revision_id": "parent-old", "snapshot_digest": "snapshot",
                "selected": [placed("later", 3, []), placed("empty", 2, [empty]), placed("first", 0, [old])],
                "next_cursor": None})
    class Transport:
        def get_object(self, ref):
            return {"data": b"Pinned wording" if ref == old["media_id"] else b""}
        def list_project_shot_text_bindings(self, *a, **kw):
            raise AssertionError("must never read latest or unplaced shots")
    timeline = Timeline()
    result = read_composition_script(timeline, Transport(), "p", "tl", revision_id="parent-old")
    assert result.ok
    assert [r["occurrence_id"] for r in result.data["occurrences"]] == ["first", "empty", "later"]
    assert [r["status"] for r in result.data["occurrences"]] == ["present", "empty", "missing"]
    assert result.data["occurrences"][0]["text"] == "Pinned wording"
    assert timeline.calls[0]["revision_id"] == "parent-old"


def test_script_pagination_pins_first_head_and_verifies_exact_bytes():
    pin = binding("old")
    class Timeline:
        def inspect(self, *args, **kw):
            if kw["cursor"]:
                assert kw["revision_id"] == "parent"
                rows, cursor = [], None
            else:
                rows, cursor = [{"role": "target", "occurrence": {"occurrence_id": "o", "text_bindings": [pin]}}], "page2"
            return DomainResult.success({"revision_id": "parent", "snapshot_digest": "d", "selected": rows, "next_cursor": cursor})
    class Transport:
        def get_object(self, ref):
            return {"data": b"changed"}
    result = read_composition_script(Timeline(), Transport(), "p", "tl")
    assert not result.ok and result.error.code == "integrity_error"


def test_script_paginates_from_first_revision_and_snapshot_without_reading_latest():
    first, second = binding("first"), binding("second", head=2)
    calls = []
    class Timeline:
        def inspect(self, project, ref, **kwargs):
            calls.append(kwargs.copy())
            if kwargs.get("cursor"):
                return DomainResult.success({
                    "revision_id": "parent-7", "snapshot_digest": "snapshot-7",
                    "selected": [{"role": "target", "occurrence": {"ordinal": 1, "occurrence_id": "second",
                        "shot_id": "s2", "shot_revision_id": "s2-r1", "start": [3, 1], "duration": [1, 1],
                        "name": "Second", "text_bindings": [second]}}], "next_cursor": None,
                })
            return DomainResult.success({
                "revision_id": "parent-7", "snapshot_digest": "snapshot-7",
                "selected": [{"role": "target", "occurrence": {"ordinal": 0, "occurrence_id": "first",
                    "shot_id": "s1", "shot_revision_id": "s1-r4", "start": [1, 1], "duration": [1, 1],
                    "name": "First", "text_bindings": [first]}}], "next_cursor": "page-2",
            })
    class Transport:
        def __init__(self): self.reads = []
        def get_object(self, ref):
            self.reads.append(ref)
            return {"data": b"first" if ref == first["media_id"] else b"second"}
        def list_project_shot_text_bindings(self, *args, **kwargs):
            raise AssertionError("the reader must use the selected revision's pins")
    transport = Transport()
    result = read_composition_script(Timeline(), transport, "p", "tl")
    assert result.ok
    assert result.data["revision_id"] == "parent-7"
    assert result.data["snapshot_digest"] == "snapshot-7"
    assert [row["text"] for row in result.data["occurrences"]] == ["first", "second"]
    assert calls[0]["revision_id"] is None
    assert calls[1]["revision_id"] == "parent-7"
    assert calls[1]["cursor"] == "page-2"
    assert transport.reads == [first["media_id"], second["media_id"]]


def test_script_rejects_changed_snapshot_and_malformed_descriptors():
    class ChangedSnapshot:
        def inspect(self, *args, **kwargs):
            return DomainResult.success({"revision_id": "parent", "snapshot_digest": "", "selected": [], "next_cursor": None})
    class Transport:
        def get_object(self, ref): raise AssertionError("malformed descriptors must fail before object reads")
    empty_snapshot = read_composition_script(ChangedSnapshot(), Transport(), "p", "tl")
    assert not empty_snapshot.ok and empty_snapshot.error.code == "protocol_error"

    class Malformed:
        def inspect(self, *args, **kwargs):
            return DomainResult.success({"revision_id": "parent", "snapshot_digest": "s", "selected": [
                {"role": "target", "occurrence": {"occurrence_id": "o", "text_bindings": [None]}}
            ], "next_cursor": None})
    malformed = read_composition_script(Malformed(), Transport(), "p", "tl")
    assert not malformed.ok and malformed.error.code == "protocol_error"

    class ChangingSnapshot:
        def inspect(self, *args, **kwargs):
            digest = "snapshot-a" if not kwargs.get("cursor") else "snapshot-b"
            return DomainResult.success({"revision_id": "parent", "snapshot_digest": digest,
                                         "selected": [], "next_cursor": "next" if not kwargs.get("cursor") else None})
    changed = read_composition_script(ChangingSnapshot(), Transport(), "p", "tl")
    assert not changed.ok and changed.error.code == "integrity_error"

    invalid_kind = read_composition_script(Malformed(), Transport(), "p", "tl", kind=None)
    assert not invalid_kind.ok and invalid_kind.error.code == "validation_error"

    class MissingBindingKind:
        def inspect(self, *args, **kwargs):
            return DomainResult.success({"revision_id": "parent", "snapshot_digest": "s", "selected": [
                {"role": "target", "occurrence": {"occurrence_id": "o", "text_bindings": [{"binding_id": "b"}]}}
            ], "next_cursor": None})
    invalid_descriptor = read_composition_script(MissingBindingKind(), Transport(), "p", "tl")
    assert not invalid_descriptor.ok and invalid_descriptor.error.code == "protocol_error"


def test_timeline_script_cli_forwards_revision_occurrence_and_kind(monkeypatch):
    from types import SimpleNamespace

    import astrid.packs.timeline.cli as cli

    calls = []
    client = SimpleNamespace(timelines=SimpleNamespace(script=lambda *args, **kwargs: calls.append((args, kwargs)) or "result"))
    monkeypatch.setattr(cli, "print_result", lambda result, as_json: 0)
    parser = cli.build_parser(client)
    parsed = parser.parse_args(["script", "timeline", "--project", "project", "--revision", "parent-9",
                                "--occurrence", "occ-2", "--kind", "voiceover_script"])
    assert parsed.handler(parsed) == 0
    assert calls == [(("project", "timeline"), {"revision_id": "parent-9", "occurrence": "occ-2", "kind": "voiceover_script"})]


def test_runtime_pin_flow_returns_old_script_after_binding_rebind(tmp_path):
    service_module = pytest.importorskip("runtime_protocol.service")
    store_module = pytest.importorskip("runtime_protocol.store")
    realm = tmp_path / "realm"
    store_module.RealmStore.initialize(realm).close()
    service = service_module.RuntimeService(realm)
    try:
        project = service.create_project({"slug": "narration", "name": "Narration"}, idempotency_key="project")
        project_id = project["id"]
        service.create_timeline(project_id, "main", idempotency_key="timeline")

        def publication(parent_id, expected_head, shot_revision, internal_revision, *, text_bindings=None):
            return {
                "project_id": project_id, "timeline_id": "main", "expected_head": expected_head,
                "parent_revision_id": parent_id,
                "internal_timeline_revisions": [{"timeline_id": "main", "revision_id": internal_revision,
                    "payload": {"tracks": [], "clips": [], "effects": [], "audio": [], "layout": {}, "registry": {}, "assets": []}}],
                "shot_revisions": [{"shot_id": "shot-1", "revision_id": shot_revision,
                    "internal_timeline_revision_id": internal_revision,
                    "payload": {"metadata": {"title": "Opening"}, "items": [], "pools": [],
                        "selected_variants": {}, "provenance": {}, "generation_inputs": {},
                        "audio_bindings": [], "text_bindings": text_bindings or []}}],
                "parent_composition": {"config": {}, "registry": {}, "clips": [], "occurrences": [{
                    "occurrence_id": "opening", "shot_id": "shot-1", "shot_revision_id": shot_revision,
                    "placement": {"start_ms": 0}, "duration_ms": 1000, "source_offset": 0,
                    "speed": 1, "track": "voice", "transform": {}, "gain": 1,
                    "mute": False, "provenance": {},
                }]},
            }

        service.publish_parent_composition(project_id, "main", publication(
            "parent-1", None, "shot-1-r1", "internal-r1"), idempotency_key="publish-no-script")
        pin = service.set_project_shot_text_binding(project_id, {
            "shot_id": "shot-1", "kind": "voiceover_script", "text": "Pinned before rebind.", "expected_head": 0,
        }, idempotency_key="register-script")["data"]
        service.publish_parent_composition(project_id, "main", publication(
            "parent-2", "parent-1", "shot-1-r2", "internal-r2", text_bindings=[pin]),
            idempotency_key="publish-pin")

        class Timelines:
            def inspect(self, project_ref, timeline_ref, **options):
                return DomainResult.success(service.inspect_timeline(project_ref, timeline_ref, options))

        class Transport:
            def get_object(self, object_id):
                return {"data": service.cas.path_for(object_id.removeprefix("sha256:")).read_bytes()}

        service.set_project_shot_text_binding(project_id, {
            "binding_id": pin["binding_id"], "text": "New mutable head.", "expected_head": pin["head"],
        }, idempotency_key="rebind-script")
        result = read_composition_script(Timelines(), Transport(), project_id, "main")
        assert result.ok
        assert result.data["revision_id"] == "parent-2"
        assert result.data["occurrences"][0]["text"] == "Pinned before rebind."
        assert result.data["occurrences"][0]["bindings"][0]["head"] == pin["head"]
    finally:
        service.close()
