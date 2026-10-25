# F-D86 pool6 source review

Disposition: SOURCE_EXACT; no worktree change.

The six held nodes in `handoff-agt-F-successor-0209-actual10077.xml` all fail
in setup with `missing or ambiguous identity 'occ-a'`, before pool assertions.
All six use the target file's `genuine_runtime` fixture, which calls
`GenuineTimeline.create()` and then the shared
`tests/editing_conformance/test_commit_runtime_occurrence_media.py::_create_fixture`.

The merged helper at `095177db79` (present in current `tl/integration` through
`25c1e18261`) now:

1. appends the original `occurrence.create` birth;
2. submits it through the genuine Runtime commit provider as `popup-birth`;
3. reloads `birth['data']['canonical_document']`; and
4. applies the guarded internal, shot, and parent patches against that reloaded
   state before the remaining setup submission.

This directly supplies the missing `occ-a` placement identity on the exact
shared path used by all six pool nodes. The target source is unchanged from
the current base (`7fbdd2f08dc1c772ce57500705a46a8b4a012d50ccd76918c50f1d45ae020b7e`).

Static checks (candidate and `git show HEAD:` baseline):

- Ruff with `pyproject.toml`: pass/pass.
- Mypy `--follow-imports=skip --ignore-missing-imports`: pass/pass.
- In-memory compile of target and shared setup helper: pass.
- AST inventory of all six runtime nodes: pass; original decorators,
  parameters, assertions, branches, and calls are unchanged.
- `git diff --check`: pass; worktree clean.

No pytest, collection, Runtime/service, build, browser, render, or product
execution was run.
