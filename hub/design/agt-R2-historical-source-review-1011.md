# PASS — R2 historical source/security review

Reviewed exact committed tree `1c9171b855f938140b5ab1a00c1c7722cbedba9b` (parent `f91ad0089e787c840f7b46df1dada7e06128d7d6`), with only the expected `inverse.py` + new regression test delta.

Evidence:

- Baseline packet on `f91`: original acceptance **6 failed, 37 passed**; new regressions **5 failed, 14 passed**.
- Candidate command: **67 passed**.
- Neighbor controls: **244 passed**, 0 failures/errors/skips.
- Scoped Ruff/mypy: passed.
- `make ruff`: **2143/2143**.
- `make mypy`: **1902/1902**.
- `git diff --check`: passed.
- Runtime guard verified exact source `becfe6db88b2cc034dba3fafa6c050117cdf2b06`.

Source audit confirms the production caller uses `_input_read_state` in both staged and landing validation. Authenticated accepted boundaries, ownership/source matching, publication preservation, exact redo-root restoration, rootless/ref mismatch refusal, and existing order/range/history/ABA guards remain enforced.

Hashes:

- `inverse.py`: `41faadf389e7d42c6d43bf0013cfec7d27b87c936e5c3e6e11e6881da9d7031c`
- New test: `ec0bf6ff0ee040ad08959804da3554223d9d06d46ff4273adfd50bd227256c54`

No findings or blockers. No full/live Runtime/browser suite run, per task scope. Baseline was reused by the authorized independent evidence packet. Metadata and `DONE` were created; no product files were modified.