# P4 single current import — PASS

Base: Agent integration `168a5c9b32e31c7f8db14a96153a3d1955054734`.
Imported only `tests/editing_conformance/test_p4_cli_sheet_v2_runtime.py` from
`417678285cb0601f3d5f99b2c63c32de4e958286`; exact final blob
`033482ec2b94c5ae4a6b5c456e2d9fab3f454022`. Worktree delta is exactly one
test file. Donor `cmp` and hash verification pass.

Evidence:

- Integration collection: PASS, exactly 1 collected, collection-only.
- Scoped Ruff: PASS.
- Scoped persistent mypy (`venv-agent-typecheck-v2`): PASS.
- Normal Ruff baseline: PASS 2149/2149.
- Persistent mypy baseline: PASS 1914/1914.
- Pinned vendor lock (`rt-pin-34eac004`): PASS.
- Artifact manifest and `git diff --check`: PASS.
- Production caller audit: PASS; the test uses the production CLI apply,
  NativeSheet export, show, history, and client history paths.

Readonly reviews: prior independent artifact review 0612 PASS (staged
original single-node proof was 1 test with all 66 assertions); current-reader
integration review 0613 PASS. No HTTP body was run here; the merged integrated
one-node proof remains Proof-owned and is not claimed by this report.

The initial general-agent whole-tree mypy environment failure and moving
runtime-head lock mismatch were environmental/read-only findings; both required
checks pass with the mandated persistent typecheck environment and pinned
runtime checkout. No plan decision was revisited.
