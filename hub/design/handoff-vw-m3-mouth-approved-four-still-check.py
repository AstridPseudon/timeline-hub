import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

worker = Path(__file__).resolve().parent
quiet = worker.parents[1] / 'managers/viewing/QUIET.md'
review = worker / 'REVIEW.md'
for path in (quiet, review):
    print(f'{path}:\n{path.read_text() if path.exists() else "ABSENT"}', flush=True)
if quiet.exists():
    (worker / 'PAUSED_ACK').write_text(datetime.now(timezone.utc).isoformat() + ' CPU paused\n')
    sys.exit(75)
artifact = worker.parent / 'vw-m3-opacity-package-ten/artifacts/banodoco-timeline-composition-0.0.10.tgz'
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=os.getcwd(),
    ASTRID_NODE_EXECUTABLE='/tmp/vw-m3-agent-gate-node20.19.4/bin/node',
    ASTRID_COMPOSITION_TEST_ARTIFACT=str(artifact),
    ASTRID_COMPOSITION_TEST_NODE_MODULES='/home/user/work/wt/vw-m3-scene-host-plumbing/remotion/node_modules')
print('COMMAND:', ' '.join(sys.argv[1:]), flush=True)
sys.exit(subprocess.call(sys.argv[1:], env=env))
