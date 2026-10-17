"""Real OS staging boundary for support(), without a renderer or Runtime task."""

import errno
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

from astrid.core.execution import generic_host as gh
from tests.core.execution import test_confinement_launch_integration as confinement

launch = confinement.launch


def test_support_asset_probe_uses_workspace_when_ambient_temp_is_denied(launch):
    policy, _, _, outside = launch
    source = Path(__file__).resolve().parents[3]
    workspace = policy.private_write_root
    (workspace / 'timeline.json').write_text(json.dumps({
        'theme': 'banodoco-default', 'tracks': [], 'clips': [],
    }))
    (workspace / 'assets.json').write_text('{"assets": {}}')
    policy = replace(policy, bootstrap_roots=(*policy.bootstrap_roots, source))
    code = """
import sys,json,tempfile
from pathlib import Path
sys.path[:0]=json.loads(sys.argv[1])
from astrid.core.rendering.contracts import RenderRequest,SCHEMA_VERSION
from astrid.packs.rendering.rendering.renderers.remotion import run
workspace,outside=map(Path,sys.argv[2:])
try:
 tempfile.gettempdir()
except FileNotFoundError:
 ambient_denied=True
else:
 raise AssertionError('fixture permits an ambient temporary directory')
stages=[]
def audit(event,args):
 if event=='tempfile.mkdtemp' and Path(args[0]).name.startswith('astrid-render-assets-'):
  stages.append(str(args[0]))
sys.addaudithook(audit)
request=RenderRequest(schema_version=SCHEMA_VERSION,timeline_path=str(workspace/'timeline.json'),
 assets_registry_path=str(workspace/'assets.json'),output_name='unused.mp4',
 backend_config={run.BACKEND_ID:{'project_dir':str(workspace/'absent-renderer')}})
report=run.support(request,workspace=workspace)
try:
 outside.read_text()
except OSError as error:
 denied=error.errno
else:
 raise AssertionError('outside read was permitted')
print(json.dumps({'ambient_denied':ambient_denied,'outside_errno':denied,'stages':stages,
 'supported':report.supported,'reasons':report.reasons,
 'remaining':sorted(p.name for p in workspace.iterdir())}))
"""
    paths = [str(source), *map(str, policy.bootstrap_roots)]
    plan = gh._confined_launch_plan(
        [sys.executable, '-I', '-S', '-B', '-c', code, json.dumps(paths), str(workspace), str(outside)],
        policy=policy, cwd=source / 'astrid/packs/rendering',
    )
    options = plan.subprocess_options()
    options['env'].update({name: str(outside.parent) for name in ('TMPDIR', 'TMP', 'TEMP')})
    process = subprocess.Popen(plan.argv, **options, text=True)
    stdout, stderr = process.communicate()
    assert process.returncode == 0, stderr
    result = json.loads(stdout.splitlines()[-1])
    # The intentionally absent renderer remains unsupported. This control
    # proves only real asset validation/staging and the unchanged OS fences.
    assert result['supported'] is False
    assert result['ambient_denied'] and result['outside_errno'] in (errno.EPERM, errno.EACCES)
    assert len(result['stages']) == 1, result
    assert Path(result['stages'][0]).parent == workspace
    assert not Path(result['stages'][0]).exists()
    assert not any('local assets are not renderable' in reason for reason in result['reasons']), result
    assert len(result['reasons']) == 1 and result['reasons'][0].startswith('Remotion project directory not found:')
    assert result['remaining'] == ['assets.json', 'timeline.json']
    print(json.dumps({'original_wait': process.returncode, **result}))
