import hashlib
import os
import shutil
import subprocess
import tarfile
import tempfile
from pathlib import Path

worker = Path(__file__).resolve().parent
artifact = worker.parent / 'vw-m3-opacity-package-ten/artifacts/banodoco-timeline-composition-0.0.10.tgz'
assert hashlib.sha256(artifact.read_bytes()).hexdigest() == 'cd83b77f72ce436e25eef697b289d33adae2087d92035aa37a27a308975ddea7'
with tempfile.TemporaryDirectory(prefix='clock-only-', dir=worker) as name:
    stage = Path(name)
    with tarfile.open(artifact) as archive:
        expected = {m.name: hashlib.sha256(archive.extractfile(m).read()).hexdigest()
                    for m in archive.getmembers() if m.isfile()}
        assert len(expected) == 77
        archive.extractall(stage, filter='data')
    shutil.copyfile(worker / 'clock-prototype.mjs', stage / 'clock-prototype.mjs')
    env = {k: v for k, v in os.environ.items() if k not in ('NODE_OPTIONS', 'NODE_PATH')}
    result = subprocess.run(['/tmp/vw-m3-agent-gate-node20.19.4/bin/node',
                             str(stage / 'clock-prototype.mjs')], env=env)
    assert {p: hashlib.sha256((stage / p).read_bytes()).hexdigest() for p in expected} == expected
    print('public10 archive + all 77 extracted files unchanged', flush=True)
    raise SystemExit(result.returncode)
