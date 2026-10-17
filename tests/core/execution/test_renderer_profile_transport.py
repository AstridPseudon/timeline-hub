"""Real Seatbelt checks for private policy transport, not a render witness."""

import errno
import json
import os
import subprocess
import sys
from dataclasses import replace

import pytest

from astrid.core.execution import generic_host as gh
from astrid.core.execution.renderer_transport import RetainedRendererProfile
from tests.core.execution import test_confinement_launch_integration as confinement

launch = confinement.launch


def test_large_exact_profile_keeps_read_write_fences(launch):
    policy, _, inside, outside = launch
    probe = """
import json,sys
from pathlib import Path
result={}
for label,raw in zip(('inside','outside','profile','directory'),sys.argv[1:]):
 try:
  if label=='directory': Path(raw,'replacement').write_text('forbidden')
  elif label=='profile': Path(raw).write_text('forbidden')
  else: result[label]=Path(raw).read_text()
 except OSError as exc: result[label]=exc.errno
print(json.dumps(result))
"""
    base = gh._confined_launch_plan([sys.executable, '-I', '-S', '-B', '-c', probe], policy=policy)
    # Exact valid clauses, larger than Darwin argv, without extra authority.
    profile = base.argv[2] + '(allow sysctl-read)\n' * 70000
    assert len(profile.encode()) > os.sysconf('SC_ARG_MAX')
    retained = RetainedRendererProfile.create(profile, policy)
    assert retained.path.read_bytes() == profile.encode()
    plan = replace(base, argv=(base.argv[0], '-f', str(retained.path), *base.argv[3:],
                              str(inside), str(outside), str(retained.path), str(retained.path.parent)),
                   renderer_profile=retained)
    options = plan.subprocess_options()
    process = subprocess.Popen(plan.argv, **options, text=True)
    stdout, stderr = process.communicate()
    assert process.returncode == 0, stderr
    result = json.loads(stdout)
    assert result['inside'] == 'synthetic-inside'
    assert all(result[key] in (errno.EPERM, errno.EACCES)
               for key in ('outside', 'profile', 'directory')), result
    retained.validate()
    print(json.dumps({'profile_bytes': len(profile.encode()), 'sha256': retained.sha256,
                      'argv_bytes': sum(len(s.encode()) + 1 for s in plan.argv),
                      'original_wait': process.returncode, 'fences': result}))


@pytest.mark.parametrize('mutation', ['content', 'replacement', 'symlink', 'hardlink', 'mode', 'directory'])
def test_changed_profile_refused_before_launch(launch, mutation):
    policy, *_ = launch
    retained = RetainedRendererProfile.create('(version 1)\n(deny default)\n', policy)
    path = retained.path
    if mutation == 'directory':
        path.parent.chmod(0o755)
    elif mutation == 'mode':
        path.chmod(0o600)
    elif mutation == 'hardlink':
        os.link(path, path.with_name('alias'))
    elif mutation in ('replacement', 'symlink'):
        original = path.read_bytes()
        path.rename(path.with_name('original'))
        if mutation == 'symlink':
            other = path.with_name('other')
            other.write_bytes(original)
            path.symlink_to(other)
        else:
            path.write_bytes(original)
            path.chmod(0o400)
    else:
        path.chmod(0o600)
        path.write_text('(version 1)\n(allow default)\n')
        path.chmod(0o400)
    with pytest.raises((ValueError, OSError)):
        retained.validate()


def test_policy_file_cannot_be_created_in_workload_writes(launch):
    policy, *_ = launch
    policy = replace(policy, private_write_root=policy.attempt_root)
    with pytest.raises(ValueError, match='overlaps workload writes'):
        RetainedRendererProfile.create('(version 1)\n(deny default)\n', policy)
    assert not list(policy.attempt_root.glob('.renderer-policy-*'))
