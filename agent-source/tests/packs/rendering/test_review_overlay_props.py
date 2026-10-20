"""Runs the Remotion review-overlay prop test (remotion/tests/review-overlay.test.cjs)."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

import pytest

REMOTION = Path(__file__).resolve().parents[3] / 'remotion'


@pytest.mark.skipif(shutil.which('node') is None or not (REMOTION / 'node_modules').is_dir(),
                    reason='node and remotion/node_modules are required for the Remotion overlay test (otto-heavy)')
def test_review_overlay_shows_only_the_active_phrase():
    result = subprocess.run(
        ['node', '--test', 'tests/review-overlay.test.cjs'],
        cwd=REMOTION, capture_output=True, text=True, timeout=180,
    )
    assert result.returncode == 0, result.stdout[-3000:] + result.stderr[-3000:]
