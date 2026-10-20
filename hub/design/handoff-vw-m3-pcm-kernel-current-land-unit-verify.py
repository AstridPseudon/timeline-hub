from pathlib import Path
import base64
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tarfile

REPO = Path('/home/user/work/wt/vw-m3-pcm-kernel-current-land-unit')
ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
PREFIX = ORCH / 'design/handoff-vw-m3-pcm-kernel-current-land-unit-'
PROJECT = ORCH / 'workers/vw-m3-pcm-kernel-current-land-unit/checks/remotion'
SHARED = Path('/home/user/work/composition/node_modules')
ARTIFACT = REPO / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz'

def output(suffix, value):
    Path(str(PREFIX) + suffix).write_text(json.dumps(value, sort_keys=True, indent=2) + '\n')

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def manifest(root):
    result = {}
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in sorted(dirs + files):
            path = Path(directory) / name
            key = str(path.relative_to(root))
            if path.is_symlink():
                result[key] = ['link', os.readlink(path)]
            elif path.is_file():
                result[key] = ['file', digest(path.read_bytes())]
            else:
                result[key] = ['directory']
    return result

paths = git('diff', '--name-only', 'ce2510034', '2019d7e69').decode().splitlines()
assert len(paths) == 10
assert paths == git('diff', '--name-only', '0a8c75772', 'ab935f773').decode().splitlines()

def verify():
    assert not git('status', '--porcelain'), 'working tree changed'
    hashes = {}
    for name in paths:
        content = (REPO / name).read_bytes()
        for ref in ['HEAD', '082cf265b', 'ab935f773', '2019d7e69']:
            assert content == git('show', ref + ':' + name), (ref, name)
        hashes[name] = digest(content)
    output('ten-file-hashes.json', hashes)
    integration = git('rev-parse', 'tl/integration').decode().strip()
    for name in paths:
        assert (REPO / name).read_bytes() == git('show', integration + ':' + name), name
    output('integration-' + sys.argv[1] + '.json', {'observed': integration, 'worktree_head': git('rev-parse', 'HEAD').decode().strip(), 'changed_since_worktree': git('diff', '--name-only', 'HEAD', integration).decode().splitlines(), 'ten_paths_identical': True})
    tracked = {}
    # One git archive avoids thousands of individual git show invocations.
    with tarfile.open(fileobj=io.BytesIO(git('archive', 'HEAD'))) as archive:
        for member in archive:
            path = REPO / member.name
            if member.isfile():
                content = path.read_bytes()
                assert content == archive.extractfile(member).read(), member.name
                tracked[member.name] = ['file', digest(content)]
            elif member.issym():
                assert path.is_symlink() and os.readlink(path) == member.linkname
                tracked[member.name] = ['link', member.linkname]
    phase = sys.argv[1]
    output('protected-repo-' + phase + '.json', {n: h for n, h in tracked.items() if n not in paths})
    if phase == 'after':
        assert json.loads(Path(str(PREFIX) + 'protected-repo-setup.json').read_text()) == {n: h for n, h in tracked.items() if n not in paths}
    payload = ARTIFACT.read_bytes()
    assert len(payload) == 58444
    assert digest(payload) == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
    lock = json.loads((REPO / 'remotion/package-lock.json').read_text())
    entry = lock['packages']['node_modules/@banodoco/timeline-composition']
    assert entry['version'] == '0.0.12'
    assert entry['integrity'] == 'sha512-' + base64.b64encode(hashlib.sha512(payload).digest()).decode()
    assert json.loads((PROJECT / 'package.json').read_text())['dependencies']['@banodoco/timeline-composition'] == 'file:artifacts/banodoco-timeline-composition-0.0.12.tgz'
    installed = PROJECT / 'node_modules/@banodoco/timeline-composition'
    members = {}
    with tarfile.open(ARTIFACT) as archive:
        assert len(archive.getmembers()) == 77
        for member in archive:
            assert member.isfile() and member.name.startswith('package/')
            name = member.name.removeprefix('package/')
            content = archive.extractfile(member).read()
            assert (installed / name).read_bytes() == content, name
            members[name] = digest(content)
    assert set(members) == {str(p.relative_to(installed)) for p in installed.rglob('*') if p.is_file()}
    output('composition77.json', members)
    for name in ['react', 'react-dom', 'remotion', '@remotion/media', '@remotion/layout-utils']:
        expected = '18.3.1' if name.startswith('react') else '4.0.509'
        assert json.loads((PROJECT / 'node_modules' / name / 'package.json').read_text())['version'] == expected
        assert (PROJECT / 'node_modules' / name).resolve() == (SHARED / name).resolve()
    for name in ['node_modules', 'node_modules/@banodoco', 'node_modules/@remotion', 'node_modules/@types', 'node_modules/@esbuild', 'node_modules/@banodoco/timeline-composition']:
        assert (PROJECT / name).is_dir() and not (PROJECT / name).is_symlink(), name
    for name in paths:
        if name.startswith('remotion/'):
            assert (PROJECT / name.removeprefix('remotion/')).read_bytes() == (REPO / name).read_bytes()
    # The only product mention is the inactive definition and its helper path.
    found = subprocess.run(['rg', '-l', 'prepare_normal_audio_sources|normal_audio|normal-audio-sources|attempt-envelope-pcm|compiled-audio-source-clock', 'astrid', 'remotion/src'], cwd=REPO, capture_output=True, text=True, check=True).stdout.splitlines()
    assert found == ['astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py'], found
    print(f'PASS: NOP exact ten paths, {len(tracked) - 10} protected tracked files, 77 exact private12 files, clean peer identity; no production caller')

