## U1c Runtime report

- Extended reviewed `0138e3af6` with upstream `795379a67`; manager staged only:
  - `runtime_protocol/service.py`
  - `tests/test_managed_output_export.py`
- Added default `~/Downloads/Astrid exports` selection while preserving containment, symlink, no-overwrite, collision, and idempotency guards.
- Removed stale test import and added typed/local root bindings for zero new Pyright diagnostics.
- Production caller verified: `RuntimeService.export_managed_output` invokes `_ensure_export_root` and `_materialize_export`.

Checks:

- Targeted pytest: `224 passed`
- Ruff: 78 inherited baseline diagnostics, zero new diagnostics.
- Pyright baseline comparison: 375 vs 375, zero new diagnostics.
- In-memory compile: passed.
- `git diff --check`: passed.
- Protected contract/client/generator/schema blobs: unchanged vs `0138e3af6` and `abd47e68d`.
- Schema digest unchanged: `sha256:35c2d9c5e0b51ab8d8b7a4f4dbafbdfcb13d232d7bd22fff21cf73e250398d4c`.

Exact refs: base tree `376760358f`; upstream tree `df154bc745`; integration tree `6047ac303`. Final worktree remains uncommitted for harness commit.

No full, browser, integration, or gate run performed. Held branch-only until freeze; independent Luna review remains next.