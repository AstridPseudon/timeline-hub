Added the tests-only guard and exact published fixtures. The withdrawn schema reports all **8 missing definitions and 7 missing operations**. No product, generated-client, schema, or pin changes.

Final validation: **76 passed**:

```bash
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/sdk/test_timeline_schema_superset.py tests/sdk/test_timeline_composed_schema.py tests/sdk/test_workspace_client_timeline_commit.py tests/sdk/test_runtime_response_conformance.py tests/stage1/test_vendored_workspace_client_parity_luna.py
```

Ruff and tracked/new-file whitespace checks passed. No full suite or sockets run.

Exact hashes, Runtime reuse instructions, and limitations are in [notes/report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-schema-superset-guard/notes/report.md) and the shared coordination document. Historical 0.2.2→0.2.3 regex rewrites remain explicitly uncertified.

Both commit-message files are ready. No task blocker; recommend applying this delta to final candidates. M2 integration remains held until PLAN M1.