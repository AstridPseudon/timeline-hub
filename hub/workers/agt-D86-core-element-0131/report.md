## F-D86 report — SOURCE_EXACT

No files changed. Target already matches `tl/integration`.

Exact identity:

- Agent HEAD/tree: `2050221347a536d0fd698817c4a200004f960564` / `499348bcf98f7c23e59a8aa5172be204ac7948b5`
- Target blob: `91b8d15affa7f21f46eef6cfef32a0f30e9d651a`
- Runtime release: `a3cd1a3214fa1632879c21d82d1abb9ea720b1de`
- Runtime harness: `766fd6700c3128ea9fc833086a517de2acb535e2`; differs only the two capture-test files.
- Contract: `0.2.14`, schema digest `sha256:867f3553ac0ff264300e5a2596b363cdb4c071842eb6570ad461c093d351708b`

Checks passed:

- AST parse/in-memory compile and selector/body conservation
- Dependency AST/compile
- Ruff candidate and baseline
- Mypy target-only; baseline is byte-identical
- `git diff --check`

Not run per brief: pytest, collection, fixtures, service/body execution, build, browser, or full suite.

Unapplied rehearsal findings:

- Lost-ACK replay: Runtime rejects with `invalid_records: sequential command metadata differs from the prepared candidate`.
- Optional-session case receives canonical status `merged`, while the retained assertion expects `rebased`.

I preserved the original assertions and genuine commit-door setup rather than fabricating acceptance or changing behavior expectations. Commit message and `DONE` marker created; harness commit and protected review remain pending.