## D134 root-008 report

Completed corrected evidence only; no Agent source, tests, fixtures, schemas, pins, or shared files changed.

- F-001 corrected: exact 18 full node IDs now byte-match root-008 membership.
- F-002 corrected: traced public Agent API → Runtime registration/invocation → Agent binding/history → Runtime acceptance/persistence.
- Classification remains `UNKNOWN_UNAPPLIED`; behavior `NOTRUN`; no product-fault or behavior credit.
- Missing evidence remains the authenticated historical ABI-1 Runtime record and canonical predecessor/output closures.

Validation:

- Python 3.11 AST/compile: PASS
- Ruff: PASS
- Mypy: PASS
- Exact membership/hash/AST checks: PASS
- JSON, whitespace, and `git diff --check`: PASS
- No pytest, collection, service, socket, browser, replay, or full suite run.

Artifacts: [evidence](</home/user/work/wt/app-D134-fork18-return-2114/evidence/wholepath.md>), [source manifest](</home/user/work/wt/app-D134-fork18-return-2114/evidence/source-manifest.json>), [findings](</home/user/work/wt/app-D134-fork18-return-2114/evidence/findings.json>). DONE marker and commit message written.