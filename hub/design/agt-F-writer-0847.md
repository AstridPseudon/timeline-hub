# agt-F-writer-0847 handoff

Base `e837e18c5156e762eca05e6d9bb15779cf847b60`; current worker changes are uncommitted on `tl/agt-F-writer-0847`.

Bounded F/R3/G3 repair:

- `Checkout.publish()` now calls `_check_core()` before the writer, preserving refusal-before-write and the no-renderer/no-Node core-only save path.
- Unchanged multi-placement documents no longer invoke narration registration; only actual `narration_changes()` use the existing TimelineSession commit seam.
- `timeline_document.py` obtains its pinned base through the opened `TimelineSession._bundle()` path, preserving the actual authenticated caller seam and making the existing detached-session fixture valid.
- The feedback test’s old `clip.move` expectation was updated to C0/G3’s intentional generic `doc.patch` wire while retaining all receipt/feedback/artifact assertions.

Evidence:

- Initial exact 13-node reproduction: `13 failed`.
- Final exact 13-node reproduction: `12 passed, 1 failed`; sole failure is `test_duplicate_preflights_and_publication_are_core_only`.
- Feedback node alone: `1 passed`.
- `make ruff PY=/home/user/work/venv-agent/bin/python`: PASS, `2149/2149` baseline.
- Vendor lock, artifact manifest, and `git diff --check`: PASS.
- Type baseline: 45-second timeout, no result.
- Scoped Ruff still shows two pre-existing findings in `publish.py`, confirmed on the starting tree.

Remaining owner/slice: G5/duplicate owner must adapt the duplicate fixture and production proof to authenticated v2 `TimelineSession` commit/narration custody. This worker deliberately did not touch `timeline_duplicate.py`, restore the retired publisher, or run any full/heavy suite.

Detailed report: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-writer-0847/detailedreport.md`
