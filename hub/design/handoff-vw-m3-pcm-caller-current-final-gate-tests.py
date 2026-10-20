from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile

O = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
W = O / 'workers/vw-m3-pcm-caller-current-final-gate'
P = O / 'design/handoff-vw-m3-pcm-caller-current-final-gate'
PY = '/home/user/work/venv-agent/bin/python'
NODE = '/tmp/vw-m3-agent-gate-node20.19.4/bin/node'
tree = sys.argv[1]
source = W / tree
project = W / 'audio-project'
if not project.exists():
    project.mkdir()
    modules = project / 'node_modules'
    modules.mkdir()
    package = modules / '@banodoco/timeline-composition'
    package.mkdir(parents=True)
    archive = source / 'remotion/artifacts/banodoco-timeline-composition-0.0.12.tgz'
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == '0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3'
    hashes = {}
    with tarfile.open(archive) as tgz:
        assert len(tgz.getmembers()) == 77
        for member in tgz.getmembers():
            assert member.isfile() and member.name.startswith('package/')
            dest = package / member.name.removeprefix('package/')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(tgz.extractfile(member).read())
            hashes[str(dest.relative_to(package))] = hashlib.sha256(dest.read_bytes()).hexdigest()
    shared = Path('/home/user/work/composition/node_modules')
    for row in shared.iterdir():
        if row.name.startswith('.'):
            continue
        for leaf in list(row.iterdir()) if row.name.startswith('@') else [row]:
            dest = modules / leaf.relative_to(shared)
            assert not os.path.lexists(dest)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.symlink_to(leaf, target_is_directory=leaf.is_dir())
    Path(str(P)+'-composition77.json').write_text(json.dumps(hashes, indent=2)+'\n')

# Refresh private entrypoints from the exact tree under test; shared leaves stay read-only.
for name in ['attempt-envelope-pcm.mjs', 'compiled-audio-source-clock.mjs', 'normal-audio-sources.mjs', 'package.json', 'package-lock.json']:
    shutil.copyfile(source / 'remotion' / name, project / name)
if not (project / 'tests').exists():
    shutil.copytree(source / 'remotion/tests', project / 'tests')

env = dict(os.environ)
for key in ['NODE_OPTIONS', 'NODE_PATH', 'NODE_TEST_CONTEXT', 'PYTHONPYCACHEPREFIX', 'PYTHONHOME']:
    env.pop(key, None)
env.update(PYTHONPATH=str(source), PYTHONDONTWRITEBYTECODE='1',
           ASTRID_NODE_EXECUTABLE=NODE, ASTRID_REMOTION_PROJECT_DIR=str(project),
           ASTRID_TEST_NODE_MODULES=str(project/'node_modules'),
           ASTRID_COMPOSITION_TEST_NODE_MODULES=str(project/'node_modules'),
           ROOT_SOURCE_DIR=str(source/'remotion/src'),
           PATH=str(Path(NODE).parent)+':'+env['PATH'])
pytest = [PY, '-B', '-m', 'pytest', '-q', '-o', 'addopts=', '-p', 'no:cacheprovider', '--tb=short']
rows = []

def run(label, command):
    child_env = dict(env)
    if label == 'root':
        child_env['NODE_PATH'] = str(project/'node_modules')
    temp = W / ('tmp-'+tree+'-'+label)
    if 'pytest' in command:
        command = command + ['--basetemp='+str(temp)]
    log = Path(str(P)+'-'+tree+'-'+label+'.log')
    with log.open('w') as out:
        result = subprocess.run(command, cwd=source, env=child_env, stdout=out, stderr=subprocess.STDOUT)
    rows.append(dict(label=label, command=command, cwd=str(source), environment={k:child_env.get(k) for k in ['PYTHONPATH','ASTRID_NODE_EXECUTABLE','ASTRID_REMOTION_PROJECT_DIR','ASTRID_TEST_NODE_MODULES','ASTRID_COMPOSITION_TEST_NODE_MODULES','NODE_PATH','ROOT_SOURCE_DIR','PATH']}, exit=result.returncode, log=str(log)))
    Path(str(P)+'-'+tree+'-results.json').write_text(json.dumps(rows, indent=2)+'\n')
    print(tree, label, result.returncode, '\n'+'\n'.join(log.read_text().splitlines()[-12:]), flush=True)
    if temp.exists():
        shutil.rmtree(temp)

files = ['test_scene_source_carry.py', 'test_live_scene_composition.py',
         'test_composition_package.py::test_locked_release_is_built_and_requires_no_separate_schema_or_theme',
         'test_remotion_native_window.py', 'test_native_layer_extent.py',
         'test_remotion_capture_scene_props.py', 'test_remotion_layer_tail_compat.py',
         'test_normal_audio_sources.py', 'test_normal_audio_source_phase.py']
if tree == 'candidate':
    files += ['test_normal_audio_run.py']
run('paired', pytest+['tests/packs/rendering/'+name for name in files]+['-k','not real_render'])
run('root', [NODE,str(source/'remotion/tests/root-metadata.test.cjs')])
run('service', pytest+['tests/core/rendering/test_service.py','-k','window_timeline or segment_request'])
if tree == 'candidate':
    run('imports', [PY,'-B','-c', "import astrid, tests, astrid.core.rendering.service as s; from astrid.packs.rendering.rendering.renderers.remotion import run; from pathlib import Path; root=Path.cwd(); paths=[Path(x.__file__).resolve() for x in [astrid,tests,s,run]]; assert all(p.is_relative_to(root) for p in paths),paths; print(paths)"])
    run('http-portability', pytest+['tests/packs/rendering/test_normal_audio_http.py','-k','project_dir_'])
    run('native-node', [NODE,str(project/'tests/normal-audio-native-sources.test.mjs')])
    run('normal-node', [NODE,str(project/'tests/normal-audio-sources.test.mjs')])
    run('independent', pytest+[str(P)+'-probe.py'])
    run('m2', pytest+['tests/editing_conformance/test_compile_contracts.py',
                      'tests/timeline/test_shot_composition_projection.py',
                      'tests/core/timeline/test_shot_composition_projection_volume.py',
                      'tests/timeline/test_authoring_bundle.py::test_full_authored_field_edits_compile_without_normalizing_opaque_fields',
                      'tests/timeline/test_authoring_bundle.py::test_placement_edits_without_shared_projection_semantics_fail_before_publish',
                      'tests/timeline/test_authoring_bundle.py::test_publish_uses_one_compilation_and_returns_complete_mapping',
                      'tests/timeline/test_authoring_bundle.py::test_independent_unique_shot_reuses_untouched_revision_and_direct_edits_compile_identically',
                      'tests/core/timeline/test_source_role_tracks.py',
                      'tests/timeline/test_timeline_characterization.py'])
    run('ruff', [PY,'-B','-m','ruff','check','--no-cache','astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py','tests/packs/rendering/test_normal_audio_run.py','tests/packs/rendering/test_normal_audio_http.py'])
sys.exit(any(row['exit'] != 0 for row in rows))
