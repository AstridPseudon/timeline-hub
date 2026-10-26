"""Replay the final independent 0253 attack matrix, preserving all expectations.

Only path/scratch parameters and the required external-digest API are adapted.
For adversarial structure tests the fixture digest is passed deliberately so
rejection must occur beyond authentication. Never use that binding at receipt.
"""
import copy
import gzip
import hashlib
import importlib.util
import io
import json
import os
import pathlib
import tarfile
import tempfile
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--archive', type=pathlib.Path, required=True)
parser.add_argument('--expected-sha256', required=True)
args = parser.parse_args()
src = pathlib.Path(__file__).with_name('package_record_closure.py')
spec = importlib.util.spec_from_file_location('d141', src)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
base = args.archive
assert hashlib.sha256(base.read_bytes()).hexdigest() == args.expected_sha256

def read():
    with tarfile.open(base, 'r:gz') as t:
        return [(copy.copy(x), t.extractfile(x).read() if x.isfile() else None) for x in t.getmembers()]

def write(path, fn):
    with open(path, 'wb') as raw:
        with gzip.GzipFile(fileobj=raw, mode='wb', compresslevel=9, mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode='w:') as t:
                for x, b in fn(read()):
                    t.addfile(x, io.BytesIO(b) if b is not None else None)
    path.with_name(path.name + '.sha256').write_text(hashlib.sha256(path.read_bytes()).hexdigest() + '\n')

def add(rs, name, b=b'x'):
    x = tarfile.TarInfo(name)
    x.mode = 420
    x.uid = x.gid = 0
    x.size = len(b)
    return rs + [(x, b)]

def link(rs, name, typ):
    x = tarfile.TarInfo(name)
    x.type = typ
    x.linkname = 'manifest.json'
    x.mode = 420
    x.uid = x.gid = 0
    return rs + [(x, None)]

def mutate(rs, suffix, b):
    obj = None
    for x, v in rs:
        if x.name.endswith('/manifest.json'):
            obj = json.loads(v)
            break
    for e in obj['closure']['files']:
        if e['path'].endswith(suffix):
            e['sha256'] = hashlib.sha256(b).hexdigest()
            e['bytes'] = len(b)
    mb = (json.dumps(obj, sort_keys=True, separators=(',', ':')) + '\n').encode()
    out = []
    for x, v in rs:
        x = copy.copy(x)
        if x.name.endswith('/manifest.json'):
            v = mb
            x.size = len(v)
        if x.name.endswith(suffix):
            v = b
            x.size = len(v)
        out.append((x, v))
    return out

def replace(rs, suffix, b):
    out = []
    for x, v in rs:
        x = copy.copy(x)
        if x.name.endswith(suffix):
            v = b
            x.size = len(v)
        out.append((x, v))
    return out

def run(root, n, fn, want):
    p = root / n
    write(p, fn)
    try:
        m.verify_received_archive(p, hashlib.sha256(p.read_bytes()).hexdigest())
        got = 'ACCEPT'
    except Exception as e:
        got = 'REJECT:' + type(e).__name__
    ok = got == 'ACCEPT' if want == 'ACCEPT' else got.startswith('REJECT:')
    print(f"{n} {want}->{got} {('PASS' if ok else 'FAIL')}")
    return ok
