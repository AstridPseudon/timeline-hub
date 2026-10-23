"""D31 legacy association obligations through the installed Python provider."""
from __future__ import annotations

import copy

import pytest

from astrid.sdk.media_transcript import transcript_document_id
from astrid.sdk.timeline._command_state import ABSENT, CommandError, present
from astrid.sdk.timeline._recording import Recording
from astrid.sdk.timeline.commands import execute
from astrid.sdk.timeline.commit import _digest, bundle_from_document
from astrid.sdk.timeline.native_transcript_association import (
    EXTENSION,
    SCHEMA,
    associate,
    caption_id,
    encode,
    resolve_transcripts,
)
from tests.editing_conformance.test_a4_transcript_doc_patch_witness import change, patch, submit
from tests.editing_conformance.test_provider_step_undo_v2 import undo
from tests.sdk.test_timeline_commit_provider import CommitRejected, DetachedPort, DetachedRealm
from tests.sdk.test_timeline_commit_provider import runtime_abi as runtime_abi
from tests.sdk.test_timeline_commit_provider_document import MEDIA, document_fixture

ASSET = 'asset-a'
SOURCE = 'source-1'
OLD = 'transcript-source:source-1:segment:segment-a'
NEW = 'transcript-source:asset-a:source:source-1:segment:segment-a'
OLD_KEY = 'transcript-source-review:' + encode(OLD)
NEW_KEY = 'transcript-source-review:' + encode(NEW)


def source(identity=NEW, version=1):
    content = {'schema': 'media.transcript/v1', 'media_id': MEDIA, 'source_id': SOURCE,
               'segments': [{'id': identity, 'start': 0, 'end': 1, 'text': 'Hello',
                             'words': [{'id': identity + ':word:word-a', 'start': 0, 'end': 1, 'text': 'Hello'}]}]}
    document_id = transcript_document_id('project-1', MEDIA, SOURCE)
    pin = {'document_id': document_id, 'version': version, 'content_digest': _digest(content)}
    return {'pin': pin, 'document': {'document_id': document_id, 'project_id': 'project-1',
                                   'kind': 'media.transcript', 'version': version, 'content': content}}


def item(identity=OLD, asset=ASSET):
    return {'id': identity, 'shape': 'interval', 'domain': 'source_seconds',
            'extent': {'start': 0, 'end': 1}, 'schemaRef': SCHEMA,
            'sourceArtifactRef': {'assetId': asset},
            'provenance': {'adapterId': 'legacy.capture', 'adapterVersion': '1'},
            'payload': {'sourceId': SOURCE, 'segmentId': identity, 'text': 'Old text',
                        'words': [{'id': identity + ':word:word-a', 'start': 0, 'end': 1, 'text': 'Old'}],
                        'documentId': 'transcript:old', 'documentVersion': 1,
                        'opaque': {'keep': [None, False]}}, 'opaqueEnvelope': {'keep': True}}


