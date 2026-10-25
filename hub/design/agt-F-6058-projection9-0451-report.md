## Report

No source patch applied. Current Runtime bootstrap creates `payload.items=[]`; `capture_occurrence_add_media` creates only the physical clip/registry binding. The legacy `item-1` cannot be reached through an allowed authentic API, and the prior fallback was synthetic.

Affected selectors:

- 3 projection golden tests
- 6 `test_real_candidate_matches_sdk_opener_exactly` variants: `parent`, `child`, `new_shot`, `duplicate`, `remove`, `sdk_bundle`

All fail at line 316 with `IndexError`.

Checks passed:

- AST conservation: 11 tests, 43 assertions, 2 raises
- In-memory compile
- Ruff
- Mypy
- `git diff --check`
- No pytest, collection, fixture execution, service, or browser run

Current target SHA-256: `90c4625a…b638`; capture blob `aaea8424…fbee`; commit blob `0ab8cb16…760e`.

Commit message written and `DONE` created. MAIN nine proof remains blocked pending an authentic legacy closure or supported item-materialization API.