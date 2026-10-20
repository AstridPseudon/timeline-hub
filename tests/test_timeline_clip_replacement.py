from __future__ import annotations

import json

from astrid.packs.timeline.cli import build_parser
from astrid.sdk.contracts import DomainResult
from astrid.sdk.remote import RemoteTimelines


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


def test_remote_parent_media_replacement_does_not_publish_a_whole_closure() -> None:
    class Transport:
        def __init__(self):
            self.published = []

        def list_timelines(self, project, *, cursor=None, limit=50):
            return ([{"project_id": project, "timeline_id": "main", "slug": "main"}], None)

        def publish_parent_composition(self, project_id, timeline_id, publication, *, idempotency_key):
            self.published.append((project_id, timeline_id, publication, idempotency_key))

    transport = Transport()
    result = RemoteTimelines(transport).replace_parent_media(
        "project-1",
        "main",
        occurrence_id="occ-1",
        clip_id="picture-1",
        source_object_id="sha256:" + "2" * 64,
        expected_head="parent-1",
        idempotency_key="parent-replace-1",
    )

    assert not result.ok
    assert result.error.code == "validation_error"
    assert transport.published == []


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


def test_selected_occurrence_replacement_uses_the_session_commit_door(monkeypatch) -> None:
    from astrid.sdk.timeline.commit import bundle_from_document
    from astrid.sdk.timeline.sync import TimelineSession
    from tests.editing_conformance.test_recipe_occurrence_media import inputs

    document, old, new, _ = inputs()
    bundle = bundle_from_document(document)
    next(iter(bundle['shots'].values()))['internal_timeline']['registry']['assets']['picture'].update(
        generationId=old['generation_id'], variantId=old['variant_id'])

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
            data = {'status': 'accepted', 'accepted_revision_id': 'parent-2',
                    'base_revision_id': 'parent-1', 'base_publication_id': 'publication-1',
                    'commands': self.state['pending']}
            receipt = {'receipt_id': 'publication-2', 'command_kind': 'timeline.commit',
                       'idempotency_key': idempotency_key, 'request_hash': 'hash',
                       'project_id': 'project-1', 'project_seq': [1, 1],
                       'event_ids': ['event-1'], 'result': data, 'created_at': 'now'}
            return {'data': data, 'receipt': receipt}

    session = Session()
    monkeypatch.setattr(TimelineSession, 'open', lambda *args, **kwargs: session)

    transport = Transport()
    timelines = RemoteTimelines(transport)
    result = timelines.replace_parent_media(
        'project-1', 'main', occurrence_id='occ-a', clip_id='clip-a',
        source_object_id=new['object_id'], expected_head='parent-1',
        expected_publication='publication-1', old_media=old, media=new,
        idempotency_key='selected-occurrence',
    )

    assert result.ok, result.error
    command = session.state['pending'][0]
    assert command['select'] == 'occurrence:occ-a/clip:clip-a'
    assert command['op'] == 'occurrence.swap-media'
    assert command['args'] == {'old_media': old, 'media': new}


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
