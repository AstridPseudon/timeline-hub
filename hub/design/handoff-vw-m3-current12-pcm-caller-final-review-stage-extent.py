from pathlib import Path
import subprocess, hashlib, json, difflib, ast

REPO = Path('/home/user/work/wt/vw-m3-current12-pcm-caller-final-review')
ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
TASK = ORCH / 'workers/vw-m3-current12-pcm-caller-final-review'
PREFIX = str(ORCH / 'design/handoff-vw-m3-current12-pcm-caller-final-review-')
worker = ORCH / 'workers/vw-m3-current-extent-landable-unit'
assert (worker / 'DONE').exists(), 'extent source is not complete'

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

source = git('rev-parse', 'tl/vw-m3-current-extent-landable-unit').decode().strip()
base = (worker / 'base.txt').read_text().strip()
assert (worker / 'exit').read_text().strip() == '0'
audit = json.loads((ORCH / 'design/handoff-vw-m3-current-extent-landable-unit-source.json').read_text())
scope_patch = ORCH / 'design/handoff-vw-m3-current-extent-landable-unit-scope.patch'
assert hashlib.sha256(scope_patch.read_bytes()).hexdigest() == audit['delta_patch_sha256']
paths = list(audit['scope_sha256'])
expected = ['astrid/core/rendering/service.py',
    'astrid/packs/rendering/rendering/renderers/remotion/run.py', 'remotion/src/Root.tsx',
    'remotion/tests/root-metadata.test.cjs', 'tests/packs/rendering/test_native_layer_extent.py',
    'tests/packs/rendering/test_live_scene_composition.py', 'tests/packs/rendering/test_remotion_layer_tail_compat.py']
assert set(paths) == set(expected), paths
# No intervening unowned modifications of these paths at the worker's newer base.
old_base = 'c456b3281497653cecf44f61acd6fa30565d83c8'
for name in paths:
    old = subprocess.run(['git', 'show', old_base + ':' + name], cwd=REPO, capture_output=True)
    current = subprocess.run(['git', 'show', base + ':' + name], cwd=REPO, capture_output=True)
    assert old.returncode == current.returncode
    assert old.stdout == current.stdout, name
facts = audit['scope_sha256']
for leaf in ['baseline', 'candidate']:
    for name in paths:
        target = TASK / leaf / name
        original = subprocess.run(['git', 'show', base + ':' + name], cwd=REPO, capture_output=True)
        if original.returncode == 0:
            target.write_bytes(original.stdout)
        else:
            target.unlink(missing_ok=True)
    applied = subprocess.run(['patch', '--batch', '--fuzz=0', '--no-backup-if-mismatch', '--reject-file=-', '-p1', '-i', str(scope_patch)],
                             cwd=TASK / leaf, capture_output=True, text=True)
    assert applied.returncode == 0, applied.stdout + applied.stderr
    for name in paths:
        assert hashlib.sha256((TASK / leaf / name).read_bytes()).hexdigest() == facts[name], name
if source != base:
    for name in paths:
        assert hashlib.sha256(git('show', source + ':' + name)).hexdigest() == facts[name], name
else:
    source = 'completed exit-0/DONE sealed source patch; harness commit pending'
# Reset the candidate's helper/test so the original caller patch is applied verbatim.
helper = 'astrid/packs/rendering/rendering/renderers/remotion/normal_audio.py'
(TASK / 'candidate' / helper).write_bytes((TASK / 'baseline' / helper).read_bytes())
(TASK / 'candidate/tests/packs/rendering/test_normal_audio_run.py').unlink()
patch = ORCH / 'design/handoff-vw-m3-current12-pcm-caller-preserve-main-caller-only.patch'
result = subprocess.run(['patch', '--batch', '--fuzz=0', '--no-backup-if-mismatch', '--reject-file=-', '-p1', '-i', str(patch)],
                        cwd=TASK / 'candidate', capture_output=True, text=True)
assert result.returncode == 0, result.stdout + result.stderr
print(result.stdout)
# Exact new helper and tests; executor body equals the reviewed caller body.
for name in [helper, 'tests/packs/rendering/test_normal_audio_run.py']:
    assert (TASK / 'candidate' / name).read_bytes() == (REPO / name).read_bytes(), name
run = 'astrid/packs/rendering/rendering/renderers/remotion/run.py'
def executor(path):
    return next(ast.dump(node, include_attributes=False) for node in ast.parse(path.read_bytes()).body
                if isinstance(node, ast.FunctionDef) and node.name == '_execute_remotion_locked')
assert executor(TASK / 'candidate' / run) == executor(REPO / run)
# Reconstructing the baseline from the candidate by reversing the ORIGINAL patch
# proves every caller byte survived; no offset/phase repair is hidden in staging.
reverse = subprocess.run(['patch', '--dry-run', '--batch', '--fuzz=0', '--no-backup-if-mismatch', '--reject-file=-', '-R', '-p1', '-i', str(patch)],
                         cwd=TASK / 'candidate', capture_output=True, text=True)
assert reverse.returncode == 0, reverse.stdout + reverse.stderr
for leaf in ['baseline', 'candidate']:
    assert not list((TASK / leaf).rglob('*.orig'))
    assert not list((TASK / leaf).rglob('*.rej'))
Path(PREFIX + 'extent-stage.json').write_text(json.dumps({'source': source, 'base': base, 'paths': facts, 'extent_patch_sha256': audit['delta_patch_sha256'],
    'caller_patch_sha256': hashlib.sha256(patch.read_bytes()).hexdigest(), 'verbatim_patch_applied': True,
    'exact_caller_helper_test_and_executor_body': True}, indent=2) + '\n')
print('PASS: completed seven-path extent unit staged on paired private trees; verbatim caller patch retained')
