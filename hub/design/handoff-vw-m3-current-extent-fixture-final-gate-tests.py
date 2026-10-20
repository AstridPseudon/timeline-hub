from pathlib import Path
import json
import os
import shutil
import subprocess

O = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
W = O / 'workers/vw-m3-current-extent-fixture-final-gate'
P = O / 'design/handoff-vw-m3-current-extent-fixture-final-gate'
copy = W / 'candidate'
assert Path(str(P)+'-freeze.json').is_file()
assert not (copy / '.git').exists()
assert not (copy / 'remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz').exists()
PY = '/home/user/work/venv-agent/bin/python'
NODE = '/tmp/vw-m3-agent-gate-node20.19.4/bin/node'
E = dict(os.environ)
for key in ['NODE_PATH','NODE_OPTIONS','PYTHONPYCACHEPREFIX','PYTHONHOME']:
    E.pop(key, None)
E.update(PYTHONPATH=str(copy), REVIEW_SOURCE_ROOT=str(copy), PYTHONDONTWRITEBYTECODE='1',
         ASTRID_INTERNAL_INVOCATION='1', PATH=str(Path(NODE).parent)+':'+E['PATH'],
         NODE_PATH=str(W/'root-modules/node_modules'), ROOT_SOURCE_DIR=str(copy/'remotion/src'))
args = [PY, '-B', '-m', 'pytest', '-q', '-o', 'addopts=', '-p', 'no:cacheprovider', '--tb=short']
rows = []

def run(label, command):
    tmp = W / ('tmp-' + label)
    if '-m' in command and 'pytest' in command:
        command = command + ['--basetemp='+str(tmp)]
    log = Path(str(P)+'-'+label+'.log')
    with log.open('w') as out:
        result = subprocess.run(command, cwd=copy, env=E, stdout=out, stderr=subprocess.STDOUT)
    rows.append(dict(label=label, command=command, cwd=str(copy),
                     environment={key:E[key] for key in ['PYTHONPATH','REVIEW_SOURCE_ROOT','PYTHONDONTWRITEBYTECODE','PATH','NODE_PATH','ROOT_SOURCE_DIR','ASTRID_INTERNAL_INVOCATION']},
                     exit=result.returncode, log=str(log)))
    Path(str(P)+'-results.json').write_text(json.dumps(rows, indent=2)+'\n')
    print(label, result.returncode, '\n'+'\n'.join(log.read_text().splitlines()[-11:]), flush=True)
    if tmp.exists(): shutil.rmtree(tmp)
    assert result.returncode == 0, label

imports = """import importlib, json, os, pathlib, sys
root=pathlib.Path(os.environ['REVIEW_SOURCE_ROOT']).resolve()
for name in ['astrid.core.rendering.service','astrid.packs.rendering.rendering.renderers.remotion.run','astrid.packs.rendering.rendering.renderers.threejs.run','tests.packs.rendering.test_live_scene_composition','tests.packs.rendering.test_remotion_layer_tail_compat']:
    importlib.import_module(name)
rows={}
for name, module in list(sys.modules.items()):
    if name=='astrid' or name.startswith('astrid.') or name=='tests' or name.startswith('tests.'):
        file=getattr(module,'__file__',None)
        if file:
            path=pathlib.Path(file).resolve()
            assert path.is_relative_to(root), (name,str(path))
            rows[name]=str(path)
print(json.dumps(rows,indent=2))
"""
run('imports', [PY,'-B','-c', imports])
run('extent-tail', args+['tests/packs/rendering/test_native_layer_extent.py','tests/packs/rendering/test_remotion_layer_tail_compat.py'])
run('native-callback', args+['tests/packs/rendering/test_remotion_native_window.py','tests/packs/rendering/test_remotion_capture_scene_props.py'])
run('live-scene17', args+['tests/packs/rendering/test_live_scene_composition.py','-k','not real_render'])
run('clock-service', args+['tests/core/rendering/test_service.py','tests/core/rendering/test_storage.py','tests/packs/rendering/test_managed_timeline_render.py','-k','render_clock or declared_render_tail or window_timeline or segment_request'])
run('root-exact', [NODE,str(copy/'remotion/tests/root-metadata.test.cjs')])
run('root-supplement', [NODE,str(P)+'-root-supplement.test.cjs'])
run('independent', args+[str(P)+'-probe.py'])
run('three-source', args+[str(P)+'-three-source.py'])
run('ruff', [PY,'-B','-m','ruff','check','--no-cache','tests/packs/rendering/test_native_layer_extent.py','tests/packs/rendering/test_remotion_layer_tail_compat.py','tests/packs/rendering/test_live_scene_composition.py'])
