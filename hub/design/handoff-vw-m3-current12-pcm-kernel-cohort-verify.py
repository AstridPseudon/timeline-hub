from pathlib import Path
import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile

REPO = Path('/home/user/work/wt/vw-m3-current12-pcm-kernel-cohort')
PREFIX = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-current12-pcm-kernel-cohort-'
PROJECT = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-current12-pcm-kernel-cohort/checks/remotion')
SHARED = Path('/home/user/work/composition/node_modules')
ARTIFACT = REPO / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz'
CONSUMER = ['astrid/core/rendering/remotion_runtime.py', 'remotion/package.json', 'remotion/package-lock.json', str(ARTIFACT.relative_to(REPO))]

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def shared_manifest():
    entries = {}
    for directory, dirs, files in os.walk(SHARED, followlinks=False):
        for name in sorted(dirs + files):
            path = Path(directory) / name
            key = str(path.relative_to(SHARED))
            if path.is_symlink():
                entries[key] = ['link', os.readlink(path)]
            elif path.is_file():
                entries[key] = ['file', hashlib.sha256(path.read_bytes()).hexdigest()]
            else:
                entries[key] = ['directory']
    return entries

def verify():
    prereq = git('diff', '--name-only', 'ce2510034', '2019d7e69').decode().splitlines()
    assert len(prereq) == 10
    assert prereq == git('diff', '--name-only', '0a8c75772', 'ab935f773').decode().splitlines()
    for name in prereq:
        assert (REPO / name).read_bytes() == git('show', '2019d7e69:' + name) == git('show', 'ab935f773:' + name), name
    # Apply just the approved public12 hunks on top of the current runtime file.
    # Package and lock have no newer additions; the runtime file does.
    runtime = CONSUMER[0]
    expected = git('show', 'HEAD:' + runtime).replace(b'_COMPOSITION_PACKAGE_VERSION = "0.0.10"', b'_COMPOSITION_PACKAGE_VERSION = "0.0.12"')
    assert (REPO / runtime).read_bytes() == expected
    for name in CONSUMER[1:]:
        assert (REPO / name).read_bytes() == git('show', 'f29a9475:' + name), name
    changed = git('diff', '--name-only', 'HEAD').decode().splitlines() + git('ls-files', '--others', '--exclude-standard').decode().splitlines()
    assert set(changed) == set(prereq + CONSUMER), changed
    for name in git('ls-files').decode().splitlines():
        if name not in changed:
            assert (REPO / name).read_bytes() == git('show', 'HEAD:' + name), name
    payload = ARTIFACT.read_bytes()
    assert len(payload) == 58444
    assert hashlib.sha256(payload).hexdigest() == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
    lock = json.loads((REPO / 'remotion/package-lock.json').read_text())
    entry = lock['packages']['node_modules/@banodoco/timeline-composition']
    assert entry['version'] == '0.0.12'
    assert entry['integrity'] == 'sha512-' + base64.b64encode(hashlib.sha512(payload).digest()).decode()
    manifest = {}
    with tarfile.open(ARTIFACT) as archive:
        members = archive.getmembers()
        assert len(members) == 77
        for member in members:
            assert member.isfile() and member.name.startswith('package/')
            name = member.name.removeprefix('package/')
            content = archive.extractfile(member).read()
            assert (PROJECT / 'node_modules/@banodoco/timeline-composition' / name).read_bytes() == content, name
            manifest[name] = hashlib.sha256(content).hexdigest()
    installed = PROJECT / 'node_modules/@banodoco/timeline-composition'
    assert set(manifest) == {str(p.relative_to(installed)) for p in installed.rglob('*') if p.is_file()}
    Path(PREFIX + 'composition77.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    for name in ['react', 'react-dom', 'remotion', '@remotion/media', '@remotion/layout-utils']:
        expected = '18.3.1' if name.startswith('react') else '4.0.509'
        assert json.loads((PROJECT / 'node_modules' / name / 'package.json').read_text())['version'] == expected
        assert (PROJECT / 'node_modules' / name).resolve() == (SHARED / name).resolve()
    for name in ['node_modules', 'node_modules/@banodoco', 'node_modules/@remotion', 'node_modules/@types']:
        assert (PROJECT / name).is_dir() and not (PROJECT / name).is_symlink()
    for name in ['attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs', 'normal-audio-sources.mjs']:
        assert (PROJECT / name).read_bytes() == (REPO / 'remotion' / name).read_bytes()
    for path in (PROJECT / 'tests').iterdir():
        assert path.read_bytes() == (REPO / 'remotion/tests' / path.name).read_bytes()
    print('PASS: exact ten-file 2019/ab935 prerequisite; exact approved consumer hunks; all other HEAD bytes including current M2/provider/client/Root preserved; actual12 lock/integrity; 77 exact package members; clean Composition peers')

if sys.argv[1] == 'setup':
    Path(PREFIX + 'shared-before.json').write_text(json.dumps(shared_manifest(), sort_keys=True))
    assert not os.path.lexists(PROJECT)
    PROJECT.mkdir(parents=True)
    modules = PROJECT / 'node_modules'
    modules.mkdir()
    for directory in ['@banodoco', '@remotion', '@types', '@esbuild']:
        (modules / directory).mkdir()
    package = modules / '@banodoco/timeline-composition'
    package.mkdir()
    with tarfile.open(ARTIFACT) as archive:
        for member in archive.getmembers():
            assert member.isfile() and member.name.startswith('package/') and '..' not in Path(member.name).parts
            target = package / member.name.removeprefix('package/')
            assert not os.path.lexists(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
    # Own real scopes; only existing individual dependency leaves are linked.
    for source in SHARED.iterdir():
        leaves = list(source.iterdir()) if source.name.startswith('@') else [source]
        for leaf in leaves:
            if source.name.startswith('.'):
                continue
            target = modules / leaf.relative_to(SHARED)
            assert not os.path.lexists(target), target
            target.parent.mkdir(parents=True, exist_ok=True)
            target.symlink_to(leaf, target_is_directory=leaf.is_dir())
    for name in ['attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs', 'normal-audio-sources.mjs']:
        shutil.copyfile(REPO / 'remotion' / name, PROJECT / name)
    (PROJECT / 'tests').mkdir()
    for name in ['normal-audio-sources.test.mjs', 'long-audio-source.test.mjs', 'gapless-mp3-source-origin.test.mjs', 'normal-audio-native-sources.test.mjs', 'composition-package.mjs']:
        shutil.copyfile(REPO / 'remotion/tests' / name, PROJECT / 'tests' / name)
    shutil.copyfile(REPO / 'remotion/package.json', PROJECT / 'package.json')
    shutil.copyfile(REPO / 'remotion/package-lock.json', PROJECT / 'package-lock.json')
    verify()
elif sys.argv[1] == 'after':
    after = shared_manifest()
    Path(PREFIX + 'shared-after.json').write_text(json.dumps(after, sort_keys=True))
    assert after == json.loads(Path(PREFIX + 'shared-before.json').read_text()), 'shared graph drift'
    verify()
    print(f'PASS: shared graph identical before/after ({len(after)} entries)')
else:
    raise SystemExit('setup or after required')
