"""Portable source/custody checks only; never execute the retained fixture."""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

PREFIX = 'handoff-runtime-OPS-bench-store-leases-package-sol-1931-'
ROOT = Path(__file__).resolve().parent


def artifact(name):
    return ROOT / (PREFIX + name)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(*args, **kwargs):
    print('+ ' + ' '.join(map(str, args)), flush=True)
    return subprocess.run(list(map(str, args)), check=True, **kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--originals', action='store_true', help='also cmp authoritative original paths')
    parser.add_argument('--runtime', type=Path, help='read-only Runtime checkout cleanliness check')
    args = parser.parse_args()
    custody = json.loads(artifact('custody.json').read_text())
    by_original = {}
    for entry in custody:
        data = (ROOT / entry['file']).read_bytes()
        if entry['gzip']:
            data = gzip.decompress(data)
        assert digest(data) == entry['sha256'], entry['file']
        by_original[entry['original']] = data
        if args.originals:
            assert data == Path(entry['original']).read_bytes(), entry['original']
            if not entry['gzip']:
                run('cmp', ROOT / entry['file'], entry['original'])
    print(f'custody SHA/cmp PASS: {len(custody)} artifacts')
    failures = []
    lines = artifact('oldmanifest.sha256').read_text().splitlines()
    for line in lines:
        expected, filename = line.split('  ', 1)
        if digest(by_original[filename]) != expected:
            failures.append(filename)
    assert len(lines) == 16 and len(failures) == 1, failures
    assert failures[0].endswith('/workers/rt-OPS-bench-store-leases-return-1918/report.md'), failures
    print('prior stable manifest: 15/15 PASS; preserved mutable worker report mismatch: 1/1 confirmed')
    run('bash', '-n', artifact('test-run'))
    shell = artifact('test-run').read_bytes()
    embedded = shell.split(b"<<'BENCH_LEASE_PY'\n", 1)[1].split(b'\nBENCH_LEASE_PY\n', 1)[0]
    assert embedded + b'\n' == artifact('lease-seam.py').read_bytes()
    for name in ('bench_store.py', 'lease-seam.py', 'test-leases.py', 'oldvalidate.py', 'validate.py'):
        compile(artifact(name).read_bytes(), str(artifact(name)), 'exec')
    print('shell syntax, 5 Python compiles, embedded seam byte equality PASS')
    target = Path(tempfile.mkdtemp(prefix='package1931-', dir=os.environ['TMPDIR']))
    (target / 'bin').mkdir()
    (target / 'bin/test-run').write_bytes(artifact('test-run.original').read_bytes())
    patch = artifact('test-run.patch').read_bytes()
    run('patch', '--dry-run', '-p1', '-d', target, input=patch)
    run('patch', '-p1', '-d', target, input=patch)
    run('cmp', target / 'bin/test-run', artifact('test-run'))
    (target / 'bin/test-run').write_bytes(artifact('predecessor1850-test-run').read_bytes())
    run('patch', '--dry-run', '-p1', '-d', target, input=artifact('caller-only.patch').read_bytes())
    run('patch', '-p1', '-d', target, input=artifact('caller-only.patch').read_bytes())
    run('cmp', target / 'bin/test-run', artifact('test-run'))
    old = artifact('predecessor1850-test-run').read_bytes()
    old_embedded = old.split(b"<<'BENCH_LEASE_PY'\n", 1)[1].split(b'\nBENCH_LEASE_PY\n', 1)[0]
    assert old.replace(old_embedded, embedded) == shell
    print('both patch replays/cmp and outside-seam preservation PASS')
    proof = gzip.decompress(artifact('independent1923-source.log.gz').read_bytes())
    assert b'Ran 24 tests in 8.631s\n\nOK\n' in proof
    print('independent1923 original log preserved losslessly; 24/24 PASS 8.631s retained, NOT rerun')
    if args.runtime:
        result = run('git', '-C', args.runtime, 'status', '--porcelain', capture_output=True, text=True)
        assert not result.stdout, result.stdout
        run('git', '-C', args.runtime, 'diff', '--check')
        result = run('git', '-C', args.runtime, 'rev-parse', 'HEAD', capture_output=True, text=True)
        assert result.stdout.strip() == '2a9e347ff0e1df1dedff5ab7b59ddb27dfe3129d'
        print('Runtime2a9 clean PASS')
    manifest = artifact('hashmanifest.sha256')
    if manifest.exists():
        lines = manifest.read_text().splitlines()
        for line in lines:
            expected, name = line.split('  ', 1)
            assert Path(name).name == name and name.startswith(PREFIX), name
            assert digest((ROOT / name).read_bytes()) == expected, name
        print(f'fresh manifest: {len(lines)}/{len(lines)} PASS')
    print('PACKAGE SOURCE PASS; combined FAIL/UNQUALIFIED; permission1905 STOPPED')


if __name__ == '__main__':
    main()
