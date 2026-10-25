Implemented G3/D100 in the two allowed files:

- Exact `Fraction` arithmetic for frame quantization, occurrence origins, durations, interval checks, and local subtraction.
- Preserved existing writes, guards, inputs, and codec forms.
- Added exact-fit regression coverage for `at`, `at_ms`, dual fields, and out-of-bounds refusal.
- No existing tests modified; no functional tests executed.

Static checks:

- In-memory AST/compile: passed.
- Ruff parent and candidate: passed.
- Mypy parent and candidate: passed.
- `git diff --check`: passed.
- Static production call trace: `capture_move → commands.execute → registered clip.move → capture.move`.

Old-RED/new-GREEN plan, not executed:

```text
pytest -q tests/sdk/test_capture_move_exact_time.py
```

Old source should fail the exact local-time assertion; candidate should pass both exact-fit and refusal cases.

Parent/candidate blobs:

- Parent capture: `aae8424fa6bbacf01df708aed4f53ede658fbee`
- Candidate capture: `59e2a6808cab24127ea796ac9e4917e7e7279eac`
- Candidate regression: `5cfd53d3ca1b65166150262074158cce0a8f3157`

Out of scope: `native_placement_commands.py` retains its separate float/tolerance arithmetic and was intentionally untouched.

Commit message written with `G3 D100` and `F-D86`; `DONE` created. Protected review and MAIN proof remain required before merge.