from __future__ import annotations

import copy
import json

import pytest

from astrid.packs.timeline.cli import build_parser
from astrid.sdk.contracts import DomainResult
from astrid.sdk.remote import RemoteTimelines


def _pending_occurrence_swap():
    from tests.editing_conformance.test_recipe_occurrence_media import inputs

    _, old, new, _ = inputs()
    command = {
        "schema_version": 1,
        "op": "occurrence.swap-media",
        "version": "1",
        "select": "occurrence:occ-a/clip:clip-a",
        "args": {"old_media": old, "media": new},
        "intent": {"ownership": "occurrence"},
        "opaque": {"preserve": ["source-window", None]},
    }
    return command, old, new


def _pending_session(command, *, flight=True, fail_flush=False):
    from astrid.sdk.timeline.sync import TimelineSession

    class Outbox:
        def __init__(self, state):
            self.state = state

        class _Lock:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        def locked(self):
            return self._Lock()

        def write(self, state):
            self.state = copy.deepcopy(state)

    class Session:
        def __init__(self):
            self.project_id, self.timeline_id = "project-1", "main"
            self.state = {
                "base": {"revision_id": "parent-1", "publication_id": "publication-1"},
                "pending": [copy.deepcopy(command)],
                "flight": ({"path": "/v1/projects/project-1/timelines/main/commit",
                             "body": '{"opaque":"body"}', "key": "original-key",
                             "count": 1, "fence": "fence-1"} if flight else None),
            }
            self.outbox = Outbox(self.state)
            self.flush_calls = []

        def _state(self):
            return self.state

        def flush(self, *, idempotency_key):
            self.flush_calls.append((idempotency_key, copy.deepcopy(self.state["pending"])))
            if fail_flush:
                raise ConnectionError("response lost after acceptance")
            data = {"status": "accepted"}
            receipt = {
                "receipt_id": "publication-2", "command_kind": "timeline.commit",
                "idempotency_key": "original-key", "request_hash": "hash",
                "project_id": "project-1", "project_seq": [1, 1],
                "event_ids": ["event-1"], "result": data, "created_at": "now",
            }
            return {"data": data, "receipt": receipt}

    return TimelineSession, Session()


def test_pending_unrelated_or_ambiguous_swap_refuses_without_flush(monkeypatch):
    command, old, new = _pending_occurrence_swap()
    TimelineSession, session = _pending_session(command)
    before = copy.deepcopy(session.state)
    monkeypatch.setattr(TimelineSession, "open", lambda *args, **kwargs: session)

    result = RemoteTimelines(object()).replace_parent_media(
        "project-1", "main", occurrence_id="other-occ", clip_id="other-clip",
        source_object_id=new["object_id"], expected_head="parent-1",
        expected_publication="publication-1", old_media=old, media=new,
        idempotency_key="other-key",
    )

    assert not result.ok and "pending native replacement" in result.error.message
    assert session.flush_calls == [] and session.state == before

    session.state["pending"].append(copy.deepcopy(command))
    before = copy.deepcopy(session.state)
    result = RemoteTimelines(object()).replace_parent_media(
        "project-1", "main", occurrence_id="occ-a", clip_id="clip-a",
        source_object_id=new["object_id"], expected_head="parent-1",
        expected_publication="publication-1", old_media=old, media=new,
        idempotency_key="original-key",
    )
    assert not result.ok and session.flush_calls == [] and session.state == before


@pytest.mark.parametrize("change", ["source", "selection", "owner", "head", "publication"])
def test_pending_swap_identity_controls_refuse_without_post(monkeypatch, change):
    command, old, new = _pending_occurrence_swap()
    TimelineSession, session = _pending_session(command)
    before = copy.deepcopy(session.state)
    monkeypatch.setattr(TimelineSession, "open", lambda *args, **kwargs: session)
    kwargs = {
        "occurrence_id": "occ-a", "clip_id": "clip-a", "source_object_id": new["object_id"],
        "expected_head": "parent-1", "expected_publication": "publication-1",
        "old_media": old, "media": new, "idempotency_key": "original-key",
    }
    if change == "source":
        kwargs["source_object_id"] = old["object_id"]
    elif change == "selection":
        kwargs["media"] = {**new, "catalog_digest": old["catalog_digest"]}
    elif change == "owner":
        kwargs["occurrence_id"] = None
    elif change == "head":
        kwargs["expected_head"] = "later-head"
    else:
        kwargs["expected_publication"] = "later-publication"

    result = RemoteTimelines(object()).replace_parent_media("project-1", "main", **kwargs)
    assert not result.ok and session.flush_calls == [] and session.state == before


