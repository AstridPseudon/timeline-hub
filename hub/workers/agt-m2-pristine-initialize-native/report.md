Implemented guarded `timeline.init`, exact App-default captures/golden, and the complete additive S2 schema. Existing publication history prevents reinitialization after edits or undo. No pins, HTTP, ABI, or storage machinery changed.

Final tests, using `/home/user/work/venv-agent/bin/python` with `PYTHONPATH=$PWD PYTHONDONTWRITEBYTECODE=1`:

```sh
python -m pytest -q -p no:cacheprovider tests/editing_conformance/test_pristine_initialize.py tests/sdk/test_timeline_pristine_initialize_provider.py tests/sdk/test_timeline_composed_schema.py
```

**32 passed.**

```sh
ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime python -m pytest -q -p no:cacheprovider -m integration tests/sdk/test_timeline_pristine_initialize_runtime.py
```

**1 passed:** actual Runtime create/restart/init/reload/undo/exact retry/redo. Neighbor selections passed **156** and **305** tests. Ruff and `git diff --check` passed. No full suite ran.

No Agent blocker remains. Next: freeze/generate the successor pair, then qualify App recovery and Runtime-owned headless repair through the Door. Those flows remain unverified here.

[Detailed report and all exact commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-pristine-initialize-native/notes/report.md). Commit message and `DONE` written; no commit or push performed.