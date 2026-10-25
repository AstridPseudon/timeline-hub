Implemented one bounded source-only patch in [test_commit_runtime_opaque_items.py](/home/user/work/wt/agt-D86-opaque9-actual-0315/tests/editing_conformance/test_commit_runtime_opaque_items.py).

- Preserved bundle provenance while emitting payload `doc.patch` changes.
- Restored occurrence fields/order via guarded patches after semantic shared allocation.
- Create/fork files unchanged.
- Base: `7e23790248f17b8a4492fc9aee88d2c4e1df328d`
- Blobs: create `0178b098…`, fork `e17b6c46…`, opaque `67691003…`
- Commit message recorded; harness will commit.

Checks passed:

- AST parse/compile
- AST test selector/body/assertion conservation
- Ruff
- Mypy
- `git diff --check`

No pytest, collection, fixture execution, service, or browser runs performed per source-only requirements.

Remaining unverified findings:

- IDs 78–79: create subprocess assertion at test line 70.
- ID 80: fork inverse native-write coverage at `runtime_protocol/service.py:2518`, outside allowed ownership.
- IDs 81–86: prior emitter failures; source seam is corrected but behavior remains unverified.

Protected review and later functional qualification remain pending.