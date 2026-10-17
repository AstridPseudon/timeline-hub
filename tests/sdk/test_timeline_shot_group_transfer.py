"""Exact cross-track group transfer on synthetic SDK source, never live Runtime."""
# ruff: noqa: F811 -- imported pytest fixtures intentionally share parameter names.
import copy
import json
from pathlib import Path

import pytest
from test_timeline_commit import Port, request
from test_timeline_publication_inverse import HistoryRuntime
from test_timeline_saved_publish import RuntimeFixture, synthetic_scene_answers  # noqa: F401
from test_timeline_shot_groups import (  # noqa: F401, F811
    GROUP,
    MEMBERS,
    apply,
    bundle,
    call,
    closure,
    video_call,
)

from astrid.core.timeline.authoring_bundle import compile_authoring_candidate
from astrid.sdk.timeline import commands, saved_publish, store
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.inverse import inverse_command
from astrid.sdk.timeline.rebase import rebase
from astrid.sdk.timeline.shot_groups import identity
from astrid.sdk.workspace_client import WorkspaceClientError

pytestmark = pytest.mark.usefixtures('synthetic_scene_answers')
TARGET = dict(GROUP, trackId='destination')


def transfer(members=MEMBERS, scope='parent'):
    return dict(op='shot-group.set', select=None,
                args=dict(group=GROUP, intent='transfer', target=scope + '/track:destination', members=list(members)))


def source(bundle, mode='images', scope='parent', *, new_lane=False):
    b = copy.deepcopy(bundle)
    if scope != 'parent':
        child = b['shots'][b['placements'][0]['shot_id']]['internal_timeline']
        child['clips'] = copy.deepcopy(b['parent']['clips'][:2])
        child['registry'] = copy.deepcopy(b['parent']['registry'])
        owner = child
    else:
        owner = b['parent']
    tracks = owner['config']['tracks'] if scope == 'parent' else owner['tracks']
    if not new_lane:
        tracks.append(dict(id='destination', kind='visual', label='Destination', opaque=None))
    members = [scope + '/clip:i1', scope + '/clip:i2']
    b, _ = apply(b, call(members=members, name='Retained name'))
    if mode == 'video':
        b, _ = apply(b, video_call())
        members = [scope + '/clip:v1']
    row = b['parent']['config']['pinnedShotGroups'][0]
    row.update(opaque=dict(null=None, literal='picture', nested=[1, {'track': 'picture'}]), videoAssetKey=row.get('videoAssetKey', 'retained-video'), poolGenerationIds=['g'], derivedFrom=None)
    neighbors = [dict(shotId=k, trackId='picture', opaque=k) for k in ('before', 'after')]
    b['parent']['config']['pinnedShotGroups'] = [neighbors[0], row, neighbors[1]]
    return b, members


def states(b):
    return commands.entity_states(Checkout(copy.deepcopy(b)))


@pytest.mark.parametrize('scope', ['parent', 'occurrence:a'])
@pytest.mark.parametrize('mode', ['images', 'video'])
def test_transfer_retains_exact_row_snapshots_scope_and_direct_receipts(bundle, scope, mode):
    before, members = source(bundle, mode, scope)
    requested = list(reversed(members))
    after, plan = apply(before, transfer(requested, scope))
    old, new = states(before), states(after)
    expected_row = copy.deepcopy(old[identity(GROUP)])
    expected_row.update(trackId='destination', clipIds=[v.split('/clip:')[1] for v in requested], memberSelectors=requested)
    for snap in expected_row.get('imageClipSnapshot', []):
        snap['track'] = snap['authoring']['clip']['track'] = 'destination'
    assert new[identity(TARGET)] == expected_row
    assert identity(GROUP) not in new
    rows = after['parent']['config']['pinnedShotGroups']
    assert rows == [before['parent']['config']['pinnedShotGroups'][0], expected_row, before['parent']['config']['pinnedShotGroups'][2]]
    for value in members:
        assert new[value] == dict(old[value], track='destination')
    changed_ids = {identity(GROUP), identity(TARGET), *members}
    for sid in set(old) & set(new) - changed_ids - {'parent'}:
        assert new[sid] == old[sid]
    assert list(k for k in old if '/clip:' in k) == list(k for k in new if '/clip:' in k)
    expected_paths = {(identity(GROUP), ''), (identity(TARGET), ''), *((v, 'track') for v in members)}
    assert {(w['id'], w['path']) for w in plan.direct_writes} == expected_paths
    for write in plan.direct_writes:
        assert write['before'] == commands.state_at(old, write['id'], write['path'])
        assert write['after'] == commands.state_at(new, write['id'], write['path'])
    assert plan.calls[0].expect[identity(GROUP) + '::group_order'] == dict(state='present', value=[identity({k:r[k] for k in ('shotId','trackId')}) for r in before['parent']['config']['pinnedShotGroups']])
    assert plan.calls[0].expect[identity(TARGET) + '::'] == dict(state='absent')
    assert not [sid for sid in plan.calls[0].created if '/clip:' in sid]
    assert rebase(plan.calls, before).document == after
    undone, undo_plan = apply(after, inverse_command(plan.calls, before, after, 'pub-transfer'))
    assert undone == before
    redone, _ = apply(undone, inverse_command(undo_plan.calls, after, undone, 'pub-undo'))
    assert redone == after


