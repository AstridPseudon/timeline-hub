from pathlib import Path
from collections import Counter
import hashlib
import importlib.util
import json
import subprocess

P = Path(__file__).with_name('handoff-vw-m3-pcm-caller-current-final-gate')
spec = importlib.util.spec_from_file_location('prepare',str(P)+'-prepare.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
W = m.W
source = W/'candidate'
freeze = json.loads(Path(str(P)+'-freeze.json').read_text())
assert m.git('rev-parse','tl/vw-m3-pcm-caller-current-land-unit').decode().strip() == freeze['producer_sha']
assert not m.git('status','--porcelain')
rows = json.loads(Path(str(P)+'-blobs.json').read_text())
for row in rows:
    dest = source/row['path']
    data = dest.readlink().as_posix().encode() if row['mode']=='120000' else dest.read_bytes()
    assert hashlib.sha256(data).hexdigest() == row['sha256'], row['path']
    if row['mode'] != '120000':
        assert bool(dest.stat().st_mode & 0o111) == (row['mode']=='100755'),row['path']
expected = {row['path'] for row in rows}
actual = {str(path.relative_to(source)) for path in source.rglob('*') if path.is_file() or path.is_symlink()}
assert actual == expected, sorted(actual ^ expected)
for name in ['normal_audio.py']:
    path = 'astrid/packs/rendering/rendering/renderers/remotion/'+name
    assert (source/path).read_bytes() == m.git('show','b24a2acf565a3ab3ce23b35c6ea0a5196c6decd6:'+path)
path = 'tests/packs/rendering/test_normal_audio_run.py'
assert (source/path).read_bytes() == m.git('show','b24a2acf565a3ab3ce23b35c6ea0a5196c6decd6:'+path)
path = 'tests/packs/rendering/test_normal_audio_http.py'
assert (source/path).read_bytes() == m.git('show','e5a636d59:'+path)
after = m.shared_manifest()
assert after == json.loads(Path(str(P)+'-shared-before.json').read_text())
Path(str(P)+'-shared-after.json').write_text(json.dumps(after,sort_keys=True)+'\n')
package = W/'audio-project/node_modules/@banodoco/timeline-composition'
hashes = json.loads(Path(str(P)+'-composition77.json').read_text())
assert {str(p.relative_to(package)):hashlib.sha256(p.read_bytes()).hexdigest() for p in package.rglob('*') if p.is_file()} == hashes
run = 'astrid/packs/rendering/rendering/renderers/remotion/run.py'
diagnostics=[]
for label in ['baseline','candidate']:
    result=subprocess.run(['/home/user/work/venv-agent/bin/ruff','check','--no-cache','--output-format=json','--stdin-filename',run,'-'],input=(W/label/run).read_bytes(),capture_output=True,cwd=source)
    assert result.returncode==1
    values=json.loads(result.stdout)
    diagnostics.append(Counter((row['code'],row['message']) for row in values))
assert diagnostics[0] == diagnostics[1]
for label in ['baseline','candidate']:
    results=json.loads(Path(str(P)+'-'+label+'-results.json').read_text())
    assert all(row['exit']==0 for row in results),label
record=dict(source_sha=freeze['producer_sha'],blobs_reverified=len(rows),extra_files=0,
            shared_entries_unchanged=len(after),public12_members_unchanged=len(hashes),
            helper_and_normal_tests_exact_frozen_caller=True,http_tests_exact_portable_source=True,
            runner_diagnostics_unchanged=[dict(code=code,message=message,count=count) for (code,message),count in diagnostics[0].items()],
            assigned_worktree_clean=True,all_test_lanes_pass=True)
Path(str(P)+'-postcheck.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