def fixture(*, fallback=False, associated=False):
    document = document_fixture(shared=False)
    parent = document['parent_revision']['payload']
    parent['occurrences'] = []
    document['shot_revisions'] = []
    document['internal_timeline_revisions'] = []
    document['dependency_manifest']['shots'] = []
    document['dependency_manifest']['internal_timelines'] = []
    media = {'id': 'media-a', 'asset': ASSET, 'track': 'A1', 'clipType': 'audio', 'at': 0, 'hold': 1}
    caption = {'id': caption_id(OLD + '@media-a'), 'track': 'transcript-caption-foundry-track',
               'clipType': 'text', 'at': 0.1, 'hold': 2.3,
               'text': {'content': 'Human correction', 'color': '#cc3377', 'fontSize': 51},
               'opaque': {'keep': [None, False, 0]}, 'app': {'retained': {'future': [None, False]},
               '__generated__': {'extensionId': EXTENSION, 'contributionId': 'transcript-caption-foundry',
               'provenance': {'contractVersion': 1, 'sourceSchemaRef': SCHEMA, 'sourceItemId': OLD,
                              'sourceFingerprint': 'keep-source-fingerprint', 'generatorVersion': '1.3.0',
                              'outputFingerprint': 'keep-output-fingerprint', 'conflictPolicy': 'preserve-output'}}}}
    parent['config'] = {
        'output': {'fps': 30}, 'tracks': [{'id': 'A1', 'kind': 'audio'},
                                       {'id': 'transcript-caption-foundry-track', 'kind': 'visual'}],
        'clips': [media, caption], 'app': {'unrelated': {'keep': True}, EXTENSION: {
            'preferences': {'color': 'blue'}, OLD_KEY: {'schemaVersion': 1, 'sourceSchemaRef': SCHEMA,
            'sourceItemId': OLD, 'status': 'accepted-for-source-update', 'proposedText': 'Human correction',
            'opaque': {'keep': [None, False]}}}},
        'bundle': {'schema_version': 1, 'transcriptReferences': {
            'schema': 'media.transcript.references/v1', 'associations': []},
            'itemsBySchemaRef': {'other/v1': [{'id': 'unrelated', 'shape': 'point', 'domain': 'ordinal',
                'extent': {'start': 0}, 'schemaRef': 'other/v1', 'payload': {'keep': True},
                'sourceArtifactRef': {'assetId': 'other'},
                'provenance': {'adapterId': 'other', 'adapterVersion': '1'}}], SCHEMA: [item()]},
            'opaqueBundle': {'keep': [None, False, 0, 0.0, '', {}, []], 'future': {'null': None}}}}
    parent['registry'] = copy.deepcopy(parent['registry'])
    parent['registry']['assets'][ASSET] = {'media_id': MEDIA, 'type': 'audio'}
    parent['clips'] = [] if fallback else copy.deepcopy(parent['config']['clips'])
    old, new = source(OLD), source(version=2 if associated else 1)
    if associated:
        carrier = parent['config']['bundle']
        carrier['transcriptReferences']['associations'] = [{'assetId': ASSET, 'documentId': old['pin']['document_id']}]
        carrier['itemsBySchemaRef'][SCHEMA][0]['payload']['documentId'] = old['pin']['document_id']
        document['dependency_manifest']['documents'] = [old['pin']]
    document['parent_revision']['content_digest'] = _digest(parent)
    realm = DetachedRealm(document)
    realm.live_sources = {_digest(capture['pin']): capture for capture in (old, new)}
    return realm, new, old


def call(new, old=None):
    return {'schema_version': 1, 'op': 'transcript.associate', 'version': '1',
            'select': 'parent/asset:' + ASSET, 'intent': {'ownership': 'parent'}, 'args': {
                'asset_id': ASSET, 'media_id': MEDIA, 'source_id': SOURCE, 'document': copy.deepcopy(new['pin']),
                'previous_document': copy.deepcopy(old['pin']) if old else None, 'source_schema_ref': SCHEMA}}


def current(realm):
    return realm.documents[realm.head['revision_id']]['parent_revision']['payload']


def capture(realm, command):
    context = realm.context([command])
    return execute(bundle_from_document(realm.documents[realm.head['revision_id']]), [command],
                   resolve_inputs=resolve_transcripts(DetachedPort(realm, context), lambda ctx: []))


def semantic_step(identity, ordinal):
    return {'id': identity, 'label': identity, 'intent': '', 'tags': [],
            'command_ordinals': [ordinal], 'patch': []}


