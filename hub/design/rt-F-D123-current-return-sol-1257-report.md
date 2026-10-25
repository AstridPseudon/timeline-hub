Prepared the current Agent patch on exact upstream `b742893426`, bound to normal `b545b616`. Preserved upstream installer/chat behavior, carried only already-normal changes, and fixed Windows schema-key normalization without weakening integrity checks.

Validation:

- Targeted installer tests: **212 passed**.
- Document-input tests: **11 passed, 6 integration deselected**.
- All **173 protected predicates conserved**.
- Mypy, compilation, chat bundle, Node syntax, source identities and `git diff --check`: passed.
- Ruff: two verified upstream-existing findings.
- Prior central chat PASS applies through exact source identity.

Exact commands, results and decisions are in [D123-REVIEW.md](/home/user/work/wt/rt-F-D123-current-return-sol-1257/D123-REVIEW.md). The complete patch and maps occupy 13 MB in the assigned evidence directory.

Unverified: the inherited wheel `astrid.core` fixture gap and full C0 reply/no-write qualification. No full suites, staging, downloads or gating changes occurred. Shared design publication metadata is staged in evidence under D30’s write restriction.

`commit-msg` and `DONE` created. Next: independent exact-source review, followed by the future b742 cut matrix.