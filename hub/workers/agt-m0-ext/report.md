Completed [extensions.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/extensions.md): five types, pack APIs, marker/signal semantics, editable views, ownership, ten persona walks, and M5 acceptance criteria only. No product implementation or integration-worktree changes.

Key findings: beat ordinals cannot preserve identity across re-detection; cut-sheet editing generalises with pinned scope/reference metadata and command builders.

Validation:

- `python3 -B tests/m0_extensions/probe_extensions.py -v` — **4 passed**.
- `PYTHONPATH="$PWD" PYTHONDONTWRITEBYTECODE=1 python3 -m pytest -q -p no:cacheprovider tests/sdk/test_timeline_sheet.py tests/sdk/test_timeline_show_views.py tests/editing_conformance` — **219 passed, 4 existing parity skips**, two missing-timeout-plugin warnings.
- `git diff --check` — passed.

Shared venv absent; tests used system Python. Ruff unavailable. App, Composition, rendering/audio parity, macOS and full gates remain unverified.

Commit message written to the assigned path. Next: reconcile the three extension counterexamples with the recipe worker’s pending hard-case evidence before Checkpoint A.