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
clips = config.pop('clips')
if value.get('mode') == 'stale':
    # Preserve the actual captured App command. The independently loaded current
    # synthetic document changed at the final member/field after capture.
    selected = value['requests'][0]['change']['commands'][-1]['select'].split('/clip:')[1]
    next(clip for clip in clips if clip['id'] == selected)['cropRight'] = 0.99
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
for original in value['requests']:
    request = copy.deepcopy(original)
    if value.get('mode') == 'unsupported':
        request['change']['commands'][-1]['args']['keys'].append('params.unsupported-final-field')
    if value.get('mode') == 'stale':
        assert request == original, 'stale proof altered the captured caller command'
    if request['request_id'] in seen:
        old_request, old_result = seen[request['request_id']]
        assert request == old_request, 'lost-response retry changed the captured request'
        results_for_wire = copy.deepcopy(old_result)
        replays.append(True)
        continue
    port = CallerPort(request)
    port.current = request['base_revision_id']
    result = service.commit(request, port)
    if value.get('mode') in {'stale', 'unsupported'}:
        assert result['status'] == 'refused', result
        if value.get('mode') == 'stale':
            assert 'same-property' in result['error']['message'], result
        assert not port.accepts
        assert document == before
        results_for_wire = result
        break
    assert result['status'] in {'accepted', 'no_change'}, result
    assert service.commit(request, port) == result, 'exact replay changed receipt'
    assert len(port.accepts) == 1
    document = copy.deepcopy(result['canonical_document'])
    assert Checkout(copy.deepcopy(document)).document() == document, 'fresh SDK readback changed authored state'
    before_ids = {sid for sid in commands.entity_states(Checkout(before)) if '/clip:' in sid}
    after_ids = {sid for sid in commands.entity_states(Checkout(document)) if '/clip:' in sid}
    assert after_ids == before_ids, 'position reset/history changed clip identities'
    results.append(result)
    ports.append(len(port.accepts))
    seen[request['request_id']] = (copy.deepcopy(request), copy.deepcopy(result))
    results_for_wire = result

if len(results) > 1:
    assert results[1]['canonical_document'] == before, 'App history Undo changed authored state'
if len(results) > 2:
    assert results[2]['canonical_document'] == results[0]['canonical_document'], 'App history Redo changed authored state'
print(json.dumps(dict(readback=document, before=before, results=results, result=results_for_wire, replay=replays,
                     accept_counts=ports, source=str(sdk))))
