Completed D80 on base `a4d4`. Runtime now derives the fork owner from the authenticated physical shot pin and scoped placement identity, and checks the complete projected row. Existing assertions remain intact.

**No Agent patch needed:** relevant ownership, materialization, and reservation functions match original22847; 97 targeted Agent tests passed.

Validation:

- Original `327da207` auth: App-shaped shared fork→add-media reproduces the owner-mismatch refusal.
- `a4d4` and candidate: same production case passes; helper invoked **four times**.
- Focused12: **12 passed**; strict9: **9 passed**.
- Additional definition/production controls: **15 passed**.
- Production tampering: **5 passed**, preserving DB, CAS, staging, and SQL change count.
- ABI/history: **10 passed**; shared inverse authority: **36 passed**.
- Ruff, Pyright, compile, diff: passed.
- Strict mypy: **13 baseline diagnostics, 13 candidate diagnostics; zero new**.

Exact commands and results: [commands.txt](/home/user/work/wt/rt-P2-D80-owner-crossrepo-sol-1850/evidence/commands.txt). Contract citations, cross-repo file/line map, custody definition, and limitations: [ownership-definition.txt](/home/user/work/wt/rt-P2-D80-owner-crossrepo-sol-1850/evidence/ownership-definition.txt). Hashes: [source-hashes.txt](/home/user/work/wt/rt-P2-D80-owner-crossrepo-sol-1850/evidence/source-hashes.txt).

Commit message and `DONE` written. Next: one cumulative independent security review, then Runtime integration preserving `1bae`’s separate empty-range changes. Actual App original and integrated four-repo proof remain open; no full/browser/HTTP suite ran.