## D128 report

- Verified exact frozen tuple and clean pin checkouts:
  - Agent `a4e016…`
  - Runtime `5e9ad…`
  - App `d8a1cd…`
  - Composition `635f…`
- Existing child environments did not match the required Agent/Runtime key.
- Submitted normal child request for `venv-agent-child-d128-a4e016`.
- Dispatcher refused at `2026-10-25T15:45:04Z`:

  `REFUSED: bench store: free-space reserve unavailable`

- No retry, substitution, reserve change, overlay, or route-around performed.
- No `agent-core-full` service was submitted; service ID: none.
- No body, preflight, D73 manifest, XML, or test results exist.
- Accounting: `core open: UNKNOWN`; classification `UNKNOWN`; retirement count `0`.
- Retained D54/D118 comparison recorded without new credit.
- JSON validation and `git diff --check`: PASS.
- Worktree unchanged.

Blocked pending normal dispatcher reserve resolution.