Implemented D118a first return.

- Changed native binding logic to preserve authority for unchanged pins, but drop stale `binding_id`/`head`/`event_stream_id` during genuine text rebinds.
- Preserved incomplete-authority refusal, Runtime verification, no-write, and privacy guards.
- Updated additive regression test.

Tests:

- Genuine Runtime rebind: `1 passed`
- Parent comparison: `1 passed`
- Focused units: `56 passed, 2 deselected`
- Ruff, mypy, py_compile, diff/scope/privacy checks: passed

Product remains HELD pending independent review and broader qualification. Commit message and evidence files are written; `DONE` marker created.