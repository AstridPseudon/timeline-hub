from pathlib import Path
import ast
import collections
import difflib
import hashlib
import io
import json
import os
import subprocess
import tarfile

ROOT = Path('/home/user/work/wt/vw-m3-pcm-caller-current-land-unit')
ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
TASK = ORCH / 'workers/vw-m3-pcm-caller-current-land-unit'
PREFIX = str(ORCH / 'design/handoff-vw-m3-pcm-caller-current-land-unit-')
RUN = 'astrid/packs/rendering/rendering/renderers/remotion/run.py'
HELPER = 'astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py'
NORMAL_TEST = 'tests/packs/rendering/test_normal_audio_run.py'
HTTP_TEST = 'tests/packs/rendering/test_normal_audio_http.py'
CALLER = [RUN, HELPER, NORMAL_TEST, HTTP_TEST]


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args])


def read(ref, path):
    return git('show', f'{ref}:{path}')


def oid(kind, data):
    return hashlib.sha1(f'{kind} {len(data)}\0'.encode() + data).hexdigest()


def tree_oid(files):
    hierarchy = {}
    for path, (mode, blob) in files.items():
        level = hierarchy
        parts = path.split('/')
        for part in parts[:-1]:
            level = level.setdefault(part, {})
        level[parts[-1]] = (mode, blob)

    def visit(level):
        rows = []
        for name, item in sorted(level.items(), key=lambda row: row[0] + ('/' if isinstance(row[1], dict) else '')):
            if isinstance(item, dict):
                mode, blob = '40000', visit(item)
            else:
                mode, blob = item
            rows.append(mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(blob))
        return oid('tree', b''.join(rows))

    return visit(hierarchy)


def functions(data):
    return {n.name: ast.dump(n, include_attributes=False) for n in ast.parse(data).body
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}


os.chdir(ROOT)
extent = git('diff', '--name-only', 'da10b0b76^', '5d0f1dd').decode().splitlines()
assert len(extent) == 7, extent
for path in extent:
    actual = (TASK / 'caller-baseline' / path) if path == RUN else ROOT / path
    assert actual.read_bytes() == read('5d0f1dd', path), path
assert functions(read('HEAD', RUN))['capture_remotion_frames'] == functions((ROOT / RUN).read_bytes())['capture_remotion_frames']
assert functions(read('b24a2acf5', RUN))['_execute_remotion_locked'] == functions((ROOT / RUN).read_bytes())['_execute_remotion_locked']
for path, ref in [(HELPER, 'b24a2acf5'), (NORMAL_TEST, 'b24a2acf5'), (HTTP_TEST, 'e5a636d59')]:
    assert (ROOT / path).read_bytes() == read(ref, path), path

lint = []
for data in [(TASK / 'caller-baseline' / RUN).read_bytes(), (ROOT / RUN).read_bytes()]:
    result = subprocess.run(['/home/user/work/venv-agent/bin/ruff', 'check', '--no-cache',
                             '--output-format=json', '--stdin-filename', RUN, '-'],
                            input=data, capture_output=True)
    lint.append(collections.Counter((x['code'], x['message']) for x in json.loads(result.stdout)))
assert lint[0] == lint[1], lint

head_files = {}
for row in git('ls-tree', '-rz', 'HEAD').split(b'\0'):
    if not row:
        continue
    metadata, path = row.split(b'\t', 1)
    mode, kind, blob = metadata.decode().split()
    assert kind == 'blob', row
    head_files[path.decode()] = (mode, blob)
assert tree_oid(head_files) == git('rev-parse', 'HEAD^{tree}').decode().strip()
untracked = git('ls-files', '--others', '--exclude-standard', '-z').decode().strip('\0').split('\0')
changed = git('diff', '--name-only', 'HEAD').decode().splitlines()
assert set(changed + untracked) == set(extent + CALLER), (changed, untracked)

final_files = {}
contents = {}
manifest = {}
for path in sorted(set(head_files) | set(untracked)):
    file = ROOT / path
    mode = head_files.get(path, ('100644', ''))[0]
    content = os.readlink(file).encode() if mode == '120000' else file.read_bytes()
    blob = oid('blob', content)
    contents[path] = content
    final_files[path] = (mode, blob)
    manifest[path] = {'mode': mode, 'git_blob': blob, 'sha256': hashlib.sha256(content).hexdigest()}

baseline = dict(final_files)
for path in CALLER:
    if path in [NORMAL_TEST, HTTP_TEST]:
        del baseline[path]
    else:
        baseline[path] = (final_files[path][0], oid('blob', (TASK / 'caller-baseline' / path).read_bytes()))
base_tree = tree_oid(baseline)
final_tree = tree_oid(final_files)
assert final_tree == '303452fe7aa075d8451f641f577db7dcd0b74ca2', final_tree

