## PASS

Changed only [`test-support/new_image_witness.py`](/home/user/work/wt/agt-A4-image-harness-arg-0420/test-support/new_image_witness.py:491), correcting `current_head(service, editing)` to `current_head(service, editing.project)`.

Checks:

- Support control with retained 0154 evidence: `1 passed`
- Ruff: passed
- Direct mypy: `Success: no issues found`
- py_compile to private TMPDIR: passed
- AST delta: exactly one `Name → Attribute` argument change; definition/assertions unchanged
- `git diff --check`: passed

Repository mypy baseline reported `1904` current vs `1909` baseline (five fewer inherited findings, zero new).

Commit message written; `DONE` marker created.