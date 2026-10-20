# Existing admitted theme input forwarding

The Agent consumer patch is ready for integration.

The normal managed render task adapter now uses only the existing generic-host
carrier `materialized_objects["theme"]`. It validates the admitted value with
the existing runtime-materialized-file helper, rejects symlinks, requires the
resolved file to remain beneath the host `managed-objects` root, and requires
the basename `theme.json`. It then passes the original admitted path string as
executor input `theme`.

No theme input is sent when the carrier is absent, so the existing builtin
fallback remains intact. A caller-only `params["theme"]` is not consulted.
The existing executor `materialized_root` and `materialized_objects` inputs are
preserved, and no slug lookup, resolver, DTO, store, or theme literal was
introduced.

Changed files:

- `astrid/packs/rendering/actions/render/task_adapter.py`
- `tests/packs/rendering/test_render_export_task_adapter.py`

Evidence: five bounded adapter tests passed; adapter Ruff and `git diff
--check` passed. No full/browser/live-render suite was run. The App/Runtime
normal producer/admission request remains a peer dependency, so this handoff
does not claim end-to-end theme parity.
