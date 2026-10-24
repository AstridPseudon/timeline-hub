Implemented the G4 tuple rebinding in exactly two files:

- Updated both runners to Agent `0ff3d103`, carrier `/home/user/work/wt/agt-pin-0ff3d103`, and candidate `venv-agent-child-final-0ff3-becfe`.
- Preserved Runtime `becfe`, canonical client tuple, source body hashes, guards, and wrappers.
- Wrote commit message and `DONE` marker.

Checks passed:

- `py_compile`
- `ruff check --no-cache`
- `mypy --follow-imports=skip`
- `bash -n` wrappers
- AST/source-hash/physical-clean/client-tuple validation
- `git diff --check`; diff limited to two files

No provisioning or candidate request was made.