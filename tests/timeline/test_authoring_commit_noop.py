from __future__ import annotations

import copy

import pytest

from astrid.core.timeline import authoring_bundle
from astrid.core.timeline.authoring_bundle import AuthoringBundleError, publish_authoring_candidate
from astrid.sdk.timeline import authoring_commit
from astrid.sdk.timeline.authoring_commit import authoring_commit_request
from tests.timeline import test_authoring_commit_media as media_tests


@pytest.fixture
def realm(tmp_path):
    yield from media_tests.realm.__wrapped__(tmp_path)


def test_unchanged_publication_preserves_bytes_metadata_and_runtime_replay(realm, monkeypatch):
    from runtime_protocol.errors import RuntimeErrorBase

    service, writer, candidate = realm
    project, timeline = candidate['project_id'], candidate['timeline_id']
    original = copy.deepcopy(candidate)
    before = writer.list_timeline_commits(project, timeline)
    compile_candidate = authoring_bundle.compile_authoring_candidate
    compilations = []

    def compile_once(value):
        compilations.append(copy.deepcopy(value))
        return compile_candidate(value)

    monkeypatch.setattr(authoring_bundle, 'compile_authoring_candidate', compile_once)
    monkeypatch.setattr(authoring_commit, 'compile_authoring_candidate', compile_once)
    commit = writer.commit_timeline
    replies = []
    submission_compilations = []

    def capture_reply(*args, **kwargs):
        submission_compilations.append(len(compilations))
        reply = commit(*args, **kwargs)
        replies.append(copy.deepcopy(reply))
        return reply

    monkeypatch.setattr(writer, 'commit_timeline', capture_reply)
    result = publish_authoring_candidate(candidate, writer, idempotency_key='unchanged')
    assert submission_compilations == [1]
    assert candidate == original
    request = writer.requests[-1]
    config = original['parent']['config']
    change = {'op': 'set', 'ref': 'parent', 'path': ['config'],
              'before': {'state': 'present', 'value': config}, 'value': config}
    assert request['commands'] == [{'schema_version': 1, 'op': 'doc.patch', 'version': '1',
                                  'select': None, 'args': {'changes': [change]}}]
    assert request['steps'][0]['patch'] == [change]
    assert request['steps'][0]['command_ordinals'] == [0]
    assert request['base_revision_id'] == before['head']['revision_id']
    assert request['base_publication_id'] == before['head']['publication_id']
    assert request['merge'] == 'atomic'
    assert request['label'] and request['source'] == {'via': 'python'}
    assert request['rationale'].endswith(result['candidate_digest'])
    publication = result['publication']
    for key, value in replies[0].items():
        if key != 'data':
            assert publication[key] == value
    for key, value in replies[0]['data'].items():
        assert publication[key] == publication['data'][key] == value
    document = publication['canonical_document']
    source = original['source_mapping']['_runtime_document']
    assert document['parent_revision']['payload'] == source['parent_revision']['payload']
    for key in ('shot_revisions', 'internal_timeline_revisions', 'dependency_manifest'):
        assert document[key] == source[key]
    assert publication['new_head'] == publication['data']['new_head']
    assert result['summary']['authored_change_count'] == 0
    assert result['summary']['catalog_media'] is None
    assert result['update'].startswith('No authored changes. Saved revision ')
    assert {action['scope'] for action in result['next_actions']} == {'current_head'}
    after = writer.list_timeline_commits(project, timeline)
    assert len(after['items']) == len(before['items']) + 1
    state = media_tests._timeline_state(service)
    retry = publish_authoring_candidate(candidate, writer, idempotency_key='unchanged')
    assert retry == result
    assert writer.requests[-1] == request
    assert media_tests._timeline_state(service) == state
    changed = copy.deepcopy(candidate)
    changed['parent']['config']['note'] = 'different payload'
    with pytest.raises(RuntimeErrorBase, match='[Ii]dempotency'):
        publish_authoring_candidate(changed, writer, idempotency_key='unchanged')
    with pytest.raises(RuntimeErrorBase):
        publish_authoring_candidate(candidate, writer, idempotency_key='stale-unchanged')
    assert media_tests._timeline_state(service) == state


def test_unchanged_preview_and_guards_cannot_write_or_forge_a_base(realm):
    from runtime_protocol.errors import RuntimeErrorBase

    service, writer, candidate = realm
    project, timeline = candidate['project_id'], candidate['timeline_id']
    before = media_tests._timeline_state(service)
    request = authoring_commit_request(candidate, writer)
    preview = writer.commit_timeline(project, timeline, {**request, 'dry_run': True},
                                     idempotency_key='unchanged-preview')
    assert preview['data']['status'] == 'preview'
    assert preview['data']['would_status'] == 'accepted'
    assert preview['receipt'] is None
    assert media_tests._timeline_state(service) == before
    forged = copy.deepcopy(candidate)
    forged['base_parent_payload']['config']['forged'] = True
    with pytest.raises((AuthoringBundleError, ValueError)):
        authoring_commit_request(forged, writer)
    wrong_pair = copy.deepcopy(candidate)
    wrong_pair['base_parent']['publication_id'] = 'foreign-publication'
    with pytest.raises(AuthoringBundleError, match='exact original'):
        authoring_commit_request(wrong_pair, writer)
    bad_guard = copy.deepcopy(request)
    bad_guard['commands'][0]['args']['changes'][0]['before']['value']['forged'] = True
    bad_guard['steps'][0]['patch'] = copy.deepcopy(bad_guard['commands'][0]['args']['changes'])
    with pytest.raises(RuntimeErrorBase):
        writer.commit_timeline(project, timeline, bad_guard, idempotency_key='bad-guard')
    assert media_tests._timeline_state(service) == before
