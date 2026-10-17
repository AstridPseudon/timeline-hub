"""App-owned caller wire proof against exact ASTRID_CHECKOUT, synthetic port only."""
# ruff: noqa: E402 -- import only after binding the task-selected immutable SDK.
import copy
import json
import os
import sys
import tempfile
from pathlib import Path

sdk = Path(os.environ['ASTRID_CHECKOUT'])
sys.path[:0] = [str(sdk), str(sdk / 'tests/sdk')]
from test_timeline_commit import Port
from astrid.core.timeline import scene_answers
from astrid.sdk.timeline.checkout import Checkout
from astrid.sdk.timeline.commit import RuntimeCommitService
from astrid.sdk.timeline.identity import retain_cut_reservations

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
fixture['parent'] = dict(config=config, clips=clips, registry=value['registry'])
if value.get('stale'):
    clips[0]['params']['data'] = 'intervening writer'
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
    port.current = request['base_revision_id']
    result = service.commit(request, port)
    assert result['status'] in {'accepted', 'no_change', 'conflict', 'refused'}, result
    assert service.commit(request, port) == result, 'exact replay changed receipt'
    assert len(port.accepts) == (1 if result['status'] in {'accepted', 'no_change'} else 0), result
    if result['status'] == 'accepted':
        document = copy.deepcopy(result['canonical_document'])
    results.append(result)
    ports.append(len(port.accepts))
    seen[request['request_id']] = (copy.deepcopy(request), copy.deepcopy(result))
    results_for_wire = result

if len(results) > 1:
    assert results[1]['canonical_document'] == before, 'App history Undo changed authored state'
if len(results) > 2:
    assert results[2]['canonical_document'] == results[0]['canonical_document'], 'App history Redo changed authored state'
with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as directory:
    saved = Path(directory) / 'params.json'
    Checkout(document).save(saved, quiet=True)
    readback = Checkout.load(saved).document()
    assert readback == document
print(json.dumps(dict(readback=readback, before=before, results=results, result=results_for_wire, replay=replays,
                     accept_counts=ports, source=str(sdk))))
