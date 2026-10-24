## D32 baseline comparison report

Completed read-only comparison against upstream `90d469808d61e469fbefbb4d00b81cbd307d904e`.

- Full map: [d32-baseline-comparison.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-D32-baseline-0148/evidence/d32-baseline-comparison.json)
- 267 unique nodes mapped:
  - `pre-existing`: 25
  - `ours`: 242
  - exact eligible unchanged files: 36
  - changed test files: 136
  - absent upstream: 95
- D14/D23/H9 remain visible and receive no PASS credit.

Evidence method:

- Byte-compared c36 test files with upstream.
- Confirmed all 36 eligible node IDs collect upstream.
- Ran the finite exact upstream targeted set with the qualified Python/runtime environment.
- Upstream result: 28 failed, 8 passed.
- 25 failures matched the original c36 signature/phase/cause and are credited `pre-existing`.
- 11 remain `ours` due to changed signatures or upstream passing.

Commands/results:

- `python3 -m json.tool .../d32-baseline-comparison.json` — passed.
- Exact upstream targeted pytest run — 28 failed, 8 passed.
- Worktree remains clean; no product/test changes, full rerun, installs, or Git operations performed.

Required `DONE` marker and commit message were created.