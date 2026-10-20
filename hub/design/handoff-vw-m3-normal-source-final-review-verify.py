from pathlib import Path
import hashlib, json, os, shutil, subprocess, sys, tarfile
REPO = Path('/home/user/work/wt/vw-m3-normal-source-final-review')
PREFIX = Path(__file__).with_name('handoff-vw-m3-normal-source-final-review-')
PROJECT = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-normal-source-final-review/project')
SHARED = Path('/home/user/work/composition/node_modules')
def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)
def manifest():
    entries = {}
    for directory, dirs, files in os.walk(SHARED, followlinks=False):
        for name in sorted(dirs + files):
            path = Path(directory) / name
            key = str(path.relative_to(SHARED))
            entries[key] = (['link', os.readlink(path)] if path.is_symlink() else
                            ['file', hashlib.sha256(path.read_bytes()).hexdigest()] if path.is_file() else ['directory'])
    return entries
def verify():
    prerequisite = git('diff', '--name-only', '0a8c75772', 'ab935f77').decode().splitlines()
    changed = git('diff', '--name-only', 'ce2510034', 'HEAD').decode().splitlines()
    assert changed == prerequisite and len(changed) == 10
    for name in changed:
        assert (REPO / name).read_bytes() == git('show', 'ab935f77:' + name), name
        assert git('rev-parse', 'ce2510034:' + name) == git('rev-parse', '0a8c75772:' + name) if name == 'tests/packs/rendering/test_normal_audio_source_phase.py' else True
    assert git('status', '--porcelain') == b''
    artifact = REPO / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz'
    assert hashlib.sha256(artifact.read_bytes()).hexdigest() == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
    if PROJECT.exists():
        with tarfile.open(artifact) as archive:
            assert len(archive.getmembers()) == 77
            for member in archive.getmembers():
                dest = PROJECT / 'node_modules/@banodoco/timeline-composition' / member.name.removeprefix('package/')
                assert dest.read_bytes() == archive.extractfile(member).read()
        for name, version in {'react':'18.3.1', 'react-dom':'18.3.1', 'remotion':'4.0.509', '@remotion/media':'4.0.509', '@remotion/layout-utils':'4.0.509'}.items():
            assert json.loads((PROJECT / 'node_modules' / name / 'package.json').read_text())['version'] == version
        for name in ['attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs', 'normal-audio-sources.mjs']:
            assert (PROJECT / name).read_bytes() == (REPO / 'remotion' / name).read_bytes()
        for path in (PROJECT / 'tests').iterdir():
            assert path.read_bytes() == (REPO / 'remotion/tests' / path.name).read_bytes()
    print('PASS: all ten files exactly ab935; no other ce251 changes; public12 archive and tested copies exact; clean review worktree')
if sys.argv[1] == 'setup':
    Path(str(PREFIX) + 'shared-before.json').write_text(json.dumps(manifest(), sort_keys=True))
    assert not os.path.lexists(PROJECT)
    PROJECT.mkdir()
    modules = PROJECT / 'node_modules'
    modules.mkdir()
    (modules / '@banodoco').mkdir()
    (modules / '@remotion').mkdir()
    package = modules / '@banodoco/timeline-composition'
    package.mkdir()
    with tarfile.open(REPO / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz') as archive:
        for member in archive.getmembers():
            assert member.isfile() and member.name.startswith('package/') and '..' not in Path(member.name).parts
            target = package / member.name.removeprefix('package/')
            assert not os.path.lexists(target)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
    for name in ['react', 'react-dom', 'remotion', '@remotion/media', '@remotion/layout-utils']:
        target = modules / name
        assert not os.path.lexists(target)
        assert (SHARED / name).is_dir()
        target.symlink_to(SHARED / name, target_is_directory=True)
    for name in ['attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs', 'normal-audio-sources.mjs']:
        shutil.copyfile(REPO / 'remotion' / name, PROJECT / name)
    (PROJECT / 'tests').mkdir()
    for name in ['normal-audio-sources.test.mjs', 'normal-audio-native-sources.test.mjs', 'gapless-mp3-source-origin.test.mjs', 'long-audio-source.test.mjs']:
        shutil.copyfile(REPO / 'remotion/tests' / name, PROJECT / 'tests' / name)
    verify()
elif sys.argv[1] == 'after':
    current = manifest()
    Path(str(PREFIX) + 'shared-after.json').write_text(json.dumps(current, sort_keys=True))
    assert current == json.loads(Path(str(PREFIX) + 'shared-before.json').read_text()), 'shared dependency graph changed'
    verify()
    print('PASS: shared dependency graph unchanged:', len(current), 'entries')
elif sys.argv[1] == 'cleanup':
    shutil.rmtree(PROJECT)
else:
    raise SystemExit('setup/after/cleanup')
