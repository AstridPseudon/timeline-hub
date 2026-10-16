"""Cross-process guard: runtime-execution imports never load the retired project-run modules."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_runtime_execution_imports_do_not_reach_retired_project_run() -> None:
    root = Path(__file__).parents[2]
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            (
                "import sys; import astrid.core.execution.executor.runner; "
                "import astrid.core.execution.orchestrator.runner; "
                "print('astrid.core.project.run' in sys.modules); "
                "print('astrid.core.contracts.run_record' in sys.modules)"
            ),
        ],
        cwd=root,
        check=True,
        capture_output=True,
        text=True,
    )
    assert result.stdout.splitlines() == ["False", "False"]
