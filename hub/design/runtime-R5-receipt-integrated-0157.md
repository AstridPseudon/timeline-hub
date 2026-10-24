## Result: scoped PASS

- Runtime: `28bb65668118282f5942aa868c235cc39a50a381`; tree `a952265a732c3ac7f4234a166c827dca321cfe92`
- Agent: `521c88802330901281cc37ba25818baf2575f05e`; tree `fcd3135b3dc8e93009b86b7e4b75053a4e5b9476`
- Both worktrees clean.
- Reviewed source blobs match exactly:
  - Receipt tests: `7a4d8e83`, `2856cab5`
  - Speed test: `be5e7c9f`

Test command:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:packages/python ASTRID_CHECKOUT=/home/user/work/agent /home/user/work/venv-runtime/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/test_spec_reference.py::test_parent_receipt_compaction_preserves_publication_integrity tests/test_stage1_runtime_contract_completion.py::test_http_target_mutations_require_idempotency_key
```

Result: `2 passed in 1.97s`.

Additional checks passed: intended Runtime/Agent module origins, no uncommitted changes, `git diff --check`, unchanged C0v2 shapes, and production caller wiring.

The prior service `13500` setup failure was due to omitted `ASTRID_CHECKOUT`, not a product or safety failure. No full suite was run or claimed. Required commit message and `DONE` marker created.