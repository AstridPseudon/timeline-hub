# Agent → Viewing: root-build write-guard current port

Date: 2026-10-20 23:10:16 UTC

The Agent current-port worker applied the independently custody-approved donor `96eb54b509b35ffe1e076b20c78a264bff77627d` exactly onto current integration. The three changed files are:

- `tests/packs/rendering/_helpers.py`
- `tests/packs/rendering/test_presenter_scene_capability.py`
- `tests/packs/rendering/test_private_node_modules_staging.py`

The helper retains one-pass peer/scope iteration, real scope directories, leaf-only `ln -sfnT`, realpath/linked-ancestor checks before every staging write, guarded tar extraction, and the existing presenter closure/source hashes. All three file blobs match the approved donor exactly; no other path changed.

Evidence on the current-port worktree:

- Direct guard regressions: `3 passed`.
- Existing presenter source-closure neighbor under `-m integration`: `1 passed`.
- Ruff and `git diff --check`: passed.
- No shared dependency or borrowed staging writes; no browser/export/E2E/full-suite claim.

Viewing can consume this exact three-file port when merging its integration work.
