## Result

PASS for requested integrated proof on actual `HEAD 92baf961…`, tree `c5265e3f…`. Worktree remained clean; no source edits or merges.

Verified:

- Helper replay/journal commit `3b0dc9e80`: `14 passed in 91.66s`.
- Reader/current-port commit `61070c542`:
  - Integrated reader/timing group: `75 passed in 7.82s`.
  - Checkout history regression: `1 passed in 2.53s`.
- Mypy: `1911 current / 1911 baseline` — PASS.
- Vendor lock: PASS against Runtime `34eac004…`.
- Artifact manifest: PASS.
- `git diff --check`: PASS.
- Import origins resolve to this worktree; Runtime protocol resolves to the pinned Runtime checkout.
- Helper blobs are byte-identical to independent review `0107`; reader blobs to independent review `0108`.
- Frozen schema digest `d106dfe8…` and Composition archive digest `819acf6b…` verified.

Ruff ran successfully but exact-count gate reports `2147 current / 2148 baseline` and fails because the count improved by one. Baseline was not changed.

No full suite, HTTP/browser, SDK4, c271, or deferred gates were run. The named prior-report directory was unavailable, so evidence came from current tests and Git history.

Required commit message and `DONE` marker were created for the harness.