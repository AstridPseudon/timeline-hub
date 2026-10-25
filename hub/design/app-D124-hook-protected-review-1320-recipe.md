# D124 normal attach recipe

Use the existing generated D66 `p2` service recipe. Keep its four exact detached source tuples unchanged, with Runtime production pinned to `5e9ad1c6f74241d8771d3284fdd2ce7a214fd344`. Add these two explicit diagnostic variables to both the generated preflight and normal rows:

```sh
D66_P2_COMMIT_PHASE_CAPTURE_HELPER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D124-helper-first-return-1312/evidence/p2_commit_phase_capture.py
D66_P2_COMMIT_PHASE_CAPTURE_HELPER_SHA256=6c9daef27884c30b8faf234349078310af7ebe016bf0c4339960d5baae5a0760
```

Run the generated `p2 --preflight` row first, then the same generated `p2` normal row. The startup environment must preserve the four `D66_*_SHA/TREE/CHECKOUT` values and `ASTRID_P2_COMMIT_PHASE_CAPTURE_WATCHDOG_SECONDS=20`. The manifest should show the exact four source identities plus a separate `diagnostic_helper` object containing the explicit path, the `6c9d…` SHA256, and `source: "explicit"`; it must not identify that helper as Runtime `5e9ad…`.

This review did not run the live bootstrap or browser/P2 tour. The author's printed recipe used the superseded 1304 helper (`13883…`) and must not be reused.
