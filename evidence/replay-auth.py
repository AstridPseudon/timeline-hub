import os, subprocess, sys
from pathlib import Path
sys.path.insert(0, os.getcwd())
import runtime_protocol.timeline_commit_auth as auth
import pytest
ref = sys.argv.pop(1)
source = subprocess.check_output(["git", "show", ref + ":runtime_protocol/timeline_commit_auth.py"], text=True)
exec(compile(source, auth.__file__, "exec"), auth.__dict__)
sys.exit(pytest.main(sys.argv[1:]))
