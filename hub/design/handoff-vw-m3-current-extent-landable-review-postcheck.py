from pathlib import Path
import ast
from collections import Counter
import hashlib
import json
import os
import subprocess

O = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
W = O / 'workers/vw-m3-current-extent-landable-review'
P = O / 'design/handoff-vw-m3-current-extent-landable-review'
R = Path('/home/user/work/wt/vw-m3-current-extent-landable-review')
state = json.loads(Path(str(P) + '-sourcebytes.json').read_text())
manifest = json.loads(Path(str(P) + '-all-blobs.json').read_text())
copy = W / 'candidate'
for name, expected in manifest.items():
    path = copy / name
    data = os.readlink(path).encode() if path.is_symlink() else path.read_bytes()
    assert hashlib.sha256(data).hexdigest() == expected['sha256'], name
assert subprocess.check_output(['git', 'rev-parse', 'tl/vw-m3-current-extent-landable-unit'], cwd=R, text=True).strip() == state['candidate']
assert not subprocess.check_output(['git', 'status', '--short'], cwd=R)
cohort = {name: subprocess.check_output(['git', '-C', '/home/user/work/' + name, 'rev-parse', 'HEAD'], text=True).strip()
          for name in ['agent', 'runtime', 'app', 'composition']}
changed_current = subprocess.check_output(['git', 'diff', '--name-only', state['base'], cohort['agent']], cwd=R, text=True).splitlines()
protected_drift = []
for name in state['protected_files']:
    before = subprocess.run(['git', 'show', state['base'] + ':' + name], cwd=R, capture_output=True)
    after = subprocess.run(['git', 'show', cohort['agent'] + ':' + name], cwd=R, capture_output=True)
    if (before.returncode, before.stdout) != (after.returncode, after.stdout):
        protected_drift.append(name)
assert not protected_drift, protected_drift
name = 'astrid/packs/rendering/rendering/renderers/remotion/run.py'
base = subprocess.check_output(['git', 'show', state['base'] + ':' + name], cwd=R)
new = (copy / name).read_bytes()
def function(data, name):
    return next(n for n in ast.walk(ast.parse(data)) if isinstance(n, ast.FunctionDef) and n.name == name)
assert ast.dump(function(base, 'capture_remotion_frames')) == ast.dump(function(new, 'capture_remotion_frames'))
def callback_calls(data):
    body = function(data, '_execute_remotion_locked')
    return [ast.dump(n) for n in ast.walk(body) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == 'on_scene_props']
assert callback_calls(base) == callback_calls(new)
new_tests = ['tests/packs/rendering/test_native_layer_extent.py',
             'tests/packs/rendering/test_remotion_layer_tail_compat.py',
             'tests/packs/rendering/test_live_scene_composition.py']
command = ['/home/user/work/venv-agent/bin/python', '-B', '-m', 'ruff', 'check', '--no-cache', *new_tests]
result = subprocess.run(command, cwd=copy, capture_output=True, text=True,
                        env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
Path(str(P) + '-ruff-tests.log').write_text(result.stdout + result.stderr)
assert result.returncode == 0, result.stdout + result.stderr
lint = {}
for name in ['astrid/core/rendering/service.py', 'astrid/packs/rendering/rendering/renderers/remotion/run.py']:
    before = subprocess.check_output(['git', 'show', state['base'] + ':' + name], cwd=R)
    pair = []
    for data in [before, (copy / name).read_bytes()]:
        command_product = ['/home/user/work/venv-agent/bin/python', '-B', '-m', 'ruff', 'check', '--no-cache', '--stdin-filename', name, '--output-format=json', '-']
        run = subprocess.run(command_product, input=data, cwd=copy, capture_output=True)
        assert run.returncode in [0, 1], run.stderr
        pair.append(json.loads(run.stdout))
    old_codes, new_codes = [Counter((x['code'], x['message']) for x in diagnostics) for diagnostics in pair]
    assert old_codes == new_codes, name
    lint[name] = {'baseline_diagnostics': len(pair[0]), 'candidate_diagnostics': len(pair[1]), 'same_codes_and_messages': True}
post = dict(candidate=state['candidate'], candidate_tracked_bytes_still_equal=True,
            blob_count=len(manifest), producer_ref_still_frozen=True, reviewer_checkout_clean=True,
            final_integration_cohort=cohort, current_agent_changes_since_base=changed_current,
            protected_drift=protected_drift, capture_remotion_frames_ast_identical=True,
            locked_on_scene_props_calls_ast_identical=True,
            direct_tests_ruff={'command': command, 'exit': result.returncode}, product_ruff=lint,
            test_environment={'node': subprocess.check_output(['/tmp/vw-m3-agent-gate-node20.19.4/bin/node', '--version'], text=True).strip(),
                              'typescript': json.loads(Path('/home/user/work/app/node_modules/typescript/package.json').read_text())['version'],
                              'private_node_scope': str(W / 'root-modules/node_modules'),
                              'shared_dependencies_written': False})
Path(str(P) + '-postcheck.json').write_text(json.dumps(post, indent=2) + '\n')
print(json.dumps(post, indent=2))
