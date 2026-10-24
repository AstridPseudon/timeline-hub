## Report

Read-only investigation completed. No product or test files changed; worktree is clean.

Causal path:

- `TimelineSession._flush()` builds the full v2 request and sends it with `Idempotency-Key` through `sync.py:529-551`.
- Runtime invokes `RuntimeCommitService.commit()` in `commit.py:933`.
- Authenticated history becomes `AcceptedRecords` at `commit.py:1059-1069`; inverse selection and later-write scans run before `commands.execute()`.
- `doc.patch` records physical bindings and calls `remember()` at `_doc_patch.py:457-510`.
- Inverse restoration calls `remember()` again at `inverse.py:1157-1168`.
- `document_from_bundle()` then calls `_doc_patch_materialize.project()` at `commit.py:302-311`; accepted results are reloaded via `bundle_from_document()`.

Findings:

1. M1’s exact ten failures are caused solely by `_doc_patch_images` remaining in the returned redo bundle. The retained XML and diagnostic show all payloads, opaque fields, row membership/order, accepted statuses, inverse guards, and canonical document values pass. Only:

   `source_mapping._doc_patch_images` — expected absent, actual present.

   `remember()` is legitimate during materialization: it retains authenticated owner → source-image mappings so `project()` can reuse exact immutable source shot/internal images when authored payloads still match. The accidental leak is retaining this execution-only projection cache in the final bundle after materialization.

2. Literal IDs remain a separate production defect. Retained R1 evidence shows:

   - `clip:a`: forward/undo/redo passes.
   - `clip/a`: forward/undo pass; redo fails.
   - `clip::a`: forward/undo pass; redo fails.

   `doc.patch` intentionally keeps slash/`::` list identities on the generic path (`_doc_patch.py:439-445`), but inverse stage order reconstruction calls `_collections.order()` (`inverse.py:982-985`), whose `_identity()` rejects `/` and `::` (`_collections.py:32-33`). Relaxing only `_identity()` would be unsafe: `/` is also the owner/member separator and `::` is the property-guard delimiter in `_command_state.py:87-109`. Literal IDs must remain opaque through collection ordering, inverse restoration, canonical address normalization, and guard comparison.

Security negatives preserved:

- No caller-supplied source image or inverse effect was accepted as authority.
- Authenticated physical bindings, materialization tuples, later-write scans, and inverse source boundaries remain enforced.
- No fragment-control authentication bypass was found.
- Any fix must not remove source retention globally, bypass authenticated successor lineage, or use prefix heuristics for literal identities.

Evidence:

- Retained M1 run: `10 failed, 116 deselected`; no blind rerun performed.
- Retained R1 focused run: `42 passed, 1 failed`; adjacent cohort `380 passed, 19 deselected`.
- AST parsing of six relevant source files: passed.
- Ruff non-import checks (`E4,E7,E9,F`): passed.
- Mypy scoped files: passed.
- `git diff --check`: passed.
- Broad Ruff including import sorting reported six existing `I001` findings; no formatting changes were made.

The requested Agent control-doc paths were absent from the frozen checkout; equivalent docs were read from `/home/user/timeline-hub/hub/design/`.

Commit message and `DONE` marker were created.