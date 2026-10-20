from pathlib import Path
import ast, hashlib, json, subprocess

repo=Path('/home/user/work/wt/vw-m3-current12-pcm-caller-final-review')
orch=Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
task=orch/'workers/vw-m3-current12-pcm-caller-final-review'
prefix=str(orch/'design/handoff-vw-m3-current12-pcm-caller-final-review-')
fixture=json.loads(Path(prefix+'fixtures.json').read_text())
extent=json.loads(Path(prefix+'extent-stage.json').read_text())
original=json.loads((orch/'design/handoff-vw-m3-current12-pcm-caller-preserve-main-source.json').read_text())
tracked=subprocess.check_output(['git','ls-files'],cwd=repo,text=True).splitlines()
expected=set(fixture['paths'])|{'astrid/packs/rendering/rendering/renderers/remotion/run.py',
    'remotion/src/Root.tsx','tests/packs/rendering/test_live_scene_composition.py',
    'tests/packs/rendering/test_remotion_layer_tail_compat.py'}
changed={}
for name in set(tracked)|{'tests/packs/rendering/test_remotion_layer_tail_compat.py'}:
    path=task/'candidate'/name
    assert path.is_file(),name
    if not (repo/name).exists() or path.read_bytes()!=(repo/name).read_bytes():
        changed[name]=hashlib.sha256(path.read_bytes()).hexdigest()
assert set(changed)==expected, (set(changed)-expected,expected-set(changed))
for name,value in fixture['paths'].items():
    for leaf in ['baseline','candidate']:
        assert hashlib.sha256((task/leaf/name).read_bytes()).hexdigest()==value,name
for name,value in extent['paths'].items():
    assert hashlib.sha256((task/'baseline'/name).read_bytes()).hexdigest()==value,name
    if name!='astrid/packs/rendering/rendering/renderers/remotion/run.py':
        assert hashlib.sha256((task/'candidate'/name).read_bytes()).hexdigest()==value,name
for name,value in original['protected'].items():
    if name in fixture['paths'] or name in extent['paths']: continue
    for leaf in ['baseline','candidate']:
        assert hashlib.sha256((task/leaf/name).read_bytes()).hexdigest()==value,name
# Final candidate keeps reviewed caller helper and tests exactly.
for name in original['caller_only_files'][1:]:
    assert (task/'candidate'/name).read_bytes()==(repo/name).read_bytes(),name
serializer='astrid/packs/rendering/shared/rendering_backend/__init__.py'
assert (task/'candidate'/serializer).read_bytes()==(repo/serializer).read_bytes()
for leaf in ['baseline','candidate']:
    for path in (task/leaf).rglob('*'):
        assert path.suffix not in ['.orig','.rej','.bak'],str(path)
        if path.is_file() and not path.is_symlink():
            assert str(path.relative_to(task/leaf)) in tracked or path.name=='test_remotion_layer_tail_compat.py',str(path)
# The reviewed staging HEAD retains the original historical archive. The
# latest extent worker needed to provision it; do not imply its latest base tracks it.
old='remotion/artifacts/banodoco-timeline-composition-0.0.10.tgz'
assert (task/'candidate'/old).read_bytes()==(repo/old).read_bytes()
Path(prefix+'private-guard.json').write_text(json.dumps({'candidate_delta_from_reviewed_caller':changed,
    'no_other_candidate_file_changed':True,'old10_fixture_retained_from_reviewed_staging_head':old,
    'fixture_overlay':fixture,'extent_overlay':extent},indent=2)+'\n')
print('PASS: private candidate has only 8 approved fixture changes + 4 extent/tail changes; caller/M2/serializer/client/pins retained; no temporary or backup files')
