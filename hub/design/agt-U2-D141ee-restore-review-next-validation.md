# Validation

Environment: `/home/user/work/venv-agent/bin/python`, `PYTHONDONTWRITEBYTECODE=1`, `PYTHONPATH=/home/user/work/wt/agt-U2-D141ee-restore-review-next:/home/user/work/runtime`; private cache/basetemp under `/tmp/agt-U2-D141ee-restore-review-next-run`; Runtime source is read-only 95d. Module origins are recorded in `evidence/module-origins.txt`.

Commands and durable outputs:

- Exact accepted-55 argv: `evidence/pytest-command.txt`; exit `4`; combined stdout/stderr: `evidence/restored-independent.log`; XML: `/tmp/agt-U2-D141ee-restore-review-next-run/restored-independent.xml`. Result: 2 collection errors, 40 nodes not collected, 0 executed in this mixed invocation.
- Exact unaffected accepted-15 argv: `evidence/pytest-unaffected-command.txt`; exit `1`; combined stdout/stderr: `evidence/restored-unaffected.log`; XML: `/tmp/agt-U2-D141ee-restore-review-next-run/restored-unaffected.xml`. Result: 15 executed, 15 failed, 0 passed.
- Ruff command: `/home/user/work/venv-agent/bin/ruff check tests/packs/timeline/test_cli_parity.py tests/packs/timeline/test_cli_status_publish.py tests/packs/timeline/test_verbs_working_copy.py tests/packs/video_editing/test_runtime_publication_chain.py tests/sdk/test_runtime_response_conformance.py tests/test_installer_schema.py tests/timeline/test_authoring_bundle.py tests/timeline/test_inverses.py tests/v10/test_timelines_create.py`; exit `1`, only the two pristine inverse diagnostics.
- `git diff --check HEAD^ HEAD`; exit `0`.
- Bounded conservation checker: `evidence/bounded-checker.log`; 55/55 blob and AST matches, 55 unique IDs, inverse whole-file SHA match.
- Targeted typecheck: N/A for this test-only change; no repository targeted typecheck workflow applies.
- Full suite/browser/render/install/dependency/child/request/CAS runs: not run.
