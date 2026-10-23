# Agent R2/R3/meta merge

Merged the manager-created `tl/integration` forward into the exact R2 current-schema base:

- R2 parent: `11176f5fe0c1d4d98f3fda83c11052b240e46bf5`
- Integration parent: `d6f05e8a983375338eabcfa45b704c1868126e3b`
- Manager marker: `MERGE_EXECUTED` at 2026-10-23T02:39Z

Only `astrid/sdk/timeline/commit.py` conflicted. The resolution preserves R2 whole/per-step guarded inverse behavior, physical source and ABA checks, CAS re-selection, and `undo_steps`; it also preserves R3/meta structured invalid/conflict errors, preview projection, meta-aware dependency handling, and authored-meta reload. R3's prepared-record helper remains authoritative for v2 metadata, with R2 `undo_steps` explicitly carried alongside it.

Protected schema/client/lock blobs were unchanged:

- `astrid/core/timeline/banodoco_schema.py` — `1b3f12da05da3bb89fa76881184eefdf8232e076`
- `astrid_runtime_client/generated.py` — `1001055e05bd76c410df4cdb0fc2efad29fb7bb9`
- `runtime.lock.json` — `49abfb998759a9638e7e22f2c9d9596de7e91f72`

Evidence:

- Requested targeted tests: **216 passed, 2 subtests passed**.
- Scoped Ruff: passed; ordinary Ruff baseline `2151/2151`.
- Ordinary mypy baseline: `1915/1915` with the private validator.
- `git diff --check`: passed.

No full/browser/native14 suite was run. Runtime's official merged-response decoder issue remains outside this Agent merge.
