"""Pure regression checks for the root-smoke child environment."""
import importlib.util
import os
from pathlib import Path
import tempfile


ORCH = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch')
CONTROLLER = ORCH / 'design/handoff-vw-m3-root-smoke-central-ready-controller.py'
spec = importlib.util.spec_from_file_location('root_smoke_controller_env_fix', CONTROLLER)
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)


with tempfile.TemporaryDirectory(prefix='vw-m3-root-controller-env-fix-') as temp_name:
    temp = Path(temp_name)
    sentinel_home = '/preserved/manager-home'
    previous_home = os.environ.get('HOME')
    os.environ['HOME'] = sentinel_home
    try:
        child_env = controller.environment(Path('/source'), Path('/project'), temp)
    finally:
        if previous_home is None:
            os.environ.pop('HOME', None)
        else:
            os.environ['HOME'] = previous_home

    assert child_env['HOME'] == sentinel_home
    assert child_env['HOME'] != str(temp)
    for name in ('TMPDIR', 'XDG_CACHE_HOME', 'XDG_CONFIG_HOME', 'XDG_STATE_HOME', 'XDG_RUNTIME_DIR'):
        path = Path(child_env[name])
        assert path.is_relative_to(temp), (name, path, temp)
        assert path.exists() and path.is_dir(), (name, path)
    assert Path(child_env['XDG_RUNTIME_DIR']).stat().st_mode & 0o777 == 0o700

print('PASS: inherited HOME is preserved; task-scoped TMPDIR/XDG paths are prepared')
