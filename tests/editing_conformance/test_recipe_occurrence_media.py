"""Native popup capture, exact recorder parity and scoped asset birth/inverse."""
from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from astrid.sdk.timeline._command_state import CommandError, State, overlaps
from astrid.sdk.timeline.commands import execute, validate_command
from astrid.sdk.timeline.commit import (
    _digest,
    _manifest,
    bundle_from_document,
    document_from_bundle,
)
from astrid.sdk.timeline.native_occurrence_media_commands import (
    capture_occurrence_add_media,
    capture_occurrence_swap_media,
)
from astrid.sdk.timeline.rebase import replay
from tests.editing_conformance.test_recipe_m1_commands import inverse, later
from tests.sdk.test_timeline_commit_provider import (
    CommitRejected,
    DetachedPort,
    DetachedRealm,
    refusal,
    runtime_abi,  # noqa: F401 -- detached ABI fixture
)
from tests.sdk.test_timeline_commit_provider import inverse as inverse_call
from tests.sdk.test_timeline_commit_provider_document import MEDIA, document_fixture

OWNER = 'occurrence:occ-a'
TARGET = OWNER + '/clip:clip-a'
NEW = 'sha256:' + '2' * 64
FIXTURE = Path(__file__).parent / 'fixtures' / 'recipe_m2_occurrence_media.json'
MATERIALIZATION_FIXTURE = FIXTURE.with_name('recipe_m2_occurrence_media_materialization_v1.json')


def inputs(kind='image'):
    document = document_fixture()
    payload = document['internal_timeline_revisions'][0]['payload']
    payload.pop('source_window')
    payload['registry']['assets']['picture']['type'] = kind
    if kind == 'video':
        payload['clips'][0].update({'from': 2, 'to': 6, 'hold': 4, 'speed': 2})
    for row in document['parent_revision']['payload']['occurrences']:
        row.update(source_offset=0, speed=1)
    document['parent_revision']['payload']['occurrences'][0]['placement']['start_ms'] = 8000
    for image in [document['parent_revision'], *document['internal_timeline_revisions']]:
        image['content_digest'] = _digest(image['payload'])
    document['dependency_manifest'] = _manifest(document['shot_revisions'],
        document['internal_timeline_revisions'], document['dependency_manifest']['media'], [])
    old = {'asset': 'picture', 'generation_id': 'generation-old', 'variant_id': 'variant-old',
           'object_id': MEDIA, 'catalog_digest': 'sha256:' + 'a' * 64}
    new = {'asset': 'reserved-new', 'generation_id': 'generation-new', 'variant_id': 'variant-new',
           'object_id': NEW, 'catalog_digest': 'sha256:' + 'b' * 64}
    verified = [{'selection': copy.deepcopy(pin), 'media_type': kind + '/fixture', 'size': 123,
                 **({'duration_seconds': 6} if kind == 'video' else {})} for pin in (old, new)]
    return document, old, new, verified


def captured(operation, kind='image', *, capture_sources=True):
    document, old, new, verified = inputs(kind)
    bundle = bundle_from_document(document, capture_sources=capture_sources)
    if operation == 'add':
        row = {'id': 'reserved-child', 'clipType': kind, 'asset': new['asset'], 'track': 'picture',
               'at': .125, 'hold': 4 if kind == 'video' else 1.25,
               'params': None, 'opaque': [None, False, {}],
               **({'from': 2, 'to': 6, 'speed': 2} if kind == 'video' else {})}
        command = capture_occurrence_add_media(bundle, OWNER, row, new, verified_media=verified)
    else:
        command = capture_occurrence_swap_media(bundle, TARGET, old, new, verified_media=verified)
    return document, bundle, command, verified


@pytest.mark.parametrize('operation', ['add', 'swap'])
@pytest.mark.parametrize('kind', ['image', 'video'])
def test_exact_capture_replay_scoped_birth_and_inverse(operation, kind):
    document, bundle, command, verified = captured(operation, kind)
    before = copy.deepcopy(bundle)
    validate_command(command)
    plan = execute(bundle, [command], verified_media=verified)
    assert replay(plan, bundle, verified_media=verified).records == plan.records
    assert inverse(plan.bundle, plan.records).bundle == before
    assert bundle == before
    assert plan.bundle['parent'] == before['parent']
    sibling = before['placements'][1]['shot_id']
    assert plan.bundle['shots'][sibling] == before['shots'][sibling]
    assert command['created'] == [OWNER + '/asset:reserved-new'] + (
        [OWNER + '/clip:reserved-child'] if operation == 'add' else [])
    assert NEW not in {pin['media_id'] for pin in document['dependency_manifest']['media']}
    output = document_from_bundle(plan.bundle)
    assert NEW in {pin['media_id'] for pin in output['dependency_manifest']['media']}
    row = State(plan.bundle).entity(OWNER + '/clip:reserved-child' if operation == 'add' else TARGET)
    assert row['at'] == (.125 if operation == 'add' else 1)
    if kind == 'video':
        assert (row['from'], row['to'], row['hold'], row['speed']) == (2, 6, 4, 2)


