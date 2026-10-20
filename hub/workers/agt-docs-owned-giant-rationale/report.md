Implemented the bounded metadata fix.

- Added `timeline_sheet.py` rationale at 1,313 lines, documenting temporary detached/native coexistence and deletion seams.
- Refreshed `timeline/cli.py` to 4,127 lines.
- Preserved threshold, tolerance, generic-host rationale, tests, and product source.
- Parser audit: 36 entries, 36 oversized files, no missing/invalid entries.
- Targeted test fails only on inherited metadata mismatches:
  - `generic_host.py`: +62
  - rendering `service.py`: +53
  - Remotion `run.py`: +78

Test command and full report: [report.md](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-docs-owned-giant-rationale/notes/report.md)

`DONE` and commit message were written.