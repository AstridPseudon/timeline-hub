# D134 bounded source first return

Decision: `UNAPPLIED_EXACTMISSING`. The assigned test file is unchanged from
parent `a30e74e901a28b39c28facba3deb00d76f186e23`; no product or test repair was
authorized. The exact seven historical node IDs and all original parameter
inputs, raises contexts, and assertions are conserved in `predicate-map.json`.

## Identity and source checks

- Parent commit: `a30e74e901a28b39c28facba3deb00d76f186e23`
- Parent/worktree tree: `ece8e0887e48e45cb1fce85b1256c49a0f6126c0`
- Changed paths: none
- Assigned file blob: `b97bd6a6b6da650cd60b48f78a31fabd7471f26b`
- Assigned file SHA-256: `6c02629fded13bbd97a2cd62d5954083c04cbead04a67e6b30df500f2a4fc1f1`
- Historical Agent pins remain unchanged: `bd3c95b1cebe3bf27c4a82919e5839efb37519db`, with hashes `eec60c…79b9cf7` and `06bd41…92cee`.
- Current normal-home Agent hashes are `2b81e46a…75107b3` and `6c794734…8d0423`; this is the exact source-identity boundary, not product-fault evidence.
- Pinned Runtime object `6634a17f3ffd885567ba3c91b6c7a560df7375a4` reproduces both retained Runtime hashes exactly.

## Static validation

Commands run from the assigned worktree:

```text
git diff --check
PASS (exit 0)

/home/user/work/venv-agent/bin/ruff check tests/editing_conformance/test_inverse_stage_runtime_regressions.py
All checks passed! (exit 0)

PYTHONPYCACHEPREFIX=/tmp/w-08f7c45155/rt-D134-inverse7-pycache \
  /home/user/work/venv-agent/bin/python -m py_compile \
  tests/editing_conformance/test_inverse_stage_runtime_regressions.py
PASS (exit 0; private cache)

PYTHONPATH=. /home/user/work/venv-agent/bin/python -m mypy \
  tests/editing_conformance/test_inverse_stage_runtime_regressions.py
Success: no issues found in 1 source file (exit 0)
```

The first attempted task-specific pycache location was already a harness-owned
regular file named `tmpdir`; no file was removed or replaced. The successful
private compilation used the permitted `/tmp/w-08f7c45155` scratch root.

## Functional gate

NOTRUN. `df -B1 /` reported `4,547,731,456` available bytes, below the exact
`5,000,000,000` light-admission floor. Per the task, no pytest/provider/body
run was submitted or retried. The `4,000,000,000` source-only stop line was not
reached.

No merge, checkout, commit, provider run, Runtime body, live caller, history
fabrication, hash refresh, assertion change, skip, or xfail was performed.
