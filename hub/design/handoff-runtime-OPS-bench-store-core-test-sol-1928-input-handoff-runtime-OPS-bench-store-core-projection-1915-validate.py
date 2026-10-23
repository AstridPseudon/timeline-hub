"""Read-only scoped validation of this source-only packet."""
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).parent
PREFIX = 'handoff-runtime-OPS-bench-store-core-projection-1915-'
BASE = 'handoff-runtime-OPS-bench-store-core-precondition-1858-'
TMP = Path(os.environ['TMPDIR']) / 'projection1915'

def run(*args):
    subprocess.run(args, check=True, capture_output=True, text=True)

for suffix in ('bench_store.py', 'test-core.py', 'test-projection.py', 'lease-seam.py', 'validate.py'):
    source = (HERE / (PREFIX + suffix)).read_text()
    compile(source, PREFIX + suffix, 'exec')
print('PASS scoped Python compile (in memory, no caches)')
old = (HERE / (BASE + 'bench_store.py')).read_text()
new = (HERE / (PREFIX + 'bench_store.py')).read_text()
assert hashlib.sha256(old.encode()).hexdigest() == '53d90fb3108b24253a29416214ec5fa8f69402f50a515f0399b7464ec39a2e14'
def methods(source):
    tree = ast.parse(source)
    store = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == 'Store')
    return {n.name: ast.get_source_segment(source, n) for n in store.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
original, current = methods(old), methods(new)
for method in ('ensure', '_delete_owned', '_sync_payload', '_owned_dir', '_lock', '_evict', 'acquire', 'run', 'initialize'):
    assert original[method] == current[method], method + ' changed'
print('PASS publication/deletion/lease FD/lock identity/retention algorithms byte-identical')
assert (HERE / (PREFIX + 'lease-seam.py')).read_bytes() == (HERE / 'handoff-runtime-OPS-bench-store-leases-1850-lease-seam.py').read_bytes()
original_tests = (HERE / (BASE + 'test-core.py')).read_text()
expected_tests = original_tests.replace(BASE + 'bench_store.py', PREFIX + 'bench_store.py')
assert (HERE / (PREFIX + 'test-core.py')).read_text() == expected_tests
print('PASS original 18 fixture expectations unchanged; only import basename differs')
for filename, expected in json.loads((HERE / (PREFIX + 'input-hashes.json')).read_text()).items():
    assert hashlib.sha256((HERE / filename).read_bytes()).hexdigest() == expected, filename + ' changed'
print('PASS frozen 1858/1850/review inputs immutable')
for name in ('make-child-venv.sh', 'request-child-venv.sh', 'make-runtime.sh', 'request-runtime.sh'):
    path = HERE / ('handoff-runtime-OPS-bench-store-creators-return-1912-' + name)
    run('bash', '-n', str(path))
creator = (HERE / 'handoff-runtime-OPS-bench-store-creators-return-1912-make-child-venv.sh').read_text()
assert "'report': data.decode('utf-8')" in creator and "store.ensure('child'" in creator
assert "'provision', name + '.txt'" in creator and 'provision_report_sha256=' in creator
runner = (HERE / 'handoff-runtime-OPS-bench-store-leases-1850-test-run').read_text()
assert 'store.names_for_suite(' in runner and 'store.acquire(names)' in runner
run('bash', '-n', str(HERE / 'handoff-runtime-OPS-bench-store-leases-1850-test-run'))
print('PASS caller source wiring (creator report + persisted verification + existing runner API); bash syntax')
for root in ('/home/user/work/wt/rt-OPS-bench-store-core-projection-1915', '/home/user/work/runtime'):
    assert not subprocess.check_output(['git', '-C', root, 'status', '--porcelain']).strip()
    run('git', '-C', root, 'diff', '--check')
assert subprocess.check_output(['git', '-C', '/home/user/work/wt/rt-OPS-bench-store-core-projection-1915', 'rev-parse', 'HEAD'], text=True).strip() == '2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d'
print('PASS Runtime assigned + integration clean; 2a9 base, C0v2/34e/product/generated untouched')
run('cmp', str(TMP / 'patch-replay/bench_store.py'), str(HERE / (PREFIX + 'bench_store.py')))
print('PASS patch replay cmp')
