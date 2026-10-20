from pathlib import Path
import ast
import difflib
import hashlib
import json
import os
import subprocess
import tarfile
import base64

REPO = Path('/home/user/work/wt/vw-m3-current12-pcm-caller-final-review')
ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
PREFIX = str(ORCH / 'design/handoff-vw-m3-current12-pcm-caller-final-review-')
TASK = ORCH / 'workers/vw-m3-current12-pcm-caller-final-review'
PROJECT = TASK / 'audio-project'
SHARED = Path('/home/user/work/composition/node_modules')
SOURCE = json.loads((ORCH / 'design/handoff-vw-m3-current12-pcm-caller-preserve-main-source.json').read_text())
PREREQS = json.loads((ORCH / 'design/handoff-vw-m3-current12-pcm-caller-preserve-main-prerequisites.json').read_text())

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def functions(data):
    return {node.name: ast.dump(node, include_attributes=False) for node in ast.parse(data).body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))}

assert git('rev-parse', 'HEAD').decode().strip() == 'b24a2acf565a3ab3ce23b35c6ea0a5196c6decd6'
assert not git('status', '--porcelain'), 'assigned worktree modified'
changed = git('diff', '--name-only', SOURCE['base'], 'HEAD').decode().splitlines()
assert set(changed) == set(SOURCE['changed']) and len(changed) == 20
for name, facts in SOURCE['changed'].items():
    assert digest((REPO / name).read_bytes()) == facts['sha256'], name
assert not any(name.endswith(('.orig', '.rej', '.bak', '~')) or 'REPORT' in name for name in changed)
for name, value in SOURCE['protected'].items():
    assert digest((REPO / name).read_bytes()) == value, name
    assert (REPO / name).read_bytes() == git('show', SOURCE['base'] + ':' + name)
# The complete M2 compiler/provider/client and pin directories are outside the delta.
assert not git('diff', SOURCE['base'], 'HEAD', '--', 'astrid/sdk/timeline', 'astrid/core/timeline',
               'astrid_runtime_client', 'runtime.lock.json')
run = 'astrid/packs/rendering/rendering/renderers/remotion/run.py'
old = functions(git('show', SOURCE['base'] + ':' + run))
new = functions((REPO / run).read_bytes())
for name in ['capture_remotion_frames', '_serialize_timeline']:
    assert old[name] == new[name], name
assert 'on_scene_props(merged_props, frame_numbers)' in (REPO / run).read_text()
extent = functions(git('show', SOURCE['extent'] + ':' + run))
assert set(new) == set(extent)
assert [name for name in new if new[name] != extent[name]] == ['_execute_remotion_locked']
patch = ''
for name in SOURCE['caller_only_files']:
    original = git('show', PREREQS['files'][name]['source'] + ':' + name).decode() if name in PREREQS['files'] else ''
    patch += ''.join(difflib.unified_diff(original.splitlines(keepends=True), (REPO / name).read_text().splitlines(keepends=True),
                    fromfile='a/' + name if original else '/dev/null', tofile='b/' + name))
assert digest(patch.encode()) == SOURCE['caller_only_patch_sha256']
assert patch == (ORCH / 'design/handoff-vw-m3-current12-pcm-caller-preserve-main-caller-only.patch').read_text()
for name, facts in PREREQS['files'].items():
    if name not in SOURCE['caller_only_files']:
        assert digest((REPO / name).read_bytes()) == facts['sha256'], name
artifact = REPO / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz'
payload = artifact.read_bytes()
assert digest(payload) == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
lock = json.loads((PROJECT / 'package-lock.json').read_text())['packages']['node_modules/@banodoco/timeline-composition']
assert lock['version'] == '0.0.12'
assert lock['integrity'] == 'sha512-' + base64.b64encode(hashlib.sha512(payload).digest()).decode()
package = PROJECT / 'node_modules/@banodoco/timeline-composition'
manifest = {}
with tarfile.open(artifact) as archive:
    for member in archive.getmembers():
        assert member.isfile() and member.name.startswith('package/')
        name = member.name.removeprefix('package/')
        data = archive.extractfile(member).read()
        assert (package / name).read_bytes() == data, name
        manifest[name] = digest(data)
assert len(manifest) == 77
assert set(manifest) == {str(p.relative_to(package)) for p in package.rglob('*') if p.is_file()}
for name in ['react', 'react-dom', 'remotion', '@remotion/media', '@remotion/layout-utils']:
    peer = PROJECT / 'node_modules' / name
    expected = '18.3.1' if name.startswith('react') else '4.0.509'
    assert json.loads((peer / 'package.json').read_text())['version'] == expected
    assert peer.resolve() == (SHARED / name).resolve()
for name in ['node_modules', 'node_modules/@banodoco', 'node_modules/@remotion', 'node_modules/@types']:
    assert (PROJECT / name).is_dir() and not (PROJECT / name).is_symlink()
for name in ['attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs', 'normal-audio-sources.mjs', 'package.json', 'package-lock.json']:
    assert (PROJECT / name).read_bytes() == (REPO / 'remotion' / name).read_bytes(), name
for path in (PROJECT / 'tests').iterdir():
    assert path.read_bytes() == (REPO / 'remotion/tests' / path.name).read_bytes()
after = {}
for directory, dirs, files in os.walk(SHARED, followlinks=False):
    for name in sorted(dirs + files):
        path = Path(directory) / name
        key = str(path.relative_to(SHARED))
        after[key] = ['link', os.readlink(path)] if path.is_symlink() else ['file', digest(path.read_bytes())] if path.is_file() else ['directory']
assert after == json.loads(Path(PREFIX + 'shared-before.json').read_text()), 'shared graph drift'
Path(PREFIX + 'shared-after.json').write_text(json.dumps(after, sort_keys=True))
Path(PREFIX + 'guard.json').write_text(json.dumps({'head': git('rev-parse', 'HEAD').decode().strip(),
    'caller_patch_sha256': digest(patch.encode()), 'source': SOURCE, 'private_composition77': manifest,
    'shared_entries': len(after), 'clean_worktree': True}, indent=2, sort_keys=True) + '\n')
print('PASS: exact caller patch; 20 frozen source paths; complete current M2/client/pins, serializer and capture callback preserved; no accidental backup/report paths; 77 exact public12 members; clean peers; shared graph unchanged (%s entries)' % len(after))
