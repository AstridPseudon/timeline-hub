# Timeline: owner update, H63 (12:55 UTC, 25 Oct)

## The headline
- **P2 is at 6 of 8 gestures on the current versions:** placement, ADD, parent move, single clear, bulk clear and asset upload. Left: **SWAP** (Runtime now labels each refusal reason, so the next tour names the cause) and **element** (its save request is still in flight at the 5 s limit; App owns finding where the time goes).
- **P1, P3, P4 and P5 are all green.**
- **Agent's test suite is the long pole, and it isn't converging fast enough.** It went from 437 to 425 failing core tests in about 2.5 h, and 14 real regressions against upstream are being fixed. Two reasons for the slow pace: the merged fixes can't be measured, because every machine is at its disk floor; and fixes were going in test file by test file, often only to reveal the next failure underneath.
- **ETA moves to about 10:00 UTC on 26 Oct** (range 04:00 to 20:00 on 26 Oct; Opus gives the same). That is about 6 h later than at H60. **Confidence: low to medium.** It depends on the Agent fixes clustering around a few shared causes.

## What changes the slope (D124, from this Opus review)
1. **The farm machine (Child 5, idle with about 21 GB free) now runs Agent's full test suite**, so the fixes already merged get counted, and Agent's own disk goes to fixing.
2. **Agent fixes shared product causes, not test files.** The deeper failures that keep showing up (auth2267, auth1645, a missing import, the word-link setup) go to one strong worker and ship as one batched release.
3. **The 14 regressions: fix or revert by 14:00 UTC.** If the current fix fails, we put that startup code back the way upstream has it, unless an approved design decision needs our version.
4. **App owns element alone,** and runs the next full tour by about 13:30, naming SWAP's refusal and timing element in the same run.

## Numbers
| | H60 (09:55) | **H63 (12:55)** |
|---|---|---|
| P1/P3/P4/P5 | GO | GO |
| P2 on current versions | 4 of 8 | **6 of 8** |
| Agent core failing | 438 | **425** (plus about 10 merged fixes not yet measured) |
| Regressions vs upstream | 0 (claim withdrawn) | **14, being fixed** |
| Merges | 20 / 3 h | 27 / 3 h |
| ETA | ~04:00 26 Oct | **~10:00 26 Oct** (04:00 to 20:00) |

## Since the last update
- **Speed-ups you approved (D120)** are live: each fix is checked against just its own failing tests, our own tests need one review, and lanes coordinate directly. **D121:** I orchestrate only; all analysis runs in Codex.
- **Element:** the server-side slowness (D111b) was fixed and released, but element still fails. A direct replay takes 1.75 s, so the delay sits between the browser and Runtime.
- **The oh-my-pi download** is solved: the repo is public, so it now comes through a normal git fetch, as you pointed out. The render-test install is being measured to make sure it fits on disk.
- **Upstream Agent moved** 14 commits. Our changes are rebased onto it, and the 6 conflicts are resolved and reviewed (D123).
- **Agent disk** was the throttle all morning, so I let lanes start small code-only work down to 4.6 GB (D89b), with the 4.0 GB stop line kept.

## Lessons logged
- **"No regressions"** is only ever claimed against the exact base the ZIP applies to, on a clean copy.
- **A diagnostic change is still a product change.** One release broke every test setup because its tests used stand-ins.
- **Before changing the product or a test,** check whose test line it is.

## Your calls
1. **Agent venv delete, still the cheapest unblock** (about 1.5 GB on Agent). Type this in **Timeline Child 4**: "I approve a plain delete of `/home/user/work/venv-agent-child` and `/home/user/work/venv-agent-child-s2`, those two directories only. Re-check that no process uses them first, then tell me the free disk."
2. **Optional:** say so if you'd rather not allow retiring any of our own tests (D120 item 5). E1 after the ZIP.
