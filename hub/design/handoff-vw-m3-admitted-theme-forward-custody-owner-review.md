# Theme forwarding custody review

Decision: **APPROVE** candidate `4d04d0b76e61112484e94e490e40ba62f9a92506` against meta base `ab4e6f6a6`.

The exact two-file diff is limited to `task_adapter.py` and its direct tests. The adapter accepts only the existing `materialized_objects["theme"]` carrier, validates it with `require_runtime_materialized_file`, enforces resolved containment under the runtime-managed `staging_dir/managed-objects` root, rejects symlink escapes, and forwards the original admitted path unchanged. Caller-only `params["theme"]` is ignored; absent carrier preserves the builtin fallback. The existing `materialized_root`, materialized map, asset staging, and source handoff are unchanged. No copied literals, slug lookup, resolver, DTO, or store were added.

Evidence: direct affected/negative tests passed `5 passed, 123 deselected`; adapter Ruff passed; `git diff --check` passed; an additional bounded symlink probe refused both direct-file and parent-directory escapes. No full/browser/live-render/install suite was run. The source producer/admission path remains a peer dependency, so this is not an end-to-end theme claim.
