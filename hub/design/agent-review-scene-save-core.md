# Agent scene/save-core review

## Verdict

**APPROVE the bounded candidate `f5d0b4e090fba31a6e3c55baa55b63b2e739d337`** (`tl/agt-m3-scene-save-core-resume`, tree `f4d74d55c77c76b8d20e5e4b3fd7bb2719f4d1be`). No blocking product defect was found.

The candidate implements the settled D09 Agent half: `Checkout.check()` keeps explicit diagnostics, while `_check_core()` shares the authoritative structural/timing/reference validation without scene evaluation or renderer-preview imports. Publication, checked transactions, duplicate preflights and the detached CLI edit report use the private core path. Ordinary file save and attached/native save remain renderer-independent. The candidate does not touch Root preparation, `run.py`, cache seams, source hosting, public APIs, DTOs, or `SourceFactory`.

## What was verified

- Candidate diff is the intended 14-path change: six production callers/methods plus focused tests, with no unrelated product or schema work.
- `_check_core()` calls the existing `_check(diagnostics=False)` implementation; there is no duplicate validator. Public `check()` calls `_check(diagnostics=True)` and retains geometry, lint, text, scene/unknown and OFFCANVAS classification.
- Core still runs the canonical authoring validator, formula resolution, orphan/empty/outside/type/stale-beat/shot-length checks, and publication guards. The renderer-bearing SDK facade is avoided by importing `astrid.core.timeline.authoring_bundle` directly.
- The explicit OFFCANVAS negative and core-valid save/publish positive are both present. The positive preserves raw `params.x=10000` through ordinary save/reload and the real publication payload; no clamp, hiding or autofix was introduced.
- Existing publication, transaction, retry/recovery, ownership, schema and native assertions remain represented. Test stubs were moved only to the new private seam or the defining pure authoring module.
- `git diff --check f5d0b4e0^ f5d0b4e0` passed. The assigned review worktree remained clean.

## Concrete finding (non-blocking)

**N1 — the fresh-process import-fence test is cwd-sensitive.** In `tests/sdk/test_scene_save_core.py:189-190`, the child `python -c` process inherits the caller's cwd and receives no explicit candidate root in `cwd` or `PYTHONPATH`. Running the focused tests from a different checkout therefore imported the review worktree's parent-side `astrid` package and failed with `AttributeError: _check_core`, rather than testing the candidate. Running from the candidate root passed. Make the child self-contained by setting its cwd or explicitly prepending the test checkout root to the child environment before relying on the test outside the normal worktree runner. This is test harness robustness, not a production save-path defect.

## Qualification boundaries

- No full suite was requested or run.
- Runtime integration was not independently rerun here. The worker's exact-tree central named lane was inspected: 40 passed / 24 deselected, exit 0. The worker also reports 958 targeted Agent passes, 27 working-copy caller passes and 10 immutable public12 scene-answer passes; those results are recorded as worker/central evidence, not re-run claims by this reviewer.
- D09 remains held for Viewing's Root-prep seam, cache physical-key parity and physical pixel/audio parity. No public13 adoption or owner-film qualification is claimed.
- The review worktree was the protected current root `8e310785`; it was not checked out over another branch and no source, branch, ref or dependency was modified.

Detailed commands and results are in the worker report:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-review-scene-save-core/notes/report.md`.
