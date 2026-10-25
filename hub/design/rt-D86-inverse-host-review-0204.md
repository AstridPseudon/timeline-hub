PASS_SOURCE

- Reviewed candidate `a1eb3fd3be...`; blob `9f84493a...`.
- Only change: exclude `repeated-third` from authored-first placement rewrites, restoring original 13s placement/order and preserving shared physical source.
- 5 tests × 2 parameters = 10 cases preserved. Test bodies, decorators, raises, inputs, and branches remain unchanged.
- `compile`: PASS
- AST contract map: PASS
- Ruff scoped check: PASS
- Mypy scoped check: PASS
- `git diff --check`: PASS
- No product source edits.

Functional status remains unknown:

- Original-third five cases remain mathematically invalid (`3.5 > host 3.3`, source window `1.8`, clip `1.8 → 2.0`); no target weakening applied.
- Authored-first was not qualified against the locked Runtime (`a3cd1a3214...`); available Runtime was `6634a17f3...`, and setup failed with closure-membership/provenance mismatch.
- Repository Mypy baseline was environment-blocked by missing YAML stubs and NumPy/Python-version incompatibility.

The requested commit message and `DONE` marker were created.