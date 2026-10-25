Changed only `tests/sdk/test_timeline_capture_projection.py` (+17/−1):

- Resolve the revision pin through genuine `source_mapping`.
- Publish and reread the authored source before duplication, giving its baselines accepted Runtime provenance.
- Preserve all 43 original assertion ASTs, 11 test-function ASTs, and original fixture statements.

Validation **PASS**:

```sh
/home/user/work/venv-agent/bin/ruff check tests/sdk/test_timeline_capture_projection.py
/home/user/work/venv-agent/bin/mypy --cache-dir "$TMPDIR/mypy" --follow-imports=skip tests/sdk/test_timeline_capture_projection.py
PYTHONPYCACHEPREFIX="$TMPDIR/pycache" /home/user/work/venv-agent/bin/python -m py_compile tests/sdk/test_timeline_capture_projection.py
git diff --check
```

Hash, caller, AST, scope and exact Runtime-pin checks also pass.

Own9 **NOTRUN**: 4,987,809,792 bytes free, **12,190,208 bytes below** the required floor. Reaching the original assertions remains unverified; no product blocker is established.

Next: keep source held for protected review and run exact9 when disk permits. [Evidence and exact commands](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D118d-projection-setup-sol-1606/evidence/commands-results.md). Required artifacts, commit message and `DONE` verified.