@pytest.mark.parametrize('fallback', [False, True])
def test_exact_legacy_caption_review_and_config_fallback_obligations(fallback):
    realm, new, _ = fixture(fallback=fallback)
    before = copy.deepcopy(current(realm))
    command = call(new)
    plan = capture(realm, command)
    assert current(realm) == before
    result, _ = submit(realm, command, reads=[], label='Associate transcript',
                       steps=[semantic_step('associate', 0)])
    parent = current(realm)
    config, original = parent['config'], before['config']
    nested = config['bundle']
    caption = config['clips'][1] if fallback else parent['clips'][1]
    record = realm.prepared[-1]['records']['commands'][0]
    assert result['data']['status'] == 'accepted'
    assert result['receipt']['result'] == result['data']
    assert result['data']['canonical_document'] == realm.documents[realm.head['revision_id']]
    assert nested['transcriptReferences']['associations'] == [{'assetId': ASSET, 'documentId': new['pin']['document_id']}]
    assert list(nested['itemsBySchemaRef']) == ['other/v1', SCHEMA]
    assert nested['itemsBySchemaRef']['other/v1'] == original['bundle']['itemsBySchemaRef']['other/v1']
    assert [row['id'] for row in nested['itemsBySchemaRef'][SCHEMA]] == [NEW]
    assert nested['itemsBySchemaRef'][SCHEMA][0]['payload']['words'] == new['document']['content']['segments'][0]['words']
    assert nested['opaqueBundle'] == original['bundle']['opaqueBundle']
    assert caption['id'] == caption_id(NEW + '@media-a')
    assert 'asset' not in caption
    expected_caption = copy.deepcopy(original['clips'][1])
    expected_caption['id'] = caption_id(NEW + '@media-a')
    expected_caption['app']['__generated__']['provenance']['sourceItemId'] = NEW
    assert caption == expected_caption
    assert (caption['at'], caption['hold']) == (0.1, 2.3)
    assert caption['text'] == {'content': 'Human correction', 'color': '#cc3377', 'fontSize': 51}
    assert caption['opaque'] == {'keep': [None, False, 0]}
    assert caption['app']['retained'] == {'future': [None, False]}
    extension = config['app'][EXTENSION]
    assert OLD_KEY not in extension
    assert extension[NEW_KEY] == {**original['app'][EXTENSION][OLD_KEY], 'sourceItemId': NEW}
    assert extension['preferences'] == original['app'][EXTENSION]['preferences']
    assert config['app']['unrelated'] == original['app']['unrelated']
    assert parent['clips'] == ([] if fallback else config['clips'])
    assert parent['unknown'] == before['unknown']
    assert record['command']['resolved'] == ['parent/asset:' + ASSET]
    assert record['command']['bindings'] == {}
    assert record['command']['created'] == record['created'] == []
    assert record['selections'] == []  # Exact array reads guard membership and order.
    assert [{key: binding[key] for key in ('key', 'ref', 'policy', 'dependencies')}
            for binding in record['bindings'][:3]] == [
        {'key': key, 'ref': 'parent/asset:' + ASSET, 'policy': 'fixed', 'dependencies': []}
        for key in ('transcript.owner', 'transcript.segment:' + NEW, 'transcript.word:' + NEW + ':word:word-a')]
    assert all(binding['physical_ref'] == 'parent' and binding['boundary']['phase'] == 'input'
               and binding['path'] == ['config', 'registry', 'assets', ASSET]
               for binding in record['bindings'][:3])
    assert record['dependencies'][0] == {'key': 'transcript.document', 'kind': 'transcript',
                                         'pin': new['pin'], 'policy': 'exact'}
    assert record['dependencies'] == plan.records[0]['dependencies']
    expected_paths = [['config', 'bundle', 'transcriptReferences'], ['config', 'bundle', 'itemsBySchemaRef'],
                      ['config', 'clips'] if fallback else ['clips'], ['config', 'app', EXTENSION]]
    assert [[write['ref'], write['path']] for write in record['writes']] == [['parent', path] for path in expected_paths]
    for write in record['writes']:
        assert write['before']['state'] == write['after']['state'] == 'present'
    assert record['derived_writes'] == ([] if fallback else [{
        'ref': 'parent', 'path': ['config', 'clips'], 'before': present(original['clips']),
        'after': present(config['clips']), 'cause': 0}])
    assert record['command']['expect'] == plan.commands[0]['expect']
    assert all(value == 'direct' for value in record['command']['authorship'].values())
    assert any(read['path'] == ['config'] and read['state'] == present(original) for read in record['reads'])
    assert any(read['path'] == ['config', 'bundle', 'itemsBySchemaRef'] for read in record['reads'])
    assert realm.retained_sources[_digest(new['pin'])] == new
    assert realm.prepared[-1]['records']['steps'][0]['patch']
    assert realm.prepared[-1]['records']['steps'][0]['dependencies']


def test_replacement_retains_exact_prior_and_source_order():
    realm, new, old = fixture(associated=True)
    new['document']['content']['segments'].append({**copy.deepcopy(new['document']['content']['segments'][0]),
        'id': NEW + '-2', 'words': []})
    new['pin']['content_digest'] = _digest(new['document']['content'])
    realm.live_sources[_digest(new['pin'])] = new
    result, _ = submit(realm, call(new, old), reads=[])
    record = realm.prepared[-1]['records']['commands'][0]
    assert [dependency['pin'] for dependency in record['dependencies'][:2]] == [new['pin'], old['pin']]
    assert [row['id'] for row in current(realm)['config']['bundle']['itemsBySchemaRef'][SCHEMA]] == [NEW, NEW + '-2']
    assert set(map(_digest, result['data']['canonical_document']['dependency_manifest']['documents'])) == {
        _digest(old['pin']), _digest(new['pin'])}


