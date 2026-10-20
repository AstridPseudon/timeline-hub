Implemented the narrow SDK source-key guard.

- Added the reviewed 7-line guard/error mapping in [invocation.py](/home/user/work/wt/agt-m3-sdk-source-guard/astrid/sdk/invocation.py).
- Flipped the three reserved-key invocation negatives to passing.
- Added [notes/report.md](/home/user/work/wt/agt-m3-sdk-source-guard/notes/report.md).
- Tests: `72 passed, 27 deselected, 2 xfailed`; focused negatives `3 passed`; import-fence test `1 passed`.
- Exact error: `CapabilityValidationError`, message `verified timeline source is host-owned`, validation category; runtime admission call count remained zero.
- No full suite run. No blockers.
- Wrote commit message and created `DONE`.