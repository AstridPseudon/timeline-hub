# Timeline: owner update, H78 (03:55 UTC, 26 Oct)

## The headline
- **Upstream moved after our 23:42 freeze, and a ZIP built now would not apply to fresh main.** Agent upstream gained 43 commits between 00:01 and 01:21 UTC: an MCP server, the OpenShell sandbox, and sandbox process control. App gained 3, the latest at 03:37 UTC. A trial merge of our versions conflicts in **10 Agent files** and **3 App files**. Runtime and Composition haven't changed.
- **The fix (D141l):**
  - We take one more merge from upstream for App now and for Agent after its current run.
  - Then we prove only what changed against the new upstream: its new tests and the files both sides touched.
  - The ZIP is built only from those final versions, and checked against upstream as it is at build time.
- **The deeper cause:** my drift checks compared against upstream copies that nobody had refreshed since the freeze, so they saw nothing. Every drift check now fetches upstream first, and it's part of the hourly check.
- **P4 is fully confirmed:** 3 of 3 passing on the final versions, and App's verdict file matches the hash we recorded.
- **Agent's full test run on the final versions is running now.** It lost about an hour to a launch-wrapper bug: the wrapper re-checked disk space after its own setup and refused itself. The test-by-test comparison against plain upstream is due around 04:00 UTC.

## Numbers
| | H75 (00:50) | **H78 (03:55)** |
|---|---|---|
| Done (ZIP chain steps) | ~35% | **~45%** |
| P1 / P4 | P1 PASS / P4 pending | P1 PASS / **P4 GO** |
| P2 (6 gestures), P3, P5 | waiting | waiting on the disk-monitoring setup (re-proof on the new App version) |
| Regression comparison | not started | Agent ~04:00, Runtime and App after the setup lands |
| Merges, last 3 h | — | 2 |
| Live workers | — | Runtime 2, App 0, Agent 1, Farm 0 → Farm now has a job |

## ETA
- **Realistic: 12:00–14:00 UTC.** Best case is about 09:30, worst is 18:00 or later.
- **Confidence: low to medium.**
- The upstream merge adds about 1–2 h.
- The Opus reviewer's view: the disk-monitoring setup is now the critical path, not the tests.

## What finished
- P4 GO on the final versions (3 of 3), with matching hashes.
- App's final version was locked in and its placement expectation fixed.
- Agent's launch-wrapper fix passed independent review with zero findings, and its full test run started.
- The Farm schema files were published and passed independent review.

## Blockers this window, how each was handled, and the deeper fix
| Blocker | Handling | Deeper fix |
|---|---|---|
| A ZIP from the frozen versions wouldn't apply to today's upstream | One more upstream merge, then a proof limited to what changed (D141l) | Drift checks fetch upstream first, every hour (lesson #100) |
| Agent's test launcher refused itself after its own setup | Ruled that disk is checked once before setup, then the wrapper was fixed | The written rule was right; the wrapper hadn't followed it |
| App's test runs would have waited on their own preflight's stricter disk limit | A run and its preflight are now admitted together (D141g-a), for App's re-proof only | — |
| The Farm run needed original setup files nobody can locate | Farm's run is now needed only if Agent's comparison asks for it (D141k), so we don't rebuild them | Cut work that isn't on the critical path |
| Each new disk exception starts another tooling build-and-review cycle | Time-box: 04:30 UTC, one review pass. Every lane frees space with the guarded tools to reach 5.0 GB (D141m) | Find the headroom instead of adding exceptions |
| I sent a duplicate message | Logged | Messages between lanes are delivered by the background sync, so I no longer relay them |

## Your calls
- **None.** SWAP and Element still ship as documented known gaps (D141).
- Nothing was blocked by a permission or safety check this window.

## Opus second opinion (headline)
"The disk-admission setup is the critical path, not the tests: every remaining proof but Agent's run waits on tooling build-and-review cycles, and Farm is idle with ~10 GB free." Acted on: Farm now smoke-tests the ZIP build and apply check, the tooling has a 04:30 time-box with one review pass, lanes free disk with the guarded tools, and cross-lane messages are capped.
