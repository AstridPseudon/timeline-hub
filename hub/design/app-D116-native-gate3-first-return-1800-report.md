# D116/G3 report

Result: `SOURCE_DEPENDENCY`; no fixture edit applied.

The exact Gate3 topology deletes `occurrence:occ`, while the authored `parent/clip:card:on` anchor still references `occurrence:occ/clip:voice`. Public `occurrence.delete` setup therefore fails at `native_word_anchor.py:71`. Clearing/rebinding the anchor or retaining the occurrence would violate predicate conservation.

Checks passed:

- Python 3.11 AST/compile
- Scoped Ruff
- Scoped mypy
- `git diff --check`
- Evidence JSON validation

No pytest or behavioral rerun was performed. Owner scope: Agent semantic-command/word-anchor integration. Evidence and validation are under the assigned worker `evidence/` directory; `DONE` and the D116 commit message were recorded.