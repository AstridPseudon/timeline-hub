from pathlib import Path
import hashlib
import json
import os
import subprocess
import tarfile

repo = Path('/home/user/work/wt/vw-m3-normal-pcm-producer-current')
orch = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
worker = orch / 'workers/vw-m3-normal-pcm-producer-current'
project = worker / 'checks/remotion'
package = worker / 'checks/public12/package'
artifact = orch / 'workers/vw-m3-release12/artifacts/banodoco-timeline-composition-0.0.12.tgz'
assert hashlib.sha256(artifact.read_bytes()).hexdigest() == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
with tarfile.open(artifact) as tar:
    members = tar.getmembers()
    assert len(members) == 77
    for member in members:
        assert member.isfile() and member.name.startswith('package/')
        assert '..' not in Path(member.name).parts
        assert tar.extractfile(member).read() == (package / member.name.removeprefix('package/')).read_bytes()
for name in ('normal-audio-sources.mjs', 'attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs'):
    assert (repo / 'remotion' / name).read_bytes() == (project / name).read_bytes()
for name in ('normal-audio-sources.test.mjs', 'long-audio-source.test.mjs', 'gapless-mp3-source-origin.test.mjs'):
    assert (repo / 'remotion/tests' / name).read_bytes() == (project / 'tests' / name).read_bytes()
for name, version in {'react': '18.3.1', 'react-dom': '18.3.1', 'remotion': '4.0.509',
                      '@remotion/media': '4.0.509', '@remotion/layout-utils': '4.0.509'}.items():
    assert json.loads((project / 'node_modules' / name / 'package.json').read_text())['version'] == version
node = '/tmp/vw-m3-agent-gate-node20.19.4/bin/node'
env = {k: v for k, v in os.environ.items() if k not in ('NODE_OPTIONS', 'NODE_PATH')}
assert subprocess.check_output([node, '--version'], env=env, text=True).strip() == 'v20.19.4'
for source in list((repo / 'remotion').glob('*audio*.mjs')) + list((repo / 'remotion/tests').glob('*audio*.test.mjs')) + [repo / 'remotion/attempt-envelope-pcm.mjs', repo / 'remotion/tests/gapless-mp3-source-origin.test.mjs']:
    subprocess.run([node, '--check', str(source)], env=env, check=True)
assert subprocess.check_output(['git', 'diff', '--name-only'], cwd=repo, text=True) == ''
print('public12 SHA256/77 archive files/peers, Node20.19.4, tested module+test bytes, JS syntax, unchanged tracked source: PASS')
