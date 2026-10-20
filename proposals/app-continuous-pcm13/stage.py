"""Read-only App extract and safe public13 unpack; no install or shared writes."""
import hashlib
import io
from pathlib import Path
import subprocess
import tarfile

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
FIXTURE = ORCH / 'workers/vw-m3-app-pcm13-implementation-brief/fixture'
REF = 'b1ef4b9b910ba72375c34cf319692f90d22edc25'
archive = (ORCH / 'artifacts/banodoco-timeline-composition-0.0.13.tgz').read_bytes()
assert hashlib.sha256(archive).hexdigest() == '9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738'
with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as packed:
    members = packed.getmembers()
    assert len(members) == 77
    for member in members:
        name = Path(member.name)
        assert member.isfile() and name.parts[0] == 'package' and '..' not in name.parts
        output = FIXTURE / 'node_modules/@banodoco/timeline-composition' / Path(*name.parts[1:])
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(packed.extractfile(member).read())

for name in [
    'compositions/AudioTrack.tsx', 'lib/time-grid.ts', 'lib/timeline-domain.ts',
    'lib/config-utils.ts', 'compositions/playerEvaluation.ts',
    'lib/canonicalRenderBounds.ts', 'compositions/MediaErrorBoundary.tsx',
    'compositions/PreviewMediaFailureContext.tsx',
]:
    relative = 'tools/video-editor/' + name
    output = FIXTURE / 'raw' / relative
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(subprocess.check_output(['git', '-C', '/home/user/work/app', 'show', f'{REF}:src/{relative}']))
print('public13 verified: 77 files; 8 App source files read at', REF)
