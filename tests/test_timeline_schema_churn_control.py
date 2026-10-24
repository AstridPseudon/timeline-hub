"""Temporary central-service entry for the bounded D83 preparation experiment."""
import importlib.util
import os
import subprocess
from pathlib import Path

import pytest

pytestmark = pytest.mark.integration


def test_preparation_churn(tmp_path, monkeypatch):
    path = Path('/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D83-schema-churn-sol-2141/evidence/measure_churn.py')
    if not os.environ.get('D83_CHURN_CHILD'):
        command = ['/home/user/work/venv-runtime/bin/python', '-m', 'pytest', '-q',
                   '-o', 'addopts=', '-p', 'no:cacheprovider', '--timeout=45',
                   __file__, '--junitxml=' + str(path.parent / 'control.xml')]
        result = subprocess.run(command, env={**os.environ, 'D83_CHURN_CHILD': '1'},
                                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        (path.parent / 'control.log').write_text(result.stdout)
        (path.parent / 'control-command.json').write_text(__import__('json').dumps(command))
        assert result.returncode == 0, result.stdout
        return
    spec = importlib.util.spec_from_file_location('measure_churn', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.run(tmp_path, monkeypatch)