# All current compiler/projector/provider/client/pins, serializer and Three.js
# files survive because the complete changed-path set is checked above.
caller_patch = ''
for path in CALLER:
    old = (TASK / 'caller-baseline' / path).read_text() if path in [RUN, HELPER] else ''
    new = contents[path].decode()
    caller_patch += f'diff --git a/{path} b/{path}\n'
    if not old:
        caller_patch += 'new file mode 100644\n'
    caller_patch += ''.join(difflib.unified_diff(old.splitlines(keepends=True), new.splitlines(keepends=True),
                                               fromfile=f'a/{path}' if old else '/dev/null', tofile=f'b/{path}'))
Path(PREFIX + 'caller-only.patch').write_text(caller_patch)

def source_diff(ref):
    patch = git('diff', '--binary', ref)
    for path in sorted(untracked):
        result = subprocess.run(['git', 'diff', '--no-index', '--binary', '/dev/null', path], capture_output=True)
        assert result.returncode == 1, (path, result.stderr)
        patch += result.stdout
    return patch

Path(PREFIX + 'scope.patch').write_bytes(source_diff('HEAD'))
Path(PREFIX + 'mainpair.patch').write_bytes(source_diff('origin/main'))
Path(PREFIX + 'blobs.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
with tarfile.open(PREFIX + 'TREE.tar.gz', 'w:gz') as archive:
    for path, content in contents.items():
        mode = final_files[path][0]
        info = tarfile.TarInfo(path)
        info.mtime = 0
        info.mode = 0o755 if mode == '100755' else 0o644
        if mode == '120000':
            info.type = tarfile.SYMTYPE
            info.linkname = content.decode()
            archive.addfile(info)
        else:
            info.size = len(content)
            archive.addfile(info, io.BytesIO(content))

# Replay whole-main and extent+caller patches without writing Git state.
for label, ref, patches in [
    ('mainpair', 'origin/main', ['mainpair.patch']),
    ('prerequisite-caller', 'HEAD', ['prerequisite.patch', 'caller-only.patch']),
]:
    replay = TASK / f'replay-{label}'
    replay.mkdir()
    source = subprocess.Popen(['git', '-C', str(ROOT), 'archive', ref], stdout=subprocess.PIPE)
    with tarfile.open(fileobj=source.stdout, mode='r|') as archive:
        archive.extractall(replay, filter='data')
    assert source.wait() == 0
    for patch in patches:
        result = subprocess.run(['git', 'apply', '--binary'], cwd=replay,
                                input=Path(PREFIX + patch).read_bytes(), capture_output=True)
        assert result.returncode == 0, (label, result.stdout, result.stderr)
    replay_files = {}
    for file in replay.rglob('*'):
        if file.is_symlink():
            content, mode = os.readlink(file).encode(), '120000'
        elif file.is_file():
            content = file.read_bytes()
            mode = '100755' if file.stat().st_mode & 0o111 else '100644'
        else:
            continue
        replay_files[str(file.relative_to(replay))] = (mode, oid('blob', content))
    assert replay_files == final_files, label

package = ROOT / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz'
data = {
    'base_HEAD': git('rev-parse', 'HEAD').decode().strip(),
    'base_tree': git('rev-parse', 'HEAD^{tree}').decode().strip(),
    'origin_main': git('rev-parse', 'origin/main').decode().strip(),
    'origin_main_tree': git('rev-parse', 'origin/main^{tree}').decode().strip(),
    'extent_source': git('rev-parse', '5d0f1dd').decode().strip(),
    'extent_paths': extent,
    'extent_plus_current_kernel_tree': base_tree,
    'caller_paths': CALLER,
    'frozen_final_tree': final_tree,
    'file_count': len(final_files),
    'caller_and_portable_HTTP_exact_frozen_bytes': True,
    'executor_AST_exact_frozen_caller': True,
    'capture_AST_unchanged': True,
    'unchanged_runner_lint': [{'code': key[0], 'message': key[1], 'count': count}
                              for key, count in lint[0].items()],
    'current_public12_sha256': hashlib.sha256(package.read_bytes()).hexdigest(),
    'mainpair_replay_tree_equal': True,
    'prerequisite_then_caller_replay_tree_equal': True,
    'artifacts': {},
}
for suffix in ['prerequisite.patch', 'caller-only.patch', 'scope.patch', 'mainpair.patch', 'TREE.tar.gz', 'blobs.json']:
    file = Path(PREFIX + suffix)
    data['artifacts'][str(file)] = {'bytes': file.stat().st_size, 'sha256': hashlib.sha256(file.read_bytes()).hexdigest()}
Path(PREFIX + 'source.json').write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
print(json.dumps({'final_tree': final_tree, 'extent_plus_current_kernel_tree': base_tree,
                  'main': data['origin_main'], 'files': len(final_files), 'both_replays_equal': True}))
