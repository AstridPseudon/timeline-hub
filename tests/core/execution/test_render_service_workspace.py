"""Real private-output write fence at the RenderService workspace producer."""

import errno
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

from astrid.core.execution import generic_host as gh
from tests.core.execution import test_confinement_launch_integration as confinement

launch = confinement.launch


def test_render_service_workspace_stays_inside_existing_output_grant(launch):
    policy, *_ = launch
    source = Path(__file__).resolve().parents[3]
    outputs = policy.attempt_root / 'outputs'
    outputs.mkdir(mode=0o700)
    policy = replace(policy, private_write_root=outputs,
                     bootstrap_roots=(*policy.bootstrap_roots, source))
    code = """
import sys,json,tempfile
from pathlib import Path
sys.path[:0]=json.loads(sys.argv[1])
from astrid.core.rendering.service import _render_workspace_parent
outputs=Path(sys.argv[2]);output=outputs/'video.mp4'
try:
 (outputs.parent/'forbidden-sibling').write_text('forbidden')
except OSError as error:
 denied=error.errno
else:
 raise AssertionError('attempt root unexpectedly writable')
outside_denials={}
for base in (Path('/tmp'),Path('/var/tmp'),outputs.parent.parent):
 try:
  (base/('astrid-denied-'+outputs.parent.name)).write_text('forbidden')
 except OSError as error:
  outside_denials[str(base)]=error.errno
 else:
  raise AssertionError(f'outside path unexpectedly writable: {base}')
parent=_render_workspace_parent(output)
with tempfile.TemporaryDirectory(prefix='.video.mp4.render-service-',dir=str(parent)) as raw:
 stage=Path(raw)
 (stage/'owned').write_text('private scratch')
 assert (stage/'owned').read_text()=='private scratch'
print(json.dumps({'parent':str(parent),'stage':str(stage),'stage_absent':not stage.exists(),
 'sibling_write_errno':denied,'outside_write_errnos':outside_denials,
 'remaining':list(p.name for p in outputs.iterdir())}))
"""
    plan = gh._confined_launch_plan(
        [sys.executable, '-I', '-S', '-B', '-c', code,
         json.dumps([str(source), *map(str, policy.bootstrap_roots)]), str(outputs)],
        policy=policy,
    )
    process = subprocess.Popen(plan.argv, **plan.subprocess_options(), text=True)
    stdout, stderr = process.communicate()
    assert process.returncode == 0, stderr
    result = json.loads(stdout.splitlines()[-1])
    assert Path(result['parent']) == outputs
    assert Path(result['stage']).parent == outputs and result['stage_absent']
    assert result['sibling_write_errno'] in (errno.EPERM, errno.EACCES)
    assert len(result['outside_write_errnos']) == 3
    assert all(value in (errno.EPERM, errno.EACCES)
               for value in result['outside_write_errnos'].values())
    assert result['remaining'] == []
    print(json.dumps({'original_wait': process.returncode, **result}))


def test_readonly_render_lock_stays_out_of_source_and_inside_workspace(launch):
    policy, *_ = launch
    source = Path(__file__).resolve().parents[3]
    policy = replace(policy, bootstrap_roots=(*policy.bootstrap_roots, source))
    code = """
import sys,json
from pathlib import Path
sys.path[:0]=json.loads(sys.argv[1])
from astrid.packs.rendering.rendering.renderers.remotion import lock
workspace=Path(sys.argv[2])
try:
 with lock.remotion_render_lock():pass
except OSError as error:
 denied=error.errno
else:
 raise AssertionError('legacy source lock unexpectedly writable')
path=workspace/'.astrid-registry.lock'
with lock._render_lock_at(path):
 assert lock.remotion_render_lock_held()
 try:
  with lock.remotion_render_lock():pass
 except RuntimeError as error:
  assert 'non-recursive' in str(error)
 else:raise AssertionError('recursive acquisition was permitted')
 identity=path.stat().st_ino
assert not lock.remotion_render_lock_held()
with lock._render_lock_at(path):assert path.stat().st_ino==identity
print(json.dumps({'source_write_errno':denied,'path':str(path),'inode':identity,'released':not lock.remotion_render_lock_held()}))
"""
    plan = gh._confined_launch_plan(
        [sys.executable, '-I', '-S', '-B', '-c', code,
         json.dumps([str(source), *map(str, policy.bootstrap_roots)]), str(policy.private_write_root)],
        policy=policy,
    )
    process = subprocess.Popen(plan.argv, **plan.subprocess_options(), text=True)
    stdout, stderr = process.communicate()
    assert process.returncode == 0, stderr
    result = json.loads(stdout.splitlines()[-1])
    assert result['source_write_errno'] in (errno.EPERM, errno.EACCES)
    assert Path(result['path']).parent == policy.private_write_root and result['released']
    print(json.dumps({'original_wait': process.returncode, **result}))