def test_exact_pending_swap_retry_survives_restart_and_keeps_opaque_body(monkeypatch):
    command, old, new = _pending_occurrence_swap()
    TimelineSession, first = _pending_session(command, fail_flush=True)
    restored = _pending_session(command)[1]
    sessions = iter((first, restored))
    monkeypatch.setattr(TimelineSession, "open", lambda *args, **kwargs: next(sessions))
    transport = object()

    failed = RemoteTimelines(transport).replace_parent_media(
        "project-1", "main", occurrence_id="occ-a", clip_id="clip-a",
        source_object_id=new["object_id"], expected_head="parent-1",
        expected_publication="publication-1", old_media=old, media=new,
        idempotency_key="original-key",
    )
    assert not failed.ok
    assert first.flush_calls == [("original-key", [command])]

    retried = RemoteTimelines(transport).replace_parent_media(
        "project-1", "main", occurrence_id="occ-a", clip_id="clip-a",
        source_object_id=new["object_id"], expected_head="parent-1",
        expected_publication="publication-1", old_media=old, media=new,
    )
    assert retried.ok and retried.idempotency_key == "original-key"
    assert restored.flush_calls == [(None, [command])]


@pytest.mark.parametrize("kind", ["bool", "list", "str", "number", "nullmix"])
def test_pending_swap_rejects_non_mapping_selections_without_flush(monkeypatch, kind):
    command, _, new = _pending_occurrence_swap()
    TimelineSession, session = _pending_session(command)
    before = copy.deepcopy(session.state)
    outbox_before = copy.deepcopy(session.outbox.state)
    monkeypatch.setattr(TimelineSession, "open", lambda *args, **kwargs: session)
    invalid = {
        "bool": (True, False),
        "list": ([], []),
        "str": ("bad", "bad"),
        "number": (7, 7),
        "nullmix": (None, new),
    }[kind]

    result = RemoteTimelines(object()).replace_parent_media(
        "project-1", "main", occurrence_id="occ-a", clip_id="clip-a",
        source_object_id=new["object_id"], expected_head="parent-1",
        expected_publication="publication-1", old_media=invalid[0], media=invalid[1],
        idempotency_key="original-key",
    )

    assert (not result.ok and session.flush_calls == [] and session.state == before
            and session.outbox.state == outbox_before)


@pytest.mark.parametrize("supplied", [False, True], ids=["none-pair", "exact-mapping-pair"])
def test_pending_swap_accepts_only_omitted_or_exact_selections(monkeypatch, supplied):
    command, old, new = _pending_occurrence_swap()
    TimelineSession, session = _pending_session(command)
    monkeypatch.setattr(TimelineSession, "open", lambda *args, **kwargs: session)
    selections = {"old_media": old, "media": new} if supplied else {}

    result = RemoteTimelines(object()).replace_parent_media(
        "project-1", "main", occurrence_id="occ-a", clip_id="clip-a",
        source_object_id=new["object_id"], expected_head="parent-1",
        expected_publication="publication-1", idempotency_key="original-key",
        **selections,
    )

    assert result.ok, result.error
    assert session.flush_calls == [("original-key", [command])]


def test_remote_timelines_replace_clip_is_typed_410() -> None:
    class Transport:
        def replace_timeline_clip(self, *args, **kwargs):
            raise AssertionError("retired route must not reach the generated document mutation")

    result = RemoteTimelines(Transport()).replace_clip(
        "project-1", "timeline-1", clip_id="clip-1",
        source_object_id="sha256:" + "b" * 64, expected_version=4,
        idempotency_key="replace-4",
    )
    assert not result.ok
    assert result.error.code == "retired_route"
    assert result.error.details["status"] == 410


def test_timeline_cli_has_no_replace_clip_command() -> None:
    client = type("Client", (), {})()
    client.timelines = type("Timelines", (), {})()
    parser = build_parser(client)
    choices = parser._subparsers._group_actions[0].choices
    assert "replace-clip" not in choices
    assert "save" not in choices
    assert "retime-clip" not in choices


