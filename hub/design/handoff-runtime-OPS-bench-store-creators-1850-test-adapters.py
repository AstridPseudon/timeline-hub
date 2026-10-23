"""Actual queue writer -> exact dispatcher branch -> staged maker -> real store.
All source/tool/installer stand-ins are explicit, tiny TMPDIR files. No Git
repository, copied venv, network, real installer, test service or daemon runs.
"""
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = Path(__file__).name.removesuffix('test-adapters.py')
ORCH = HERE.parent
ROOT = Path(tempfile.mkdtemp(prefix='creator-fixture-', dir=os.environ['TMPDIR']))
assert ROOT.resolve().is_relative_to(Path(os.environ['TMPDIR']).resolve())
O, W, A, R = [ROOT / name for name in ('orch', 'work', 'agent', 'runtime')]
for directory in (O / 'bin', O / 'tests', O / 'queue/pending', W / 'runtimes', A, R, ROOT / 'tools'):
    directory.mkdir(parents=True)

def write(path, content, executable=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    if executable:
        path.chmod(0o755)

# Exactly approved legacy bytes, copied read-only into this private fixture.
rows = (ORCH / 'tests/suites.conf').read_text().splitlines()
row = next(line for line in rows if line.split()[:2] == ['agent', 'remotion-env-nodes'])
envtext = (ORCH / 'tests/agent-remotion.env').read_text()
assert hashlib.sha256(row.encode()).hexdigest() == 'ffdb0b13c65f106d7b818208343feb3f438dfc943f4af57c5f612ddcf73dc036'
assert hashlib.sha256(envtext.encode()).hexdigest() == 'e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02'
write(O / 'tests/suites.conf', row + '\nagent child-base env PATH=/usr/bin:/bin /home/user/work/venv-agent-child-old/bin/python -c pass\n')
write(O / 'tests/agent-remotion.env', envtext)
for name in ('make-runtime', 'request-runtime', 'make-child-venv', 'request-child-venv'):
    source = (HERE / (PREFIX + name + '.sh')).read_text()
    # Private installed-layout defaults are the only fixture rewriting.
    source = source.replace(str(ORCH), str(O)).replace('/home/user/work/agent', str(A)).replace('/home/user/work/runtime', str(R))
    source = source.replace(':-/home/user/work}', ':-' + str(W) + '}')
    source = source.replace(':-python3.13}', ':-' + str(ROOT / 'tools/fixture-python') + '}')
    write(O / 'bin' / name, source, True)
# One synthetic source DB, consumed by an explicit git stand-in. No real repo.
common = '[project]\nname="{name}"\nversion="0.1.0"\n[tool.setuptools.packages.find]\ninclude={include}\n'
client = {'astrid_runtime_client/__init__.py': 'CLIENT=1\n'}
package = json.dumps({'engines': {'node': '=20.19.4', 'npm': '=10.8.2'}})
lock = json.dumps({'packages': {'node_modules/remotion': {'version': '1.0.0'}, 'node_modules/@banodoco/timeline-composition': {'version': '1.0.0'}}})
agent_files = {'pyproject.toml': common.format(name='astrid', include='["astrid*"]'), 'astrid/__init__.py': 'VERSION=1\n', 'requirements/proof.lock': 'fixture==1\n', **client, 'remotion/package.json': package, 'remotion/package-lock.json': lock}
runtime_files = {'pyproject.toml': common.format(name='astrid-runtime', include='["astrid_runtime*","runtime_protocol*"]'), 'astrid_runtime/__init__.py': 'VERSION=1\n', 'runtime_protocol/__init__.py': 'VERSION=1\n', **{'packages/python/' + p: v for p, v in client.items()}}
db = {'agent': 'a'*40, 'backend': 'b'*40, 'tree': 'c'*40, 'agent_files': agent_files, 'runtime_files': runtime_files}
write(ROOT / 'db.json', json.dumps(db))
write(ROOT / 'tools/git', '''#!/usr/bin/python3
import io,json,os,sys,tarfile
from pathlib import Path
root=Path(__file__).resolve().parent.parent
d=json.loads((root/'db.json').read_text())
a=sys.argv[1:]; checkout=a[1]; a=a[2:]
files=d['agent_files'] if checkout.endswith('/agent') else d['runtime_files']
sha=d['agent'] if checkout.endswith('/agent') else d['backend']
if a[0]=='rev-parse':
 print(d['tree'] if a[-1].endswith(':remotion') else 'true' if a[-1]=='--is-inside-work-tree' else sha)
elif a[0]=='status': pass
elif a[0]=='cat-file':
 if ':' in a[-1] and a[-1].split(':',1)[1] not in files: sys.exit(1)
elif a[0]=='ls-tree':
 print('\\n'.join(sorted(p for p in files if p.startswith('packages/python/astrid_runtime_client/'))))
elif a[0]=='show': sys.stdout.write(files[a[-1].split(':',1)[1]])
elif a[0]=='archive':
 with tarfile.open(fileobj=sys.stdout.buffer,mode='w|') as tar:
  for p,value in files.items():
   if len(a)>2 and not p.startswith(a[2]+'/'): continue
   data=value.encode(); entry=tarfile.TarInfo(p); entry.size=len(data);tar.addfile(entry,io.BytesIO(data))
else: raise SystemExit('unexpected fake git call '+repr(a))
''', True)
write(ROOT / 'tools/fixture-python', '''#!/usr/bin/python3
import base64,csv,hashlib,importlib.metadata as md,json,os,pathlib,shutil,sys,tomllib
me=pathlib.Path(__file__).resolve(); args=sys.argv[1:]; root=me.parent.parent
if args==['--version']: print('Python 3.13.0');sys.exit()
if args[:2]==['-m','venv']:
 if '--help' in args: sys.exit()
 if os.environ.get('FIXTURE_FAIL_VENV')=='1':sys.exit(71)
 with open(os.environ['FIXTURE_EVENTS'],'a') as output:output.write('child-build\\n')
 target=pathlib.Path(args[-1]);(target/'bin').mkdir(parents=True,exist_ok=True)
 shutil.copyfile(me,target/'bin/python');(target/'bin/python').chmod(0o755)
 for name in ['astrid-runtime','astrid-runtime-protocol']:
  (target/'bin'/name).write_text('#!/bin/bash\\nexit 0\\n');(target/'bin'/name).chmod(0o755)
 sys.exit()
site=root/'lib/python3.13/site-packages';site.mkdir(parents=True,exist_ok=True)
if args and args[0]=='-I': args=args[1:]
if args[:2]==['-m','pip']:
 if args[2]=='freeze':
  for dist in md.distributions(path=[str(site)]):
   direct=json.loads((pathlib.Path(dist._path)/'direct_url.json').read_text());print(dist.metadata['Name']+' @ '+direct['url'])
 elif args[2]=='install' and pathlib.Path(args[-1]).is_dir():
  source=pathlib.Path(args[-1]);project=tomllib.loads((source/'pyproject.toml').read_text())['project'];name=project['name'];owned=[]
  for path in source.rglob('*.py'):
   rel=path.relative_to(source)
   if rel.parts[0]=='packages' or rel.parts[0]=='remotion':continue
   dest=site/rel;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(path.read_bytes());owned.append(dest)
  dist=site/(name.replace('-','_')+'-0.1.0.dist-info');dist.mkdir()
  (dist/'METADATA').write_text('Name: '+name+'\\nVersion: 0.1.0\\n');owned.append(dist/'METADATA')
  (dist/'direct_url.json').write_text(json.dumps({'url':source.as_uri(),'dir_info':{'editable':False}}));owned.append(dist/'direct_url.json')
  with (dist/'RECORD').open('w') as f:
   writer=csv.writer(f)
   for path in owned:
    data=path.read_bytes();writer.writerow([path.relative_to(site).as_posix(),'sha256='+base64.urlsafe_b64encode(hashlib.sha256(data).digest()).decode().rstrip('='),len(data)])
   writer.writerow([(dist/'RECORD').relative_to(site).as_posix(),'',''])
 sys.exit()
if args[:2]==['-m','astrid_runtime']:sys.exit()
if args and args[0]=='-c':
 sys.path.insert(0,str(site));sys.dont_write_bytecode=True;sys.argv=['-c',*args[2:]];exec(args[1]);sys.exit()
raise SystemExit('unexpected fixture python '+repr(args))
''', True)
node=W/'toolchain/node-v20.19.4-linux-x64/bin'
write(node/'node', '''#!/usr/bin/python3
import json,os,pathlib,sys
if sys.argv[-1]=='--version':print('10.8.2' if len(sys.argv)>2 else 'v20.19.4');sys.exit()
if 'ci' in sys.argv:
 with open(os.environ['FIXTURE_EVENTS'],'a') as output:output.write('runtime-build\\n')
 root=pathlib.Path.cwd();lock=json.loads((root/'package-lock.json').read_text())
 for name,data in lock['packages'].items():
  dest=root/name/'package.json';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps({'version':data['version']}))
 (root/'node_modules/.package-lock.json').write_text(json.dumps(lock));sys.exit()
if '-e' in sys.argv:print('remotion=1.0.0\\n@banodoco/timeline-composition=1.0.0');sys.exit()
raise SystemExit('unexpected fixture node')
''',True)
write(node/'npm','#!/bin/bash\nprintf "10.8.2\\n"\n',True)
write(node.parent/'lib/node_modules/npm/bin/npm-cli.js','// explicit nonexecuting installer fixture\n')
for tool in ('curl','npm','pip'):
    write(ROOT/'tools'/tool,'#!/bin/bash\necho UNEXPECTED-NETWORK-OR-INSTALLER >&2\nexit 99\n',True)

raw=(ORCH/'bin/dispatcher-daemon').read_text()
branches=[next(line.strip() for line in raw.splitlines() if "'^"+kind+" '" in line) for kind in ('CHILDVENV','RUNTIME')]
context=next(line for line in raw.splitlines() if line.startswith('O=')).replace(str(ORCH),str(O))
write(ROOT/'dispatch', '#!/bin/bash\n'+context+'\nf=$1\nif false; then :\n'+'\n'.join(branches)+'\nelse exit 42; fi\nprintf "%s\\n" "$out"\nexit "$rc"\n',True)
base_env={'PATH':str(ROOT/'tools')+':/usr/bin:/bin','HOME':str(ROOT),'TMPDIR':str(ROOT),'FIXTURE_EVENTS':str(ROOT/'events.txt')}
count=0

def request(kind,args,success=True,minimal=False):
    global count
    script='request-child-venv' if kind=='CHILDVENV' else 'request-runtime'
    env=base_env if minimal else {**os.environ,**base_env}
    command=[str(O/'bin'/script),*args]
    if minimal: command=['/usr/bin/env','-i',*[key+'='+value for key,value in base_env.items()],*command]
    queued=subprocess.run(command,env=env,capture_output=True,text=True)
    assert queued.returncode==0,queued
    pending=O/'queue/pending'/('childvenv-' if kind=='CHILDVENV' else 'runtime-')
    pending=Path(str(pending)+args[0])
    assert pending.read_text()==kind+' '+' '.join(args)+'\n'
    command=[str(ROOT/'dispatch'),str(pending)]
    if minimal: command=['/usr/bin/env','-i',*[key+'='+value for key,value in base_env.items()],*command]
    result=subprocess.run(command,env=env,capture_output=True,text=True)
    (ROOT/('call-'+str(count)+'.log')).write_text(result.stdout+result.stderr)
    count+=1
    assert (result.returncode==0)==success,(args,result)
    print('PASS actual requester/dispatcher/maker',kind,args[0],'rc='+str(result.returncode),flush=True)
    return result

def runtime_args(name):
    return [name,db['agent'],hashlib.sha256(lock.encode()).hexdigest(),str(A),str(R),db['backend'],'remotion-env-nodes']

def events():
    return (ROOT/'events.txt').read_text().splitlines() if (ROOT/'events.txt').exists() else []

if '--build-body-smoke' in sys.argv:
    for component, args in [('runtime', runtime_args('agent-remotion-body')), ('child-venv', ['venv-agent-child-body',db['agent'],'child-base','agent-remotion-body'])]:
        text=(O/'bin'/('make-'+component)).read_text()
        pre=text.split('STORE_HELPER=',1)[0]
        stage=W/('body-'+component)
        stage.mkdir()
        body=text.split('# STORE_BUILD_BEGIN\n',1)[1].split('# STORE_BUILD_END',1)[0]
        if component=='runtime':
            setup='T='+str(stage)+'; D=$T\n'
        else:
            setup='T='+str(stage)+'; D=$T; RUN_ID=smoke; SRC=$T/.child-venv-source-$N; REPORT_DIR=$T; REPORT_TMP=$T/.provision-report; F=$REPORT_TMP; mkdir -p "$SRC"\n'
        result=subprocess.run(['bash','-u','-o','pipefail','-c',pre+'\n'+setup+body,'smoke',*args],env=base_env,capture_output=True,text=True)
        (ROOT/('body-'+component+'.log')).write_text(result.stdout+result.stderr)
        assert result.returncode==0,(component,result)
        if component=='runtime':
            verify=subprocess.run(['bash','-c',pre+'\ncandidate_matches '+str(stage),'smoke',*args],env=base_env,capture_output=True,text=True)
        else:
            verifier=text.split('# STORE_VERIFY_BEGIN\n',1)[1].split('# STORE_VERIFY_END',1)[0]
            identity='\n'.join('packages/python/'+p+'='+hashlib.sha256(v.encode()).hexdigest() for p,v in client.items())
            verify=subprocess.run(['python3','-I','-',str(stage),identity,str(A),db['agent'],str(R),db['backend'],str(W),str(ROOT/'tools/fixture-python')],input=verifier,env=base_env,capture_output=True,text=True)
        assert verify.returncode==0,(component,verify)
        print('PASS exact build body and full custody verifier',component,flush=True)
    print('PASS builder smoke real_installers=0 network=0 fixture='+str(ROOT))
    sys.exit(0)

helper = HERE / 'handoff-runtime-OPS-bench-store-core-resume-1854-bench_store.py'
assert helper.is_file(), 'core source not published yet'
shutil.copyfile(helper, O / 'bin/bench_store.py')
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('bench_store', helper)
core = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = core
spec.loader.exec_module(core)
store = core.Store.initialize(W / 'bench-store', O / 'tests')
if store is None:
    store = core.Store(W / 'bench-store', O / 'tests')

first=request('RUNTIME',runtime_args('agent-remotion-one'),minimal=True)
assert 'status=created' in first.stdout
assert events()==['runtime-build']
second=request('RUNTIME',runtime_args('agent-remotion-two'))
assert 'status=reused' in second.stdout
assert events()==['runtime-build']
assert re.search(r'^runtime=(.*)$',first.stdout,re.M).group(1)==re.search(r'^runtime=(.*)$',second.stdout,re.M).group(1)
db['agent']='d'*40;db['backend']='e'*40;write(ROOT/'db.json',json.dumps(db))
third=request('RUNTIME',runtime_args('agent-remotion-three'),minimal=True)
assert 'status=reused' in third.stdout and 'build_origin_agent_sha='+'a'*40 in third.stdout
child=request('CHILDVENV',['venv-agent-child-one',db['agent'],'child-base','agent-remotion-three'],minimal=True)
child2=request('CHILDVENV',['venv-agent-child-two',db['agent'],'child-base','agent-remotion-three'])
assert 'reused child venv path=' in child2.stdout
assert events()==['runtime-build','child-build']
# Production adapter negatives: restore only the named tiny fixture file.
def negative(path, content, kind, args, writable=False):
    assert path.resolve().is_relative_to(ROOT)
    prior, mode = path.read_bytes(), path.stat().st_mode & 0o777
    try:
        path.chmod(mode | 0o200)
        path.write_bytes(content)
        path.chmod(mode | 0o200 if writable else mode)
        request(kind,args,success=False)
    finally:
        path.chmod(mode | 0o200)
        path.write_bytes(prior)
        path.chmod(mode)
    print('PASS restored negative',path.name,flush=True)
child_path=Path(re.search(r'reused child venv path=(\S+)',child2.stdout).group(1))
site=next((child_path/'lib').glob('python*/site-packages'))
negative(site/'astrid/__init__.py',b'TAMPER=1\n','CHILDVENV',['venv-agent-child-badsource',db['agent'],'child-base','agent-remotion-three'])
record=next(site.glob('astrid-*.dist-info/RECORD'))
negative(record,b'bad-row\n','CHILDVENV',['venv-agent-child-badrecord',db['agent'],'child-base','agent-remotion-three'])
direct=record.parent/'direct_url.json'
value=json.loads(direct.read_text());value['dir_info']['editable']=True
negative(direct,json.dumps(value).encode(),'CHILDVENV',['venv-agent-child-editable',db['agent'],'child-base','agent-remotion-three'])
negative(site/'astrid/__init__.py',(site/'astrid/__init__.py').read_bytes(),'CHILDVENV',['venv-agent-child-writable',db['agent'],'child-base','agent-remotion-three'],writable=True)
negative(child_path/'.astrid-runtime-source-commit',('0'*40+'\n').encode(),'CHILDVENV',['venv-agent-child-marker',db['agent'],'child-base','agent-remotion-three'])
runtime_path=Path(re.search(r'^runtime=(.*)$',third.stdout,re.M).group(1))
negative(runtime_path/'package.json',b'{}','RUNTIME',runtime_args('agent-remotion-tamper'))
negative(O/'tests/agent-remotion.env',envtext.encode()+b'BAD=1\n','RUNTIME',runtime_args('agent-remotion-template'))
negative(node/'node',b'#!/bin/bash\necho v99.0.0\n','RUNTIME',runtime_args('agent-remotion-toolchain'))
assert events()==['runtime-build','child-build'],'negative accidentally invoked builder'
# Supported optional forms register metadata without fabricating a suite.
request('CHILDVENV',['venv-agent-child-twoarg',db['agent']],minimal=True)
request('CHILDVENV',['venv-agent-child-threearg',db['agent'],'child-base'])
assert events()==['runtime-build','child-build']
old_key=core.child_key(db['agent'],db['backend'],{'packages/python/astrid_runtime_client/__init__.py':hashlib.sha256(client['astrid_runtime_client/__init__.py'].encode()).hexdigest()})
db['backend']='f'*40;write(ROOT/'db.json',json.dumps(db))
request('CHILDVENV',['venv-agent-child-backend',db['agent'],'child-base','agent-remotion-three'])
assert len(events())==3
# First child stays leased while a third distinct tuple displaces the unleased one.
with store.acquire(['venv-agent-child-one']):
    db['backend']='1'*40
    db['runtime_files']['packages/python/astrid_runtime_client/__init__.py']='CLIENT=2\n'
    db['agent_files']['astrid_runtime_client/__init__.py']='CLIENT=2\n'
    write(ROOT/'db.json',json.dumps(db))
    request('CHILDVENV',['venv-agent-child-client',db['agent'],'child-base','agent-remotion-three'],minimal=True)
    assert store.registered('venv-agent-child-one')
request('CHILDVENV',['venv-agent-child-client',db['agent'],'child-base','agent-remotion-three'])
try:
    store.registered('venv-agent-child-one')
except core.Refused:
    pass
else:
    raise AssertionError('retired child registration remained usable')
assert store.registered('venv-agent-child-backend')
print('PASS backend/client keys distinct; max2 keeps leased entry; eviction removes only owned projection')
# A real build-stage failure and postbuild registration refusal roll back exact public rows.
with store.acquire(['venv-agent-child-backend','venv-agent-child-client']):
    before=(O/'tests/suites.conf').read_bytes()
    db['backend']='2'*40;write(ROOT/'db.json',json.dumps(db))
    base_env['FIXTURE_FAIL_VENV']='1'
    request('CHILDVENV',['venv-agent-child-buildfail',db['agent'],'child-base','agent-remotion-three'],success=False)
    base_env.pop('FIXTURE_FAIL_VENV')
    assert (O/'tests/suites.conf').read_bytes()==before
    request('CHILDVENV',['venv-agent-child-regfail',db['agent'],'missing-base','agent-remotion-three'],success=False)
    assert (O/'tests/suites.conf').read_bytes()==before
print('PASS build and registration failures preserve exact prior suites')
print('PASS caller integration normal/env-i; tree-only runtime reuse; child exact-key reuse')
size=sum(p.lstat().st_blocks*512 for p in ROOT.rglob('*'))
assert size<20*1024*1024,size
print('PASS footprint allocated='+str(size)+' real_installers=0 network=0 fixture='+str(ROOT))
