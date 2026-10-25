# D118a numeric params3 facts

- No file was changed. The assigned test remains byte- and AST-identical to base `cf7b8d7c2b4cb980de1d873f0498784d5210d508` (SHA-256 `1ced4d39f8c2da4972863500b20aa67da1ee458f20ee9f4c86be152fd716b5d6`).
- The assigned file is absent at pristine/D60 commit `08e6b905`.
- Exact three retained nodes were run once with clean immutable Runtime checkout `/home/user/work/wt/rt-pin-42aad0e9`, receipt `42aad0e92f6da8ea83dd0a382a87e3acd12651b0`, tree `085a5be70b56353deb41ae7d743336a4ccb7f29c`, and genuine registered `astrid` provider.
- Result: all three fail only during redo inverse at Runtime `runtime_protocol/timeline_commit_auth.py:1755`, surfaced through `runtime_protocol/service.py:2524`, with `inverse stage native writes do not cover its authenticated effect image`. The accepted numeric save, canonical reload, and first inverse checks pass.
- This is a Runtime custody/validation defect outside the only allowed test file. No setup/caller correction was proven, so no speculative metadata, guard, normalizer, or assertion change was made.
- Ruff, mypy with `--follow-imports=skip`, `py_compile`, `git diff --check`, and byte/AST conservation all passed.
