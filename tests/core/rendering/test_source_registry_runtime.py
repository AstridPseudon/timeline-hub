"""Source registry children keep the Runtime used by their launching process."""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from astrid.core.rendering import remotion_runtime as runtime
from astrid.core.subprocess_env import build_child_subprocess_env


@pytest.mark.parametrize('generator', [False, True])
@pytest.mark.parametrize('shadowed', [False, True])
def test_filtered_source_registry_child_imports_parent_runtime(tmp_path, monkeypatch, generator, shadowed):
    # Rendering transport removes PYTHONPATH even when the host supplied an
    # approved Runtime checkout. Exercise the real fresh child, not sys.modules.
    parent = {
        'HOME': str(tmp_path),
        'PATH': os.environ.get('PATH', os.defpath),
        'PYTHONPATH': str(Path(runtime.platform.__file__).resolve().parents[1]),
        runtime.REMOTION_PROJECT_DIR_ENV: os.environ.get(
            runtime.REMOTION_PROJECT_DIR_ENV, str(runtime.REPO_ROOT / 'remotion')),
        runtime.NODE_EXECUTABLE_ENV: os.environ.get(runtime.NODE_EXECUTABLE_ENV) or shutil.which('node'),
    }
    environment = build_child_subprocess_env(base=parent, parent=parent)
    assert 'PYTHONPATH' not in environment
    if shadowed:
        package = tmp_path / 'runtime_protocol'
        package.mkdir()
        (package / '__init__.py').write_text('')
        (package / 'platform.py').write_text('# foreign Runtime\n')
        environment['PYTHONPATH'] = str(tmp_path)

    class DiscoveryObserved(Exception):
        pass

    def launch(argv, *, cwd, env, phase):
        # Test the actual launch argv and fresh imports without manufacturing
        # an owned-probe receipt. Custody remains covered by its existing suite.
        result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=30)
        if shadowed:
            assert result.returncode != 0
            assert 'registry Runtime origin differs' in result.stderr
        else:
            assert result.returncode == 0, result.stderr
            observation = json.loads(result.stdout)
            assert observation['runtime_origin'] == str(Path(runtime.__file__).resolve())
            assert str(Path(runtime.platform.__file__).resolve()) in observation['module_files']
        raise DiscoveryObserved

    monkeypatch.setattr(runtime, '_owned_registry_probe', launch)
    with pytest.raises(DiscoveryObserved):
        runtime._registry_probe(environment, sys.executable, generator=generator)


@pytest.mark.parametrize('generator', [False, True])
@pytest.mark.parametrize('attack', ['symlink', 'spoof'])
def test_source_registry_rejects_foreign_package_before_initializer(tmp_path, monkeypatch, generator, attack):
    expected_platform = Path(runtime.platform.__file__).resolve()
    package = tmp_path / 'runtime_protocol'
    package.mkdir()
    marker = tmp_path / 'foreign-initializer-ran'
    (package / '__init__.py').write_text(
        f'from pathlib import Path\nPath({str(marker)!r}).touch()\n'
        f'__path__.append({str(expected_platform.parent)!r})\n'
    )
    if attack == 'symlink':
        (package / 'platform.py').symlink_to(expected_platform)
    else:
        (package / 'platform.py').write_text(f'__file__ = {str(expected_platform)!r}\n')
    environment = {
        'HOME': str(tmp_path), 'PATH': os.environ.get('PATH', os.defpath),
        'PYTHONPATH': str(tmp_path), 'PYTHONDONTWRITEBYTECODE': '1',
    }

    class DiscoveryObserved(Exception):
        pass

    def launch(argv, *, cwd, env, phase):
        result = subprocess.run(argv, cwd=cwd, env=env, capture_output=True, text=True, timeout=30)
        assert not marker.exists(), 'foreign Runtime package initializer executed'
        assert result.returncode != 0
        assert 'registry Runtime origin differs' in result.stderr
        raise DiscoveryObserved

    monkeypatch.setattr(runtime, '_owned_registry_probe', launch)
    with pytest.raises(DiscoveryObserved):
        runtime._registry_probe(environment, sys.executable, generator=generator)
