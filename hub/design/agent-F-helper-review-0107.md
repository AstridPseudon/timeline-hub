## Review report

Verdict: candidate-specific PASS; neighbour suite remains FAIL and is not waived.

Changed files are limited to [journal.py](/home/user/work/wt/agt-F-helper-review-0107/astrid/sdk/timeline/journal.py) and the new numeric coverage test.

Tests:

- New suite: `14 passed in 92.99s`.
- Neighbours: `42 passed, 3 failed`.
  - `test_nudge_restart_merges_peer_other_clip`: fails before helper code; test wrapper pops an already-absent `_runtime_document`.
  - `test_contiguous_helpers_keep_sequential_steps[True]`: Runtime rejects at `timeline_commit_auth.py:2196` with authenticated sequential replay-map duplication/omission; no accepted write.
  - `test_cut_nudge_restart_merges_other_cut["second"]`: setup commit fails before candidate code with Runtime’s missing exact word binding.
- Ruff touched file: PASS.
- Whole-tree Ruff: 2,148 diagnostics; durable parent/new identities unchanged.
- Mypy: 1,911 diagnostics; durable parent/new identities unchanged.
- Vendor lock, artifact manifest, and `git diff --check`: PASS.
- No full suite run.

Durable `commands.txt` and `numeric-capture.json.gz` confirm authenticated base pair/source, digest and reads, exact commands/steps, accepted then merged Runtime replies, opaque `null` preservation, and disjoint peer preservation.

No production files were edited; no protected-property bypass was found. Recommended next step: resolve the three original neighbour failures separately, then rerun that bounded neighbour suite.