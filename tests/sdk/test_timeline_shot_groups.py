"""Focused shared shot-group producer proof over synthetic authoritative inputs."""
import copy

import pytest
from test_timeline_graph_commands import closure, opened  # noqa: F401
from test_timeline_saved_publish import synthetic_scene_answers, setup  # noqa: F401
from test_timeline_commit import Port, request

from astrid.sdk.timeline import commands
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService, _digest
from astrid.sdk.timeline.inverse import inverse_command
from astrid.sdk.timeline.rebase import rebase
from astrid.sdk.timeline.shot_groups import identity

pytestmark = pytest.mark.usefixtures("synthetic_scene_answers")
GROUP = dict(shotId="s", trackId="picture")
MEMBERS = ["parent/clip:i1", "parent/clip:i2"]


def call(intent="pin", **args):
    if intent == "pin":
        args.setdefault("members", MEMBERS)
    return dict(op="shot-group.set", select=None, args=dict(group=GROUP, intent=intent, **args))


def remove(*ids):
    return dict(op="shot-group.remove", select=None, args=dict(group=GROUP, remove_clip_ids=list(ids)))


def apply(bundle, *values):
    return RuntimeCommitService._apply(bundle, values)[:2]


@pytest.fixture
def bundle(closure):
    b = opened(closure)
    b["parent"].update(tracks=[dict(id="picture", kind="visual")], clips=[
        dict(id="i1", clipType="media", track="picture", asset="image", at=0, hold=0.5, params=dict(x=3), keyframes=[dict(at=0, x=2)], anchors=dict(start="captured-anchor"), opaque=dict(null=None, literal="i1")),
        dict(id="i2", clipType="media", track="picture", asset="image", at=0.5, hold=0.5, params={}, opaque=[1, None]),
        dict(id="other", clipType="media", track="picture", at=1, hold=1, params={})], registry=dict(assets=dict(image=dict(media_id="sha256:" + "a" * 64, type="image/png"))))
    return b


def selected():
    record = dict(realm_id="realm", project_id="p", asset="video", generation_id="g1", variant_id="v1", object_id="sha256:" + "b" * 64,
                  generation=dict(opaque=None), variant=dict(metadata={}), entry=dict(object_id="sha256:" + "b" * 64, media_type="video/mp4", duration_seconds=2))
    record["catalog_digest"] = _digest(record)
    media = {k: record[k] for k in ("asset", "generation_id", "variant_id", "object_id", "catalog_digest")}
    return media, record


def video_call():
    media, record = selected()
    return call("video", media=media, identities=dict(clip_id="v1"), media_record=record)


def test_pin_unpin_delete_and_selected_group_scope(bundle):
    original = copy.deepcopy(bundle)
    pinned, plan = apply(bundle, call(name="Name"))
    assert pinned["parent"]["clips"] == original["parent"]["clips"]
    row = pinned["parent"]["config"]["pinnedShotGroups"][0]
    row.update(poolGenerationIds=["g"], derivedFrom=None, opaque=dict(keep=True))
    other = dict(shotId="other", trackId="picture", clipIds=["other"], memberSelectors=["parent/clip:other"], mode="images", name="Other")
    pinned["parent"]["config"]["pinnedShotGroups"].append(other)
    updated, _ = apply(pinned, call(name="Updated"))
    assert updated["parent"]["config"]["pinnedShotGroups"][0]["opaque"] == dict(keep=True)
    unpinned, _ = apply(updated, remove())
    assert unpinned["parent"]["clips"] == original["parent"]["clips"]
    assert unpinned["parent"]["config"]["pinnedShotGroups"] == [other]
    deleted, _ = apply(updated, remove(MEMBERS[0]))
    assert [c["id"] for c in deleted["parent"]["clips"]] == ["i2", "other"]
    assert deleted["parent"]["config"]["pinnedShotGroups"] == [other]
    assert bundle == original
    assert identity(GROUP) + "::" in plan.calls[0].expect


