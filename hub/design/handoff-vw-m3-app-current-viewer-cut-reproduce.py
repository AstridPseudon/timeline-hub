"""Recreate the tested offline source/peer overlay. No installs or shared writes."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
PREFIX = ORCH / 'design/handoff-vw-m3-app-current-viewer-cut'
REPO = Path('/home/user/work/wt/vw-m3-app-current-viewer-cut')
OVERLAY = ORCH / 'workers/vw-m3-app-current-viewer-cut/overlay'
SHARED = Path('/home/user/work/app/node_modules')
metadata = json.loads(Path(str(PREFIX) + '-source.json').read_text())
if OVERLAY.exists():
    raise SystemExit('Overlay already exists; inspect it before recreating.')
OVERLAY.mkdir()

def extract(data, destination):
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        for member in archive.getmembers():
            assert not Path(member.name).is_absolute() and '..' not in Path(member.name).parts
        archive.extractall(destination, filter='data')

extract(subprocess.check_output(['git', '-C', str(REPO), 'archive', metadata['current']]), OVERLAY)
patch = Path(str(PREFIX) + '-UNAPPLIED-current.patch')
assert hashlib.sha256(patch.read_bytes()).hexdigest() == metadata['patches']['current']['sha256']
subprocess.run(['git', 'apply', '--unsafe-paths', str(patch)], cwd=OVERLAY, check=True)
artifact = ORCH / 'design/handoff-vw-m3-app12-pin-prep-artifact.tgz'
assert hashlib.sha256(artifact.read_bytes()).hexdigest() == metadata['artifact_sha256']
extract(artifact.read_bytes(), OVERLAY / 'public12')
node_modules = OVERLAY / 'node_modules'
node_modules.mkdir()
for package in SHARED.iterdir():
    if package.name == '@banodoco':
        (node_modules / package.name).mkdir()
        for scoped in package.iterdir():
            target = OVERLAY / 'public12/package' if scoped.name == 'timeline-composition' else scoped
            (node_modules / package.name / scoped.name).symlink_to(target, target_is_directory=True)
    else:
        (node_modules / package.name).symlink_to(package, target_is_directory=package.is_dir())
(OVERLAY / 'public12/package/node_modules').symlink_to(node_modules, target_is_directory=True)
for package, expected in metadata['peer_manifests'].items():
    manifest = node_modules / package / 'package.json'
    assert hashlib.sha256(manifest.read_bytes()).hexdigest() == expected['manifest_sha256'], package
for suffix, target in [('-tsconfig.json', 'tsconfig.viewer.json'), ('-vitest.config.ts', 'qualification.config.ts')]:
    (OVERLAY / target).write_bytes(Path(str(PREFIX) + suffix).read_bytes())
for relative, expected in metadata['files_sha256'].items():
    assert hashlib.sha256((OVERLAY / relative).read_bytes()).hexdigest() == expected, relative
print(OVERLAY)
print('Prepared exact source and public12 package. Run the two commands in the report here.')
