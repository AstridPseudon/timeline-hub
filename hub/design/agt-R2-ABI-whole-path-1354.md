## D30 report

Audited the complete ABI1/v2 path from the production client through Agent provider reservation checks, Runtime validation, `load_boundary`, and inverse selection. Read PLAN §3, `commit-v2.md` §§1–5, D54–D60, 1350 evidence, and 1340 source-caller proof.

Finding: the required discriminator is unavailable at the current boundary.

- Genuine ABI1 fork record: four bindings only—`collection.owner:collection.clips`, `collection.owner:collection.tracks`, `fork.source`, `fork.owner`—each with only `key/ref/policy/dependencies`.
- Genuine v2 fork record: those bindings are physically enriched, plus six `commit.effect` bindings; each includes `physical_ref`, revision/digest, boundary, and related provenance.
- Current `restore_native_fork` accepts ABI1 when the two fork bindings have the four-key shape and no binding has `physical_ref`; it does not require the complete ABI1 binding set.
- The 1350 attack strips physical fields from all bindings and reduces only `fork.source`/`fork.owner` to the ABI1 shape. It therefore passes the native branch while retaining v2 metadata.
- Runtime schema permits physical fields to be absent, and `timeline_commit_auth.validate_bindings` explicitly skips such bindings as legacy ABI1. `load_boundary` authenticates document history boundaries, not recorder mode or binding provenance. Inverse selection likewise falls back to legacy behavior when no physical binding remains.

Existing request fields, normalized steps, labels, merge mode, source/rationale, equal bytes, and final document digests cannot serve as authority under the settled constraints. The missing proof is an authenticated provider-side commitment that the complete accepted record was produced in ABI1 mode versus v2 mode, including complete binding coverage. No existing permissible fact supplies that commitment.

Commands/results:

- Read-only producer probe comparing ABI1 and v2 fork records: passed; produced the shapes above.
- `git status --short --branch && git diff --stat`: clean worktree.
- Tests: none run, per task instruction prohibiting worktree/tests.

No product files changed. Commit message written and `DONE` marker created. Recommended next step: Sol owner should treat this as an unavailable-boundary result unless an already-authorized authenticated mode/coverage proof is identified.