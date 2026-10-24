Blocked; no Runtime product, schema, client, or Agent edits.

Added `tests/test_timeline_recorder_abi_authority.py` with real-provider controls. The current Runtime accepts both stripped and FULL REWRITE v2 bindings, so its existing validation cannot certify complete recorder coverage. Injected history `recorder_abi` values also pass authentication. The genuine ABI1 fork independently fails the current Agent guard with `fork source binding changed`; no guard was bypassed.

`HistoryEntry` is closed, requiring the D61 additive schema field and coordinated D39 regeneration. Boundary facts, source excerpts, commands, logs, and XML are retained in [evidence](​/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-R-recorder-abi-authority-sol-1410/evidence/abi-boundary.json).

Commands and results:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_recorder_abi_authority.py tests/test_timeline_commit_authentication.py tests/test_timeline_commit_sequential_verifier.py --junitxml="$TMPDIR/recorder-abi.xml"
```

192 passed, 14 failed. All failures are in the new file; existing authentication and sequential tests passed.

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_timeline_commit_port.py --junitxml="$TMPDIR/recorder-abi-port.xml"
```

94 passed. No `test_timeline_commit_v2.py` exists. Scoped Ruff, source-configured Pyright, compilation, and `git diff --check` passed.

Decision: fail closed rather than invent mode authority. A trusted validation/execution fact proving mode and complete coverage remains necessary. RED→GREEN, merged landing, restart/preview qualification, and Agent consumer qualification remain incomplete.

Wrote `commit-msg` and `BLOCKED`; no `DONE`. Hold this candidate from merge pending the missing authority source, D39 coordination, and independent security review.