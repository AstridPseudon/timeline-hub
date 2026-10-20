"""Native numeric moves on API-built films, including the M1 command surface."""
from __future__ import annotations

import copy
from types import SimpleNamespace

import pytest

from astrid.sdk.timeline import commit
from astrid.sdk.timeline._command_state import State
from astrid.sdk.timeline.capture import capture_move
from tests.helpers.runtime import use_runtime

pytestmark = pytest.mark.integration


@pytest.fixture
def numeric_film(tmp_path, monkeypatch):
    runtime = use_runtime('6be970633cc82ab412428151e6bf42f3e7fc3081')
    monkeypatch.syspath_prepend(str(runtime / 'tests'))
    from runtime_protocol.service import RuntimeService
    from timeline_commit_film_fixture import build_film_fixture

    film = build_film_fixture(tmp_path)
    service = RuntimeService(film.duplicate_root)
    case = SimpleNamespace(service=service, film=film)

    def head():
        row = case.service.get_project_timeline(film.project_id, film.timeline_id)
        return {'revision_id': row['head_revision_id'], 'publication_id': row['head_publication_id']}

    def document(revision=None):
        return case.service._timeline_commits()[0].revision_closure(
            film.project_id, film.timeline_id, revision or head()['revision_id'])

    def submit(calls, key):
        base = head()
        body = {'api_version': 1, 'project_id': film.project_id, 'timeline_id': film.timeline_id,
                'base_revision_id': base['revision_id'], 'base_publication_id': base['publication_id'],
                'commands': calls}
        return case.service.commit_timeline(
            film.project_id, film.timeline_id, body, idempotency_key=key, publisher='author',
            invocation_path=f'/v1/projects/{film.project_id}/timelines/{film.timeline_id}/commit',
            authorize=lambda: None)

    case.head, case.document, case.submit = head, document, submit
    try:
        yield case
    finally:
        case.service.close()


def exact(actual, expected):
    assert commit._json(actual) == commit._json(expected)


@pytest.mark.parametrize('scope', ['parent', 'occurrence'])
@pytest.mark.parametrize('start,on', [(0, 0), (0.0, 0), (0, 1)])
def test_native_move_keeps_exact_numeric_image_and_unchanged_history(numeric_film, scope, start, on):
    case = numeric_film
    source = case.document()
    parent = copy.deepcopy(source['parent_revision']['payload'])
    shots, internals = [], []
    if scope == 'parent':
        ref = 'parent/clip:music-bed'
        target = parent['clips'][0]
    else:
        ref = 'occurrence:occurrence-1/clip:clip-1'
        internal = copy.deepcopy(source['internal_timeline_revisions'][0])
        shot = next(copy.deepcopy(row) for row in source['shot_revisions']
                    if row['internal_timeline_revision_id'] == internal['revision_id'])
        internal.update(revision_id='numeric-internal')
        shot.update(revision_id='numeric-shot', internal_timeline_revision_id='numeric-internal')
        shot['payload']['internal_timeline_revision_id'] = 'numeric-internal'
        for occurrence in parent['occurrences']:
            if occurrence['shot_id'] == shot['shot_id']:
                occurrence['shot_revision_id'] = 'numeric-shot'
        target = internal['payload']['clips'][0]
        target['hold'] = 0.25
        for row in (internal, shot):
            row.pop('content_digest')
        shots, internals = [shot], [internal]
    target['at'] = start
    target['app'] = {'astrid': {'fixed_start': True, 'for': target['hold']},
                     'org.example/opaque': [None, False, 1, 1.0]}
    case.service.publish_parent_composition(case.film.project_id, case.film.timeline_id, {
        'project_id': case.film.project_id, 'timeline_id': case.film.timeline_id,
        'expected_head': case.head()['revision_id'], 'parent_revision_id': 'numeric-baseline',
        'parent_composition': parent, 'shot_revisions': shots, 'internal_timeline_revisions': internals,
    }, idempotency_key='numeric-baseline')
    case.service.register_timeline_commit_provider(commit.create_runtime_commit_service())
    original, base = case.document(), case.head()
    bundle = commit.bundle_from_document(original)
    command = capture_move(bundle, ref, on)
    accepted = case.submit([command], 'numeric-move')
    document = accepted['data']['canonical_document']
    actual = State(commit.bundle_from_document(document)).entity(ref)
    assert type(actual['at']) is float and actual['at'] == on
    assert actual['app']['org.example/opaque'] == [None, False, 1, 1.0]
    changed = commit._json(start) != commit._json(float(on))
    assert (case.head()['revision_id'] != base['revision_id']) is changed
    assert case.head()['publication_id'] != base['publication_id']
    exact(case.document(), document)
    exact(case.document(base['revision_id']), original)
    exact(document['dependency_manifest']['media'], original['dependency_manifest']['media'])
    history = case.service.list_timeline_commits(
        case.film.project_id, case.film.timeline_id, authorize=lambda: None)['items']
    record = next(row for row in history if row['publication_id'] == case.head()['publication_id'])
    assert any(write['ref'] == ref and write['path'] == ['at']
               for item in record['records']['commands'] for write in item['writes'])
