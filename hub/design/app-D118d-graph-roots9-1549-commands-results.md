# D118d commands and results

All commands were run in `/home/user/work/wt/app-D118d-graph-roots9-1549`.

```text
PYTHONPYCACHEPREFIX=$TMPDIR/pycache /home/user/work/venv-agent/bin/python -m py_compile tests/sdk/test_timeline_commit_graph_roots.py
PASS (using TMPDIR=/tmp/w-001c986ed5; the first attempt against the harness worker tmpdir was not a directory)

/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_commit_graph_roots.py
PASS — All checks passed!

/home/user/work/venv-agent/bin/mypy --cache-dir $TMPDIR/mypy --follow-imports=skip tests/sdk/test_timeline_commit_graph_roots.py
PASS — Success: no issues found in 1 source file

git diff --check
PASS

git cat-file -e 92443771676ef2bbb547d0a103d708fa8bec4c63:tests/sdk/test_timeline_commit_graph_roots.py
EXPECTED ABSENCE — exit 128; path is not present in that upstream commit
```

The mandated exact-nine command was not run: `df -B1` reported `4,953,280,512` available bytes, below the `5,000,000,000` light-run threshold.
