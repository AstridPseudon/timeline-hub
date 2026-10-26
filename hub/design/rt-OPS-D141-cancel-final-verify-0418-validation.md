# OPS D141h validation

## Candidate identity

- Branch: `tl/rt-OPS-D141-cancel-final-verify-0418`
- Immutable terminal ref: `tl/rt-OPS-D141-cancel-finalize-sol-0410`
- Commit: `56f2d56e7d241d303be85df62166570d51602101`
- Tree: `744cca68f672153dd84f7ba20e580b6e917ccf6d`
- Parent: `f0ef96c415ff299b1456ed71b695000afd2165b9` / `2e12d3f102ee067b24068aa169d840d38ed77fa7`
- Worktree source status before evidence creation: clean; no product/DTO files changed.

## Exact controls

`TMPDIR=/tmp/w-621ef7b92a/d141h-controls PYTHONDONTWRITEBYTECODE=1 python3 -I privateops-d141-measured-floor/controls/real-controls.py` — **PASS**, exit 0, 49 cases. This covered the retained 44 purposes, exact targeted15 and P5 6934 positives, default/cache/source/snapshot/lease/one-heavy/4GB-stop floors, continuous 5-second KEEP traces, actual cancellation/reaping, mounted stop-test, all seven custody attacks, held IDs, invalid receipts, and App refusal.

The assigned worker `tmpdir` path was a regular file, so the same author command was run with the private harness-cleaned `/tmp/w-621ef7b92a/d141h-controls` directory. The failed `mkdir` happened before Python started and is not a test result.

## Static and source checks

- `bash -n privateops-d141-measured-floor/bin/test-run` — PASS.
- `python3 -I -c 'import ast, pathlib; files=[*pathlib.Path("privateops-d141-measured-floor/bin").glob("*.py"), pathlib.Path("privateops-d141-measured-floor/controls/real-controls.py")]; [ast.parse(p.read_text(), filename=str(p)) for p in files]; print(f"PythonAST PASS: {len(files)} files")'` — PASS, 5 files.
- `ruff check --no-cache privateops-d141-measured-floor/bin/*.py privateops-d141-measured-floor/controls/real-controls.py` — PASS, all checks passed.
- `python3 -m json.tool privateops-d141-measured-floor/install-manifest.json` — PASS.
- Manifest source SHA-256/mode consistency check — PASS, all five regular 0755 files match manifest.
- Exact live precondition `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run`: SHA-256 `0be17b74ad1e324bc84e50e61e50e3e07390b262b7abe17a37ad22b9bd10d0fe`, regular, mode 0755, one link — PASS.
- The four helper names are absent, including dangling symlinks, at that live precondition — PASS.
- `git diff --check HEAD^ HEAD` — PASS.
- `git diff --quiet HEAD^ HEAD -- ops-d141-measured-floor` — PASS; parent route unchanged.

## Isolated publication smoke

The controls copied only the five manifest files through installed → published → received temporary bin roots, checked SHA-256 and modes, and found no `controls/` sibling in the received layout. `bin/test-run` received hash differs only because the harness rewrites private orchestration/snapshot paths; its source hash was checked before rewrite. No live install, CAS, hub write, or receipt was performed.

## Contract preservation

Read-only review of approved `design/commit-v2.md` confirms the full C0v2 request and reply surface remains the governing interface: scope/base pair, commands, label/steps/per-step patches, reads, `fields|atomic`, idempotency, dry-run/source annotations, accepted/merged canonical authenticated receipt records, closure bindings/effects/dependencies/history/guarded undo, conflict reason/head, invalid diagnostics, and preview. No DTO or product source is in the candidate diff.
