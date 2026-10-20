from pathlib import Path
import ast
import base64
import hashlib
import io
import json
import subprocess
import tarfile

O = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
NAME = 'vw-m3-current-extent-fixture-final-gate'
W = O / 'workers' / NAME
P = O / 'design' / ('handoff-' + NAME)
REPO = Path('/home/user/work/wt') / NAME
PRODUCER = O / 'workers/vw-m3-current-extent-fixture-portability'
REF = 'tl/vw-m3-current-extent-fixture-portability'
BASE = 'da10b0b7690a8c2a4032e75eb3d4a3e988121997'
TAIL = 'tests/packs/rendering/test_remotion_layer_tail_compat.py'

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args])

assert (PRODUCER / 'DONE').is_file(), 'Producer has not declared DONE'
assert not (PRODUCER / 'running').exists(), 'Producer still running'
assert (PRODUCER / 'exit').read_text().strip() == '0', 'Producer not successful'
sha = git('rev-parse', REF).decode().strip()
assert sha != BASE, 'Harness has not committed producer changes'
assert git('rev-parse', sha + '^').decode().strip() == BASE
changed = git('diff', '--name-only', BASE, sha).decode().splitlines()
assert changed == [TAIL], changed
copy = W / 'candidate'
assert not copy.exists(), 'Do not overwrite an existing frozen archive'
archive = git('archive', '--format=tar', sha)
archive_path = W / 'final-source.tar'
archive_path.write_bytes(archive)
copy.mkdir()
with tarfile.open(fileobj=io.BytesIO(archive)) as source:
    source.extractall(copy, filter='data')
rows = []
for entry in git('ls-tree', '-r', '-z', sha).split(b'\0'):
    if not entry:
        continue
    header, name = entry.split(b'\t', 1)
    mode, kind, blob = header.decode().split()
    assert kind == 'blob'
    path = name.decode()
    dest = copy / path
    data = dest.readlink().as_posix().encode() if mode == '120000' else dest.read_bytes()
    digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
    assert digest == blob, path
    rows.append(dict(path=path, mode=mode, blob=blob, sha256=hashlib.sha256(data).hexdigest()))
Path(str(P) + '-all-blobs.json').write_text(json.dumps(rows, indent=2) + '\n')
old = git('show', BASE + ':' + TAIL).decode()
new = (copy / TAIL).read_text()
old_tree, new_tree = ast.parse(old), ast.parse(new)
old_f = {f.name: ast.dump(f, include_attributes=False) for f in old_tree.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))}
new_f = {f.name: ast.dump(f, include_attributes=False) for f in new_tree.body if isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef))}
assert set(new_f) - set(old_f) == {'_composition_archive'}
assert set(old_f) - set(new_f) == set()
assert [name for name in old_f if old_f[name] != new_f[name]] == ['_root_probe']
old_asserts = [ast.dump(node, include_attributes=False) for node in ast.walk(old_tree) if isinstance(node, ast.Assert)]
new_asserts = [ast.dump(node, include_attributes=False) for node in ast.walk(new_tree) if isinstance(node, ast.Assert)]
assert all(x in new_asserts for x in old_asserts)
for forbidden in ['0.0.10', '/scratchpad/', 'git show', 'subprocess.check_output', '2019d7e69:']:
    assert forbidden not in new, forbidden
pkg = json.loads((copy / 'remotion/package.json').read_text())
dep = pkg['dependencies']['@banodoco/timeline-composition']
assert dep == 'file:artifacts/banodoco-timeline-composition-0.0.12.tgz'
public_archive = copy / 'remotion' / dep.removeprefix('file:')
assert public_archive.is_file()
lock = json.loads((copy / 'remotion/package-lock.json').read_text())
pin = lock['packages']['node_modules/@banodoco/timeline-composition']
assert pin['resolved'] == dep
integrity = 'sha512-' + base64.b64encode(hashlib.sha512(public_archive.read_bytes()).digest()).decode()
assert pin['integrity'] == integrity
with tarfile.open(public_archive) as tgz:
    public_version = json.load(tgz.extractfile('package/package.json'))['version']
    duration = tgz.extractfile('package/dist/chunk-SE4TPVLW.js').read()
assert public_version == '0.0.12'
assert not (copy / 'remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz').exists()
protected = ['astrid/core/rendering/service.py', 'astrid/packs/rendering/rendering/renderers/remotion/run.py', 'remotion/src/Root.tsx']
protected_rows = []
for path in protected:
    before = git('show', BASE + ':' + path)
    after = (copy / path).read_bytes()
    assert before == after
    protected_rows.append(dict(path=path, sha256=hashlib.sha256(after).hexdigest(), byte_equal_to_base=True))
record = dict(source_sha=sha, source_tree=git('rev-parse', sha+'^{tree}').decode().strip(), base=BASE,
              source_archive=str(archive_path), archive_sha256=hashlib.sha256(archive).hexdigest(),
              tracked_blobs=len(rows), changed_paths=changed, protected=protected_rows,
              old_assert_count=len(old_asserts), new_assert_count=len(new_asserts),
              unchanged_test_function_count=sum(name.startswith('test_') for name in old_f),
              package_dependency=dep, package_version=public_version, package_integrity=integrity,
              package_sha256=hashlib.sha256(public_archive.read_bytes()).hexdigest(),
              duration_chunk_sha256=hashlib.sha256(duration).hexdigest(),
              old_archive_absent=True, git_directory_absent=not (copy/'.git').exists())
Path(str(P)+'-freeze.json').write_text(json.dumps(record, indent=2)+'\n')
Path(str(P)+'-scope.patch').write_bytes(git('diff', '--binary', BASE, sha))
print(json.dumps(record, indent=2))
