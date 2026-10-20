import json
from pathlib import Path
P=Path(__file__).parent
D=Path('/home/user/work/wt/vw-m3-audio-compile-vector-reconcile/src/tools/video-editor/data')
view=json.loads((D/'shotCompositionAudio.fixture.json').read_text())
agent=json.loads((D/'shotCompositionAudio.agent.fixture.json').read_text())
refs=json.loads((D/'shotCompositionAudio.reference.json').read_text())
relations=[
 ('unity occurrence gain',[], 'Agent has no child-volume .8/unity occurrence row; absent-volume unity is distinct.'),
 ('missing child volume',['gain-child-absent-is-unity'], 'Same scalar rule; Viewing trim .125..1.125 at .25s versus Agent 0..2 at 0.'),
 ('occurrence mute',['muted-occurrence-silences-child-gain'], 'Same mute rule; different base trim/placement.'),
 ('child times occurrence gain',['gain-child-x-occurrence'], 'Same .8 x .5; different base trim/placement.'),
 ('boost times occurrence gain',['gain-boost-x-occurrence'], 'Same 1.5 x 2; different base trim/placement.'),
 ('occurrence source offset',['source-offset-is-metadata-only'], 'Viewing authored source_offset=350; Agent=.35, retained verbatim as metadata. Viewing volume=.8 and at=.25; Agent volume absent and at=0.'),
 ('occurrence speed without child speed',['occurrence-speed-not-inherited'], 'Same placement speed=1.5; different child trim, volume and placement.'),
 ('source hold capped at next occurrence',[], 'Missing from Agent draft: hold=10, child speed=2, at=.25, occurrence duration=4s; output hold=7.5.'),
 ('source trim capped at next occurrence',[], 'Missing from Agent draft: .125..10.125, child speed=2, at=.25, occurrence duration=4s; output to=7.625.'),
 ('params fades',['fade-in-needs-prepared-envelope-source','fade-out-needs-prepared-envelope-source'], 'Viewing has combined .1s in/out on .05..55, volume=.8, at=.25; Agent separate .5s fades on 0..2, volume absent, at=0.'),
 ('fixture effects shape',[], 'Missing from Agent draft: effects=[{fade_in:.1,fade_out:.1}] is opaque/preserved and is not a public envelope.'),
]
refs_by={(r['corpus'],r['id']):r for r in refs['results']}
def record(corpus,vector):
 key=vector.get('name',vector.get('id'))
 # Read the actual retained closure, not a reimplementation of authored defaults.
 index=next(i for i,r in enumerate(refs['results'],1) if (r['corpus'],r['id'])==(corpus,key))
 full=json.loads((P/f'{corpus}-{index}.json').read_text())
 occurrence=full['graph']['occurrences'][0]
 revision=next(r for r in full['graph']['shot_revisions'] if (r['shot_id'],r['revision_id'])==('shot-alpha','rev-a'))
 child=next(c for c in revision['internal_timeline_revision']['timeline']['clips'] if c['id']=='alpha-audio')
 return {'vector':vector,'actualAuthoredChild':child,'actualAuthoredOccurrence':occurrence,'runtimeClip':refs_by[corpus,key]['clip'],'graphClip':refs_by[corpus,key]['graphClip'],'fullClosureAndOutput':str(P/f'{corpus}-{index}.json')}
rows=[]
used=set()
for name,ids,note in relations:
 used.update(ids)
 rows.append({'viewing':record('viewing',next(v for v in view if v['name']==name)), 'agent':[record('agent',next(v for v in agent['vectors'] if v['id']==key)) for key in ids], 'sameAuthoredInput':False,'reason':note})
mapdata={'viewingRef':'1bfa51d5a','agentRef':refs['agentRef'],'status':'comparison for Agent domain review; neither corpus supersedes the other','rows':rows,'agentOnly':[record('agent',v) for v in agent['vectors'] if v['id'] not in used]}
(P/'audio-corpus-map.json').write_text(json.dumps(mapdata,indent=2)+'\n')
print('map: 11 Viewing rows,',len(used),'related Agent rows,',len(mapdata['agentOnly']),'Agent-only rows; 0 identical authored inputs')
