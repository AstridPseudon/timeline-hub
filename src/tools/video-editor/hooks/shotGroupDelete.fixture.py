"""App-owned caller wire proof against exact ASTRID_CHECKOUT, synthetic port only."""
# ruff: noqa: E402 -- import only after binding the task-selected immutable SDK.
import copy
import json
import os
import sys
from pathlib import Path

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
    mapping = {clip['id']: identity['sourceClipId'] for clip, identity in zip(clips, identities)}
    for group in config['pinnedShotGroups']:
        group['clipIds'] = [mapping.get(id, id) for id in group['clipIds']]
    internal = dict(tracks=config['tracks'], clips=[identity['sourceClip'] for identity in identities], registry=value['registry'])
    fixture['shots']['A'].update(shot_id='A', payload={'name': 'A'}, base_payload={'name': 'A'},
                               internal_timeline=copy.deepcopy(internal), base_internal_timeline=copy.deepcopy(internal))
    fixture['placements'] = [dict(shot_id='A', occurrence_id='occ-A', placement=dict(start_ms=0), duration_ms=10000)]
    clips = []
fixture['parent'] = dict(config=config, clips=clips, registry=value['registry'])
retain_cut_reservations(fixture)
tl = Checkout(fixture)
tl.resolve()
before = copy.deepcopy(tl.document())
document = before
results = []
persisted_documents = []
revision_reads = []
replays = []
ports = []
seen = {}

class CallerService(RuntimeCommitService):
    @staticmethod
    def _load_revision(port, request, revision):
        # The acceptance double provides this exact immutable synthetic closure.
        revision_reads.append(revision)
        return copy.deepcopy(document)

class CallerPort(Port):
    def accept(self, prepared):
        response = super().accept(prepared)
        result = response['stored_result']
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
    port.current = request['base_revision_id']
    result = service.commit(request, port)
    if result['status'] != 'accepted':
        print(json.dumps(dict(before=before, document=document, results=results, result=result, attempted_accept_count=len(port.accepts), accept_counts=ports, persisted_documents=persisted_documents, source=str(sdk))))
        sys.exit(0)
    assert service.commit(request, port) == result, 'exact replay changed receipt'
    assert len(port.accepts) == 1
    assert port.saved['result']['canonical_document'] == result['canonical_document']
    document = copy.deepcopy(port.saved['result']['canonical_document'])
    persisted_documents.append(copy.deepcopy(document))
    before_ids = {sid for sid in commands.entity_states(Checkout(before)) if '/clip:' in sid}
    after_ids = {sid for sid in commands.entity_states(Checkout(document)) if '/clip:' in sid}
    assert after_ids <= before_ids, 'delete/history allocated foreign clip identities'
    results.append(result)
    ports.append(len(port.accepts))
    seen[request['request_id']] = (copy.deepcopy(request), copy.deepcopy(result))
    results_for_wire = result

if len(results) > 1:
    assert results[1]['canonical_document'] == before, 'App history Undo changed authored state'
if len(results) > 2:
    assert results[2]['canonical_document'] == results[0]['canonical_document'], 'App history Redo changed authored state'
print(json.dumps(dict(before=before, results=results, result=results_for_wire, replay=replays,
                     accept_counts=ports, persisted_documents=persisted_documents, revision_reads=revision_reads, source=str(sdk))))