@pytest.mark.parametrize('mutation', ['target-collision','stale-row','group-order','member-order','member-value','member-track','missing-member','duplicate-member','mixed-owner','wrong-group-owner','invalid-target','wrong-target-scope','audio-target','snapshot-owner','snapshot-track','snapshot-collision'])
def test_transfer_refuses_changed_ambiguous_or_colliding_inputs_atomically(bundle, mutation):
    before, members = source(bundle, 'video' if mutation.startswith('snapshot') else 'images')
    operation = transfer(members)
    _, plan = apply(before, operation)
    head = copy.deepcopy(before)
    groups = head['parent']['config']['pinnedShotGroups']
    if mutation == 'target-collision':
        groups.append(dict(groups[1], trackId='destination'))
    elif mutation == 'stale-row':
        groups[1]['opaque']['later'] = True
    elif mutation == 'group-order':
        groups.reverse()
    elif mutation == 'member-order':
        head['parent']['clips'][:2] = reversed(head['parent']['clips'][:2])
    elif mutation == 'member-value':
        head['parent']['clips'][0]['opaque'] = 'later'
    elif mutation == 'member-track':
        head['parent']['clips'][0]['track'] = 'destination'
    elif mutation == 'missing-member':
        head['parent']['clips'].pop(0)
    elif mutation == 'duplicate-member':
        head['parent']['clips'].append(copy.deepcopy(head['parent']['clips'][0]))
    elif mutation == 'mixed-owner':
        operation['args']['members'] = ['parent/clip:i1', 'occurrence:a/clip:i2']
    elif mutation == 'wrong-group-owner':
        groups[1]['ownerOccurrenceId'] = 'a'
    elif mutation == 'invalid-target':
        operation['args']['target'] = 'parent/track:missing'
    elif mutation == 'wrong-target-scope':
        operation['args']['target'] = 'occurrence:a/track:destination'
    elif mutation == 'audio-target':
        head['parent']['config']['tracks'][1]['kind'] = 'audio'
    elif mutation == 'snapshot-owner':
        groups[1]['imageClipSnapshot'][0]['authoring']['selector'] = 'occurrence:a/clip:i1'
    elif mutation == 'snapshot-track':
        groups[1]['imageClipSnapshot'][0]['authoring']['clip']['track'] = 'destination'
    elif mutation == 'snapshot-collision':
        head['parent']['clips'].append(copy.deepcopy(groups[1]['imageClipSnapshot'][0]['authoring']['clip']))
    captured = [v.to_json() for v in plan.calls]
    # For changed command intent, test the fresh call's validation as well.
    values = [operation] if operation != transfer(members) else captured
    draft = Checkout(copy.deepcopy(head))
    with pytest.raises((commands.CommandError, commands.TimelineEditError)):
        draft.batch(values)
    assert draft.bundle == head
    if values == captured:
        assert rebase(plan.calls, head).conflicts


@pytest.mark.parametrize('scope', ['parent', 'occurrence:a'])
def test_transfer_new_lane_composes_existing_guarded_add_and_timing(bundle, scope):
    before, members = source(bundle, scope=scope, new_lane=True)
    owner = before['parent'] if scope == 'parent' else before['shots'][before['placements'][0]['shot_id']]['internal_timeline']
    owner['clips'][0]['hold'] = .2
    owner['clips'][1].update(at=.2, hold=.2)
    target = scope + '/track:destination'
    add = dict(op='timeline.add', select=target, args=dict(track=dict(id='destination', kind='visual', label='New')), expect={target + '::': dict(state='absent')})
    moves = [dict(op='clip.nudge', select=value, args=dict(seconds=.2)) for value in members]
    after, plan = apply(before, add, transfer(list(reversed(members)), scope), *moves)
    assert states(after)[members[0]]['at'] == states(before)[members[0]]['at'] + .2
    assert (target, '') in {(w['id'], w['path']) for w in plan.direct_writes}
    assert rebase(plan.calls, before).document == after
    restored, undo_plan = apply(after, inverse_command(plan.calls, before, after, 'pub-new-lane'))
    assert restored == before
    redone, _ = apply(restored, inverse_command(undo_plan.calls, after, restored, 'undo-new-lane'))
    assert redone == after
    changed = copy.deepcopy(before)
    owner = changed['parent']['config'] if scope == 'parent' else changed['shots'][changed['placements'][0]['shot_id']]['internal_timeline']
    owner['tracks'].append(dict(id='destination', kind='visual', label='Concurrent'))
    draft = Checkout(copy.deepcopy(changed))
    with pytest.raises((commands.CommandError, commands.TimelineEditError)):
        draft.batch([v.to_json() for v in plan.calls])
    assert draft.bundle == changed


