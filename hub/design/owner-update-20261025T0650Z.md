# Timeline: owner update, H57 (06:50 UTC, 25 Oct)

## The headline
- **P4 now passes: the ten-note test runs in 28.1 s against its 45 s budget** (it was 45.5 s). The D94 fix, with D97's safety condition, shipped at 04:25 after an independent security review passed.
- **P1, P3, P4 and P5 are green; P2 is at 4 of 8 gestures** (parent move passed at 05:14). P2 is the only test group still open.
- **ETA moves to about 01:00 UTC on 26 Oct** (range 20:00 on 25 Oct to 12:00 on 26 Oct; the Opus estimate is 03:00 on 26 Oct). That is about 5 h later than at H54. The reason: Agent's test suite has not been run in full on the current versions. 47 of its fixes are merged but not yet proven, and there is no count of what still fails. I'm fixing that now (D108).
- **One self-inflicted setback, now closed:** a Runtime release meant only to add diagnostics (689) broke every test setup. It had passed 36 tests, but those tests used stand-ins instead of the real Agent component. The fix is out, and the gap now has a rule (see below).

## Numbers
| | H54 (03:55) | **H57 (06:50)** |
|---|---|---|
| P1 / P3 / P5 | GO | GO (on their recorded versions; re-run on the final versions before shipping) |
| P4 ten-note | 45.5 s FAIL | **28.1 s GO** |
| P2 gestures | 2 of 8 | **4 of 8** (single clear, asset upload, bulk clear, parent move) |
| Agent fixes | most merged | 160 merged; **47 awaiting proof** (one full run is being set up now) |
| Merges | | 46 in 3 h (about 15 per hour) |
| Regressions vs upstream | 0 | **0** |
| ETA | ~20:00 25 Oct | **~01:00 26 Oct** (20:00 on 25 Oct to 12:00 on 26 Oct) |

## Blockers hit, how each was overcome, and the deeper cause fixed
| Blocker | Fix | Deeper cause fixed |
|---|---|---|
| P4 too slow | D94: Runtime keeps the already-verified history in memory (a security review passed) | D97: the safety assumption behind it ("whoever can edit the data can also edit the code") is now checked by Runtime at run time on each machine instead of being assumed. If the check fails, Runtime does the full check. |
| P2 Undo fails with "Runtime not ready", cause invisible | D102: every place that hid an error now logs one line, with private details removed | Standing rule: hiding an unexpected error without logging it counts as a defect. D102c gives each of the roughly six internal causes of "not ready" its own tag. |
| D102 itself broke every test setup (689) | Found by comparing old, new, and new-with-the-fix on main; fixed in 1daca within about an hour | Standing rule: any Runtime release that touches editing must first pass a test-setup run through the **real** Agent component, not stand-ins. |
| Too many "test setup is invalid" questions came to me | Decided D91, D96, D99, D100 and D103 one by one | D104: the lanes now decide setup-only fixes themselves under five strict conditions, and only bring me changes to test inputs or checks. |
| Placement gesture | Two App fixes (a preview label bug, then the test's clip lookup) | D105a: the test file turned out to be **ours**, and upstream already behaved the right way, so our test changes, not the product. Lesson: check whose line it is first. That also turned a check that could never fail into a real one. |
| A float rounding error refused exact-fit moves for real users | Agent fixes timing arithmetic to be exact (D100), with no tolerance added to Runtime's check | Rounding left over at an exact limit is now treated as a product bug, never as a reason to stretch the test setup. |
| Error logs lost before the test phase starts | App now keeps logs from launch, and its event capture keeps the most recent events | Rule: diagnostics must cover the whole run, including setup. |
| Disk | App freed 1.6 GB by releasing unused copies through the approved tools; logs are compressed after 1 h | Compression timing now follows the disk floors. |

## What's next (D108, from this Opus review)
1. **Agent:** one full suite run on the current versions, replacing 47 separate proof runs, then a published count of failing tests, each compared with upstream.
2. **Runtime:** a practice run of the final ZIP build now, instead of waiting for the final cut: apply the patches to fresh upstream, compare against upstream to check nothing got weaker, and do a real installed render. The final cut then becomes a re-run.
3. **App:** once the current ADD diagnostic names the Undo error, run the **full** P2 tour instead of one gesture at a time. Re-run P1 and P3 on the current versions.

## Opus second opinion, headline
"P2 is the visible bottleneck, but Agent core is the long pole and isn't being measured: 47 rows are merged without behaviour proof, and there is no core-open count. Final-cut prep is all gated on the cut when it could be rehearsed now. Run one full Agent core, rehearse F-final now, and do the full P2 tour once the 503 is named. ETA about 03:00 on 26 Oct." **All three actions taken (D108).**

## Your calls (all optional)
1. **Timeline Child 4 (Agent): the venv delete.** Type this in that session: "I approve a plain delete of `/home/user/work/venv-agent-child` and `/home/user/work/venv-agent-child-s2`, those two directories only. Re-check that no process uses them first, then tell me the free disk." It would free about 1.5 GB on Agent's machine (now 5.3 GB).
2. **The D94 trade-off:** D97 has narrowed it. Object only if you want the full check on every request regardless.
3. **E1 after the ZIP:** yes or no.
