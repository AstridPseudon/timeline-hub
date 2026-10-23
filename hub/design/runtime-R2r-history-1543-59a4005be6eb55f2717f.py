"""Run the authorized original Agent nine through the central service."""
from pathlib import Path
import json
import os
import subprocess


def test_original_agent_nine():
    worker = Path(__file__).parent
    evidence = worker / "evidence" / "original9"
    evidence.mkdir(parents=True, exist_ok=True)
    root = Path.cwd()
    agent = Path("/home/user/work/wt/agt-pin-67ba416b")
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", ASTRID_RUNTIME_CHECKOUT=str(root),
               ASTRID_CHECKOUT=str(agent), ORIGINAL9_EVIDENCE=str(evidence),
               PYTHONPATH=f"{worker}:{agent}:{root}:{root / 'packages/python'}")
    command = ["/home/user/work/venv-agent/bin/python", "-m", "pytest", "-q", "-o", "addopts=",
               "-p", "no:cacheprovider", "-p", "original9_observer",
               str(agent / "tests/editing_conformance/test_doc_patch_sequential_rebase.py")]
    (evidence / "command.json").write_text(json.dumps({"command": command, "cwd": str(root),
        "env": {key: env[key] for key in ("PYTHONDONTWRITEBYTECODE", "ASTRID_RUNTIME_CHECKOUT",
        "ASTRID_CHECKOUT", "ORIGINAL9_EVIDENCE", "PYTHONPATH")}}, indent=2) + "\n")
    with (evidence / "original9.log").open("w") as log:
        result = subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, timeout=240)
    (evidence / "exit").write_text(str(result.returncode) + "\n")
    print((evidence / "original9.log").read_text())
    assert result.returncode == 0
