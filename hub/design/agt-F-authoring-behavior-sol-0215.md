Prepared the bounded **F-authoring-behavior** correction; **blocked from integrated PASS**.

- Reused one candidate compilation.
- Restored unchanged publication through an ordinary guarded track reaffirmation.
- Routed removal through registered `occurrence.delete`.
- Filtered unplaced shots while preserving reachable edits and provenance.
- Emitted source-bound occurrence reorder guards and restored `publication.data`.
- Added `tests/timeline/test_authoring_publication_migrations.py`. Runtime-owned fixtures remain unchanged.

Test evidence used the specified pinned Runtime environment and `/home/user/work/venv-agent/bin/python -m pytest -q -oaddopts= -p no:cacheprovider`:

- New migration file, with `--timeout=45 --tb=short`: **10 passed, 1 failed**. Before the source fix, its initial cases produced **4 failed, 4 passed**.
- Exact `b7820cebaf` fixture files imported into `$TMPDIR/qualification`, selecting the seven named review cases with `--import-mode=importlib --tb=short`: **6 passed, 1 failed**.
- Follow-up of `test_publish_uses_one_compilation_and_returns_complete_mapping` after restoring `publication.data`: **1 failed**, exposing the fixture mismatch below.

Two blockers remain:

1. `_doc_patch.py:328` rejects occurrence `list.move`. Its ordered managed-edge comparison and collection installation also require R1-owned support. The execution assertion remains intact and failing.
2. The migrated mapping fixture now supplies `previous_revision_id`, but retains an assertion expecting only current-head actions. Both authoritative heads correctly produce saved-revision-pair actions. I preserved that information and left the Runtime-owned assertion unchanged.

Quality commands:

- `python -m ruff check <three changed files> --no-cache`: **pass**.
- Private mypy on those files: **pass**.
- Whole-tree parent/current `ruff check . --no-cache --output-format=json`: **2145 / 2145**, identical diagnostic identities.
- Whole-tree private `mypy astrid scripts/reshape --hide-error-context --no-color-output --no-pretty --show-error-codes`: **1909 / 1909**, identical diagnostic identities; inherited errors remain.
- `python scripts/artifact_manifest.py --check` and `git diff --check`: **pass**.

No full suite or vendor checker ran. Wrote `commit-msg` and `BLOCKED`; no `DONE`. Recommended next steps: coordinate R1 reorder support, resolve the Runtime fixture mismatch, then qualify the combined tree.