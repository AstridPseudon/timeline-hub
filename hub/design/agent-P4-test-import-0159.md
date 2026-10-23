# Agent P4 test import

Accepted-source base: `5a313eb88`.

Imported only:

- `tests/sdk/test_p4_commit_v2.py` exact donor `2d21a98919767016b5ff32a37c2ee207ec1c31fe` (blob `85218e8e99a1c7602d2b7ee399f3847fac759186`)
- `tests/sdk/test_p4_ten_note_provider.py` exact donor `e7385882ef50a59e6f62f32058fe211eb6e0b69f` (blob `1ed257c4604552793d2eaabfc117babe93c5b445`)

Verification: targeted P4 tests (`test_p4_commit_v2.py`, `test_p4_ten_note_provider.py`, `test_p4_commit_cases.py`) passed 15 tests; scoped Ruff passed; private `/tmp/astrid-u2-typecheck/bin/python` mypy passed on both imported files. No product/schema/generated/pin changes or automatic Proof merge. No full/browser/shared-dependency suite run.
