import copy
import hashlib
import json
import subprocess
import tarfile
from pathlib import Path
from astrid.core.timeline.shot_composition_projection import project_runtime_parent_composition, project_shot_composition

P = Path(__file__).parent
ROOT = Path('/home/user/work/wt/vw-m3-audio-compile-vector-reconcile')
D = ROOT / 'src/tools/video-editor/data'
REF = 'fd82c36c7cd66d1d58aa0250a008245a43e6fbaa'
AGENT = Path('/home/user/work/agent')
for name in ['shot_composition_projection.py', 'duration.py', 'shot_composition.py']:
    path = 'astrid/core/timeline/' + name
    assert (AGENT / path).read_bytes() == subprocess.check_output(['git', '-C', str(AGENT), 'show', REF + ':' + path])
artifact = P.parent / 'vw-m3-envelope-public-clock-join/artifact/package'
tarpath = P.parents[1] / 'artifacts/banodoco-timeline-composition-0.0.11.tgz'
assert hashlib.sha256(tarpath.read_bytes()).hexdigest() == 'dfa824a475737598477d98a2be2c2ad6ab9c3e6c8b0f967fad22e154afd74601'
with tarfile.open(tarpath) as archive:
    members = [m for m in archive.getmembers() if m.isfile()]
    for member in members:
        assert archive.extractfile(member).read() == (artifact / member.name.removeprefix('package/')).read_bytes()
print('public11: exact archive/extraction verified:', len(members), 'files')

viewing = json.loads((D / 'shotCompositionAudio.fixture.json').read_text())
agent = json.loads((D / 'shotCompositionAudio.agent.fixture.json').read_text())

def graph_for(corpus, vector):
    graph = json.loads((D / ('shotComposition.fixture.json' if corpus == 'viewing' else 'shotCompositionAudio.agentGraph.fixture.json')).read_text())
    revision = next(r for r in graph['shot_revisions'] if (r['shot_id'], r['revision_id']) == ('shot-alpha', 'rev-a'))
    clips = revision['internal_timeline_revision']['timeline']['clips']
    if corpus == 'viewing':
        graph['occurrences'][0].update(duration_ms=4000, **vector['occurrence'])
        clips[1] = {'id': 'alpha-audio', 'clip_type': 'media', 'track': 'audio', 'at': 0.25, **vector['clip']}
    else:
        graph['occurrences'][0].update(vector['occurrence'])
        child = next(c for c in clips if c['id'] == 'alpha-audio')
        child.pop('duration_ms')
        child.update(agent['base']['child_default'])
        child.update(vector['child'])
    return graph

# Transport reshaping only: exact pins, payloads and authored occurrence values.
def closure_for(graph):
    shots, internals = [], []
    for row in graph['shot_revisions']:
        internal = row['internal_timeline_revision']
        shots.append({**copy.deepcopy(row), 'internal_timeline_revision_id': internal['revision_id']})
        internals.append({'revision_id': internal['revision_id'], 'payload': copy.deepcopy(internal['timeline'])})
    return {'parent_revision': {
        'project_id': graph['project']['project_id'],
        'timeline_id': graph['primary_timeline']['document_id'],
        'revision_id': graph['primary_timeline']['head']['revision_id'],
        'payload': {'config': {}, **copy.deepcopy(graph.get('parent_composition', {})), 'occurrences': copy.deepcopy(graph['occurrences']), 'registry': {'assets': {}}}},
        'shot_revisions': shots, 'internal_timeline_revisions': internals}

results = []
for corpus, vectors in [('viewing', viewing), ('agent', agent['vectors'])]:
    for vector in vectors:
        graph = graph_for(corpus, vector)
        before = copy.deepcopy(graph)
        closure = closure_for(graph)
        original = copy.deepcopy(closure)
        projected = project_runtime_parent_composition(**closure)
        legacy = project_shot_composition(graph)
        assert graph == before and closure == original and projected.graph == original
        pick = lambda projection: next(c for c in projection.config['clips'] if c['id'] == 'occ-1:alpha-audio')
        results.append({'corpus': corpus, 'id': vector.get('name', vector.get('id')), 'clip': pick(projected), 'graphClip': pick(legacy)})
        # Complete source inputs and output are retained outside the product tree.
        (P / (corpus + '-' + str(len(results)) + '.json')).write_text(json.dumps({'vector': vector, 'graph': graph, 'closure': closure, 'projection': projected.as_dict()}, indent=2) + '\n')
(D / 'shotCompositionAudio.reference.json').write_text(json.dumps({'agentRef': REF, 'results': results}, indent=2) + '\n')
print('existing Agent projectors:', len(results), 'unchanged graphs/exact closures')
