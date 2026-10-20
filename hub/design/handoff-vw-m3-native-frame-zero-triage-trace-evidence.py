import json
from pathlib import Path
from zipfile import ZipFile
orch=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
p=Path('/tmp/viewing-native-frame-parity-2EZi8v/player-export-normal-profi-1fbe1-al-CPU-Remotion-task-output-native-codec-chrome155/trace.zip')
with ZipFile(p) as z:
 trace=[json.loads(l) for l in z.read('0-trace.trace').decode().splitlines()]
snapshots=[v['snapshot'] for v in trace if v['type']=='frame-snapshot']
cache={}
def nodes(index):
 if index not in cache:
  out=[]
  def visit(n):
   if isinstance(n,str):out.append(n)
   elif isinstance(n,list) and n and isinstance(n[0],str):
    for c in n[2:]:visit(c)
    out.append(n)
  visit(snapshots[index]['html']);cache[index]=out
 return cache[index]
def resolve(n,index):
 if isinstance(n,list) and n and isinstance(n[0],list):
  delta,node=n[0];return resolve(nodes(index-delta)[node],index-delta)
 if isinstance(n,list) and n and isinstance(n[0],str):return [n[0],n[1],*[resolve(c,index) for c in n[2:]]]
 return n
screenshot=next(v for v in trace if v.get('stepId')=='pw:api@256' and v.get('type')=='before')
index=next(i for i,s in enumerate(snapshots) if s['snapshotName']==screenshot['beforeSnapshot'])
root=resolve(snapshots[index]['html'],index)
selected=[]
def attrs_only(n):
 a=n[1]
 keys=['class','style','role','data-testid','data-open','data-dialog-backdrop','data-dialog-content','data-video-editor-render-player','data-frame-parity-native-host','src','controls']
 return {'tag':n[0],**{k:a[k] for k in keys if k in a}}
def walk(n,ancestors):
 if not isinstance(n,list) or not n or not isinstance(n[0],str):return
 a=n[1]
 if n[0]=='IMG' or '__remotion-player' in a.get('class','') or any(k in a for k in ['data-video-editor-render-player','data-dialog-backdrop','data-frame-parity-native-host']):
  selected.append({'element':attrs_only(n),'ancestors':[attrs_only(v) for v in ancestors[-7:]]})
 for child in n[2:]:walk(child,ancestors+[n])
walk(root,[])
ids={'call@1028','call@1038','call@1052'}
values=[{k:v[k] for k in ['callId','result','afterSnapshot'] if k in v} for v in trace if v.get('type')=='after' and v.get('callId') in ids]
evidence={'qualification':'Retained DOM snapshot only, no browser launch or computed layout re-evaluation. Whitelisted attributes exclude task/auth inputs. Subtree references expanded using Playwright snapshotNodes postorder semantics.', 'trace':str(p),'screenshotLocatorResolutionCall':{k:screenshot[k] for k in ['callId','method','params','beforeSnapshot']},'snapshot':{k:snapshots[index][k] for k in ['snapshotName','viewport','timestamp']},'returnedPlayerValues':values,'selectedDOM':selected}
(orch/'design/handoff-vw-m3-native-frame-zero-triage-trace-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n')
print(json.dumps({'snapshot':evidence['snapshot'],'screenshotLocatorResolutionCall':evidence['screenshotLocatorResolutionCall'],'selectedDOMCount':len(selected),'PlayerValues':values},indent=2))
