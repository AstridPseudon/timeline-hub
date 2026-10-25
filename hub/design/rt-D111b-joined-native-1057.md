## Report

- Waited for and verified the sanctioned merge-forward.
  - Auth blob: `66d899...` from `42aad0e`.
  - Port: `61aa1357...`.
  - Store: `0ffaac...`.
  - Ancestry test: `c309169...`.
- Bound the diagnostic evidence path to this worker.
- Native route: `full-d111b-native-1047` — **FAIL** unchanged 1.5× gate:
  - `_read`: 94.563 ms → 186.383 ms, **1.971×**.
  - Eight POSTs accepted; receipt/readback equality, unchanged rows, and 401 refusal passed.
  - Evidence: 104 KB under the worker evidence directory.
  - Dominant growth: revision-closure reads 29.34 ms → 122.79 ms; history reads 23.75 ms → 48.86 ms.
- Tests:
  - Focused joined controls: **360 passed, 1 failed**.
  - Native seed smoke: **2 passed**.
  - Real-provider smoke: **2 passed**.
  - Central HTTP/history controls: **8 passed**.
  - Ruff: passed.
  - Compile and diff checks: passed.
  - Pyright: 57 diagnostics, identical to prior baseline; zero new diagnostics.
- The failing auth test is `test_created_child_public_captured_transcript_advances_sequential_manifest[None-True]`, due to sequential capture not matching the authenticated head. Released auth was preserved; no product fix attempted.

Source remains held pending independent security/core review and resolution of the joined auth regression. Commit message and `DONE` marker were created.