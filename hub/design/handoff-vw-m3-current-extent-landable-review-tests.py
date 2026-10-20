from pathlib import Path
import json
import os
import subprocess
import sys

O = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
W = O / 'workers/vw-m3-current-extent-landable-review'
P = O / 'design/handoff-vw-m3-current-extent-landable-review'
PY = '/home/user/work/venv-agent/bin/python'
NODE = '/tmp/vw-m3-agent-gate-node20.19.4/bin/node'
phase = sys.argv[1]
copy = W / phase
E = dict(os.environ)
for key in ['NODE_PATH', 'NODE_OPTIONS', 'PYTHONPYCACHEPREFIX']:
    E.pop(key, None)
E.update(PYTHONPATH=str(copy), REVIEW_SOURCE_ROOT=str(copy), PYTHONDONTWRITEBYTECODE='1',
         ASTRID_INTERNAL_INVOCATION='1', PATH=str(Path(NODE).parent) + ':' + E['PATH'])
args = [PY, '-B', '-m', 'pytest', '-q', '-o', 'addopts=', '-p', 'no:cacheprovider', '--tb=short']
rows = []
selected = set(sys.argv[2:])

def run(label, command, expected=0, node=False):
    if selected and label not in selected:
        return
    env = dict(E)
    if node:
        env.update(NODE_PATH=str(W / 'root-modules/node_modules'), ROOT_SOURCE_DIR=str(copy / 'remotion/src'))
    log = Path(str(P) + '-' + phase + '-' + label + '.log')
    with log.open('w') as out:
        result = subprocess.run(command, cwd=copy, env=env, stdout=out, stderr=subprocess.STDOUT)
    rows.append(dict(label=label, command=command, cwd=str(copy),
                     environment={key: env[key] for key in ['PYTHONPATH', 'REVIEW_SOURCE_ROOT', 'PYTHONDONTWRITEBYTECODE', 'PATH', 'NODE_PATH', 'ROOT_SOURCE_DIR', 'ASTRID_INTERNAL_INVOCATION'] if key in env},
                     exit=result.returncode, expected_exit=expected, log=str(log)))
    Path(str(P) + '-' + phase + ('-' + '-'.join(sorted(selected)) + '-results.json' if selected else '-results.json')).write_text(json.dumps(rows, indent=2) + '\n')
    print(label, result.returncode, '\n' + '\n'.join(log.read_text().splitlines()[-10:]), flush=True)
    assert result.returncode == expected, label

run('native-callback', args + ['tests/packs/rendering/test_remotion_native_window.py', 'tests/packs/rendering/test_remotion_capture_scene_props.py'])
run('live-scene', args + ['tests/packs/rendering/test_live_scene_composition.py', '-k', 'not real_render'])
run('service-neighbors', args + ['tests/core/rendering/test_service.py', 'tests/core/rendering/test_storage.py', 'tests/packs/rendering/test_managed_timeline_render.py', '-k', 'render_clock or declared_render_tail or window_timeline or segment_request'])
run('root-exact', [NODE, str(P) + '-root-exact.test.cjs'], 0 if phase == 'candidate' else 1, node=True)
run('root-supplement', [NODE, str(P) + '-root-supplement.test.cjs'], 0 if phase == 'candidate' else 1, node=True)
run('independent', args + [str(P) + '-probe.py'], 0 if phase == 'candidate' else 1)
if phase == 'baseline':
    run('old-two-positive', [PY, '-B', str(P) + '-tail-replay.py', 'old'])
    run('pre-tail-red', [PY, '-B', str(P) + '-tail-replay.py', 'pre-tail-red'], 1)
else:
    run('extent-tail', args + ['tests/packs/rendering/test_native_layer_extent.py', 'tests/packs/rendering/test_remotion_layer_tail_compat.py'])

run('three-source', args + [str(P) + '-three-source.py'])
