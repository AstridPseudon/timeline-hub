from pathlib import Path
import ast
import hashlib
import io
import json
import os
import subprocess
import tarfile

O = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
W = O / 'workers/vw-m3-current-extent-landable-review'
D = O / 'workers/vw-m3-current-extent-landable-unit'
P = O / 'design/handoff-vw-m3-current-extent-landable-review'
R = Path('/home/user/work/wt/vw-m3-current-extent-landable-review')
BASE = 'df2739f903edac02bd36b4446deeea847524c040'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=R)

assert (D / 'DONE').exists(), 'producer has not finished'
assert (D / 'exit').read_text().strip() == '0', 'producer harness not complete'
assert not (D / 'running').exists(), 'producer still running'
TIP = git('rev-parse', 'tl/vw-m3-current-extent-landable-unit').decode().strip()
assert TIP != BASE
assert git('rev-parse', TIP + '^').decode().strip() == BASE
copy = W / 'candidate'
assert not copy.exists()
copy.mkdir()
with tarfile.open(fileobj=io.BytesIO(git('archive', TIP))) as archive:
    archive.extractall(copy, filter='data')
manifest = {}
for item in git('ls-tree', '-rz', TIP).split(b'\0'):
    if not item:
        continue
    header, filename = item.split(b'\t')
    mode, kind, oid = header.split()
    if kind != b'blob':
        continue
    name = filename.decode()
    data = os.readlink(copy / name).encode() if mode == b'120000' else (copy / name).read_bytes()
    assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == oid.decode(), name
    manifest[name] = dict(git_blob=oid.decode(), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
changed = git('diff', '--name-only', BASE, TIP).decode().splitlines()
assert set(changed) == {
    'astrid/core/rendering/service.py',
    'astrid/packs/rendering/rendering/renderers/remotion/run.py',
    'remotion/src/Root.tsx',
    'tests/packs/rendering/test_native_layer_extent.py',
    'remotion/tests/root-metadata.test.cjs',
    'tests/packs/rendering/test_remotion_layer_tail_compat.py',
    'tests/packs/rendering/test_live_scene_composition.py',
}, changed
exact = {}
for name, ref in {
    'astrid/core/rendering/service.py': '626eed656',
    'astrid/packs/rendering/rendering/renderers/remotion/run.py': '883549d3',
    'remotion/src/Root.tsx': '883549d3',
    'tests/packs/rendering/test_native_layer_extent.py': '626eed656',
    'remotion/tests/root-metadata.test.cjs': '20d4ab1aa9',
    'tests/packs/rendering/test_remotion_layer_tail_compat.py': '883549d3',
    'tests/packs/rendering/test_live_scene_composition.py': 'c068503e',
}.items():
    expected = git('show', ref + ':' + name)
    actual = (copy / name).read_bytes()
    exact[name] = dict(reference=ref, byte_equal=(actual == expected), sha256=hashlib.sha256(actual).hexdigest())
    assert actual == expected, name
protected = {}
for name in [
    'astrid/core/timeline/banodoco_composer.py', 'astrid/core/timeline/duration.py',
    'astrid/core/rendering/contracts.py',
    'astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py',
    'astrid/packs/rendering/rendering/renderers/threejs/run.py',
    'tests/packs/rendering/test_remotion_capture_scene_props.py',
    'tests/packs/rendering/test_remotion_native_window.py',
    'remotion/package.json', 'remotion/package-lock.json',
    'remotion/normal-audio-sources.mjs', 'remotion/attempt-envelope-pcm.mjs',
]:
    old = subprocess.run(['git', 'show', BASE + ':' + name], cwd=R, capture_output=True)
    if old.returncode:
        assert not (copy / name).exists()
        protected[name] = 'absent at both'
    else:
        assert old.stdout == (copy / name).read_bytes(), name
        protected[name] = manifest[name]
root_old = git('show', BASE + ':remotion/src/Root.tsx').decode()
root_new = (copy / 'remotion/src/Root.tsx').read_text()
tail = lambda text: text.split('const RenderClockTail =', 1)[1].split('const ReviewedTimelineWithRenderTail', 1)[0]
assert tail(root_old) == tail(root_new)
methods = {}
for name in changed:
    if name.startswith('astrid/') and name.endswith('.py'):
        def defs(data):
            return {n.name: ast.dump(n, include_attributes=False) for n in ast.walk(ast.parse(data))
                    if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}
        old, new = defs(git('show', BASE + ':' + name)), defs((copy / name).read_bytes())
        methods[name] = sorted(k for k, value in new.items() if old.get(k) != value)
state = dict(base=BASE, candidate=TIP, parent=BASE,
             candidate_tree=git('rev-parse', TIP + '^{tree}').decode().strip(),
             harness_exit=0, producer_done=True, archive_all_blob_bytes_equal=True,
             archive_blob_count=len(manifest), changed_files=changed,
             exact_approved_sources=exact, protected_files=protected,
             render_clock_tail_unchanged=True, ast_changed_functions=methods,
             archive=str(copy), composition_pin=json.loads((copy / 'remotion/package.json').read_text())['dependencies']['@banodoco/timeline-composition'])
Path(str(P) + '-sourcebytes.json').write_text(json.dumps(state, indent=2) + '\n')
Path(str(P) + '-all-blobs.json').write_text(json.dumps(manifest, indent=2) + '\n')
Path(str(P) + '-scope.patch').write_bytes(git('diff', '--binary', BASE, TIP))
subprocess.run(['git', 'diff', '--check', BASE, TIP], cwd=R, check=True)
fixture = W / 'fixtures/banodoco-timeline-composition-0.0.10.tgz'
(copy / 'remotion/artifacts' / fixture.name).symlink_to(fixture)
print(json.dumps(state, indent=2))
