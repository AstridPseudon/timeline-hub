Implemented the F-D86 fixture repair.

- Native clip seeding now uses literal timing only.
- Original `app.astrid.on`/`for` values are restored via guarded `doc.patch` at the correct sequential boundary.
- Retained-input tests and all assertions/choices remain unchanged.
- Commit message written; `DONE` created.

Checks passed:

- Ruff (candidate and parent): pass
- Mypy (candidate and parent): pass
- AST/in-memory compile: pass
- `git diff --check`: pass

No pytest or runtime suites were run, per instructions. Recommended next step: protected review followed by the exact MAIN proof.