# D116/G3 whole-path review

Verdict: `SOURCE_DEPENDENCY/EXACTMISSING`

- The protected current companion authors `parent/clip:card.on` from `occurrence:occ/clip:voice`.
- Gate3 deletes `occurrence:occ`; `compile_recorded` then finds zero source placements and raises `bound source occurrence/clip is missing or ambiguous`.
- The genuine current seed briefly has no active anchor, but `prepare()` deliberately restores the protected picker/declaration input. Omitting or clearing it changes the required authored topology.
- Removing the card, rebinding, or fabricating another occurrence/pin is prohibited.
- No fixture-only exact route exists. Existing owner for future semantic support: Agent G3/R2. No product or guard fault established.

No repository files, tests, or fixtures were modified or rerun.

Static checks:

- Python 3.11 AST/compile: PASS
- Protected JSON parsing: PASS
- Scoped Ruff: PASS
- `git diff --check HEAD^ HEAD`: PASS
- Worktree: clean
- Pytest/body/service/browser runs: not run

Evidence written under the requested worker `evidence/` directory; `DONE` and commit message were recorded.