def test_video_images_round_trip_exact_metadata_order_and_replacement(bundle):
    pinned, _ = apply(bundle, call())
    video, plan = apply(pinned, video_call())
    row = video["parent"]["config"]["pinnedShotGroups"][0]
    assert row["clipIds"] == ["v1"]
    assert row["imageClipSnapshot"][0]["authoring"]["clip"] == pinned["parent"]["clips"][0]
    assert plan.calls[0].created == ("parent/clip:v1",)
    restored, _ = apply(video, call("images"))
    assert restored["parent"]["clips"] == pinned["parent"]["clips"]
    assert restored["parent"]["registry"]["assets"]["image"] == pinned["parent"]["registry"]["assets"]["image"]
    media, record = selected()
    media["asset"] = record["asset"] = "replacement"
    replaced, _ = apply(video, call("replace-video", media=media, media_record=record))
    assert replaced["parent"]["clips"][0]["id"] == "v1"
    assert replaced["parent"]["clips"][0]["asset"] == "replacement"
    trimmed = copy.deepcopy(video)
    trimmed["parent"]["clips"][0].update(speed=2, hold=.25, **{"from":.25,"to":.75})
    retrimmed, _ = apply(trimmed, call("replace-video", media=media, media_record=record))
    assert {k:retrimmed["parent"]["clips"][0][k] for k in ("from","to","hold","speed")} == {"from":.25,"to":.75,"hold":.25,"speed":2}
    inverse = inverse_command(plan.calls, pinned, video, "pub-video")
    undone, _ = apply(video, inverse)
    assert undone["parent"] == pinned["parent"]


@pytest.mark.parametrize("operation", [call(), remove(), remove(MEMBERS[0]), video_call(), call("images")])
def test_exact_inverse_all_intents(bundle, operation):
    pinned, _ = apply(bundle, call())
    before = bundle if operation == call() else pinned
    if operation["args"].get("intent") == "images":
        before, _ = apply(pinned, video_call())
    after, plan = apply(before, operation)
    inv = inverse_command(plan.calls, before, after, "pub")
    actual, _ = apply(after, inv)
    assert actual["parent"] == before["parent"]


def test_rebase_unrelated_groups_and_conflicting_members_snapshot_registry(bundle):
    pinned, _ = apply(bundle, call())
    _, plan = apply(pinned, video_call())
    other = copy.deepcopy(pinned)
    other["parent"]["config"]["pinnedShotGroups"].append(dict(shotId="other", trackId="picture", clipIds=["other"], mode="images"))
    assert not rebase(plan.calls, other).conflicts
    for mutate in (lambda b: b["parent"]["clips"][0].update(opaque="changed"),
                   lambda b: b["parent"]["registry"]["assets"]["image"].update(type="image/jpeg"),
                   lambda b: b["parent"]["config"]["pinnedShotGroups"][0].update(name="changed")):
        head = copy.deepcopy(pinned)
        mutate(head)
        assert rebase(plan.calls, head).conflicts


@pytest.mark.parametrize("mutation", ["duplicate", "bare", "reserved", "ambiguous", "delete-other"])
def test_refusal_is_atomic(bundle, mutation):
    pinned, _ = apply(bundle, call())
    bad = video_call()
    if mutation == "duplicate":
        pinned["parent"]["config"]["pinnedShotGroups"] *= 2
    elif mutation == "bare":
        bad = call(members=["i1"])
    elif mutation == "reserved":
        bad["args"]["identities"]["clip_id"] = "other"
    elif mutation == "ambiguous":
        pinned["parent"]["clips"].append(copy.deepcopy(pinned["parent"]["clips"][0]))
    else:
        bad = remove("parent/clip:other")
    tl = Checkout(copy.deepcopy(pinned))
    original = copy.deepcopy(tl.bundle)
    with pytest.raises(commands.CommandError):
        tl.batch([bad])
    assert tl.bundle == original


