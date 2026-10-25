## F-D86 report

- No source change made; owned test remains identical to reviewed candidate `1ce55afcf9`.
- Confirmed contradiction: original fixture is explicit `image/png` PNG bytes, but authored timing requires `from=1`, `to=6`, `hold=5`, `speed=2`. The registered provider correctly refuses this at `native_occurrence_media_commands.py:181`.
- Changing media type/bytes, removing timing, or relaxing the guard violates C0.

Checks:

- In-memory compile: PASS
- AST conservation: PASS
- Ruff: PASS
- Mypy: PASS
- `git diff --check`: PASS
- Pytest/service execution: not run per source-only brief

Wrote `commit-msg` and `BLOCKED`; no commit was possible because no safe change exists.