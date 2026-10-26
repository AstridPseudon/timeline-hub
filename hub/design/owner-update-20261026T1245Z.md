# Timeline: owner update, H87 (12:45 UTC, 26 Oct)

## The headline
**About 85% done. The proofs are finished except for Agent's 55 restored upstream tests, and those wait only on your decisions.**

## Results on the final versions
| Area | Result |
|---|---|
| Runtime | No regressions (15 found, fixed and re-proven). P5 passes |
| App unit tests | No regressions |
| App journeys | Placement, parent move, bulk, single, register-asset, P1 and P3 all pass. Popup ADD is a known gap |
| P4 | Passes on the current versions |
| Agent | 0 regressions in the full comparison, but 55 upstream tests that our patches dropped now fail. They need your decision |
| Disk | Fixed by your compaction approvals (Runtime 5.7 GB, Agent 7.6 GB, App 6.1 GB) |

## Your decisions (my recommendation)
1. Inverse, 38 tests: **A**, put back the upstream module our 19 Oct commit deleted.
2. Installer, 2 tests: **A**, retire the old npm-package tests and keep ours.
3. Writers, 15 tests: **A**, migrate them to the commit path and keep their checks; `force` stays refused.
4. App upstream target: **latest upstream**, with one catch-up merge (about 1–2 h). The shot-layering plan builds on it.
5. Shot-layering plan: **start the read-only prep on Farm now**, and build the release after the ZIP lands.

Reply "Go with your recommendations" to start all five.

## ETA
About 3–4 h to the ZIP after your reply.

## Opus second opinion
Skipped this round. Every remaining blocker is a decision of yours, so a review would add nothing new.
