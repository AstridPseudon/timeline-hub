from pathlib import Path
import base64
import hashlib
import io
import json
import subprocess
import sys
import tarfile

O = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
W = O / 'workers/vw-m3-current-extent-landable-review'
phase = sys.argv[1]
assert phase in ['baseline', 'candidate']
root = W / phase
fixture = W / 'fixtures/banodoco-timeline-composition-0.0.10.tgz'
link = root / 'remotion/artifacts' / fixture.name
if '--clean' in sys.argv:
    assert link.is_symlink() and link.resolve() == fixture
    link.unlink()
    print('Removed private fixture leaf:', link)
else:
    expected = subprocess.check_output(['git', 'show', '626eed656:remotion/artifacts/' + fixture.name], cwd='/home/user/work/wt/vw-m3-current-extent-landable-review')
    assert fixture.read_bytes() == expected
    current = root / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz'
    lock = json.loads((root / 'remotion/package-lock.json').read_text())
    assert lock['packages']['node_modules/@banodoco/timeline-composition']['integrity'] == 'sha512-' + base64.b64encode(hashlib.sha512(current.read_bytes()).digest()).decode()
    member = 'package/dist/chunk-SE4TPVLW.js'
    with tarfile.open(fileobj=io.BytesIO(expected)) as old, tarfile.open(current) as new:
        assert old.extractfile(member).read() == new.extractfile(member).read()
    assert not link.exists()
    link.symlink_to(fixture)
    print('Provisioned frozen byte-verified duration fixture:', link)
