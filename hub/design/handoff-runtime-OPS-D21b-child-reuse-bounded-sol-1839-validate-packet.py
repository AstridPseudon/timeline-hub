"""Read-only syntax/source checks and disposable exact patch replay."""
from pathlib import Path
import hashlib
import os
import runpy
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = Path(__file__).name.removesuffix('validate-packet.py')
def artifact(name): return HERE / (PREFIX + name)
ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
footprint = runpy.run_path(str(artifact('fixture-sources.py')))['footprint']
footprint('before-validation-group')
def check(args, **kwargs):
    result = subprocess.run(args, capture_output=True, text=True, **kwargs)
    print('COMMAND', repr(args), 'rc=' + str(result.returncode), flush=True)
    print(result.stdout + result.stderr, end='', flush=True)
    assert result.returncode == 0
    return result

for name in ('make-child-venv.sh', 'request-child-venv.sh', 'fixture-python.sh'):
    check(['bash', '-n', str(artifact(name))])
for name in ('fixture-sources.py', 'test-child-reuse.py', 'test-dispatcher.py', 'validate-packet.py'):
    path = artifact(name)
    compile(path.read_bytes(), str(path), 'exec')
    print('PASS Python compile', name)
source = artifact('request-child-venv.sh').read_text()
compile(source.split("<<'PY'\n", 1)[1].split('\nPY\n', 1)[0], 'requester-embedded', 'exec')
print('PASS embedded requester Python compile')
# Also compile maker Python snippets extracted by shell assignment boundaries.
source = artifact('make-child-venv.sh').read_text()
for name in ('PROVENANCE_SCRIPT', 'DIST_METADATA_SCRIPT', 'IDENTITY_SCRIPT'):
    code = source.split(name + "='", 1)[1].split("'\nrun_stage", 1)[0]
    compile(code, name, 'exec')
    print('PASS embedded maker Python compile', name)
for name in ('astrid_runtime/__init__.py', 'astrid_runtime/cli.py', 'astrid_runtime/runtime_boundary.py'):
    path = Path.cwd() / name
    compile(path.read_bytes(), str(path), 'exec')
    print('PASS scoped Runtime compile', name)
with tempfile.TemporaryDirectory(prefix='patch-replay-', dir=os.environ['TMPDIR']) as temp:
    root = Path(temp)
    (root / 'bin').mkdir()
    for script in ('make-child-venv', 'request-child-venv'):
        original = ORCH / 'bin' / script
        print('INSTALLED INPUT', script, hashlib.sha256(original.read_bytes()).hexdigest())
        destination = root / 'bin' / script
        shutil.copyfile(original, destination)
        check(['patch', '--batch', str(destination), '-i', str(artifact(script + '.patch'))], cwd=root)
        assert destination.read_bytes() == artifact(script + '.sh').read_bytes()
        print('PASS installed patch replay cmp', script)
        parent = ORCH / 'workers/rt-OPS-child-reuse-return-1811/evidence' / (script + '.sh')
        shutil.copyfile(parent, destination)
        check(['patch', '--batch', str(destination), '-i', str(artifact(script + '.from-1811.patch'))], cwd=root)
        assert destination.read_bytes() == artifact(script + '.sh').read_bytes()
        print('PASS 1811 patch replay cmp', script)
for name in ('make-child-venv.sh', 'request-child-venv.sh'):
    previous = ORCH / 'workers/rt-OPS-child-reuse-sol-1826/evidence' / name
    assert previous.read_bytes() == artifact(name).read_bytes()
    print('PASS byte-identical 1826 candidate', name)
check(['git', 'diff', '--check'])
assert check(['git', 'status', '--porcelain', '--untracked-files=all']).stdout == ''
head = check(['git', 'rev-parse', 'HEAD']).stdout.strip()
assert head == '2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d'
check(['git', 'diff', '--exit-code', head, '--'])
footprint('after-validation-group')
print('PASS syntax/scoped compile/patch replay/Runtime clean')
