from pathlib import Path
import json, os, subprocess

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
TASK = ORCH / 'workers/vw-m3-current12-pcm-caller-final-review'
PREFIX = str(ORCH / 'design/handoff-vw-m3-current12-pcm-caller-final-review-')
assert Path(PREFIX + 'extent-stage.json').exists()
project = TASK / 'audio-project'
common = [
    'tests/packs/rendering/test_scene_source_carry.py',
    'tests/packs/rendering/test_live_scene_composition.py',
    'tests/packs/rendering/test_composition_package.py::test_locked_release_is_built_and_requires_no_separate_schema_or_theme',
    'tests/packs/rendering/test_remotion_native_window.py',
    'tests/packs/rendering/test_native_layer_extent.py',
    'tests/packs/rendering/test_remotion_capture_scene_props.py',
    'tests/packs/rendering/test_remotion_layer_tail_compat.py',
    'tests/packs/rendering/test_normal_audio_sources.py',
    'tests/packs/rendering/test_normal_audio_source_phase.py',
]
results = []
for leaf in ['baseline', 'candidate']:
    tree = TASK / leaf
    env = {k:v for k,v in os.environ.items() if k not in ['NODE_OPTIONS','NODE_PATH','NODE_TEST_CONTEXT']}
    env.update(PYTHONDONTWRITEBYTECODE='1', PYTHONPATH=str(tree),
        ASTRID_NODE_EXECUTABLE='/tmp/vw-m3-agent-gate-node20.19.4/bin/node',
        ASTRID_REMOTION_PROJECT_DIR=str(project), ASTRID_TEST_NODE_MODULES=str(project / 'node_modules'),
        ASTRID_COMPOSITION_TEST_NODE_MODULES=str(project / 'node_modules'),
        PATH='/tmp/vw-m3-agent-gate-node20.19.4/bin:' + env['PATH'])
    argv = ['/home/user/work/venv-agent/bin/python', '-B', '-m', 'pytest', '-q', '-o', 'addopts=',
            '-p', 'no:cacheprovider', '--tb=short', *common, '-k', 'not real_render']
    if leaf == 'candidate': argv.insert(-2, 'tests/packs/rendering/test_normal_audio_run.py')
    log = Path(PREFIX + 'final-' + leaf + '.log')
    with log.open('w') as output:
        result = subprocess.run(argv, cwd=tree, env=env, stdout=output, stderr=subprocess.STDOUT)
    results.append({'tree': str(tree), 'argv':argv, 'exit_code':result.returncode, 'log':str(log)})
    print(leaf, 'exit',result.returncode, flush=True)
    print('\n'.join(log.read_text().splitlines()[-10:]), flush=True)
Path(PREFIX + 'paired-results.json').write_text(json.dumps(results, indent=2) + '\n')
assert all(row['exit_code'] == 0 for row in results)
