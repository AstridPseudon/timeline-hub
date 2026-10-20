"""Materialize exact read-only Git snapshots in this worker's scratch directory."""
import io
from pathlib import Path
import subprocess
import tarfile

WORKER = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-m2-bootstrap-current-contract-audit/notes')
SOURCES = {
    'app-stage': ('/home/user/work/app', 'f0112b846c1084b0902cdba091442cc840d8e88d', ['src', 'config', 'vendor', 'package.json', 'scripts']),
    'app-fixed': ('/home/user/work/app', '3a1d9c8524f37a2960d37d1b892d041b4c19ed0b', ['src', 'config', 'vendor', 'package.json', 'scripts']),
    'agent-31d': ('/home/user/work/agent', '31d02d45ad21f452724091b94b285478d00c9c21', []),
    'agent-pristine': ('/home/user/work/agent', '487ca1e0d74edf4aecdd2b4e045294ab089fc273', []),
    'agent-current': ('/home/user/work/agent', 'a2ba1bca3cb68a15abb62a1260162c4cb73903af', []),
    'runtime-s2': ('/home/user/work/runtime', 'f7081c14efd9a5b834987e7a1e2abf597b66313b', []),
}
for name, (repo, sha, paths) in SOURCES.items():
    target = WORKER / 'snapshots' / name
    target.mkdir(parents=True, exist_ok=True)
    data = subprocess.check_output(['git', '-C', repo, 'archive', sha, *paths])
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:
        archive.extractall(target, filter='data')
    if name.startswith('app-'):
        if not (target / 'node_modules').is_symlink():
            (target / 'node_modules').symlink_to('/home/user/work/app/node_modules', target_is_directory=True)
    print(name, sha)