def test_stale_track_only_unambiguous_destination(bundle):
    pinned, _ = apply(bundle, call())
    pinned["parent"]["config"]["pinnedShotGroups"][0]["trackId"] = "stale"
    operation = video_call()
    operation["args"]["group"] = dict(GROUP, trackId="stale")
    corrected, plan = apply(pinned, operation)
    assert corrected["parent"]["config"]["pinnedShotGroups"][0]["trackId"] == "picture"
    assert identity(dict(GROUP, trackId="stale")) + "::" in plan.calls[0].expect
    assert identity(GROUP) + "::" in plan.calls[0].expect


def test_commit_exact_media_capture_replay_and_id_map(bundle):
    pinned, _ = apply(bundle, call())
    operation = video_call()
    record = operation["args"].pop("media_record")
    body = request(operation)
    class GroupService(RuntimeCommitService):
        @staticmethod
        def _load_revision(port, request, rid):
            return copy.deepcopy(pinned)
    port = Port(body)
    reads = []
    port.selected_media = lambda selection: (reads.append(selection) or copy.deepcopy(record))
    service = GroupService()
    result = service.commit(body, port)
    assert result["status"] == "accepted", result
    assert service.commit(body, port) == result
    assert len(reads) == len(port.accepts) == 1
    assert result["id_map"]["parent/clip:v1"] == "parent/clip:v1"


def test_child_owner_round_trip_after_materialization_and_snapshot_reservation(bundle, closure):
    from astrid.core.timeline.authoring_bundle import compile_authoring_candidate, open_authoring_bundle
    b = copy.deepcopy(bundle)
    placement = b['placements'][0]
    owner = placement['shot_id']
    child = b['shots'][owner]['internal_timeline']
    child['clips'] = copy.deepcopy(b['parent']['clips'][:2])
    child['registry'] = copy.deepcopy(b['parent']['registry'])
    child_members = ['occurrence:a/clip:i1', 'occurrence:a/clip:i2']
    pin = call(members=child_members)
    pinned, _ = apply(b, pin)
    video_op = video_call()
    video, plan = apply(pinned, video_op)
    pub = compile_authoring_candidate(video).publication
    parent = dict(project_id='p', timeline_id='t', revision_id='child-video', payload=pub['parent_composition'], content_digest=_digest(pub['parent_composition']))
    reopened = open_authoring_bundle(parent, shot_revisions=[*closure['shot_revisions'], *[dict(r,project_id='p') for r in pub['shot_revisions']]], internal_timeline_revisions=[*closure['internal_timeline_revisions'], *[dict(r,project_id='p') for r in pub['internal_timeline_revisions']]])
    restored, _ = apply(reopened, call('images'))
    current_shot = restored['placements'][0]['shot_id']
    assert restored['shots'][current_shot]['internal_timeline']['clips'] == child['clips']
    assert restored['shots'][restored['placements'][1]['shot_id']] == reopened['shots'][reopened['placements'][1]['shot_id']]
    # Ordinary additions must not steal IDs retained in a dormant snapshot.
    collision = dict(op='timeline.add',select=None,args={'from':'occurrence:a/clip:v1','clip_id':'i1'})
    with pytest.raises(commands.CommandError):
        apply(video, collision)


def test_restore_refuses_active_collision_and_shared_owner_ambiguity(bundle):
    pinned, _ = apply(bundle, call())
    video, _ = apply(pinned, video_call())
    video['parent']['clips'].append(copy.deepcopy(bundle['parent']['clips'][0]))
    original = copy.deepcopy(video)
    with pytest.raises(commands.CommandError):
        apply(video, call('images'))
    assert video == original


