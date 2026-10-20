import json,os,shlex,subprocess
from pathlib import Path
O=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch');W=O/'workers/vw-m3-tab-clean-install-final-gate';D=O/'design';S=Path('/home/user/work/wt/vw-m3-tab-clean-install-source-compose');N='/tmp/vw-m3-agent-gate-node20.19.4/bin/node';G=O/'workers/vw-m3-app-private12-clean-install/clean-project/node_modules'
assert (D/'handoff-vw-m3-tab-clean-install-source-compose-READY').exists()
assert (O/'workers/vw-m3-tab-clean-install-source-compose/DONE').exists()
for name in ['tmp','cache','config','transform','output']:(W/name).mkdir(exist_ok=True)
env=dict(os.environ,TMPDIR=str(W/'tmp'),TMP=str(W/'tmp'),TEMP=str(W/'tmp'),XDG_CACHE_HOME=str(W/'cache'),XDG_CONFIG_HOME=str(W/'config'),PWTEST_CACHE_DIR=str(W/'transform'),NODE_PATH='',NODE_OPTIONS='--import='+str(W/'write-guard.mjs'))
env['PATH']=str(Path(N).parent)+':'+env['PATH']
commands=[
 ('analysis',[N,str(S/'tests/e2e/timeline/tab-audio-capture.analysis.test.mjs')]),
 ('controller',[N,str(S/'tests/e2e/timeline/tab-audio-capture.controller.test.mjs')]),
 ('environment',[N,str(S/'tests/e2e/timeline/tab-audio-capture.environment.test.mjs')]),
 ('fingerprint',[N,str(S/'tests/e2e/timeline/tab-audio-capture.controller.mjs'),'--fingerprint']),
 ('discovery',[N,str(G/'playwright/cli.js'),'test','--config',str(S/'tests/e2e/timeline/tab-audio-capture.config.ts'),'--project=native-codec-chrome155-tab-audio','--output',str(W/'output'),'--list']),
 ('shell',['bash','-n',str(S/'tests/e2e/timeline/setup-tab-audio-capture.sh')]),
 ('independent-controls',[N,str(W/'independent-controls.mjs')]),
]
results=[]
for name,command in commands:
 r=subprocess.run(command,cwd=S,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 log=D/('handoff-vw-m3-tab-clean-install-final-gate-'+name+('.json' if name=='fingerprint' else '.log'))
 log.write_text(r.stdout if name=='fingerprint' and r.returncode==0 else r.stdout+r.stderr)
 results.append(dict(name=name,command=command,cwd=str(S),exit=r.returncode,stdoutArtifact=str(log),stderr=r.stderr))
 print(name,r.returncode,flush=True)
(D/'handoff-vw-m3-tab-clean-install-final-gate-commands.json').write_text(json.dumps({'environment':{k:env[k] for k in ['TMPDIR','TMP','TEMP','XDG_CACHE_HOME','XDG_CONFIG_HOME','PWTEST_CACHE_DIR','NODE_PATH','NODE_OPTIONS','PATH']},'commands':results},indent=2)+'\n')
assert not any(r['exit'] for r in results),results
