# R5 full receipt-key review — FAIL

Finding: `tests/test_spec_reference.py` deletes the original publication operation and three original assertions:

- `replay["data"] == original["data"]`
- replay receipt equality
- committed receipt equality

The replacement checks baseline/compaction markers and a separate current-commit retry, but does not preserve the original replay/receipt proof. This violates the no-lost-original-assertions requirement.

`tests/test_stage1_runtime_contract_completion.py` is acceptable: active missing-key `400` remains, current authenticated commit accepts and exactly retries, and the retired route adds `410` plus DB no-write proof.

Evidence:

- Targeted pytest: `2 passed in 1.88s`
- Ruff: passed
- In-memory compile: passed
- `git diff --check`: passed
- Pyright: candidate 39 diagnostics; reproduced parent 45. Normalized comparison: zero new diagnostics, but six removed diagnostics corresponding to the deleted original assertions.
- Non-target ASTs and existing xfail marker unchanged.
- Only the two permitted test files differ: `86 insertions/17 deletions` and `73 insertions/4 deletions`.
- No status allowlist broadening, skips, deselection, or new xfails.

Authenticity verified through the real Astrid provider loader, Runtime service/daemon boundary, canonical HTTP commit route, schema-digest provider validation, real authoring bundle/capture imports, receipts, events, integrity, and exact retry. No fabricated authority or accepted response.

Source:

- Candidate Runtime: `abbb75da3c8e`, tree `e28be460`
- Compared base: `458595850c35`, tree `703b1aac`
- Agent used during review: `92baf961`, tree `c5265e3f` (different from the author report’s captured Agent SHA)

No full suite or final gate was run. No tracked files were modified.