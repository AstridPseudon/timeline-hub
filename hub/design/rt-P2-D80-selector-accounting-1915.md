## Report

**PASS — bounded D80 selector accounting.**

- Final Runtime file: 23 unique cases = 8 preserved `a4d4` owner cases + 15 additive D80 cases.
- Earlier “12 + 15 = 27” included four unchanged authority-file selectors; no behavior was dropped or renamed.
- Original assertions are preserved; the production case adds a stronger exact-four-call assertion.
- Relevant Runtime ASTs match carrier `52b`; only unrelated empty-range comparator changes differ.
- Evidence: [selector map]( /home/user/work/wt/rt-P2-D80-selector-accounting-1915/evidence/d80-selector-accounting.md) and [source hashes]( /home/user/work/wt/rt-P2-D80-selector-accounting-1915/evidence/d80-selector-source-hashes.txt).

Verification used authentic XML/source ASTs only:

- Runtime home command: `pytest ... tests/test_timeline_popup_fork_owner_projection.py` → **23 passed**.
- Agent home command: targeted helper test → **4 passed**.
- XML hashes: Runtime `1e47ff32…`, Agent `6f04700f…`.
- Combined run is not claimed: initial collection hit `ImportPathMismatchError`; `home.xml` was later overwritten.

No blockers. No product/test changes. Commit message and empty `DONE` marker are prepared for the harness.