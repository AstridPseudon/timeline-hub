# Report

- Fixed R0 public export for `DocPatchArgs` in:
  - `generators/python_client_init_template.py`
  - `packages/python/astrid_runtime_client/__init__.py`
- Generated output changed only in the allowed rendered `__init__.py`.
- Original RED: `AttributeError: ... has no attribute 'DocPatchArgs'`; 1 failed, 143 passed.
- New GREEN: 144 passed.

Checks:

- Targeted pytest: `144 passed`
- `generators/generate.py`: passed
- `generate.py --check`: passed
- Ruff: passed
- Pyright baseline/current: identical 6 existing diagnostics; zero new normalized diagnostics
- In-memory compilation: passed
- `git diff --check`: passed
- Full-v2 `WorkspaceClient` wire probe and root-object identity: passed
- Generated schema digest unchanged: `sha256:35c2d9...`
- 12 other generated outputs byte-identical; only rendered package `__init__.py` changed.
- No full suite run or current gate claim made.

Commit message and `DONE` marker created. Next step: independent Luna review, then normal merge request.