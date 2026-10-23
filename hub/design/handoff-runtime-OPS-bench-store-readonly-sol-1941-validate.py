"""Read-only packet integrity, syntax, replay and Runtime product checks."""
import argparse
import ast
from collections import Counter
import difflib
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
P = 'handoff-runtime-OPS-bench-store-readonly-sol-1941-'
def file(suffix): return HERE / (P + suffix)
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def run(*args, **kwargs):
    return subprocess.run(args, check=True, capture_output=True, text=True, **kwargs).stdout

def functions(source, cls):
    node = next(n for n in ast.parse(source).body if isinstance(n, ast.ClassDef) and n.name == cls)
    return {n.name: ast.get_source_segment(source,n) for n in node.body if isinstance(n, ast.FunctionDef)}

def assertions(source):
    return Counter(ast.dump(n) for n in ast.walk(ast.parse(source)) if isinstance(n,ast.Assert))

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--originals', action='store_true', help='also check immutable historical dependencies')
parser.add_argument('--runtime', type=Path, default=Path.cwd())
args=parser.parse_args()
manifest=file('hashmanifest.sha256')
names=set()
for line in manifest.read_text().splitlines():
    expected,name=line.split('  ',1)
    assert Path(name).name==name and name.startswith(P)
    assert sha(HERE/name)==expected,name
    assert name not in names;names.add(name)
assert names=={p.name for p in HERE.glob(P+'*') if p!=manifest}
print('PASS manifest',len(names),'files')
before=json.loads(file('source-before.json').read_text())
assert before==json.loads(file('source-after.json').read_text())
if args.originals:
    for name,expected in before.items():
        path=Path(name) if Path(name).is_absolute() else HERE/name
        assert sha(path)==expected,name
print('PASS source before/after',len(before),'immutable inputs; originals='+str(args.originals))
original=functions(file('input-bench_store.py').read_text(),'Store')
current=functions(file('bench_store.py').read_text(),'Store')
changed={name for name in original if original[name]!=current[name]}
assert changed=={'ensure','recover','_delete_owned'},changed
assert sha(file('input-bench_store.py'))=='88ae9e5af3425639b7eba0b79aa6b84e78a319fe810c0c6a2d3ceece1be8b5f3'
for suffix in ('request-child-venv.sh','request-runtime.sh'):
    assert file(suffix).read_bytes()==file('input-'+suffix).read_bytes()
old=assertions(file('input-test-adapters.py').read_text())
new=assertions(file('test-adapters.py').read_text())
assert not old-new,old-new
old_child=file('input-make-child-venv.sh').read_text()
child=file('make-child-venv.sh').read_text()
assert old_child.split('# STORE_VERIFY_BEGIN\n',1)[1]==child.split('# STORE_VERIFY_BEGIN\n',1)[1]
assert 'readonly-final' not in child and 'seal=seal' in child
assert 'seal=seal' in file('make-runtime.sh').read_text()
print('PASS minimal lifecycle hunks; identical child final custody; all original adapter assertions retained')
blocks=0
for path in HERE.glob(P+'*.py'):
    compile(path.read_bytes(),str(path),'exec')
for suffix in ('make-child-venv.sh','make-runtime.sh','request-child-venv.sh','request-runtime.sh','test-run'):
    source=file(suffix).read_text();run('bash','-n',str(file(suffix)))
    for match in re.finditer(r"<<'([A-Z_]+)'\n(.*?)\n\1(?:\n|$)",source,re.S):
        tag,body=match.groups()
        if tag in {'STORE_PY','PY','RELOCATE','BENCH_LEASE_PY'}:
            compile(body,str(file(suffix))+':'+tag,'exec');blocks+=1
    if suffix=='make-child-venv.sh':
        for tag in ('PROVENANCE_SCRIPT','DIST_METADATA_SCRIPT','IDENTITY_SCRIPT'):
            code=source.split("\n"+tag+"='",1)[1].split("'\nrun_stage",1)[0]
            compile(code,str(file(suffix))+':'+tag,'exec');blocks+=1
        code=source.split('# STORE_VERIFY_BEGIN\n',1)[1].split('# STORE_VERIFY_END',1)[0]
        compile(code,str(file(suffix))+':custody','exec');blocks+=1
print('PASS bash syntax, all Python files,',blocks,'embedded Python blocks')
# Replay only into a new tiny TMPDIR directory; compare exact resulting bytes.
with tempfile.TemporaryDirectory(prefix='d27-replay-',dir=os.environ['TMPDIR']) as temp:
    root=Path(temp)
    for suffix in ('bench_store.py','make-child-venv.sh','make-runtime.sh','request-child-venv.sh','request-runtime.sh','test-adapters.py'):
        target=root/suffix;target.write_bytes(file('input-'+suffix).read_bytes())
        patch=file(suffix+'.patch').read_text()
        if patch:
            run('patch','--batch','--fuzz=0','-p0','-d',str(root),input=patch)
        run('cmp','--',str(target),str(file(suffix)))
print('PASS six incremental patch replay/cmp, zero fuzz')
for root in (args.runtime.resolve(),Path('/home/user/work/runtime')):
    assert run('git','-C',str(root),'rev-parse','HEAD').strip()=='2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d'
    assert not run('git','-C',str(root),'status','--porcelain','--untracked-files=no')
    run('git','-C',str(root),'diff','--check')
    run('git','-C',str(root),'diff','--exit-code')
print('PASS assigned/integration Runtime2a9 tracked product clean; diff --check; C0v2/frozen34e untouched')
