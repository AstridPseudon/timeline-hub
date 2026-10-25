# FAIL — owned-move fixture migration

Scope: `tests/editing_conformance/test_owned_move_publish_runtime.py`; the
neighbor `tests/editing_conformance/test_prepared_video_birth.py` is unchanged.

Candidate: `43bc0b71922e1791b12590e2132ddde1063d25b2`, parent
`0ae146e1b0acc6e4a82ba6b4f905d88bad48320c`; author-only candidate file
SHA-256:
`2f83ea67363832a8f260c818ecdb79c92ab4298594d1df98f2c3d407f0a8223b`.
The candidate has an exact one-file diff from its author parent. All nine test
function ASTs, including the eight assigned scenarios, selectors, assertions,
raises, retry/rebase, undo/ABA, and no-write paths, are unchanged.

Bounded finding: the new `_commit_parent_variant` helper always invokes
`emit_document_commands(before, after)` at candidate line 53. The
`delete_film` fixture at candidate lines 125–132 intentionally sets
`parent['occurrences'] = []`. The emitter checks `managed_edges` and explicitly
raises `DocumentPatchError("parent changes managed closure edges; use a
semantic command")` at `astrid/sdk/timeline/emitter.py:272-273`. Therefore the
owned-delete baseline cannot be authored through this helper. This violates
the task requirement to migrate all four baselines and the explicit prohibition
on unsupported emitter membership. It is a source finding; no runtime
execution was used to establish it.

The other three variants use the registered provider and full C0 request shape,
but that does not clear the fourth-baseline failure. No merge request was sent
for this candidate.

Checks:

- In-memory compile: baseline and candidate PASS.
- Ruff: baseline, candidate, and unchanged neighbor PASS; `git diff --check`
  PASS.
- Default mypy baseline and candidate both exit 2 on the identical installed
  NumPy stub Python-version diagnostic (`numpy/__init__.pyi:737`); this remains
  an explicit environment result.
- `mypy --python-version 3.13 --follow-imports=silent`: baseline and candidate
  PASS (`Success: no issues found in 1 source file`).
- No pytest, collection, fixture/helper execution, service, build, browser,
  render, probe, or full suite was run.

Recommended next step: return this exact membership seam to the normal Agent
queue for a bounded repair that uses the registered semantic membership path,
then request one fresh protected review of the original author branch. Do not
relax the emitter guard or fabricate accepted history.