class GroupHistoryRuntime(HistoryRuntime):
    def __init__(self, bundle):
        RuntimeFixture.__init__(self, bundle=bundle)
        self.history = [[self.event('rev-0', 'pub-0', None, None, via='app')], None]
        self.restores = []
        self.summaries, self.evidence_store = [], {}


def history_draft(before, tmp_path, monkeypatch):
    monkeypatch.setenv('BANODOCO_LOCAL_DATA_ROOT', str(tmp_path / 'data'))
    monkeypatch.setattr(Checkout, 'SAY_SAVED', False)
    materialized = copy.deepcopy(before)
    # This double owns a complete synthetic closure, including unchanged shots.
    for mapping in materialized['source_mapping']['shots'].values():
        mapping['linked'] = False
    runtime = GroupHistoryRuntime(materialized)
    client = runtime.product()
    body = dict(project_id='p', timeline_id='t', base_revision_id='rev-0')
    monkeypatch.setattr(store, 'resolve_ids', lambda *a, **kw: ('p', 't', runtime.current))
    monkeypatch.setattr(store, 'fetch_bundle', lambda *a, revision_id=None, **kw: saved_publish._exact(client._transport, body, revision_id or runtime.current))
    return Checkout.draft('p', 't'), runtime, client


def content(document):
    # Compare all authored content, excluding the new publication's head/ID envelope.
    publication = compile_authoring_candidate(document).publication
    return {k: publication[k] for k in ('parent_composition', 'shot_revisions', 'internal_timeline_revisions')}


@pytest.mark.parametrize('mode', ['images', 'video'])
def test_accepted_publication_receipts_replay_and_exact_undo_redo(bundle, mode, tmp_path, monkeypatch):
    before, members = source(bundle, mode)
    draft, runtime, client = history_draft(before, tmp_path, monkeypatch)
    exact_before = draft.document()
    original = content(exact_before)
    commands.run(draft, transfer(list(reversed(members))))
    runtime.lose = True
    with pytest.raises(WorkspaceClientError, match='timed out'):
        draft.publish('transfer group', client=client)
    draft = Checkout.load(draft.path)
    moved = draft.publish(client=client)
    assert runtime.commits[0][0] == runtime.commits[1][0]
    assert len(runtime.publications) == 1
    assert moved['status'] == 'accepted', moved
    paths = {(identity(GROUP), ''), (identity(TARGET), ''), *((v,'track') for v in members)}
    assert {(w['id'],w['path']) for w in moved['change']['direct_writes']} == paths
    assert moved['shot_groups'] == [dict(operation_index=0, group=TARGET, created=[], reused=list(reversed(members)), restored=[])]
    assert moved['id_map'][identity(GROUP)] == identity(TARGET)
    assert all(moved['id_map'][v] == v for v in members)
    moved_content = content(moved['canonical_document'])
    # The actual accepted, recorded commands reproduce the accepted closure.
    replayed, _ = apply(exact_before, *moved['change']['commands'])
    assert content(replayed) == moved_content
    assert json.loads(runtime.calls[-1][0])['base_revision_id'] == 'rev-0'
    draft = Checkout.load(draft.path)
    draft.undo(client=client, publication=moved['accepted_publication_id'])
    undone = draft.publish('undo transfer', client=client)
    assert undone['status'] == 'accepted', undone
    assert content(undone['canonical_document']) == original
    draft = Checkout.load(draft.path)
    draft.undo(client=client, publication=undone['accepted_publication_id'])
    redone = draft.publish('redo transfer', client=client)
    assert redone['status'] == 'accepted', redone
    assert content(redone['canonical_document']) == moved_content
    (tmp_path / 'accepted-transfer-proof.json').write_text(json.dumps(dict(
        scope='synthetic SDK acceptance double only', before=exact_before,
        transferred=moved, undone=undone, redone=redone), indent=2, sort_keys=True) + '\n')


