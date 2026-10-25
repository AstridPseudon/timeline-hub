import ast,hashlib,json,pathlib,subprocess
from collections import Counter
M=pathlib.Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D108-rehearsal-source-0645/../rt-F-D108-rehearsal-source-0645/evidence/d108-source-rehearsal-manifest.json')
# use explicit absolute path above may normalize through ..
M=pathlib.Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-F-D108-rehearsal-source-0645/evidence/d108-source-rehearsal-manifest.json');d=json.loads(M.read_text());repos={'agent':'/home/user/peteromallet/astrid-agent','runtime':'/home/user/banodoco/banodoco-workspace-runtime'}
def show(repo,ref,p):
 q=subprocess.run(['git','-C',repo,'show',f'{ref}:{p}'],capture_output=True,text=True);return q.stdout if q.returncode==0 else ''
def parse(s):
 try:t=ast.parse(s)
 except: return {}
 o={}
 def rec(xs,p=''):
  for n in xs:
   if isinstance(n,ast.ClassDef): rec(n.body,p+n.name+'.')
   elif isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) and n.name.startswith('test'):
    q=p+n.name; ds=' '.join(ast.dump(x,include_attributes=False) for x in n.decorator_list)
    o[q]={'h':hashlib.sha256((ast.get_source_segment(s,n) or '').encode()).hexdigest(),'a':Counter(ast.dump(x.test,include_attributes=False) for x in ast.walk(n) if isinstance(x,ast.Assert)),'ops':Counter(type(op).__name__ for x in ast.walk(n) if isinstance(x,ast.Compare) for op in x.ops),'skip':ds.count('skip'),'xfail':ds.count('xfail'),'param':ds.count('parametrize')}
 rec(t.body);return o
for name,repo in repos.items():
 r=d['repositories'][name];rows=[x for x in r['source_upstream_blobs'] if x['path'].endswith('.py') and ('tests/' in x['path'] or '/tests/' in x['path'])];U={};A={}
 for x in rows:
  p=x['path'];us=show(repo,r['fresh_upstream']['commit'],p);ap=show(repo,r['captured_integration']['commit'],p) if x['status'] in ('A','M') else ''
  U.update({p+':'+k:v for k,v in parse(us).items()});A.update({p+':'+k:v for k,v in parse(ap).items()})
 common=set(U)&set(A);miss=set(U)-set(A);add=set(A)-set(U);changed={k for k in common if U[k]['h']!=A[k]['h']};rem=sum((U[k]['a']-A[k]['a']).total() for k in common);addassert=sum((A[k]['a']-U[k]['a']).total() for k in common);eqdec=sum(max(0,U[k]['ops']['Eq']-A[k]['ops']['Eq']) for k in common);ininc=sum(max(0,A[k]['ops']['In']-U[k]['ops']['In']) for k in common);skip=sum(max(0,A[k]['skip']-U[k]['skip']) for k in common);xfail=sum(max(0,A[k]['xfail']-U[k]['xfail']) for k in common);param=sum(max(0,U[k]['param']-A[k]['param']) for k in common)
 print(name,'up',len(U),'applied',len(A),'missing',len(miss),'added',len(add),'changed',len(changed),'removed_assert_fp',rem,'added_assert_fp',addassert,'Eq_dec',eqdec,'In_inc',ininc,'skip_add',skip,'xfail_add',xfail,'param_drop',param)