def test_remote_parent_media_replacement_publishes_exact_closure_once() -> None:
    """Keep the original raw-media success contract visible while native data is incomplete."""
    from tests.timeline.test_authoring_bundle import NEW, _closure, _digest

    parent, shots, internals = _closure(shared=False)
    internal = internals[0]
    internal["payload"]["registry"]["assets"]["new-picture"] = {
        "media_id": NEW,
        "type": "image",
    }
    internal["content_digest"] = _digest(internal["payload"])
    shot = shots[0]
    parent["content_digest"] = _digest(parent["payload"])

    class Transport:
        def __init__(self):
            self.published = []
            self._last_handshake = {'realm_id': 'realm-1', 'actor_id': 'media-editor'}

        def list_timelines(self, project, *, cursor=None, limit=50):
            return ([{"project_id": project, "timeline_id": "main", "slug": "main"}], None)

        def get_timeline(self, timeline_id, *, project_id=None):
            raise AssertionError("canonical parent replacement must not read the legacy timeline document")

        def get_project_parent_composition_revision(self, project_id, timeline_id, revision):
            assert (project_id, timeline_id, revision) == ("project-1", "main", "parent-1")
            return parent

        def get_project_shot_revision(self, project_id, shot_id, revision):
            assert (project_id, shot_id, revision) == ("project-1", "shot-shared", "shot-rev-1")
            return shot

        def get_project_timeline_revision(self, project_id, timeline_id, revision):
            assert (project_id, timeline_id, revision) == ("project-1", "main", "internal-1")
            return internal

        def publish_parent_composition(self, project_id, timeline_id, publication, *, idempotency_key):
            self.published.append((project_id, timeline_id, publication, idempotency_key))
            return {"data": {"new_head": publication["parent_revision_id"]}, "receipt": None}

    transport = Transport()
    result = RemoteTimelines(transport).replace_parent_media(
        "project-1",
        "main",
        occurrence_id="occ-1",
        clip_id="picture-1",
        source_object_id=NEW,
        expected_head="parent-1",
        idempotency_key="parent-replace-1",
    )

    assert result.ok, result.error
    assert len(transport.published) == 1
    _project, _timeline, publication, key = transport.published[0]
    assert key == "parent-replace-1"
    child = publication["internal_timeline_revisions"][0]["payload"]
    selected = next(clip for clip in child["clips"] if clip["id"] == "picture-1")
    assert selected["asset"] == "new-picture"
    assert selected["at"] == 0 and selected["hold"] == 1
    assert publication["expected_head"] == "parent-1"


def test_parent_media_cli_forwards_exact_locator_and_head(capsys) -> None:
    class Timelines:
        def __init__(self):
            self.calls = []

        def replace_parent_media(self, *args, **kwargs):
            self.calls.append((args, kwargs))
            return DomainResult.success({"representation": "parent_composition"}, idempotency_key=kwargs["idempotency_key"])

    class Client:
        def __init__(self):
            self.timelines = Timelines()

    client = Client()
    parser = build_parser(client)
    parsed = parser.parse_args([
        "replace-parent-media", "--project", "project-1", "main",
        "--occurrence-id", "occ-1", "--clip-id", "picture-1",
        "--source-object-id", "sha256:" + "d" * 64,
        "--expected-head", "parent-1", "--idempotency-key", "parent-1",
    ])

    assert parsed.handler(parsed) == 0
    assert json.loads(capsys.readouterr().out)["data"] == {"representation": "parent_composition"}
    assert client.timelines.calls == [
        (("project-1", "main"), {
            "occurrence_id": "occ-1",
            "clip_id": "picture-1",
            "source_object_id": "sha256:" + "d" * 64,
            "expected_head": "parent-1",
            "idempotency_key": "parent-1",
        })
    ]


