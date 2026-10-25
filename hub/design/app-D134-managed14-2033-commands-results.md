# D134 managed14 source validation

Status: UNAPPLIED. The authorized three files remain byte-identical to base `a30e74e901a28b39c28facba3deb00d76f186e23`; no source diff was made.

## Commands

| Command | Result |
|---|---|
| `git rev-parse HEAD HEAD^{tree}` | `a30e74e901a28b39c28facba3deb00d76f186e23`, `ece8e0887e48e45cb1fce85b1256c49a0f6126c0` |
| `git status --short` | empty before/after evidence collection; evidence is outside the worktree |
| Python AST/hash inventory over the three authorized files | passed; hashes are in `source-manifest.json` |
| Canonical `inputs('image')`/`inputs('video')` hash inventory | passed; document, parent, shot, internal, occurrence and media hashes are in `source-manifest.json` |
| `PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -c 'py_compile.compile(..., cfile=<private /tmp/w-5ffcea0124 output>, doraise=True)'` for each authorized file | all three compiled, exit 0 |
| `PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m ruff check <three files>` | `All checks passed!`, exit 0 |
| `PYTHONPATH=$PWD:/home/user/work/runtime /home/user/work/venv-agent/bin/python -m mypy --follow-imports=skip --no-incremental <three files>` | `Success: no issues found in 3 source files`, exit 0 |
| `git diff --check` | exit 0; no product diff |

## Registered semantic trace

The read-only command trace used the public Agent helpers on the current source:

- `occurrence.create` generated an empty shot payload (`items=[]`) and a generated managed shot revision.
- The existing whole-shot `doc.patch` attempted to replace that root with the authored shot payload containing `item-1`; executing the equivalent patch against the full authored bundle raises `CommandError: shot item correspondence changed` (`kind=identity_conflict`).
- `occurrence.add-media` preserves the existing authored `item-1`; it creates an occurrence clip and registry binding, not a new shot item.
- `placement.create` accepts only `id`, `on`, `hold` and `media`, and is a clip-membership command.
- `shot.set` source inspection shows only `payload.name` and `payload.settings` writes; it cannot carry `items`.

This establishes the precise unsupported seam without running the original integration body. The prior review's managed-edge classification is therefore retained, but no migration or behavior credit is claimed.
