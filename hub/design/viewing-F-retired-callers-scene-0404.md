## PASS

No code changes were needed; the requested base already contains the fix in `915bd2a594`:

- Replaced stale `main`/`parent-1` setup with `runtime.timeline_id`/`runtime.parent_revision_id`.
- Setup uses `service.commit_timeline` semantic commands; no `publish_parent_composition`.
- Existing Scene admission, certified-source, working-copy, materialization, execution, and provenance assertions remain intact.

Original nodes:

- `[False]` — PASS
- `[True]` — PASS

Caller path verified: semantic Runtime setup → `_scene_only_request`/`prepare_filmstrip` → private `rendering.timeline_visualize` admission → host materialization → `_execute_scene_only`.

Commands:

- Targeted pytest: `2 passed`; full target file: `4 passed`
- Ruff: PASS
- Mypy: PASS
- Vendor lock: PASS
- Artifact manifest: PASS
- `git diff --check`: PASS

The first pytest invocation required `ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`; with that existing Runtime checkout configured, all tests passed. No production edits or test weakening were performed. DONE marker and commit message were recorded.