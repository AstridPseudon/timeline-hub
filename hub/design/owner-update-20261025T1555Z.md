# Timeline: owner update, H66 (15:55 UTC, 25 Oct)

## The headline
- **The 14 regressions against upstream are fixed and merged.** It was a one-line restore of upstream behaviour in Agent's startup code. They count as closed once the next full Agent test run confirms them.
- **P2 is still 6 of 8.** But the last timed tour finally showed why element fails. In the real browser setup, a save request spends about 20 seconds on the server, about 12 of them in Agent's save handler. Element only allows 5 seconds. A direct replay takes 1.75 s, so it was missing something. SWAP's failure turns out to come from inside the database-reconnect code added this morning (D112), which now errors out itself. Runtime has both.
- **The biggest drag:** we haven't been able to measure Agent's test suite since 10:24 (it was 425 failing then). The farm machine was meant to do it, but its setup kept hitting an over-strict registry check, one problem at a time, for about 2.5 hours.
- **ETA moves to about 14:00 UTC on 26 Oct** (range 08:00 on 26 Oct to 00:00 on 27 Oct; the Opus reviewer gives the same). That's 4 hours later than at H63. **Confidence: low.** The main risk is that Agent's failures don't share a few root causes.

## What changes now (D128)
1. **Agent's full test suite runs on Agent's own machine now**, under the measured disk rule (start at 4.7 GB or more; the 4.0 GB stop line holds). Agent pauses its new fixes while the run is going.
2. **The farm gets until 16:30 UTC** to finish its setup fix. After that it only does the final render test, and no further review cycles go into it.
3. **SWAP:** Runtime fixes the reconnect path directly. Reverting it would just bring back the original refusal.
4. **Element:** exactly one fix, aimed at whatever cost the 20-second profile shows to be dominant.

## Numbers
| | H63 (12:55) | **H66 (15:55)** |
|---|---|---|
| P1/P3/P4/P5 | GO | GO |
| P2, current versions | 6 of 8 | 6 of 8; **both causes now identified** |
| Regressions vs upstream | 14 | **fixed and merged** (confirmed at the next full run) |
| Agent core failing | 425 (10:24 run) | 425, **not re-measured yet** |
| Merges | 27 / 3 h | 12 / 3 h (disk and setup-bound) |
| ETA | ~10:00 26 Oct | **~14:00 26 Oct** (08:00 26 Oct to 00:00 27 Oct) |

## Blockers this window, how each was handled, and the deeper fix
| Blocker | Handling | Deeper fix |
|---|---|---|
| 14 regressions | Fixed by a one-line restore to upstream, merged before the 14:00 deadline | Rule: claim "no regressions" only against the exact base the ZIP applies to |
| Disk on every machine | Tests moved to the farm and Proof; small work allowed down to 4.6 GB; admission checked once per run | The disk-cleanup tool had been touching `~/.codex` against your rule, so the lanes refused to run it. Fixed; the tool works again. |
| Farm setup refused, one problem at a time | Stop-and-report each time; the fix is to list every problem first, then fix them all at once | Rule: when a strict checker refuses, list all its findings before fixing any |
| A manager acted ahead of a decision (Proof unpacked Node early) | Verified the result byte for byte, then accepted it | Rule: a step on HOLD never runs early |
| A test assumed the old timeline behaviour | One-word method change in an upstream test, approved with review and noted in the ZIP notes | Changes to upstream tests always come to me and go in the ledger |

## Your calls
1. **The Agent venv delete is now the cheapest unblock** (1.5 GB on Agent's machine, which is stuck at 4.3–4.9 GB). Type this in **Timeline Child 4**: "I approve a plain delete of `/home/user/work/venv-agent-child` and `/home/user/work/venv-agent-child-s2`, those two directories only. Re-check that no process uses them first, then tell me the free disk." If you'd rather keep them, tell me and I'll stop asking.
2. **Optional:** say whether to allow retiring any of our own legacy tests (D120 item 5; none retired so far). E1 after the ZIP.
