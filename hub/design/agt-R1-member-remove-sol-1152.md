Implemented the core R1 correction; **qualification remains blocked**.

Only `_doc_patch.py` and one new focused test file changed. Removal now captures the complete removed row and collection shape separately. Mixed structural operations and non-native identities retain conservative aggregate guards.

Results:

- Identical focused tests: old handler **25 passed / 18 failed**; new handler **42 passed / 1 failed** — **17 red→green, no lost passes**.
- Existing doc.patch/inverse suites: **268 passed / 2 failed**.
- Scoped Ruff, qualified mypy, vendor/artifact checks and `git diff --check`: **passed**.
- Security refusal controls passed; authentication guards remain unchanged.

All three remaining failures reproduce with the original handler:

- Ancestor-config redo: `_step_undo.py:227`.
- Two existing fork-redo positives: `_commit_patch.py:1003`.

Those files are outside ownership and remain untouched. Failing expectations remain visible, without skips or xfails.

[Exact commands, XML results and actual source origins](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-R1-member-remove-sol-1152/evidence/commands.txt) are retained. No full suite, live HTTP or durable Runtime qualification was performed.

Commit message and `BLOCKED` marker are written. Next: inverse owners resolve the baseline failures, then rerun targeted qualification and independent security review.