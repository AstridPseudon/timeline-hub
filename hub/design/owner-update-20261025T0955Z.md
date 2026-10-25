# Timeline: owner update, H60 (09:55 UTC, 25 Oct)

## The headline
- **We finally have a measured count for Agent's tests.** One full run on the current versions took 24 min: 8,763 passed and 506 failed. 438 of those are core tests that we wrote; the rest are environment or non-core issues. **None is a proven regression against upstream.** This is now the long pole.
- **It is far fewer than 438 separate bugs.** 483 of the 506 sit in our own test files, which don't exist upstream. 29 files fail completely (267 tests), which points to shared test setup out of step with the current design, not 267 product bugs. The top 7 failure locations cover about 300 tests.
- **P1, P3, P4 and P5 are green.** P1 and P3 were re-proven on the current versions this morning. **P2 has 4 of 8 gestures proven on the current versions** (ADD, parent move, single clear, bulk clear). The other 4 have known causes, and each has a fix in review.
- **New owner decision, the only real blocker outside our control (see below):** the final installed-render test can't download one GitHub archive.
- **ETA: about 04:00 UTC on 26 Oct** (range 23:00 on 25 Oct to 14:00 on 26 Oct; the Opus estimate is the same). That is about 3 h later than at H57, because Agent's test count turned out to be 438.

## Numbers
| | H57 (06:50) | **H60 (09:55)** |
|---|---|---|
| P1 / P3 | GO on old versions | **GO on current versions** |
| P4 / P5 | GO | GO |
| P2 gestures | 4 of 8 (older versions) | **4 of 8 on current versions**; the other 4 each have a named cause and a fix in review |
| Agent core | not measured | **438 failing, all ours, 0 regressions**, concentrated in about 7 root locations |
| Merges | 46 in 3 h | 20 in 3 h (work moved to diagnosis) |
| ETA | ~01:00 26 Oct | **~04:00 26 Oct** (23:00 25 Oct to 14:00 26 Oct) |

## Blockers hit, how each was overcome, and the deeper cause fixed
| Blocker | Fix | Deeper cause fixed |
|---|---|---|
| P2 Undo failed with "Runtime not ready" | It was a lookup error in Agent's Undo code (a removed shot); Agent fixed it (D110), and ADD now passes | The new error logging (D102) named it in one run. Rule: every "no evidence" claim lists the files it searched (an early summary missed the log line). |
| A Runtime release broke every test setup (689) | Found by comparing versions; fixed in about 1 h (D102c) | Rule: any Runtime release that touches editing must pass a setup run through the **real** Agent component first. |
| Element too slow | The first theory (D111) was disproved by measurement and withdrawn; a proper whole-request profile now points at the document read (68–97% of the time); fix D111b is in review | Hard rule: no performance fix without an aggregated profile of the real request. One stack snapshot is a lead, not a measurement. |
| SWAP failed | A D94 safety check refused where it should re-verify (D112); fixed and as fast as before | Fallback behaviour now follows the approved design: when anything outside changes, Runtime does a full re-check instead of refusing. |
| Placement and asset upload failed | Both were **our own test**: a missing "close the dialog" step, and an expectation predating the D101 precision fix | Rule: before choosing between changing the product and changing the test, check whose test line it is. |
| Agent test fixes merged without proof (47) | One full run instead of 47 separate proofs, then fixing by cluster | New routine: every Agent version with product changes gets one full test run before other lanes adopt it. |

## What's next (D118, from this Opus review)
1. **Agent:** land the already-reviewed test-only fixes and rerun the full suite now, then after every batch of fixes. Group product fixes into a few releases, because each release re-triggers the final P1–P5 re-runs.
2. **App** (idle while waiting) helps Agent: up to 3 workers on Agent's remaining failure groups. It runs the full P2 tour as soon as Runtime releases the SWAP fix.
3. **Runtime:** release the SWAP fix; make sure the element fix really cuts the document-read time before releasing it; and re-check Agent's 23 failing tests in files that also exist upstream against fresh upstream, so the "0 regressions" claim rests on the exact base the ZIP applies to.

## Opus second opinion, headline
"Not all 438 by midnight, but they are far fewer than 438 bugs: 483 of 506 are in our own test files, and 29 files fail 100%, which is setup drift. Land the reviewed test-only fixes and rerun now. Batch product fixes. Put idle App on Agent's tail. Don't hold the P2 tour for element. Re-check the 23 upstream-file failures against fresh upstream. The real risk is the tail of about 106 assertion failures, which may hide real bugs. ETA about 04:00 on 26 Oct." **All acted on (D118).**

## Your calls
1. **NEW, needed for the ZIP: GitHub access for the installed-render test.** The installer downloads a pinned archive of `peteromallet/oh-my-pi`. This session only has access to `hannahsubmarine/repo`. My request to add read access was refused by the automatic permission check, so I stopped. Options:
   - (a) Give this session read access to `peteromallet/oh-my-pi`. Connect GitHub at https://claude.ai/connect-github, and install the Claude GitHub App on that repo if needed. Then let me retry adding it, or allow `mcp__claude-code-remote__add_repo` in your settings. If that can't apply to this session, add the repo to the environment's repositories.
   - (b) Provide an approved copy of that pinned archive.
   - (c) Accept the installed-render test as a known gap in the ZIP.
2. **Timeline Child 4 (Agent): the venv delete.** This is now the cheapest speed-up: Agent sits at about 5.0 GB, just under the floor for starting new work. Type in that session: "I approve a plain delete of `/home/user/work/venv-agent-child` and `/home/user/work/venv-agent-child-s2`, those two directories only. Re-check that no process uses them first, then tell me the free disk."
3. **Optional:** an objection to the D94 trade-off; E1 after the ZIP.
