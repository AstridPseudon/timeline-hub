from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile

REPO = Path('/home/user/work/wt/vw-m3-normal-pcm-source-carry')
PREFIX = Path(__file__).with_name('handoff-vw-m3-normal-pcm-source-carry-')
PROJECT = Path(str(PREFIX) + 'project')
SHARED = Path('/home/user/work/composition/node_modules')
ARTIFACT = REPO / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz'


def manifest():
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
    paths = subprocess.check_output(
        ['git', 'diff', '--name-only', '0a8c75772', 'ab935'], cwd=REPO, text=True,
    ).splitlines()
    for name in paths:
        expected = subprocess.check_output(['git', 'show', 'ab935:' + name], cwd=REPO)
        assert (REPO / name).read_bytes() == expected, name
    # Every tracked path outside the prerequisite stays byte-exact to ce251.
    for name in subprocess.check_output(['git', 'ls-files'], cwd=REPO, text=True).splitlines():
        if name not in paths:
            expected = subprocess.check_output(['git', 'show', 'HEAD:' + name], cwd=REPO)
            assert (REPO / name).read_bytes() == expected, name
    assert hashlib.sha256(ARTIFACT.read_bytes()).hexdigest() == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
    with tarfile.open(ARTIFACT) as archive:
        members = archive.getmembers()
        assert len(members) == 77
        for member in members:
            assert member.isfile() and member.name.startswith('package/')
            target = PROJECT / 'node_modules/@banodoco/timeline-composition' / member.name.removeprefix('package/')
            assert target.read_bytes() == archive.extractfile(member).read()
    for path in (REPO / 'remotion').glob('*.mjs'):
        if (PROJECT / path.name).exists():
            assert (PROJECT / path.name).read_bytes() == path.read_bytes()
    for path in (PROJECT / 'tests').iterdir():
        assert path.read_bytes() == (REPO / 'remotion/tests' / path.name).read_bytes()
    for name, version in {'react': '18.3.1', 'react-dom': '18.3.1', 'remotion': '4.0.509',
                          '@remotion/media': '4.0.509', '@remotion/layout-utils': '4.0.509'}.items():
        assert json.loads((PROJECT / 'node_modules' / name / 'package.json').read_text())['version'] == version
    print('PASS: exact 10-file prerequisite, all other tracked ce251 bytes, public12 archive/77 members, tested source copies and peer versions')


if sys.argv[1] == 'setup':
    before = manifest()
    Path(str(PREFIX) + 'shared-before.json').write_text(json.dumps(before, sort_keys=True))
    assert not os.path.lexists(PROJECT), PROJECT
    PROJECT.mkdir()
    modules = PROJECT / 'node_modules'
    modules.mkdir()
    (modules / '@banodoco').mkdir()
    (modules / '@remotion').mkdir()
    package = modules / '@banodoco/timeline-composition'
    package.mkdir()
    with tarfile.open(ARTIFACT) as archive:
        for member in archive.getmembers():
            assert member.isfile() and member.name.startswith('package/') and '..' not in Path(member.name).parts
            target = package / member.name.removeprefix('package/')
            assert not os.path.lexists(target), target
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
    for name in ['react', 'react-dom', 'remotion', '@remotion/media', '@remotion/layout-utils']:
        target = modules / name
        assert not os.path.lexists(target), target
        assert (SHARED / name).is_dir(), name
        target.symlink_to(SHARED / name, target_is_directory=True)
    for name in ['attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs', 'normal-audio-sources.mjs']:
        shutil.copyfile(REPO / 'remotion' / name, PROJECT / name)
    (PROJECT / 'tests').mkdir()
    for name in ['normal-audio-sources.test.mjs', 'long-audio-source.test.mjs', 'gapless-mp3-source-origin.test.mjs', 'normal-audio-native-sources.test.mjs', 'composition-package.mjs']:
        shutil.copyfile(REPO / 'remotion/tests' / name, PROJECT / 'tests' / name)
    verify()
elif sys.argv[1] == 'after':
    after = manifest()
    Path(str(PREFIX) + 'shared-after.json').write_text(json.dumps(after, sort_keys=True))
    before = json.loads(Path(str(PREFIX) + 'shared-before.json').read_text())
    assert before == after, 'SHARED GRAPH DRIFT: central qualification blocked; baseline not replaced'
    verify()
    print(f'PASS: shared graph unchanged, {len(after)} file/link/directory entries')
else:
    raise SystemExit('setup or after required')
