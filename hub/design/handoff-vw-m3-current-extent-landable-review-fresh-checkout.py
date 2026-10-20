from pathlib import Path
import json
import os
import subprocess

O = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
W = O / 'workers/vw-m3-current-extent-landable-review'
P = O / 'design/handoff-vw-m3-current-extent-landable-review'
copy = W / 'candidate'
old_fixture = copy / 'remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz'
assert not old_fixture.exists()
command = ['/home/user/work/venv-agent/bin/python', '-B', '-m', 'pytest', '-q', '-o', 'addopts=', '-p', 'no:cacheprovider', '--tb=short', '--basetemp=' + str(W / 'fresh-pytest-tmp'), 'tests/packs/rendering/test_remotion_layer_tail_compat.py']
env = dict(os.environ)
env.pop('NODE_PATH', None)
env.pop('NODE_OPTIONS', None)
env.update(PYTHONPATH=str(copy), PYTHONDONTWRITEBYTECODE='1', ASTRID_INTERNAL_INVOCATION='1', PATH='/tmp/vw-m3-agent-gate-node20.19.4/bin:' + env['PATH'])
log = Path(str(P) + '-candidate-fresh-tail.log')
with log.open('w') as out:
    result = subprocess.run(command, cwd=copy, env=env, stdout=out, stderr=subprocess.STDOUT)
record = dict(command=command, cwd=str(copy), environment={key: env[key] for key in ['PYTHONPATH', 'PYTHONDONTWRITEBYTECODE', 'ASTRID_INTERNAL_INVOCATION', 'PATH']}, exit=result.returncode, missing_fixture=str(old_fixture), log=str(log))
Path(str(P) + '-candidate-fresh-tail.json').write_text(json.dumps(record, indent=2) + '\n')
print('\n'.join(log.read_text().splitlines()[-17:]))
assert result.returncode == 1
assert '11 failed, 11 passed' in log.read_text()
assert 'Cannot open: No such file or directory' in log.read_text()
