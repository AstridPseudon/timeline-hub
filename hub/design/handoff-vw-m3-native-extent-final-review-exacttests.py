from pathlib import Path
import hashlib, io, json, os, shutil, subprocess, tarfile

ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
WORK = ORCH / 'workers/vw-m3-native-extent-final-review'
PRODUCER = ORCH / 'workers/vw-m3-native-layer-extent-fix'
REPO = Path('/home/user/work/wt/vw-m3-native-extent-final-review')
REF = 'tl/vw-m3-native-layer-extent-fix'
PREFIX = ORCH / 'design/handoff-vw-m3-native-extent-final-review'
NODE = '/tmp/vw-m3-agent-gate-node20.19.4/bin/node'
PYTHON = '/home/user/work/venv-agent/bin/python'
BASE = 'abd41eb2a6a8fe9224028018ac65225018e490bd'
assert (PRODUCER / 'exit').read_text().strip() == '0'
assert (PRODUCER / 'DONE').exists()
assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=REPO).strip()
TIP = subprocess.check_output(['git', 'rev-parse', REF], cwd=REPO, text=True).strip()
assert TIP != BASE
CANDIDATE = WORK / 'candidate'
CANDIDATE.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(subprocess.check_output(['git', 'archive', TIP], cwd=REPO))) as archive:
    archive.extractall(CANDIDATE, filter='data')
patch = (WORK / 'root-regressions.patch').read_bytes()
for copy in [WORK / 'baseline', CANDIDATE]:
    if not (copy / 'remotion/tests/root-metadata.test.cjs').exists():
        subprocess.run(['patch', '-p1'], input=patch, cwd=copy, check=True, capture_output=True)
modules = WORK / 'root-modules/node_modules'
modules.mkdir(parents=True, exist_ok=True)
if not (modules / 'typescript').exists():
    (modules / 'typescript').symlink_to('/home/user/work/app/node_modules/typescript', target_is_directory=True)
root_test = CANDIDATE / 'remotion/tests/root-metadata.test.cjs'
supplement = WORK / 'root-supplement.test.cjs'
helpers = root_test.read_text().split("test('Root registers", 1)[0]
supplement.write_text(helpers + '''
test('both callbacks distinguish identical empty and sparse layers with original 300/600 extents and rational FPS', async () => {
  for (const local of [1, 31]) for (const total of [300, 600]) {
    const fps = 30000 / 1001;
    const props = propsFor(timelineWithDuration(local, {
      clips: local === 1 ? [] : [{id: 'early'}],
      theme_overrides: {visual: {canvas: {width: 320, height: 180, fps}}},
    }), {astridCompositionDurationInFrames: total});
    assertSameMetadata(await metadataFor(props), {width: 320, height: 180, fps, durationInFrames: total});
  }
});
test('boolean retained extents are refused by both callbacks', async () => {
  for (const value of [true, false]) await assert.rejects(() => metadataFor(
    propsFor(timelineWithDuration(1), {astridCompositionDurationInFrames: value})));
});
''')
# Keep the independently authored behavior expectations as a flat handoff artifact.
shutil.copyfile(WORK / 'test_original_bad_cases.py', str(PREFIX) + '-probe.py')
files = subprocess.check_output(['git', 'diff', '--name-only', BASE, TIP], cwd=REPO, text=True).splitlines()
sources = {'base': BASE, 'candidate': TIP, 'candidate_tree': subprocess.check_output(['git', 'rev-parse', TIP + '^{tree}'], cwd=REPO, text=True).strip(),
           'producer_exit': (PRODUCER / 'exit').read_text().strip(), 'setup': json.loads((WORK / 'setup.json').read_text()), 'files': {}}
for name in files:
    new = subprocess.check_output(['git', 'show', TIP + ':' + name], cwd=REPO)
    old = subprocess.run(['git', 'show', BASE + ':' + name], cwd=REPO, capture_output=True)
    sources['files'][name] = {'candidate_sha256': hashlib.sha256(new).hexdigest(), 'candidate_bytes': len(new),
                            'baseline_sha256': hashlib.sha256(old.stdout).hexdigest() if old.returncode == 0 else None}
