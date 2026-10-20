from pathlib import Path
import json, os, subprocess, sys
O=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
W=O/'workers/vw-m3-current-native-extent-review'
P=O/'design/handoff-vw-m3-current-native-extent-review'
NODE='/tmp/vw-m3-agent-gate-node20.19.4/bin/node'
PY='/home/user/work/venv-agent/bin/python'
phase=sys.argv[1]
copy=W/phase
E=dict(os.environ)
for k in ['NODE_PATH','NODE_OPTIONS','PYTHONPYCACHEPREFIX']: E.pop(k,None)
E.update(PYTHONPATH=str(copy),PYTHONDONTWRITEBYTECODE='1',PATH=str(Path(NODE).parent)+':'+E['PATH'])
args=[PY,'-B','-m','pytest','-q','-o','addopts=','-p','no:cacheprovider','--tb=short']
rows=[]
def run(label,cmd,expect=0,node=False):
 env=dict(E)
 if node:env.update(NODE_PATH=str(W/'root-modules/node_modules'),ROOT_SOURCE_DIR=str(copy/'remotion/src'))
 log=Path(str(P)+'-'+phase+'-'+label+'.log')
 with log.open('w') as out:r=subprocess.run(cmd,cwd=copy,env=env,stdout=out,stderr=subprocess.STDOUT)
 rows.append({'label':label,'command':cmd,'cwd':str(copy),'environment':{k:env[k] for k in ['PYTHONPATH','NODE_PATH','ROOT_SOURCE_DIR','PYTHONDONTWRITEBYTECODE','PATH'] if k in env},'exit':r.returncode,'expected_exit':expect,'log':str(log)})
 Path(str(P)+'-'+phase+'-results.json').write_text(json.dumps(rows,indent=2)+'\n')
 print(label,r.returncode,'\n'+'\n'.join(log.read_text().splitlines()[-8:]),flush=True)
 assert r.returncode==expect
run('native-controls',args+['tests/packs/rendering/test_remotion_native_window.py','tests/packs/rendering/test_remotion_capture_scene_props.py'])
run('service-neighbors',args+['tests/core/rendering/test_service.py','-k','window_timeline or segment_request'])
run('root-exact',[NODE,str(copy/'remotion/tests/root-metadata.test.cjs')],0 if phase=='candidate' else 1,True)
run('root-supplement',[NODE,str(P)+'-root-supplement.test.cjs'],0 if phase=='candidate' else 1,True)
run('independent',args+[str(P)+'-probe.py'],0 if phase=='candidate' else 1)
if phase=='candidate':run('extent',args+['tests/packs/rendering/test_native_layer_extent.py'])
