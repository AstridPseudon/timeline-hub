# D134 independent validation

## Result

`PASS_UNAPPLIED`. Source and authored inputs remain unchanged. The review is
read-only; no pytest, provider/body, browser, socket, acquisition, or full
suite was run.

## Exact source custody

- `git rev-parse HEAD HEAD^{tree}`: `a30e74e901a28b39c28facba3deb00d76f186e23`, `ece8e0887e48e45cb1fce85b1256c49a0f6126c0`.
- Each authorized file's working-tree SHA-256 equals its `HEAD:path` SHA-256.
- AST and AST-without-attributes hashes match the prior source manifest exactly.
- `git status --short`: empty before and after review.
- `git diff --check`: exit 0.

## Static checks

Commands were run with system Python 3.11 (`python3.11`) for compilation and
the installed scoped `ruff`/`mypy` tools:

- `python3.11 -c 'import py_compile; ... doraise=True'` with private `/tmp/d134-review311-*` output on all three authorized files: PASS.
- `ruff check tests/editing_conformance/test_commit_runtime_video_unplace.py tests/editing_conformance/test_recipe_m2_auto_placement.py tests/editing_conformance/test_recipe_m2_placement_create_unplace.py`: `All checks passed!` (PASS).
- `mypy --follow-imports=skip --no-incremental <same three files>`: `Success: no issues found in 3 source files` (PASS).

## Input/predicate custody

The canonical input hashes for both image and video, exact topology, all 14
node IDs, and the original predicate map are retained in `source-manifest.json`
and `predicate-map.json`. The image/video source, parent, shot, internal,
occurrence, old-selection, new-selection, and verified-media hashes match the
author's manifest. The authored shot remains `item-1` with its exact old media
ID and `opaque_literal` metadata; both original occurrences point to
`chapter-shot`/`shot-1`.

## Production route conclusion

The current registry was enumerated from `commands.operations()`. The source
audit covers direct shot/media/placement commands plus all registered routes
that could plausibly introduce an item-bearing shot root. Duplicate/fork/shared
routes require an existing authenticated source; timeline duplication requires
an authenticated foreign closure; restructure derives only from the current
authenticated closure. None is an initial source option in the exact caller.
The positive comparator confirms preservation of an already-existing item, not
creation from an empty shot. No faithful supported source construction exists
within scope.