@pytest.mark.parametrize('damage', ['caption_collision', 'review_collision', 'shared_review', 'shared_caption',
                                    'duplicate_item', 'ambiguous_owner', 'foreign', 'malformed', 'uncaptured',
                                    'prior_missing', 'wrong_prior', 'wrong_new', 'forged_read', 'forged_previous',
                                    'foreign_owner', 'null_refs', 'null_items', 'null_bundle', 'raw_carrier'])
def test_strict_refusals_leave_no_authored_write_or_acceptance(damage):
    realm, new, old = fixture(associated=damage in ('prior_missing', 'wrong_prior'))
    parent = current(realm)
    config = parent['config']
    rows = config['bundle']['itemsBySchemaRef'][SCHEMA]
    command = call(new, old if damage == 'wrong_prior' else None)
    if damage == 'caption_collision':
        config['clips'].append({'id': caption_id(NEW + '@media-a'), 'track': 'A1', 'clipType': 'text', 'at': 0, 'hold': 1})
    elif damage == 'review_collision':
        config['app'][EXTENSION][NEW_KEY] = None
    elif damage in ('shared_review', 'shared_caption'):
        rows.append(item(asset='asset-b'))
        if damage == 'shared_caption':
            config['clips'][1]['id'] = caption_id(OLD)
    elif damage == 'duplicate_item':
        rows.append(copy.deepcopy(rows[0]))
    elif damage == 'ambiguous_owner':
        config['bundle']['transcriptReferences']['associations'] = [
            {'assetId': ASSET, 'documentId': 'transcript:old'}] * 2
    elif damage == 'foreign':
        new['document']['project_id'] = 'foreign'
    elif damage == 'malformed':
        new['document']['content']['segments'][0]['words'][0]['end'] = 2
        new['pin']['content_digest'] = _digest(new['document']['content'])
        command = call(new)
    elif damage == 'uncaptured':
        realm.live_sources = {}
    elif damage == 'wrong_prior':
        wrong = source(OLD, 2)
        realm.live_sources[_digest(wrong['pin'])] = wrong
        command = call(new, wrong)
    elif damage == 'wrong_new':
        command['args']['document']['version'] = 99
    elif damage == 'forged_read':
        command['reads'] = [{'ref': 'parent', 'path': ['config'], 'state': present({})}]
    elif damage == 'forged_previous':
        command['expect'] = {'parent::config.bundle.transcriptReferences': present({})}
    elif damage == 'foreign_owner':
        command['select'] = 'occurrence:occ-a/asset:' + ASSET
    elif damage == 'null_refs':
        config['bundle']['transcriptReferences'] = None
    elif damage == 'null_items':
        config['bundle']['itemsBySchemaRef'] = None
    elif damage == 'null_bundle':
        config['bundle'] = None
    elif damage == 'raw_carrier':
        parent['transcriptReferences'] = {}
    parent['clips'] = copy.deepcopy(config['clips'])
    realm.documents[realm.head['revision_id']]['parent_revision']['content_digest'] = _digest(parent)
    if damage not in ('uncaptured', 'wrong_new'):
        realm.live_sources[_digest(new['pin'])] = new
    before = copy.deepcopy((realm.head, realm.documents, realm.entries))
    with pytest.raises(CommitRejected):
        submit(realm, command, reads=[])
    assert (realm.head, realm.documents, realm.entries) == before
    assert realm.accepted == []
    if damage in ('caption_collision', 'review_collision', 'shared_review', 'shared_caption',
                  'duplicate_item', 'ambiguous_owner', 'prior_missing', 'wrong_prior', 'foreign_owner',
                  'null_refs', 'null_items', 'null_bundle', 'raw_carrier'):
        bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
        ctx = Recording(bundle, command, 0)
        ctx.transcript_inputs = [new] + ([realm.live_sources[_digest(command['args']['previous_document'])]]
                                      if command['args']['previous_document'] else [])
        original = copy.deepcopy(bundle)
        with pytest.raises(CommandError):
            associate(ctx, command)
        assert ctx.record['writes'] == []
        assert ctx.state.bundle == original


def test_illustrative_capture_in_bundle_does_not_authorize_source():
    realm, new, _ = fixture()
    bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
    bundle['source_mapping']['pinned_documents'] = [new]
    with pytest.raises(CommandError, match='Runtime-authenticated'):
        execute(bundle, [call(new)])