@pytest.mark.parametrize('later', ['member-track', 'target-group', 'old-key-collision'])
def test_publication_inverse_attributes_later_work_without_loss(bundle, later, tmp_path, monkeypatch):
    before, members = source(bundle)
    draft, runtime, client = history_draft(before, tmp_path, monkeypatch)
    commands.run(draft, transfer())
    moved = draft.publish('transfer group', client=client)
    assert moved['status'] == 'accepted', moved
    other = Checkout.draft('p','t',name='later')
    if later == 'member-track':
        commands.run(other, dict(op='clip.set-track',select=members[0],args=dict(track='picture')))
    elif later == 'target-group':
        commands.run(other, dict(op='shot-group.set',select=None,args=dict(group=TARGET,intent='pin',members=MEMBERS,name='Later group')))
    else:
        commands.run(other, dict(op='shot-group.set',select=None,args=dict(group=GROUP,intent='pin',members=['parent/clip:other'],name='Later collision')))
    accepted = other.publish('later work',client=client)
    assert accepted['status'] == 'accepted', accepted
    clean = Path(draft.path).read_bytes()
    head = copy.deepcopy(runtime.parents[runtime.current])
    with pytest.raises(commands.TimelineEditError, match='same-property') as exc:
        draft.undo(client=client,publication=moved['accepted_publication_id'])
    assert accepted['accepted_publication_id'] in str(exc.value)
    assert 'later work' in str(exc.value)
    assert Path(draft.path).read_bytes() == clean
    assert runtime.parents[runtime.current] == head


@pytest.mark.parametrize('scoped_clip_ids', [False, True])
def test_transfer_preserves_legacy_member_representation(bundle, scoped_clip_ids):
    before, members = source(bundle)
    row = before['parent']['config']['pinnedShotGroups'][1]
    row.pop('memberSelectors')
    row.pop('mode')
    row.update(ownerOccurrenceId=None, imageClipSnapshot=[])
    if scoped_clip_ids:
        row['clipIds'] = list(members)
    after, _ = apply(before, transfer(list(reversed(members))))
    result = after['parent']['config']['pinnedShotGroups'][1]
    assert 'memberSelectors' not in result
    assert result['clipIds'] == list(reversed(row['clipIds']))
    class GroupService(RuntimeCommitService):
        @staticmethod
        def _load_revision(port, request, revision):
            return copy.deepcopy(before)
    operation = transfer(list(reversed(members)))
    body = request(operation)
    port = Port(body)
    service = GroupService()
    accepted = service.commit(body, port)
    assert accepted['status'] == 'accepted', accepted
    assert accepted['shot_groups'] == [dict(operation_index=0, group=TARGET, created=[], reused=list(reversed(members)), restored=[])]
    assert all(accepted['id_map'][value] == value for value in members)
    assert service.commit(body, port) == accepted and len(port.accepts) == 1


def test_video_transfer_then_images_restores_same_images_on_destination(bundle):
    before, members = source(bundle, 'video')
    moved, _ = apply(before, transfer(members))
    restored, _ = apply(moved, dict(op='shot-group.set', select=None, args=dict(group=TARGET, intent='images')))
    row = restored['parent']['config']['pinnedShotGroups'][1]
    assert row['mode'] == 'images' and row['trackId'] == 'destination'
    assert row['opaque'] == before['parent']['config']['pinnedShotGroups'][1]['opaque']
    for snap in before['parent']['config']['pinnedShotGroups'][1]['imageClipSnapshot']:
        assert states(restored)[snap['authoring']['selector']] == dict(snap['authoring']['clip'], track='destination')


def test_new_lane_rolls_back_if_target_group_collides_after_add(bundle):
    before, members = source(bundle, new_lane=True)
    before['parent']['config']['pinnedShotGroups'].append(dict(shotId='s', trackId='destination', opaque='existing'))
    target = 'parent/track:destination'
    add = dict(op='timeline.add', select=target, args=dict(track=dict(id='destination', kind='visual', label='New')), expect={target + '::': dict(state='absent')})
    draft = Checkout(copy.deepcopy(before))
    with pytest.raises(commands.CommandError, match='collides'):
        draft.batch([add, transfer(members)])
    assert draft.bundle == before


def test_image_transfer_preserves_absent_mode_and_retained_snapshots(bundle):
    video, _ = source(bundle, 'video')
    before, _ = apply(video, call('images'))
    row = before['parent']['config']['pinnedShotGroups'][1]
    row.pop('mode')
    after, plan = apply(before, transfer())
    result = after['parent']['config']['pinnedShotGroups'][1]
    expected = copy.deepcopy(row)
    expected['trackId'] = 'destination'
    for snap in expected['imageClipSnapshot']:
        snap['track'] = snap['authoring']['clip']['track'] = 'destination'
    assert result == expected
    undone, _ = apply(after, inverse_command(plan.calls, before, after, 'absent-mode'))
    assert undone == before
