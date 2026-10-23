"""Standalone source packet checks; run from a clean assigned Runtime worktree."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
PREFIX = 'handoff-runtime-OPS-bench-store-core-test-sol-1928-'
OLD = 'handoff-runtime-OPS-bench-store-core-projection-1915-'
BASE = 'handoff-runtime-OPS-bench-store-core-precondition-1858-'
HEAD = '2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d'
CORE = '88ae9e5af3425639b7eba0b79aa6b84e78a319fe810c0c6a2d3ceece1be8b5f3'


def run(*args, **kwargs):
    return subprocess.run(args, check=True, capture_output=True, text=True, **kwargs).stdout


def packet(suffix):
    return HERE / (PREFIX + suffix)


def frozen(name):
    return packet('input-' + name)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest():
    lines = packet('hashmanifest.sha256').read_text().splitlines()
    names = []
    for line in lines:
        digest, name = line.split('  ', 1)
        assert Path(name).name == name and name.startswith(PREFIX), name
        assert sha(HERE / name) == digest, name
        names.append(name)
    assert len(names) == len(set(names))
    assert set(names) == {p.name for p in HERE.glob(PREFIX + '*') if p.name != PREFIX + 'hashmanifest.sha256'}
    print('PASS final packet manifest:', len(names), 'files')


def functions(source, cls):
    tree = ast.parse(source)
    node = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == cls)
    return {n.name: ast.get_source_segment(source, n) for n in node.body if isinstance(n, ast.FunctionDef)}


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--runtime', type=Path, default=Path.cwd(), help='current assigned clean Runtime worktree (default: cwd)')
parser.add_argument('--integration-runtime', type=Path, default=Path('/home/user/work/runtime'), help='read-only integration Runtime worktree')
args = parser.parse_args()
manifest()
inputs = json.loads(packet('input-hashes.json').read_text())
for name, digest in inputs.items():
    assert sha(frozen(name)) == digest, name
print('PASS immutable frozen input copies:', len(inputs))
assert sha(packet('bench_store.py')) == CORE
assert packet('bench_store.py').read_bytes() == frozen(OLD + 'bench_store.py').read_bytes()
assert sha(frozen(BASE + 'bench_store.py')) == '53d90fb3108b24253a29416214ec5fa8f69402f50a515f0399b7464ec39a2e14'
original = functions(frozen(BASE + 'bench_store.py').read_text(), 'Store')
current = functions(packet('bench_store.py').read_text(), 'Store')
for name in ('ensure', '_delete_owned', '_sync_payload', '_owned_dir', '_lock', '_evict', 'acquire', 'run', 'initialize'):
    assert original[name] == current[name], name
assert frozen(OLD + 'lease-seam.py').read_bytes() == frozen('handoff-runtime-OPS-bench-store-leases-1850-lease-seam.py').read_bytes()
old_test = frozen(OLD + 'test-core.py').read_text()
new_test = packet('test-core.py').read_text()
old_methods = functions(old_test, 'CoreTests')
new_methods = functions(new_test, 'CoreTests')
assert old_methods.keys() == new_methods.keys()
assert len([n for n in new_methods if n.startswith('test_')]) == 18
corrected = 'test_reclamation_is_real_before_callback_and_failure_preserves_eviction'
for name in old_methods:
    if name != corrected:
        assert old_methods[name] == new_methods[name], name
# Every original assertion except the global inode-nonreuse assertion is retained.
before = ast.parse('class Fixture:\n    ' + old_methods[corrected].replace('\n', '\n    '))
after = ast.parse('class Fixture:\n    ' + new_methods[corrected].replace('\n', '\n    '))
after_calls = {ast.dump(n) for n in ast.walk(after) if isinstance(n, ast.Call)}
replaced = 0
for node in ast.walk(before):
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr.startswith('assert'):
        if 'old_inode' in ast.unparse(node):
            replaced += 1
        else:
            assert ast.dump(node) in after_calls, ast.unparse(node)
assert replaced == 1
print('PASS core BYTEIDENTICAL; lifecycle algorithms/seam unchanged; 17 fixtures exact; one assertion corrected with original guards retained')
for suffix in ('bench_store.py', 'test-core.py', 'test-oracle.py', 'validate.py'):
    compile(packet(suffix).read_bytes(), PREFIX + suffix, 'exec')
for name in (OLD + 'test-projection.py', OLD + 'lease-seam.py'):
    compile(frozen(name).read_bytes(), name, 'exec')
for suffix in ('make-child-venv.sh', 'request-child-venv.sh', 'make-runtime.sh', 'request-runtime.sh'):
    run('bash', '-n', str(frozen('handoff-runtime-OPS-bench-store-creators-return-1912-' + suffix)))
creator = frozen('handoff-runtime-OPS-bench-store-creators-return-1912-make-child-venv.sh').read_text()
assert "'report': data.decode('utf-8')" in creator and "store.ensure('child'" in creator
assert "'provision', name + '.txt'" in creator and 'provision_report_sha256=' in creator
runner = frozen('handoff-runtime-OPS-bench-store-leases-return-1918-test-run')
run('bash', '-n', str(runner))
assert 'store.names_for_suite(' in runner.read_text() and 'store.acquire(names)' in runner.read_text()
print('PASS scoped in-memory compile; bash syntax; unchanged production caller/creator/test-run API')
for root in (args.runtime, args.integration_runtime):
    root = root.resolve(strict=True)
    assert (root / 'astrid_runtime').is_dir() and (root / 'contract').is_dir(), root
    assert Path(run('git', '-C', str(root), 'rev-parse', '--show-toplevel').strip()) == root
    assert run('git', '-C', str(root), 'rev-parse', 'HEAD').strip() == HEAD, root
    assert not run('git', '-C', str(root), 'status', '--porcelain').strip(), root
    run('git', '-C', str(root), 'diff', '--check')
    print('PASS explicit clean Runtime head2a9:', root)
replay = Path(tempfile.mkdtemp(prefix='core1928-replay-', dir=os.environ['TMPDIR']))
(replay / 'bench_store.py').write_bytes(frozen(BASE + 'bench_store.py').read_bytes())
run('patch', '--batch', '--directory=' + str(replay), '-p0', input=packet('core.patch').read_text())
run('cmp', str(replay / 'bench_store.py'), str(packet('bench_store.py')))
print('PASS fresh TMPDIR patch replay/cmp')
manifest()