if __name__ == "__main__":
    td = tempfile.mkdtemp(prefix='d141-review0253-', dir=os.environ['TMPDIR'])
    r = pathlib.Path(td)
    ok = []
    ok.append(run(r, '01-baseline.tgz', lambda x: x, 'ACCEPT'))
    with tarfile.open(base, 'r:gz') as t:
        files = [x for x in t.getmembers() if x.isfile()]
        man = json.loads(t.extractfile(next((x for x in files if x.name.endswith('/manifest.json')))).read())
        trust = json.loads(t.extractfile(next((x for x in files if x.name.endswith('/trusted-schema-manifest.json')))).read())
        assert len(man['closure']['files']) == 18 and man['closure']['record']['rows'] == 18 and (man['closure']['record']['hashed_rows'] == 12) and (len(man['closure']['record']['unhashed_rows']) == 6)
        assert trust['commit'] == '242f9c4306bf3b501222cb041a9eb246ef47bc85' and hashlib.sha256(json.dumps(trust, sort_keys=True, separators=(',', ':')).encode()).hexdigest() == m.EXPECTED_MANIFEST_SHA256
    ok.append(True)
    print('02-exact-18-12-6-and-c9a87be: ACCEPT->ACCEPT PASS')
    side = r / '03-sidecar.tgz'
    write(side, lambda x: x)
    (r / '03-sidecar.tgz.sha256').write_text('0' * 64 + '\n')
    try:
        m.verify_received_archive(side, hashlib.sha256(side.read_bytes()).hexdigest())
        got = 'ACCEPT'
    except Exception as e:
        got = 'REJECT:' + type(e).__name__
    ok.append(got.startswith('REJECT:'))
    print('03-sidecar-tamper REJECT->' + got, 'PASS' if ok[-1] else 'FAIL')
    cases = [('04-unknown-file.tgz', lambda x: add(x, 'unknown.txt'), 'REJECT'), ('05-missing-file.tgz', lambda x: [z for z in x if not z[0].name.endswith('/validate.py')], 'REJECT'), ('06-absolute.tgz', lambda x: add(x, '/absolute.txt'), 'REJECT'), ('07-traversal.tgz', lambda x: add(x, 'x/../../escape.txt'), 'REJECT'), ('08-symlink.tgz', lambda x: link(x, 'link', tarfile.SYMTYPE), 'REJECT'), ('09-hardlink.tgz', lambda x: link(x, 'hardlink', tarfile.LNKTYPE), 'REJECT')]

    def mode(x):
        out = []
        for a, b in x:
            a = copy.copy(a)
            a.mode = 493 if a.name.endswith('/validate.py') else a.mode
            out.append((a, b))
        return out

    def owner(x):
        out = []
        for a, b in x:
            a = copy.copy(a)
            a.uid = 12345 if a.name.endswith('/validate.py') else a.uid
            out.append((a, b))
        return out
    cases += [('10-mode.tgz', mode, 'REJECT'), ('11-owner.tgz', owner, 'REJECT'), ('12-duplicate-member.tgz', lambda x: x + [(copy.copy(a), b) for a, b in x if a.name.endswith('/manifest.json')], 'REJECT')]

    def extra_dir(x):
        a = tarfile.TarInfo('unknown-directory/')
        a.type = tarfile.DIRTYPE
        a.mode = 493
        a.uid = a.gid = 0
        return x + [(a, None)]
    cases += [('13-extra-directory.tgz', extra_dir, 'REJECT'), ('14-oversize.tgz', lambda x: mutate(x, '/generated.py', os.urandom(21 * 1024 * 1024)), 'REJECT'), ('15-direct-url.tgz', lambda x: mutate(x, '/direct_url.json', b'{"url":"https://evil.invalid/"}\n'), 'REJECT')]
    dup = b'{"commit":"242f9c4306bf3b501222cb041a9eb246ef47bc85","source_tree":"75a5a697f630affee40632e500b3f5b704a9b834","subdirectory":"packages/timeline-schema/python","url":"https://github.com/banodoco/ArtAgents.git","url":"https://github.com/banodoco/ArtAgents.git"}'
    cases += [('16-duplicate-json-key.tgz', lambda x: replace(x, '/trusted-schema-manifest.json', dup), 'REJECT')]
    for n, fn, want in cases:
        ok.append(run(r, n, fn, want))
    print('RESULT total_subtests=16 passed_expected=%d unexpected=%d' % (sum(ok), len(ok) - sum(ok)))
    assert all(ok), 'review0253 matrix has unexpected outcomes'
