## Report

Behavior: **PASS**

- Required integration command: **7 passed in 9.66s**
- No skips, deselections, or xfails.
- Agent HEAD: `415181d983d6d1d56a912da16ad4c5690e663187`
- Runtime pin: `8ea0766f5e9fb23cea26c7398770a8aaac06b258`
- Worktree was clean; no product files changed.

Static: **BLOCKED**

- `make ruff`: current `2145`, baseline `2147`; two improvements identified in `astrid/sdk/authoring_remote.py`:
  - `I001` import ordering
  - `F821` undefined `WorkspaceClient`
- `make mypy`: current `1909`, baseline `1911`; two improvements identified:
  - `[name-defined]` undefined `WorkspaceClient`
  - `[no-redef]` duplicate `result`
- Baselines were not modified.
- Required vendor-lock command was refused with `Permission denied`; per instructions, no alternate invocation was attempted.
- Artifact and diff checks were not run after the refusal.

A `BLOCKED` marker was written. Fixture files were not modified; dedicated fixture digests were not captured.