def test_queued_group_suffix_survives_acknowledgment(setup):
    from astrid.sdk.timeline import saved_publish
    from pathlib import Path
    draft, runtime = setup
    clip = draft.clip('c1.rocket')
    selector = commands.scoped_clip(draft, clip)
    placement = next(r for r in draft.bundle['placements'] if r['shot_id'] == clip.shot_id)
    source = draft.bundle['source_mapping']['shots'][clip.shot_id]
    group = dict(shotId=source['shot_id'], trackId=clip.data['track'])
    pin = dict(op='shot-group.set',select=None,args=dict(group=group,intent='pin',members=[selector]))
    commands.run(draft, pin)
    runtime.unavailable = True
    draft.publish(idempotency_key='group-pending',client=runtime.client())
    first = runtime.calls[0][0]
    commands.run(draft,dict(op='shot-group.remove',select=None,args=dict(group=group,remove_clip_ids=[])))
    suffix = Path(draft.path).read_bytes()
    runtime.unavailable = False
    result = Checkout.load(draft.path).publish(client=runtime.client())
    assert runtime.calls[-1][0] == first
    assert result['local_state'] == saved_publish._RETAINED
    assert Path(draft.path).read_bytes() == suffix


def test_rebase_unrelated_clip_addition_preserves_requested_scope(bundle):
    pinned, _ = apply(bundle, call())
    _, plan = apply(pinned, video_call())
    unrelated=copy.deepcopy(pinned)
    unrelated['parent']['tracks'].append(dict(id='text',kind='visual'))
    unrelated['parent']['clips'].append(dict(id='unrelated',track='text',clipType='media',at=0,hold=1,params={}))
    rebased=rebase(plan.calls,unrelated)
    assert not rebased.conflicts
    assert rebased.document['parent']['clips'][-1]['id']=='unrelated'
    changed=copy.deepcopy(pinned)
    changed['parent']['clips'][:2]=reversed(changed['parent']['clips'][:2])
    assert rebase(plan.calls,changed).conflicts


def test_saved_video_request_recaptures_media_and_retains_suffix(bundle,tmp_path,monkeypatch):
    import json
    from pathlib import Path
    from test_timeline_saved_publish import RuntimeFixture
    from astrid.sdk.timeline import saved_publish, store
    monkeypatch.setenv('BANODOCO_LOCAL_DATA_ROOT',str(tmp_path/'data'))
    monkeypatch.setattr(Checkout,'SAY_SAVED',False)
    materialized=copy.deepcopy(bundle)
    for source in materialized["source_mapping"]["shots"].values():
        source["linked"]=False
    runtime=RuntimeFixture(bundle=materialized)
    workspace=runtime.client()
    exact=saved_publish._exact(workspace,dict(project_id='p',timeline_id='t',base_revision_id='rev-0'),'rev-0')
    monkeypatch.setattr(store,'resolve_ids',lambda *a,**kw:('p','t','rev-0'))
    monkeypatch.setattr(store,'fetch_bundle',lambda *a,**kw:copy.deepcopy(exact))
    draft=Checkout.draft('p','t')
    commands.run(draft,call())
    commands.run(draft,video_call())
    port=runtime.port
    media,record=selected()
    reads=[]
    def selected_port(body):
        result=port(body)
        result.selected_media=lambda selection:(reads.append(copy.deepcopy(selection)) or copy.deepcopy(record))
        return result
    monkeypatch.setattr(runtime,'port',selected_port)
    runtime.unavailable=True
    draft.publish(idempotency_key='video-pending',client=runtime.client())
    first=runtime.calls[0][0]
    submitted=json.loads(first)
    assert all('media_record' not in value['args'] for value in submitted['change']['commands'])
    commands.run(draft,call('images'))
    suffix=Path(draft.path).read_bytes()
    runtime.unavailable=False
    result=Checkout.load(draft.path).publish(client=runtime.client())
    assert result['status']=='accepted',result
    assert runtime.calls[-1][0]==first and reads==[media]
    assert result['local_state']==saved_publish._RETAINED
    assert Path(draft.path).read_bytes()==suffix


def test_group_inverse_restores_absent_config_without_changing_other_fields(bundle):
    before=copy.deepcopy(bundle)
    before['parent'].pop('config',None)
    after,plan=apply(before,call())
    restored,_=apply(after,inverse_command(plan.calls,before,after,'pin-absent-config'))
    assert restored['parent']==before['parent']
    assert commands.state_at(commands.entity_states(Checkout(bundle)),'parent','config')=={'state':'present','value':{}}
