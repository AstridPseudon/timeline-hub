Prepared the review candidate: **53 definitions / 26 operations**, preserving full S2 and current safeguards.

- Portable checks: **220 passed, 4 existing xfails**.
- Current neighbors: **918 passed**; all capture checks subsequently passed.
- Private Runtime: **93 passed, 1 new strict xfail**; producer tests **5 passed**.
- Lint and patch checks passed.

**Qualification is BLOCKED:** grouped media-birth/word-anchor undo fails a derived-cache guard. Successful pristine-to-word authoring also needs first-occurrence creation, absent from this cohort. Recommend a bounded inverse fix before freeze.

[Detailed report with exact commands, results and limits](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-next-command-union-compose/notes/report.md).

Source patch, schema, commit message and `BLOCKED` marker are written. No public freeze, pin change or full suite.