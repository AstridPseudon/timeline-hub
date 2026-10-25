# D134 managed16 command results

| Command/check | Result |
| --- | --- |
| `python3.11 -m py_compile` on the three authorized files with private `PYTHONPYCACHEPREFIX` | PASS |
| `ruff check --no-cache` on the three authorized files | PASS |
| `mypy --cache-dir` on the three authorized files | PASS |
| `git diff --check a30e74e... --` | PASS |
| complete worktree diff against `a30e74e901a28b39c28facba3deb00d76f186e23` | EMPTY / PASS |
| exact blob SHA-256 and AST conservation | PASS; 173 assertion ASTs |
| pytest / test service / Runtime service / sockets / test bodies | NOT RUN by instruction |

Historical result retained only as context: the prior targeted request stopped during conftest import with `ModuleNotFoundError: runtime_protocol`; it receives zero behavior credit.
