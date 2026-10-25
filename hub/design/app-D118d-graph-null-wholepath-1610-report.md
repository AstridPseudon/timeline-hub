# D118d report

- Verdict: **PASS** on the independent source finding.
- Confirmed first-return’s no-diff conclusion: the candidate changes only six request-envelope lines.
- Actual seam: fixture authors `gain: None` (`test_recorded_graph_roots.py:46-51`); the compiler preserves it (`authoring_bundle.py:1249-1305`); the genuine registered provider path reaches Runtime; the public schema requires numeric `Occurrence.gain` (`timeline-commit-bundle.json:3376-3385`).
- The passing comparison uses `gain: 1`, so it does not establish null support.
- Classification: deliberate existing schema refusal; intended null semantics remain a C0 owner decision. No repair, normalization, test weakening, or functional GO proposed.
- D12/D12a unchanged-invalid retention does not apply to this newly written occurrence.
- No product files changed. Worktree is clean. Required evidence files, commit message, and `DONE` marker exist.

Checks passed:

- Ruff
- Mypy
- `py_compile`
- `git diff --check`
- JSON validation
- Source-only AST/hash and producer/schema comparison

Pytest/own9/live/full suites were not run per task scope; behavioral acceptance remains unverified.