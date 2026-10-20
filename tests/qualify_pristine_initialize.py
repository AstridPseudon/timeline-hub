"""Central targeted launcher; the service snapshots the Runtime cwd before this runs."""
import os
from pathlib import Path
import subprocess

WORKER = Path("/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-m2-init-current-private-qualification")


def test_approved_init_private_pair():
    result = subprocess.run([
        '/home/user/work/venv-agent/bin/python', '-m', 'pytest', '-q', '-ra',
        '-o', 'addopts=', '-p', 'no:cacheprovider',
        'tests/test_timeline_pristine_initialize_integration.py',
        'tests/test_timeline_projection_occupancy.py::test_actual_provider_historical_slot_rematerializes_after_verified_restore',
    ], env={**os.environ, 'ASTRID_CHECKOUT': str(WORKER / 'agent-source'),
            'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONPATH': str(Path.cwd())},
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    (WORKER / 'central-integration.log').write_text(result.stdout)
    assert result.returncode == 0, result.stdout
