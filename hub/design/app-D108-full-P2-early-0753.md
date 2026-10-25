# D108 early full P2 report

Submitted exactly one normal D66 `p2` service using the authorized tuple. Source preflight passed.

- Target: `app-pin-04beedcd`
- Service ID: `app-pin-04beedcd-d73-p2-04beedcd-submit-1025075440-19078`
- Terminal: `FAIL`, 716s
- Readiness: PASS 1/1
- Original: PASS 4, FAIL 2, ERROR 1, NOTRUN 1

Gesture results:

- PASS: ADD, parent move, transition-none single, transition-none bulk
- FAIL: SWAP — `three-products.p2-popup.spec.ts:495`, expected 200, received 409 `history_unavailable`
- FAIL: element edit — `three-products.p2-elements-assets.spec.ts:1037`, expected `applied` status missing
- ERROR: automatic placement — `three-products.p2-elements-assets.spec.ts:1263`, response wait timed out
- NOTRUN: registerAsset — serially skipped after an earlier failure

Tuple trees:

- App `04beedcd…` / `300d186a…`
- Agent `070dfc5e…` / `60564143…`
- Runtime `1daca2a3…` / `a5225114…`
- Composition `635f4de0…` / `5ab5191a…`

Exact hashes and retained diagnostic filenames are recorded in [terminal-safe-facts.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D108-full-P2-early-0753/submission/full-p2/terminal-safe-facts.json). The submit plan is [p2-submit-plan.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D108-full-P2-early-0753/submission/full-p2/p2-submit-plan.json).

Commands/results:

- Normal checkout requests completed for missing App, Agent, and Runtime detached checkouts.
- D66 `p2 --submit`: preflight PASS; one normal service queued.
- `wait-test <same service ID>`: terminal FAIL, exit 1.
- Worktree remained clean; no product/test changes, lint, or unrelated suites run.

No retry, collector, alternate route, or cause inference was made.