@pytest.mark.parametrize('operation', ['add', 'swap'])
@pytest.mark.parametrize('fixture_path', [FIXTURE, MATERIALIZATION_FIXTURE])
def test_portable_goldens(operation, fixture_path):
    golden = json.loads(fixture_path.read_text())[operation]
    document, bundle, command, verified = captured(
        operation, 'video', capture_sources=fixture_path == MATERIALIZATION_FIXTURE)
    plan = execute(bundle, [command], verified_media=verified)
    assert golden == {'input': document, 'verified_media': verified, 'commands': [command],
                      'records': plan.records, 'output': document_from_bundle(plan.bundle)}


@pytest.mark.parametrize('operation', ['add', 'swap'])
def test_existing_binding_is_required_exactly_without_birth(operation):
    _, bundle, command, verified = captured(operation)
    ctx = State(bundle)
    assets = ctx.config(OWNER)['registry']['assets']
    assets['reserved-new'] = {'media_id': NEW, 'type': 'image',
                             'generationId': 'generation-new', 'variantId': 'variant-new'}
    plain = {key: command[key] for key in ('schema_version', 'op', 'version', 'select', 'args', 'intent')}
    plan = execute(bundle, [plain], verified_media=verified)
    assert OWNER + '/asset:reserved-new' not in plan.commands[0]['created']
    assert inverse(plan.bundle, plan.records).bundle == bundle
    assets['reserved-new']['opaque'] = None
    with pytest.raises(CommandError, match='existing registry binding'):
        execute(bundle, [plain], verified_media=verified)


@pytest.mark.parametrize('operation', ['add', 'swap'])
@pytest.mark.parametrize('damage', ['missing-input', 'wrong-object', 'wrong-catalog', 'shared', 'parent',
    'display-child', 'track', 'source-map', 'window', 'zero-speed', 'negative-speed', 'boolean-speed',
    'outside', 'membership', 'order', 'birth', 'binding'])
def test_refusals_preserve_input(operation, damage):
    _, bundle, command, verified = captured(operation, 'video')
    if damage == 'missing-input':
        verified.pop()
    elif damage in ('wrong-object', 'wrong-catalog'):
        command['args']['media']['object_id' if damage == 'wrong-object' else 'catalog_digest'] = MEDIA
    elif damage == 'shared':
        command['intent']['ownership'] = 'shared'
    elif damage == 'parent':
        command['select'] = 'parent'
    elif damage == 'display-child':
        command['select'] = OWNER + '/clip:occ-a:clip-a'
    elif damage == 'track':
        State(bundle).config(OWNER)['tracks'][0]['hidden'] = True
    elif damage == 'source-map':
        State(bundle).occurrence(OWNER)['source_offset'] = 1
    elif damage in ('window', 'zero-speed', 'negative-speed', 'boolean-speed', 'outside'):
        row = command['args']['row'] if operation == 'add' else State(bundle).entity(TARGET)
        if damage == 'window':
            row['to'] = 7
        elif damage == 'outside':
            row['at'] = 9
        else:
            row['speed'] = {'zero-speed': 0, 'negative-speed': -1, 'boolean-speed': True}[damage]
    elif damage in ('membership', 'order'):
        rows = State(bundle).config(OWNER)['tracks' if operation == 'add' else 'clips']
        if damage == 'membership':
            rows.append(dict(copy.deepcopy(rows[0]), id='other'))
        else:
            rows.insert(0, dict(copy.deepcopy(rows[0]), id='other'))
    elif damage == 'birth':
        command['created'] = []
    else:
        command['bindings']['media.owner'] = 'occurrence:foreign'
    before = copy.deepcopy(bundle)
    with pytest.raises(CommandError):
        execute(bundle, [command], verified_media=verified)
    assert bundle == before


def test_asset_address_alias_overlap_and_guarded_dependency():
    assert overlaps((OWNER + '/asset:reserved-new', ()),
                    (OWNER + '/source', ('registry', 'assets', 'reserved-new', 'type')))
    _, bundle, command, verified = captured('swap')
    plan = execute(bundle, [command], verified_media=verified)
    # A later clip uses the created alias even when the object was already pinned.
    State(plan.bundle).entity(OWNER + '/clip:clip-b')['asset'] = 'reserved-new'
    with pytest.raises(CommandError, match='surviving dependents'):
        inverse(plan.bundle, plan.records)


