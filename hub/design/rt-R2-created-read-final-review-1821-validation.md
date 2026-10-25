# R2 created-read corrected assessment: first-return review

## Result

`PASS` for the corrected source/contract report. The correction fixes the
superseded interpretation rejected by review 1808 while preserving the
original 1803/1808 FAIL findings as historical findings about that
interpretation. C0 defines public sequential operand/change visibility at
314-322, same-batch subsequent patches at 356-367, and subsequent qualified
operand visibility with verified intermediate images at 2825-2837.

The correction also preserves the required boundary: staged provider
`record["reads"]` are observations, while `finish(capture=True)` derives
public guards from `command_input` (frozen Agent `_recording.py:93-99,249-262`).
A raw post-handler read therefore does not grant authenticated public trust.
Runtime's smallest proved seam remains
`validate -> validate_step -> native_site -> site`; no Runtime guard, alias,
root, ownership, recorder, provider, or trust widening follows by inference.

The exact authenticated actual records remain missing: accepted
`records.commands`/`records.steps`, failing read ref/path/state and ordinal,
intra-command boundary, undo/redo stage range, per-ordinal closure images,
physical bindings/continuations, paired receipts, and historical-root
provenance. No causal attribution is inferred.

## Checks

All checks were bounded source/evidence validation; no source investigation,
provider execution, or test suite was rerun.

- Runtime frozen source identity: PASS. `contract/commit-v2.md`,
  `runtime_protocol/timeline_commit_auth.py`, and
  `runtime_protocol/timeline_commit_store.py` matched the recorded git blobs
  and SHA-256 values at e319fdbcd512bd5fc9bc5b2c43abfa4d749c34d9.
- Agent frozen source identity: PASS. `_recording.py` and the two cited graph
  test files matched their recorded blobs and SHA-256 values at
  224de4697c36b8958d94c0b85626e0fedaf007cb.
- AST/compile-in-memory: PASS, five cited Python files.
- Static callgraph/source predicates: PASS for `validate`, `validate_step`,
  `native_site`, `site`, `command_output`, `_project_created_child`, and the
  store `_validate` dispatch.
- Evidence JSON parsing: PASS for the corrected and original packets plus App
  1753 facts.
- C0 JSON example parsing: PASS, all 20 fenced JSON examples.
- `git diff --check`: PASS; Runtime worktree clean.

No pytest/provider/body/socket/browser/tour/P4/full-suite/D130 SWAP-WAL check
was run. No product, test, contract, generated-file, pin, permission, Git,
credential, or hub file was changed.