if sys.argv[1] == 'setup':
    output('shared-before.json', manifest(SHARED))
    assert not os.path.lexists(PROJECT)
    PROJECT.mkdir(parents=True)
    modules = PROJECT / 'node_modules'
    for scope in ['', '@banodoco', '@remotion', '@types', '@esbuild']:
        (modules / scope).mkdir(exist_ok=True)
    package = modules / '@banodoco/timeline-composition'
    package.mkdir()
    with tarfile.open(ARTIFACT) as archive:
        for member in archive:
            assert member.isfile() and member.name.startswith('package/') and '..' not in Path(member.name).parts
            target = package / member.name.removeprefix('package/')
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
    for source in SHARED.iterdir():
        if source.name.startswith('.'):
            continue
        for leaf in (list(source.iterdir()) if source.name.startswith('@') else [source]):
            target = modules / leaf.relative_to(SHARED)
            assert not os.path.lexists(target), target
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(leaf, target_is_directory=leaf.is_dir())
    for name in paths + ['remotion/package.json', 'remotion/package-lock.json', 'remotion/tests/composition-package.mjs']:
        if name.startswith('remotion/'):
            target = PROJECT / name.removeprefix('remotion/')
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / name, target)
    (PROJECT / 'artifacts').mkdir(exist_ok=True)
    shutil.copyfile(ARTIFACT, PROJECT / 'artifacts' / ARTIFACT.name)
    Path(str(PREFIX) + 'landing.patch').write_bytes(git('diff', '--binary', 'HEAD'))
    with tarfile.open(str(PREFIX) + 'source.tar', 'w') as archive:
        for name in paths:
            archive.add(REPO / name, arcname=name, recursive=False)
    output('source.json', {'status': 'NOP', 'base': git('rev-parse', 'HEAD').decode().strip(), 'base_tree': git('rev-parse', 'HEAD^{tree}').decode().strip(), 'paths': paths, 'landing_patch_bytes': 0, 'source_archive': str(PREFIX) + 'source.tar'})
    verify()
elif sys.argv[1] == 'after':
    current = manifest(SHARED)
    output('shared-after.json', current)
    assert current == json.loads(Path(str(PREFIX) + 'shared-before.json').read_text()), 'shared graph changed'
    verify()
    print(f'PASS: all {len(current)} shared graph entries unchanged')
else:
    raise SystemExit('setup or after')