def test_disjoint_edit_rebases_but_same_value_asset_write_blocks_undo():
    _, bundle, command, verified = captured('swap')
    plan = execute(bundle, [command], verified_media=verified)
    head = copy.deepcopy(bundle)
    State(head).entity('parent/clip:clip-b')['at'] = 6
    rebased = replay(plan, head, verified_media=verified,
                     intervening_records=[later('parent/clip:clip-b', ['at'], 6)])
    assert State(inverse(rebased.bundle, rebased.records).bundle).entity('parent/clip:clip-b')['at'] == 6
    with pytest.raises(CommandError, match='intervening'):
        inverse(plan.bundle, plan.records, [later(OWNER + '/source',
            ['registry', 'assets', 'reserved-new', 'type'], 'image')])


class MediaRealm(DetachedRealm):
    def __init__(self, document, verified):
        super().__init__(document)
        self.verified = copy.deepcopy(verified)

    def call(self, calls, *, base=None, dry_run=False):
        from astrid.sdk.timeline.commit import create_runtime_commit_service

        class MediaPort(DetachedPort):
            def selected_media(self, pin):
                matches = [value for value in self.realm.verified if value['selection'] == pin]
                if not matches:
                    raise refusal('dependency_unavailable')
                return copy.deepcopy(matches[0])

        context = self.context(calls, base=base, dry_run=dry_run)
        return create_runtime_commit_service().commit(context, MediaPort(self, context))


@pytest.mark.parametrize('operation', ['add', 'swap'])
def test_provider_exact_reload_inverse_redo_and_retired_asset_reservation(operation):
    document, _, command, verified = captured(operation, 'video')
    realm = MediaRealm(document, verified)
    created = realm.call([command])
    undo = realm.call([inverse_call([created['receipt']['receipt_id']])])
    assert undo['data']['canonical_document'] == document
    head, history = copy.deepcopy(realm.head), copy.deepcopy(realm.entries)
    # A fresh request cannot reuse an alias retired by accepted history.
    with pytest.raises(CommitRejected) as error:
        realm.call([command])
    assert error.value.failure['details']['reason'] == 'identity_collision'
    assert (realm.head, realm.entries) == (head, history)
    redo = realm.call([inverse_call([undo['receipt']['receipt_id']])])
    assert redo['data']['canonical_document'] == created['data']['canonical_document']
    again = realm.call([inverse_call([redo['receipt']['receipt_id']])])
    assert again['data']['canonical_document'] == document


@pytest.mark.parametrize('operation', ['add', 'swap'])
def test_missing_port_pin_refuses_before_acceptance(operation):
    document, _, command, verified = captured(operation)
    realm = MediaRealm(document, verified[:-1])
    head, history = copy.deepcopy(realm.head), copy.deepcopy(realm.entries)
    with pytest.raises(CommitRejected, match='dependency_unavailable'):
        realm.call([command])
    assert (realm.head, realm.entries) == (head, history)
    assert not realm.prepared


@pytest.mark.parametrize('scope', ['local-alias', 'foreign-ref', 'shot-ref'])
def test_asset_removal_checks_declared_references_across_owners(scope):
    _, bundle, command, verified = captured('swap')
    plan = execute(bundle, [command], verified_media=verified)
    ref = OWNER + '/asset:reserved-new'
    if scope == 'local-alias':
        State(plan.bundle).entity(OWNER + '/clip:clip-b')['asset'] = 'reserved-new'
    elif scope == 'foreign-ref':
        State(plan.bundle).entity('occurrence:occ-b/clip:clip-b')['asset_ref'] = ref
    else:
        plan.bundle['shots'][plan.bundle['placements'][1]['shot_id']]['payload']['asset_ref'] = ref
    with pytest.raises(CommandError, match='surviving dependents'):
        inverse(plan.bundle, plan.records)


@pytest.mark.parametrize('entry', [None, False, [], {'media_id': NEW, 'type': 'video'}])
def test_occupied_asset_alias_is_never_replaced(entry):
    _, bundle, command, verified = captured('swap')
    State(bundle).config(OWNER)['registry']['assets']['reserved-new'] = copy.deepcopy(entry)
    before = copy.deepcopy(bundle)
    plain = {key: command[key] for key in ('schema_version', 'op', 'version', 'select', 'args', 'intent')}
    with pytest.raises(CommandError):
        execute(bundle, [plain], verified_media=verified)
    assert bundle == before


def test_noninteger_positive_speed_preserves_source_units_and_half_open_boundary():
    _, bundle, command, verified = captured('add', 'video')
    plain = {key: command[key] for key in ('schema_version', 'op', 'version', 'select', 'args', 'intent')}
    plain['args']['row'].update(at=7, hold=4.5, speed=1.5, **{'from': 1.5, 'to': 6})
    plan = execute(bundle, [plain], verified_media=verified)
    row = State(plan.bundle).entity(OWNER + '/clip:reserved-child')
    assert (row['at'], row['hold'], row['speed'], row['from'], row['to']) == (7, 4.5, 1.5, 1.5, 6)
    assert inverse(plan.bundle, plan.records).bundle == bundle
    plain['args']['row']['at'] = 7.001
    with pytest.raises(CommandError, match='exceeds occurrence'):
        execute(bundle, [plain], verified_media=verified)
