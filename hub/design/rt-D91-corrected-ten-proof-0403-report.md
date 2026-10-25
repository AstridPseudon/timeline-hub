## D91 report

- Verified reviewed source `39fcc678…`, tree `0c74e497…`, target blob `19ad54ba…`; worktree clean.
- Used exact authoritative D91 ten selectors and immutable tuple:
  - Agent `39fcc678…`
  - Runtime `6634a17…`
  - App `24865fa…`
  - Composition `635f4de…`
- Central proof ID: `rt-D91-corrected-ten-proof-0403-d91-corrected-ten-proof-0403-1025040452-17648`
- Exact command: `pytest -q -n 3 -o addopts= -p no:cacheprovider --timeout=45`; no marker filter or `-m integration`.
- Result: `10 errors, 0 failures`, XML exit 1, all cases reached Runtime and failed with `step patch omits doc.patch changes`. Automatic NO-GO; no rerun.
- Controls: route `bash -n` passed; corrected positive control exited 17 with one 4-byte body; poison control exited 1 with zero body bytes. One earlier malformed run-mode stub was a zero-body harness setup error.
- No local pytest/collection/fixture/helper execution. Evidence is under `evidence/` (~1.28 MB); suite registry restored byte-identically.
- Commit message written and `DONE` created. No product files changed.

Recommended next step: resolve the Runtime step-patch rejection, then schedule a new authorized proof; do not repeat this unchanged run.