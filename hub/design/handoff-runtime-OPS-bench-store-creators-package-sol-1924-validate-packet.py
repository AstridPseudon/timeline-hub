"""Compile/check exact sources and replay installed-source patches in TMPDIR."""
from pathlib import Path
import hashlib
import json
import re
import os
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = Path(__file__).name.removesuffix('validate-packet.py')
ORCH = HERE.parent

def artifact(name): return HERE / (PREFIX + name)

def check(args, **kw):
    result = subprocess.run(args, capture_output=True, text=True, **kw)
    print('COMMAND', repr(args), 'rc=' + str(result.returncode))
    print(result.stdout + result.stderr, end='')
    assert result.returncode == 0
    return result

baselines = json.loads(artifact('baselines.json').read_text())
for name, record in baselines.items():
    data = Path(record['path']).read_bytes()
    assert len(data) == record['bytes'] and hashlib.sha256(data).hexdigest() == record['sha256']
    print('PASS actual installed baseline hash', name, record['sha256'])

with tempfile.TemporaryDirectory(prefix='creator-patch-', dir=os.environ['TMPDIR']) as temp:
    for name in ('make-child-venv', 'request-child-venv', 'make-runtime', 'request-runtime'):
        source = artifact(name + '.sh')
        check(['bash', '-n', str(source)])
        text = source.read_text()
        if "<<'STORE_PY'\n" in text:
            compile(text.split("<<'STORE_PY'\n", 1)[1].split('\nSTORE_PY\n', 1)[0], name + ':store', 'exec')
        destination = Path(temp, name)
        destination.write_bytes((ORCH / 'bin' / name).read_bytes())
        patch = artifact(name + '.patch')
        check(['patch', '--dry-run', '--batch', str(destination), '-i', str(patch)])
        check(['patch', '--batch', str(destination), '-i', str(patch)])
        check(['cmp', str(destination), str(source)])
        assert destination.read_bytes() == source.read_bytes()
        print('PASS installed patch replay cmp', name)
    child = artifact('make-child-venv.sh').read_text()
    old = HERE / 'handoff-runtime-OPS-D21b-child-reuse-bounded-sol-1839-request-child-venv.sh'
    expected = old.read_text().split("<<'PY'\n", 1)[1].split('\nPY\n', 1)[0]
    actual = child.split('# STORE_VERIFY_BEGIN\n', 1)[1].split('# STORE_VERIFY_END', 1)[0].removesuffix('\n')
    assert actual == expected
    compile(actual, 'exact-child1839-verifier', 'exec')
    print('PASS byte-exact terminal1839 full child custody verifier')
    request = artifact('request-child-venv.sh').read_text()
    compile(request.split("<<'PY'\n", 1)[1].split('\nPY\n', 1)[0], 'request-child-verifier', 'exec')
    for name in ('PROVENANCE_SCRIPT', 'DIST_METADATA_SCRIPT', 'IDENTITY_SCRIPT'):
        matches = re.findall(r"^" + name + r"='(.*?)'\nrun_stage", child, re.M | re.S)
        assert len(matches) == 1, (name, 'shell assignment missing or duplicated')
        code = matches[0]
        compile(code, name, 'exec')
    compile(child.split("<<'RELOCATE'\n", 1)[1].split('\nRELOCATE\n', 1)[0], 'path-relocation', 'exec')
    original = (ORCH / 'bin/make-runtime').read_text()
    runtime = artifact('make-runtime.sh').read_text()
    for start, end in [('registration() {', 'registration validate'), ('artifact_integrity() {', 'verify_node() {')]:
        assert runtime.split(start, 1)[1].split(end, 1)[0] == original.split(start, 1)[1].split(end, 1)[0]
    for token in ('7a488a09e2fc02fbd1bc4ae084bea8a589314f741c182fc02c5f3f07c79a29d4', 'f8537bd20c8fdc951a20a4278e380e03e58e0a1689eaaa5c170b221435f3a22e', 'ffdb0b13c65f106d7b818208343feb3f438dfc943f4af57c5f612ddcf73dc036', 'e53a69a465e05976dcf7a781f420b1c7def64a13691f7a5f387f6a0609a6da02'):
        assert token in runtime
    print('PASS byte-exact Remotion registration/artifact/source guards and pins')
    assert artifact('request-runtime.sh').read_bytes() == (ORCH / 'bin/request-runtime').read_bytes()
    print('PASS byte-exact runtime request writer')
for name in ('test-adapters.py', 'test-receipts.py', 'validate-packet.py'):
    path = artifact(name)
    compile(path.read_bytes(), str(path), 'exec')
    print('PASS scoped Python compile', path.name)
check(['git', 'diff', '--check'])
assert check(['git', 'status', '--porcelain']).stdout == ''
check(['git', '-C', '/home/user/work/runtime', 'diff', '--check'])
status = check(['git', '-C', '/home/user/work/runtime', 'status', '--porcelain']).stdout
assert status == ''
check(['sha256sum', '-c', str(artifact('hashmanifest.txt'))], cwd=HERE)
print('PASS packet syntax/compile/hash/cmp/patch replay; integration Runtime unchanged')

old_prefix = 'handoff-runtime-OPS-bench-store-creators-1850-'
for name in ('make-runtime.sh', 'request-runtime.sh', 'test-adapters.py'):
    assert artifact(name).read_bytes() == (HERE / (old_prefix + name)).read_bytes()
old_child = (HERE / (old_prefix + 'make-child-venv.sh')).read_text()
for start, end in [('# STORE_BUILD_BEGIN\n', '# STORE_BUILD_END'), ('# STORE_VERIFY_BEGIN\n', '# STORE_VERIFY_END')]:
    assert child.split(start, 1)[1].split(end, 1)[0] == old_child.split(start, 1)[1].split(end, 1)[0]
old_request = (HERE / (old_prefix + 'request-child-venv.sh')).read_text()
assert request.replace('registration=existing status=passed\\n', 'registration=existing\\n') == old_request
check(['sha256sum', '-c', str(HERE / (old_prefix + 'hashmanifest.txt'))], cwd=HERE)
print('PASS immutable1850; exact build/verifier/runtime/requester guards retained')

# All packet and old1850 hashes must still agree after the scoped checks.
check(['sha256sum', '-c', str(artifact('hashmanifest.txt'))], cwd=HERE)
for name, record in baselines.items():
    assert hashlib.sha256(Path(record['path']).read_bytes()).hexdigest() == record['sha256']
print('SOURCE PASS; combined FAIL / UNQUALIFIED / STOPPED; STOP1905 pending')
