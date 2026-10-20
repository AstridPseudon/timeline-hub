from pathlib import Path
import hashlib
import json
import os
import shutil
import tarfile

REPO = Path('/home/user/work/wt/vw-m3-pcm-caller-current-land-unit')
TASK = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/vw-m3-pcm-caller-current-land-unit')
PREFIX = '/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-vw-m3-pcm-caller-current-land-unit-'
PROJECT = TASK / 'audio-project'
SHARED = Path('/home/user/work/composition/node_modules')

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

Path(PREFIX + 'shared-before.json').write_text(json.dumps(shared_manifest(), sort_keys=True))
assert not os.path.lexists(PROJECT)
PROJECT.mkdir()
modules = PROJECT / 'node_modules'
modules.mkdir()
for directory in ['@banodoco', '@remotion', '@types', '@esbuild']:
    (modules / directory).mkdir()
package = modules / '@banodoco/timeline-composition'
package.mkdir()
artifact = REPO / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz'
assert len(artifact.read_bytes()) == 58444
assert hashlib.sha256(artifact.read_bytes()).hexdigest() == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
manifest = {}
with tarfile.open(artifact) as archive:
    assert len(archive.getmembers()) == 77
    for member in archive.getmembers():
        assert member.isfile() and member.name.startswith('package/') and '..' not in Path(member.name).parts
        target = package / member.name.removeprefix('package/')
        target.parent.mkdir(parents=True, exist_ok=True)
        content = archive.extractfile(member).read()
        target.write_bytes(content)
        manifest[str(target.relative_to(package))] = hashlib.sha256(content).hexdigest()
for source in SHARED.iterdir():
    if source.name.startswith('.'):
        continue
    leaves = list(source.iterdir()) if source.name.startswith('@') else [source]
    for leaf in leaves:
        target = modules / leaf.relative_to(SHARED)
        assert not os.path.lexists(target), target
        target.parent.mkdir(parents=True, exist_ok=True)
        target.symlink_to(leaf, target_is_directory=leaf.is_dir())
for name in ['attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs', 'normal-audio-sources.mjs', 'package.json', 'package-lock.json']:
    shutil.copyfile(REPO / 'remotion' / name, PROJECT / name)
assert json.loads((PROJECT / 'package.json').read_text())['dependencies']['@banodoco/timeline-composition'].endswith('0.0.12.tgz')
assert json.loads((package / 'package.json').read_text())['version'] == '0.0.12'
for name in ['react', 'react-dom', 'remotion', '@remotion/media', '@remotion/layout-utils']:
    expected = '18.3.1' if name.startswith('react') else '4.0.509'
    assert json.loads((modules / name / 'package.json').read_text())['version'] == expected
    assert (modules / name).resolve() == (SHARED / name).resolve()
for name in ['node_modules', 'node_modules/@banodoco', 'node_modules/@remotion', 'node_modules/@types']:
    assert (PROJECT / name).is_dir() and not (PROJECT / name).is_symlink()
Path(PREFIX + 'composition77.json').write_text(json.dumps(manifest, indent=2, sort_keys=True) + '\n')
print('Private actual12 graph ready: 77 package bytes verified; real own scopes, existing Composition peer leaves only')