for name in ['astrid/core/timeline/banodoco_composer.py', 'astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py',
             'astrid/core/timeline/duration.py', 'remotion/normal-audio-sources.mjs', 'remotion/attempt-envelope-pcm.mjs']:
    old = subprocess.check_output(['git', 'show', BASE + ':' + name], cwd=REPO)
    new = subprocess.check_output(['git', 'show', TIP + ':' + name], cwd=REPO)
    sources['files'][name] = {'candidate_sha256': hashlib.sha256(new).hexdigest(), 'baseline_sha256': hashlib.sha256(old).hexdigest(), 'unchanged': old == new}
Path(str(PREFIX) + '-sourcebytes.json').write_text(json.dumps(sources, indent=2) + '\n')
Path(str(PREFIX) + '-scope.patch').write_bytes(subprocess.check_output(['git', 'diff', '--binary', BASE, TIP], cwd=REPO))
results = []
def run(label, argv, cwd, env, expected):
    logfile = Path(str(PREFIX) + '-' + label + '.log')
    print(label + ': running', flush=True)
    with logfile.open('w') as output:
        result = subprocess.run(argv, cwd=cwd, env=env, stdout=output, stderr=subprocess.STDOUT)
    row = {'label': label, 'argv': list(map(str, argv)), 'cwd': str(cwd), 'environment': {k: env[k] for k in ['PYTHONPATH', 'PYTHONDONTWRITEBYTECODE', 'ASTRID_NODE_EXECUTABLE', 'ASTRID_REMOTION_PROJECT_DIR', 'NODE_PATH', 'ROOT_SOURCE_DIR'] if k in env},
           'exit': result.returncode, 'expected_exit': expected, 'log': str(logfile)}
    results.append(row)
    Path(str(PREFIX) + '-results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(label + ': exit ' + str(result.returncode) + '\n' + '\n'.join(logfile.read_text().splitlines()[-6:]), flush=True)
    assert result.returncode == expected, row

env = dict(os.environ)
for key in ['NODE_OPTIONS', 'NODE_PATH', 'PYTHONPYCACHEPREFIX']:
    env.pop(key, None)
env.update(PYTHONDONTWRITEBYTECODE='1', ASTRID_NODE_EXECUTABLE=NODE,
           ASTRID_REMOTION_PROJECT_DIR=str(WORK / 'audio-project'),
           PATH=str(Path(NODE).parent) + ':' + env['PATH'])
pytest = [PYTHON, '-B', '-m', 'pytest', '-q', '-o', 'addopts=', '-p', 'no:cacheprovider', '--tb=short']
for label, copy, expected in [('baseline', WORK / 'baseline', 1), ('candidate', CANDIDATE, 0)]:
    selected = dict(env, PYTHONPATH=str(copy), ROOT_SOURCE_DIR=str(copy / 'remotion/src'))
    run(label + '-independent', pytest + [str(WORK / 'test_original_bad_cases.py')], copy, selected, expected)
    node_env = dict(selected, NODE_PATH=str(modules))
    run(label + '-root-patch', [NODE, str(root_test)], copy, node_env, expected)
    run(label + '-root-supplement', [NODE, str(supplement)], copy, node_env, expected)
selected = dict(env, PYTHONPATH=str(CANDIDATE))
run('targeted', pytest + [
    'tests/packs/rendering/test_native_layer_extent.py',
    'tests/packs/rendering/test_remotion_native_window.py',
    'tests/packs/rendering/test_normal_audio_run.py',
    'tests/packs/rendering/test_normal_audio_sources.py',
    'tests/packs/rendering/test_normal_audio_source_phase.py'], CANDIDATE, selected, 0)
run('service-neighbors', pytest + ['tests/core/rendering/test_service.py', '-k', 'window_timeline or segment_request'], CANDIDATE, selected, 0)
assert subprocess.check_output(['git', 'rev-parse', REF], cwd=REPO, text=True).strip() == TIP
assert not subprocess.check_output(['git', 'status', '--porcelain'], cwd=REPO).strip()
print('All expected outcomes confirmed for frozen ' + TIP, flush=True)
