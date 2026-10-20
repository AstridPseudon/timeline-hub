"""Run the actual registered host against a private normally generated native pair."""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from tests.helpers.registered_native_pair import prepare_pair


@pytest.mark.integration
def test_registered_native_pair(tmp_path, capsys):
    agent, runtime = prepare_pair(Path(__file__).resolve().parents[3], tmp_path)
    result = subprocess.run([sys.executable, '-m', 'pytest', '-q', '-p', 'no:cacheprovider', '-m', 'integration',
                    'tests/packs/rendering/test_registered_native_assembler.py',
                    'tests/packs/rendering/test_registered_proposal_requester.py',
                    'tests/packs/rendering/test_registered_assembler_admission.py',
                    'tests/packs/rendering/test_registered_assembler_producer.py'],
                   cwd=agent, env={**os.environ, 'PYTHONPATH': str(agent),
                                   'PYTHONDONTWRITEBYTECODE': '1',
                                   'ASTRID_RUNTIME_CHECKOUT': str(runtime)}, text=True, capture_output=True)
    with capsys.disabled():
        print(result.stdout, end='')
        print(result.stderr, end='')
    result.check_returncode()