@pytest.mark.parametrize("occurrence_id", [None, "occ-a"], ids=["parent", "occurrence"])
def test_selected_parent_and_occurrence_replacement_preserve_accepted_wire(
        monkeypatch, occurrence_id) -> None:
    from astrid.sdk.timeline._command_state import State
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.sync import TimelineSession
    from tests.editing_conformance.test_recipe_occurrence_media import inputs

    document, old, new, _ = inputs()
    bundle = bundle_from_document(document)
    owner = "parent" if occurrence_id is None else "occurrence:" + occurrence_id
    State(bundle).registry(owner)["assets"]["picture"].update(
        generationId=old["generation_id"], variantId=old["variant_id"])
    select = owner + "/clip:clip-a"
    expected_op = "clip.swap-media" if occurrence_id is None else "occurrence.swap-media"
    key = "selected-" + str(occurrence_id)
    accepted = {
        "status": "accepted",
        "accepted_revision_id": "parent-2",
        "base_revision_id": "parent-1",
        "base_publication_id": "publication-1",
    }
    receipt = {
        "receipt_id": "publication-2", "command_kind": "timeline.commit",
        "idempotency_key": key, "request_hash": "hash",
        "project_id": "project-1", "project_seq": [1, 1],
        "event_ids": ["event-1"], "result": accepted, "created_at": "now",
    }
    opened = []

    class Transport:
        def list_timelines(self, project, *, cursor=None, limit=50):
            return ([{'project_id': project, 'timeline_id': 'main', 'slug': 'main'}], None)

        def get_project_media_selection(self, project, selector):
            return next(pin for pin in (old, new)
                        if all(pin[key] == selector[key]
                               for key in ('asset', 'generation_id', 'variant_id')))

        def get_project_verified_media(self, project, selection):
            return {'selection': selection, 'media_type': 'image/fixture', 'size': 123}

    class Outbox:
        def __init__(self):
            self.state = None

        class _Lock:
            def __enter__(self):
                return self

            def __exit__(self, *args):
                return False

        def locked(self):
            return self._Lock()

        def write(self, state):
            self.state = state

    class Session:
        def __init__(self):
            self.project_id, self.timeline_id = 'project-1', 'main'
            self.outbox = Outbox()
            self.state = {'base': {'revision_id': 'parent-1', 'publication_id': 'publication-1'},
                          'pending': [], 'flight': None}

        def _state(self):
            return self.state

        def _bundle(self, state):
            return bundle

        def flush(self, *, idempotency_key):
            data = {**accepted, 'commands': copy.deepcopy(self.state['pending'])}
            returned_receipt = {**receipt, 'idempotency_key': idempotency_key,
                                'result': data}
            self.flush_request = {'project': self.project_id, 'timeline': self.timeline_id,
                                  'key': idempotency_key, 'body': data}
            return {'data': data, 'receipt': returned_receipt}

    session = Session()
    monkeypatch.setattr(
        TimelineSession, 'open',
        lambda *args, **kwargs: (opened.append((args, kwargs)) or session),
    )

    transport = Transport()
    timelines = RemoteTimelines(transport)
    result = timelines.replace_parent_media(
        'project-1', 'main', occurrence_id=occurrence_id, clip_id='clip-a',
        source_object_id=new['object_id'], expected_head='parent-1',
        expected_publication='publication-1', old_media=old, media=new,
        idempotency_key=key,
    )

    assert result.ok, result.error
    assert opened[0][0][:2] == ('project-1', 'main')
    assert session.flush_request['project'] == 'project-1'
    assert session.flush_request['timeline'] == 'main'
    assert session.flush_request['key'] == key
    assert result.data['base_revision_id'] == 'parent-1'
    assert result.data['base_publication_id'] == 'publication-1'
    assert result.receipt.as_dict() == {**receipt, 'result': result.data}
    command = session.state['pending'][0]
    assert command['select'] == select
    assert command['op'] == expected_op
    assert command['args'] == {'old_media': old, 'media': new}
    assert command['intent'] == {'ownership': 'parent' if occurrence_id is None else 'occurrence'}
    target_read = next(read for read in command['reads'] if read['ref'] == select)
    original_row = State(bundle).entity(select)
    assert target_read['state']['value'] == original_row
    assert {field: original_row[field] for field in ('at', 'hold')} == {'at': 1, 'hold': 2}
    assert original_row['app'] == {'org.example': {'literal': 'clip-a', 'clear': None}}


def test_incomplete_or_mismatched_selection_never_falls_back_to_publication() -> None:
    from tests.editing_conformance.test_recipe_occurrence_media import inputs

    _, old, new, _ = inputs()

    class Transport:
        def __getattr__(self, name):
            raise AssertionError('invalid selected requests must not read or write Runtime')

    for values in ({'media': new}, {'old_media': old}, {'expected_publication': 'pub-1'},
                   {'old_media': old, 'media': new, 'expected_publication': 'pub-1',
                    'source_object_id': old['object_id']}):
        args = {'source_object_id': new['object_id'], **values}
        result = RemoteTimelines(Transport()).replace_parent_media(
            'project-1', 'main', occurrence_id=None, clip_id='picture-1',
            expected_head='parent-1', idempotency_key='invalid', **args,
        )
        assert not result.ok
        assert result.error.code == 'validation_error'
