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

from astrid.core.element import catalog
if '--reference' in sys.argv:
    declaration = catalog._element_descriptor(catalog._registry().get('transitions', 'cross-fade'))
    print(json.dumps({key: declaration[key] for key in ('id', 'revision', 'kind', 'packId')}))
    sys.exit(0)

value = json.load(sys.stdin)
config = copy.deepcopy(value['config'])
fixture = json.loads((sdk / 'tests/fixtures/timeline_editing/tiny_publishable.json').read_text())
# Retain the admitted synthetic film's picture duration and shot closure.
clips = config.pop('clips')
# Exercise the real canonical authority by default. Legacy flat-only and
# rejected dual authorities are explicit test inputs, never synthesized repairs.
fixture['parent'] = dict(config=config, clips=clips, registry=value['registry'])
if value.get('track_authority') == 'flat':
    fixture['parent']['tracks'] = config.pop('tracks')
elif value.get('track_authority') == 'dual':
    fixture['parent']['tracks'] = copy.deepcopy(config['tracks'])
retain_cut_reservations(fixture)
tl = Checkout(fixture)
# Invalid dual-authority input must reach the commit service intact; resolving
# it locally first would throw outside the provider's returned refusal boundary.
if value.get('track_authority') != 'dual':
    tl.resolve()
before = copy.deepcopy(tl.document())
document = before
results = []
replays = []
ports = []
persisted_documents = []
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
        print(json.dumps(dict(before=before, results=results, result=result, replay=replays, accept_counts=ports, document=document, attempted_accept_count=len(port.accepts), persisted_documents=persisted_documents, source=str(sdk))))
        sys.exit(0)
    assert service.commit(request, port) == result, 'exact replay changed receipt'
    assert len(port.accepts) == 1
    persisted = port.saved['result']['canonical_document']
    assert persisted == result['canonical_document'], 'saved document differs from accepted result'
    persisted_documents.append(copy.deepcopy(persisted))
    document = copy.deepcopy(persisted)
    before_ids = {sid for sid in commands.entity_states(Checkout(before)) if '/clip:' in sid}
    after_ids = {sid for sid in commands.entity_states(Checkout(document)) if '/clip:' in sid}
    assert after_ids == before_ids, 'transition/history changed clip identities'
    results.append(result)
    ports.append(len(port.accepts))
    seen[request['request_id']] = (copy.deepcopy(request), copy.deepcopy(result))
    results_for_wire = result

if len(results) > 1:
    assert results[1]['canonical_document'] == before, 'App history Undo changed authored state'
if len(results) > 2:
    assert results[2]['canonical_document'] == results[0]['canonical_document'], 'App history Redo changed authored state'
print(json.dumps(dict(before=before, results=results, result=results_for_wire, replay=replays,
                     accept_counts=ports, persisted_documents=persisted_documents, source=str(sdk))))
