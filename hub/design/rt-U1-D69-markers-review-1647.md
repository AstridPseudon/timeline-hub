## Verdict: FAIL

Candidate `925a7dd1c648a7632ba5b44a53566329ad947564`, tree `f8c534e73e321f42ad53b64a72363bc1e75f138b`; base `bc227de07262accb702eae8a44c4a666b568c08e`, tree `1d410a674d827979caf10d2da2ce3767b68c75da`.

Findings:

- Own-only diff is limited to the three assigned files.
- Live catalog predicates, exact project-reference test body, original catalog test body, and unconditional second-client subprocess path were preserved.
- Direct checks passed: 76 qualified catalog/refusal cases; central second-client test 1 passed.
- The authored ledger proposal is insufficient: it cites broad legacy controls and an xfail positive instead of exact direct-shot/direct-reference 410/no-write replacements.
- The two removed revision predicates lack exact v2 replacement selectors/predicate mapping, including complete history ABI 1|2/D62 coverage.

Tests:

- Qualified pytest cohort: `76 passed in 39.35s`
- Second-client central test: `1 passed in 4.53s`
- `tsc --noEmit`: passed
- Ruff: passed
- Python compile: passed
- Diff/clean-tree checks: passed
- Pyright: 13 inherited diagnostics, no new product diagnostics
- Generator `--check`: pre-existing stale generated artifacts; no regeneration performed

No product fixes were authored. Merge should wait for corrected ledger citations and exact v2 predicate mapping.