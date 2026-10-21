from __future__ import annotations

import copy
import json

from astrid.packs.timeline.cli import build_parser
from astrid.sdk.contracts import DomainResult
from astrid.sdk.remote import RemoteTimelines


def _native_session(monkeypatch, bundle, verified, *, fail=False, pending=None, flight=None):
    from astrid.sdk.timeline.sync import TimelineSession

    class Outbox:
        def __init__(self, owner, state):
            self.owner = owner
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
            self.owner.state = self.state

    class Session:
        def __init__(self):
            self.project_id, self.timeline_id = 'project-1', 'main'
            self.state = {
                'base': {'revision_id': 'parent-1', 'publication_id': 'publication-1'},
                'pending': copy.deepcopy(pending or []), 'flight': copy.deepcopy(flight),
            }
            self.outbox = Outbox(self, self.state)
            self.flush_calls = []

        def _state(self):
            return self.state

        def _bundle(self, state):
            return bundle

        def commit(self, command, *, idempotency_key=None, verified_media=()):
            self.state['pending'] = [copy.deepcopy(command)]
            return self.flush(idempotency_key=idempotency_key)

        def flush(self, *, idempotency_key=None):
            self.flush_calls.append((idempotency_key, copy.deepcopy(self.state['pending'])))
            if fail:
                raise ConnectionError('response lost after acceptance')
            data = {
                'status': 'accepted', 'accepted_revision_id': 'parent-2',
                'base_revision_id': 'parent-1', 'base_publication_id': 'publication-1',
                'commands': copy.deepcopy(self.state['pending']),
            }
            receipt = {
                'receipt_id': 'publication-2', 'command_kind': 'timeline.commit',
                'idempotency_key': (idempotency_key or 'original-key'),
                'request_hash': 'hash', 'project_id': 'project-1',
                'project_seq': [1, 1], 'event_ids': ['event-1'],
                'result': data, 'created_at': 'now',
            }
            return {'data': data, 'receipt': receipt}

    session = Session()
    monkeypatch.setattr(TimelineSession, 'open', lambda *args, **kwargs: session)
    return session


def _media_transport(old, new):
    class Transport:
        def __init__(self):
            self.published = []

        def get_project_media_selection(self, _project, selector):
            return next(pin for pin in (old, new)
                        if all(pin[key] == selector[key]
                               for key in ('asset', 'generation_id', 'variant_id')))

        def get_project_verified_media(self, _project, selection):
            return {'selection': selection, 'media_type': 'image/fixture', 'size': 123}

        def list_generations(self, _project, *, cursor=None, limit=50):
            return ([{'generation_id': new['generation_id']}], None)

        def list_variants(self, _generation_id, *, cursor=None, limit=50):
            return ([{'variant_id': new['variant_id'], 'object_id': new['object_id']}], None)

        def publish_parent_composition(self, *args, **kwargs):
            self.published.append((args, kwargs))

    return Transport()


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
        "project-1", "main", occurrence_id="occ-1", clip_id="picture-1",
        source_object_id=NEW, expected_head="parent-1", idempotency_key="parent-replace-1",
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


def test_selected_parent_and_occurrence_replacement_use_the_native_outbox(monkeypatch) -> None:
    from astrid.sdk.timeline._command_state import State
    from astrid.sdk.timeline.commands import execute
    from astrid.sdk.timeline.commit import bundle_from_document
    from tests.editing_conformance.test_recipe_occurrence_media import inputs

    document, old, new, verified = inputs()
    bundle = bundle_from_document(document)
    State(bundle).entity('parent/asset:picture').update(
        generationId=old['generation_id'], variantId=old['variant_id'])
    State(bundle).entity('occurrence:occ-a/asset:picture').update(
        generationId=old['generation_id'], variantId=old['variant_id'])
    for occurrence, clip_id in ((None, 'clip-a'), ('occ-a', 'clip-a')):
        session = _native_session(monkeypatch, bundle, verified)
        transport = _media_transport(old, new)
        result = RemoteTimelines(transport).replace_parent_media(
            'project-1', 'main', occurrence_id=occurrence, clip_id=clip_id,
            source_object_id=new['object_id'], expected_head='parent-1',
            expected_publication='publication-1', old_media=old, media=new,
            idempotency_key='selected-' + str(occurrence),
        )
        assert result.ok, result.error
        assert transport.published == []
        assert session.flush_calls[0][0] == 'selected-' + str(occurrence)
        call = session.flush_calls[0][1][0]
        assert call['select'] == ('parent' if occurrence is None else 'occurrence:occ-a') + '/clip:' + clip_id
        assert call['op'] == ('clip.swap-media' if occurrence is None else 'occurrence.swap-media')
        assert call['args'] == {'old_media': old, 'media': new}
        changed = execute(bundle, [call], verified_media=verified).bundle
        owner = 'parent' if occurrence is None else 'occurrence:occ-a'
        assert State(changed).entity(owner + '/clip:' + clip_id)['asset'] == new['asset']


def test_native_media_retry_keeps_original_command_and_key_after_lost_ack(monkeypatch) -> None:
    from astrid.sdk.timeline.commit import bundle_from_document
    from tests.editing_conformance.test_recipe_occurrence_media import inputs

    document, old, new, verified = inputs()
    bundle = bundle_from_document(document)
    bundle['shots'][bundle['placements'][0]['shot_id']]['internal_timeline']['registry']['assets']['picture'].update(
        generationId=old['generation_id'], variantId=old['variant_id'])
    first = _native_session(monkeypatch, bundle, verified, fail=True)
    transport = _media_transport(old, new)
    failed = RemoteTimelines(transport).replace_parent_media(
        'project-1', 'main', occurrence_id='occ-a', clip_id='clip-a',
        source_object_id=new['object_id'], expected_head='parent-1',
        expected_publication='publication-1', old_media=old, media=new,
        idempotency_key='original-key',
    )
    assert not failed.ok
    assert first.flush_calls[0][0] == 'original-key'
    pending = first.state['pending']
    restored = _native_session(monkeypatch, bundle, verified, pending=pending,
                               flight={'key': 'original-key'})
    retried = RemoteTimelines(transport).replace_parent_media(
        'project-1', 'main', occurrence_id='occ-a', clip_id='clip-a',
        source_object_id=new['object_id'], expected_head='parent-1',
        expected_publication='publication-1', old_media=old, media=new,
    )
    assert retried.ok, retried.error
    assert restored.flush_calls == [(None, pending)]


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
