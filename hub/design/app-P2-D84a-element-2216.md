## Report

- Ran only the original isolated `p2-element` via the existing D66 `--submit` command.
- Source preflight: PASS.
- Host: `app-pin-bceb0350`
- Preflight: `app-pin-bceb0350-p2-d84a-element-2216-preflight-1024221720-29193`
- Normal request: `app-pin-bceb0350-p2-d84a-element-2216-1024221750-7131`

Source tuple was pinned exactly:

- App `bceb0350326f22beefdde5c5ba275412bb09b419`
- Agent `039ff2c2187d02b723074a8a6dfcbc6a70544c19`
- Runtime `732c48c6f5a9441a65c61b24595d454a1cd3e180`
- Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`

Result: automatic case-level NO-GO.

- Readiness: 1 passed, 24.1 s.
- Original ELEMENT: 1 failed, 22.517 s; service total 172 s.
- Failure: unchanged line 412, expected dialog status `"applied"` within 5 s.
- Actual gesture reached pending/unknown state; runtime accept/receipt/HTTP response phases were not observed. Eventual outcome: UNKNOWN.
- The 90 s response ceiling was not reached. Prior 2058 run failed identically at the same 5 s assertion; waits are unchanged.
- Aggregate 8-case tour was not run.

All outputs remain retained under the central result directory and private runtime diagnostics. No product files changed. DONE and commit message were created.