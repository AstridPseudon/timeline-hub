## Report

Changed only `tests/editing_conformance/test_m1_current_equivalent.py`:

- Updated baseline history count from `5` to `8`.
- Documented the three bootstrap entries and five authored setup entries.
- Preserved all existing assertions and ordering checks.
- No fixture, product, Runtime, or native changes.

Validation:

- Ruff: passed.
- `py_compile`: passed.
- `git diff --check`: passed.
- Protected AST review: passed; 131 assertions and 5 `pytest.raises` contexts conserved.
- Exact two rerun: both IDs reached the next predicate, then failed at line 317 with `exact transcript pin is missing or revoked or ambiguous`.
  - `[disjoint-rebase-undo]`: RED
  - `[touched-basis-conflict]`: RED
  - No timeout or setup errors.
- XML: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/rt-D107-current-baseline-1530/evidence/current-equivalents.xml`

The remaining failure appears to cross the public Runtime transcript-pin hydration boundary; I did not invent test setup or modify protected product code. Completion marker and commit message were written.