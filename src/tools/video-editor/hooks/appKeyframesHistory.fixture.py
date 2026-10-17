"""App-owned W26 keyframe caller wire proof against exact ASTRID_CHECKOUT, synthetic port only."""
# ruff: noqa: E402 -- import only after binding the task-selected immutable SDK.
import copy
import json
import os
import sys
from pathlib import Path
import tempfile

sdk = Path(os.environ['ASTRID_CHECKOUT'])
sys.path[:0] = [str(sdk), str(sdk / 'tests/sdk')]
from test_timeline_commit import Port
from astrid.core.timeline import scene_answers
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.identity import retain_cut_reservations
from astrid.sdk.timeline import commands

# Same explicit synthetic scene boundary as the sealed SDK proof. No renderer,
# real Runtime store, source patch, or producer test invocation.
class Answers:
    def query_scene(self, *, revision_digest, scene, frames):
        return [dict(frame=frame, coverage='COVERED', content='CONTENT', findings=[], layers=[]) for frame in frames]
scene_answers._client = lambda: Answers()
Checkout._native_outline_integrity = lambda *args: None

value = json.load(sys.stdin)
config = copy.deepcopy(value['config'])
fixture = json.loads((sdk / 'tests/fixtures/timeline_editing/tiny_publishable.json').read_text())
identities = [clip.get('app', {}).get('canonical') for clip in config['clips']]
occurrence = any(identities)
clips = config.pop('clips')
if occurrence:
    assert all(identities)
    internal = dict(tracks=config['tracks'], clips=[identity['sourceClip'] for identity in identities], registry=value['registry'])
    fixture['shots']['A'].update(shot_id='A', payload={'name': 'A'}, base_payload={'name': 'A'},
                               internal_timeline=copy.deepcopy(internal), base_internal_timeline=copy.deepcopy(internal))
    fixture['placements'] = [dict(shot_id='A', occurrence_id='occ-A', placement=dict(start_ms=0), duration_ms=10000)]
    fixture['source_mapping']['shots']['A'].update(revision_id=identities[0]['revisionId'],
        internal_timeline_revision_id=identities[0]['internalTimelineRevisionId'])
    if value.get('variant') == 'refused':
        fixture['source_mapping']['shots']['A']['revision_id'] = 'different-pinned-revision'
    clips = []
if value.get('variant') == 'stale-second-origin':
    second_id = value['requests'][0]['change']['commands'][1]['select'].split('/clip:')[1]
    next(clip for clip in clips if clip['id'] == second_id)['keyframeOrigin'] = 123.125
if value.get('variant') == 'stale-origin':
    clips[0]['keyframeOrigin'] = 123.125
if value.get('variant') == 'stale':
    clips[0]['keyframes'] = {'stale': []}
fixture['parent'] = dict(config=config, clips=clips, registry=value['registry'])
retain_cut_reservations(fixture)
tl = Checkout(fixture)
tl.resolve()
before = copy.deepcopy(tl.document())
document = before
results = []
replays = []
ports = []
seen = {}

class CallerService(RuntimeCommitService):
    @staticmethod
    def _load_revision(port, request, revision):
        # The acceptance double provides this exact immutable synthetic closure.
        return copy.deepcopy(document)

class CallerPort(Port):
    def accept(self, prepared):
        response = super().accept(prepared)
        result = response['stored_result']
        if result['status'] == 'accepted':
            result.update(accepted_revision_id='parent-r' + str(len(results) + 2),
                          accepted_publication_id='pub-parent-r' + str(len(results) + 2))
        self.saved['result'] = copy.deepcopy(result)
        return response

service = CallerService()
for request in value['requests']:
    if request['request_id'] in seen:
        old_request, old_result = seen[request['request_id']]
        assert request == old_request, 'lost-response retry changed the captured request'
        results_for_wire = copy.deepcopy(old_result)
        replays.append(True)
        continue
    port = CallerPort(request)
    port.current = 'advanced-head' if value.get('variant') == 'stale-base' else request['base_revision_id']
    result = service.commit(request, port)
    assert result['status'] in {'accepted', 'no_change', 'refused', 'conflict'}, result
    assert service.commit(request, port) == result, 'exact replay changed receipt'
    assert len(port.accepts) == (1 if result['status'] in {'accepted', 'no_change'} else 0), result
    if result['status'] == 'accepted':
        calls = request['change']['commands']
        if calls and all(call['op'] == 'clip.set' for call in calls):
            # Full-document expectation for this exact caller pair, not a diff writer.
            expected = copy.deepcopy(document)
            for call in calls:
                target = commands.recorded_owner(Checkout(expected), commands.EditCommand.coerce(call), 'clip')
                target.data.update(copy.deepcopy(call['args']))
            assert result['canonical_document'] == expected, 'W26 changed an unowned document field'
            assert len(result['change']['commands']) == len(calls)
            for captured, call in zip(result['change']['commands'], calls):
                # SDK adds version/bindings/created/authorship metadata; all
                # caller-owned fields must remain exact and in command order.
                for field in ('op', 'select', 'resolved', 'args', 'expect'):
                    assert captured[field] == call[field]
        document = copy.deepcopy(result['canonical_document'])
    before_ids = {sid for sid in commands.entity_states(Checkout(before)) if '/clip:' in sid}
    after_ids = {sid for sid in commands.entity_states(Checkout(document)) if '/clip:' in sid}
    assert after_ids == before_ids, 'fade/history allocated or restored clip identities'
    results.append(result)
    ports.append(len(port.accepts))
    seen[request['request_id']] = (copy.deepcopy(request), copy.deepcopy(result))
    results_for_wire = result

if len(results) > 1 and results[1]['status'] == 'accepted':
    assert results[1]['canonical_document'] == before, 'App history Undo changed authored state'
if len(results) > 2 and results[2]['status'] == 'accepted':
    assert results[2]['canonical_document'] == results[0]['canonical_document'], 'App history Redo changed authored state'
with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as directory:
    saved = Path(directory) / 'keyframes.json'
    Checkout(document).save(saved, quiet=True)
    readback = Checkout.load(saved).document()
    assert readback == document
print(json.dumps(dict(readback=readback, before=before, results=results, result=results_for_wire, replay=replays,
                     accept_counts=ports, source=str(sdk))))