def test_absent_planes_preserve_presence_and_opaque_values():
    realm, new, _ = fixture()
    carrier = current(realm)['config']['bundle']
    del carrier['transcriptReferences']
    del carrier['itemsBySchemaRef']
    current(realm)['config']['clips'] = []
    current(realm)['clips'] = []
    realm.documents[realm.head['revision_id']]['parent_revision']['content_digest'] = _digest(current(realm))
    submit(realm, call(new), reads=[])
    writes = realm.prepared[-1]['records']['commands'][0]['writes']
    assert [write['before'] for write in writes] == [ABSENT, ABSENT]
    assert current(realm)['config']['bundle']['opaqueBundle']['future'] == {'null': None}


@pytest.mark.parametrize('control', ['order', 'membership', 'ABA'])
def test_captured_input_replay_refuses_changed_order_membership_and_aba(control):
    realm, new, _ = fixture()
    rows = current(realm)['config']['bundle']['itemsBySchemaRef'][SCHEMA]
    rows.append(item('other-id', 'other-asset'))
    realm.documents[realm.head['revision_id']]['parent_revision']['content_digest'] = _digest(current(realm))
    captured = capture(realm, call(new)).commands[0]
    base = copy.deepcopy(realm.head)
    original = copy.deepcopy(rows)
    changed = list(reversed(rows)) if control != 'membership' else rows[:1]
    path = ['config', 'bundle', 'itemsBySchemaRef', SCHEMA]
    submit(realm, patch(change(path, present(original), changed)), reads=[])
    if control == 'ABA':
        submit(realm, patch(change(path, present(changed), original)), reads=[])
    before = copy.deepcopy((realm.head, realm.entries))
    with pytest.raises(CommitRejected):
        submit(realm, captured, base=base, reads=[])
    assert (realm.head, realm.entries) == before


@pytest.mark.parametrize('fallback', [False, True])
@pytest.mark.parametrize('selected', [False, True])
def test_whole_selected_inverse_and_redo_keep_unselected_note(selected, fallback):
    realm, new, _ = fixture(fallback=fallback)
    before = copy.deepcopy(current(realm))
    note = patch(change(['unknown', 'note'], ABSENT, 'kept'))
    result, _ = submit(realm, call(new), note, reads=[], steps=[semantic_step('association', 0),
        {'id': 'note', 'label': 'note', 'intent': '', 'tags': [], 'command_ordinals': [1], 'patch': note['args']['changes']}])
    publication = result['receipt']['receipt_id']
    command = undo(publication, 'association') if selected else undo(publication)
    undone, _ = submit(realm, command, reads=[])
    expected = copy.deepcopy(before)
    if selected:
        expected['unknown']['note'] = 'kept'
    assert current(realm) == expected
    assert realm.prepared[-1]['records']['undo_steps'] == ({publication: ['association']} if selected else None)
    submit(realm, undo(undone['receipt']['receipt_id']), reads=[])
    assert current(realm) == result['data']['canonical_document']['parent_revision']['payload']


def test_preview_is_nonwriting_and_disjoint_merge_retains_full_metadata():
    realm, new, _ = fixture()
    before = copy.deepcopy((realm.head, realm.entries, realm.documents))
    preview, _ = submit(realm, call(new), reads=[], dry_run=True)
    assert preview['data']['status'] == 'preview'
    assert preview['data']['would_status'] == 'accepted'
    assert preview['receipt'] is None
    assert preview['data']['steps'][0]['patch']
    assert (realm.head, realm.entries, realm.documents) == before
    base = copy.deepcopy(realm.head)
    submit(realm, patch(change(['unknown', 'other'], ABSENT, 'kept')), reads=[])
    merged, _ = submit(realm, call(new), base=base, reads=[])
    # DetachedPort preserves the legacy stored spelling; production v2 Runtime
    # owns the accepted/merged wire envelope, without rewriting old receipts.
    assert merged['data']['status'] == 'rebased'
    assert current(realm)['unknown']['other'] == 'kept'
    assert merged['receipt']['result'] == merged['data']
    assert realm.prepared[-1]['records']['steps'][0]['patch']


def test_resolver_preserves_immutable_initial_image_across_command_boundary():
    realm, new, _ = fixture()
    bundle = bundle_from_document(realm.documents[realm.head['revision_id']])
    initial = copy.deepcopy(bundle['source_mapping']['_runtime_document'])
    command = call(new)
    plan = capture(realm, command)
    assert plan.bundle['source_mapping']['_runtime_document'] == initial
    assert plan.bundle['source_mapping']['_copy_manifest']['documents'] == [new['pin']]
    assert initial['dependency_manifest']['documents'] == []
    assert any(kind == 'transcript' and pin == new['pin'] for kind, pin in realm.reads if kind == 'transcript')
