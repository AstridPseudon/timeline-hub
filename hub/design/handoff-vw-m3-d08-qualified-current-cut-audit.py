import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

root = Path('/home/user/work/wt/vw-m3-d08-qualified-current-cut')
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip() == '0ea988bdd2907c876b82fd2620820e3fb6d6ea84'
raw = (root / 'vendor/artifacts/banodoco-timeline-composition-0.0.12.tgz').read_bytes()
assert hashlib.sha256(raw).hexdigest() == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
with tarfile.open(fileobj=io.BytesIO(raw), mode='r:gz') as archive:
    members = [entry for entry in archive.getmembers() if entry.isfile()]
    assert len(members) == 77
    assert json.load(archive.extractfile('package/package.json'))['version'] == '0.0.12'
    evaluation = archive.extractfile('package/dist/evaluation.d.ts').read().decode()
    for export in ('clipOpacity', 'computeMediaTrim', 'prepareTrack', 'queryDrawFrame', 'applyAudioEnvelope'):
        assert export in evaluation
paths = subprocess.check_output(['git', 'ls-files', 'src/tools/video-editor/compositions'], cwd=root, text=True).splitlines()
for name in paths:
    assert (root / name).read_bytes() == subprocess.check_output(['git', 'show', f'HEAD:{name}'], cwd=root)
assert subprocess.check_output(['git', 'status', '--porcelain'], cwd=root, text=True) == ''
print(f'PASS: public12 archive SHA256/version/{len(members)} members/API declarations; {len(paths)} composition files unchanged; worktree clean.')
