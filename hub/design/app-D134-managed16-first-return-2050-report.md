# D134 first return report

- Restored the exact original `a30e…` blobs for all three authorized files.
- Complete worktree now equals original `a30e…`; WIP `6c5c…` remains untouched.
- Verdict: `UNAPPLIED_SOURCE_DEPENDENCY`; behavior credit 0.
- Findings: F1 parent membership removal, F2 unsupported authored `item-1` creation, F3 shared unsupported seam across all 16 nodes.
- Missing capability/records: registered semantic birth/restore with authenticated item closure, item mapping, media/opaque metadata, and managed edges. Owner: `UNKNOWN`.

Validation:

- Python 3.11 compile: PASS
- Ruff: PASS
- Mypy: PASS
- Diff/source-scope checks: PASS
- AST conservation: PASS, 173 assertions (71/59/43)
- Pytest, services, sockets, and test bodies: not run as instructed

Artifacts: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D134-managed16-first-return-2050/evidence/`

Recommended next step: add the missing registered semantic capability in Agent/Runtime, then rerun D134 with independent protected review.