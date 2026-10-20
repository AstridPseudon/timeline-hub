from pathlib import Path
import hashlib
import io
import json
import os
import subprocess
import tarfile

O = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
W = O / 'workers/vw-m3-pcm-caller-current-final-gate'
P = O / 'design/handoff-vw-m3-pcm-caller-current-final-gate'
REPO = Path('/home/user/work/wt/vw-m3-pcm-caller-current-final-gate')
BASE = '43d567f9d972386dc4cf585fbacc3ad9afc56bdd'
EXTENT_BASE = 'df2739f903edac02bd36b4446deeea847524c040'
EXTENT = '5d0f1ddcad54936b36cedf1d89bf34f45fa612b5'

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args])

def extract(ref, target):
    assert not target.exists()
    data = git('archive', '--format=tar', ref)
    (W / (target.name + '-source.tar')).write_bytes(data)
    target.mkdir()
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(target, filter='data')
    return hashlib.sha256(data).hexdigest()

def shared_manifest():
    root = Path('/home/user/work/composition/node_modules')
    rows = {}
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in sorted(dirs + files):
            path = Path(directory) / name
            key = str(path.relative_to(root))
            rows[key] = ['link', os.readlink(path)] if path.is_symlink() else ['file', hashlib.sha256(path.read_bytes()).hexdigest()] if path.is_file() else ['directory']
    return rows

if __name__ == '__main__':
    assert git('rev-parse', 'HEAD').decode().strip() == BASE
    assert not git('status', '--porcelain')
    baseline = W / 'baseline'
    digest = extract(BASE, baseline)
    patch = git('diff', '--binary', EXTENT_BASE, EXTENT)
    Path(str(P)+'-extent.patch').write_bytes(patch)
    result = subprocess.run(['patch', '-p1', '--batch', '--fuzz=0'], input=patch, cwd=baseline, capture_output=True)
    assert result.returncode == 0, result.stdout + result.stderr
    assert not list(baseline.rglob('*.orig')) and not list(baseline.rglob('*.rej'))
    Path(str(P)+'-baseline.json').write_text(json.dumps(dict(base=BASE, archive_sha256=digest, extent=EXTENT, extent_patch_sha256=hashlib.sha256(patch).hexdigest(), apply_output=result.stdout.decode()), indent=2)+'\n')
    Path(str(P)+'-shared-before.json').write_text(json.dumps(shared_manifest(), sort_keys=True)+'\n')
    print('Frozen CURRENT baseline and applied exact approved seven-path extent delta')
