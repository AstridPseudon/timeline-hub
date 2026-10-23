"""Scoped source-only checks; all compilation output stays in TMPDIR."""
import os
from pathlib import Path
import py_compile
import subprocess

HERE = Path(__file__).resolve().parent
PREFIX = 'handoff-runtime-OPS-bench-store-'
for name in ('core-precondition-1858-bench_store.py', 'core-precondition-1858-test-core.py',
             'leases-1850-test-leases.py', 'creators-1850-test-adapters.py'):
    path = HERE / (PREFIX + name)
    py_compile.compile(str(path), cfile=str(Path(os.environ['TMPDIR']) / (name + '.pyc')), doraise=True)
    print('PASS scoped py_compile', path.name)
for name in ('make-child-venv.sh', 'make-runtime.sh', 'request-child-venv.sh', 'request-runtime.sh'):
    path = HERE / (PREFIX + 'creators-1850-' + name)
    subprocess.run(['bash', '-n', str(path)], check=True)
    print('PASS bash -n', path.name)
path = HERE / (PREFIX + 'leases-1850-test-run')
subprocess.run(['bash', '-n', str(path)], check=True)
print('PASS bash -n', path.name)
subprocess.run(['cmp', str(HERE / (PREFIX + 'core-precondition-1858-bench_store.py')),
                str(HERE / (PREFIX + 'core-resume-1854-bench_store.py'))], check=True)
print('PASS cmp core and 1854 compatibility copy')
subprocess.run(['git', '-C', '/home/user/work/runtime', 'status', '--porcelain'], check=True)
subprocess.run(['git', 'diff', '--check'], check=True)
subprocess.run(['git', 'status', '--porcelain'], check=True)
print('PASS Runtime status and diff --check (empty status output means clean)')
