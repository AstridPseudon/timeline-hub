"""Source-only staged packet verification; patch replay stays in TMPDIR."""
import hashlib
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).parent.parent
PREFIX = Path(__file__).with_name('handoff-runtime-OPS-bench-store-leases-return-1918-')
WORKER = ROOT / 'workers/rt-OPS-bench-store-leases-return-1918'


def run(argv, **kwargs):
    print('+ ' + ' '.join(map(str, argv)), flush=True)
    return subprocess.run(list(map(str, argv)), check=True, **kwargs)


def verify_manifest(path):
    for line in path.read_text().splitlines():
        digest, filename = line.split('  ', 1)
        assert hashlib.sha256(Path(filename).read_bytes()).hexdigest() == digest, filename
    print('manifest OK: ' + str(path), flush=True)


shell = Path(str(PREFIX) + 'test-run')
original = Path(str(PREFIX) + 'test-run.original')
seam = Path(str(PREFIX) + 'lease-seam.py')
run(['bash', '-n', shell])
embedded = shell.read_text().split("<<'BENCH_LEASE_PY'\n", 1)[1].split('\nBENCH_LEASE_PY\n', 1)[0]
assert embedded + '\n' == seam.read_text(), 'embedded/exported seam differ'
for source in (seam, Path(str(PREFIX) + 'test-leases.py'), Path(__file__)):
    compile(source.read_bytes(), str(source), 'exec')
print('embedded/exported Python compilation and byte comparison OK')
patch_target = Path(tempfile.mkdtemp(prefix='lease1918-patch-', dir=os.environ['TMPDIR']))
(patch_target / 'bin').mkdir()
(patch_target / 'bin/test-run').write_bytes(original.read_bytes())
patch = Path(str(PREFIX) + 'test-run.patch').read_bytes()
run(['patch', '--dry-run', '-p1', '-d', patch_target], input=patch)
run(['patch', '-p1', '-d', patch_target], input=patch)
run(['cmp', patch_target / 'bin/test-run', shell])
run(['cmp', ROOT / 'bin/test-run', original])
verify_manifest(Path(__file__).with_name('handoff-runtime-OPS-bench-store-leases-1850-hashmanifest.sha256'))
for manifest in ('immutable-inputs.sha256', 'live-inputs.sha256'):
    verify_manifest(WORKER / manifest)
old = Path(__file__).with_name('handoff-runtime-OPS-bench-store-leases-1850-test-run').read_text()
new = shell.read_text()
old_embedded = old.split("<<'BENCH_LEASE_PY'\n", 1)[1].split('\nBENCH_LEASE_PY\n', 1)[0]
assert old.replace(old_embedded, embedded) == new, 'shell changed outside embedded seam'
for repo in (Path.cwd(), Path('/home/user/work/runtime')):
    result = run(['git', '-C', repo, 'status', '--porcelain'], capture_output=True, text=True)
    assert not result.stdout, result.stdout
    run(['git', '-C', repo, 'diff', '--check'])
    run(['git', '-C', repo, 'rev-parse', 'HEAD'])
print('all source-only validation passed; no installation or service run')
