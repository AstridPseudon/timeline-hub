# Timeline: owner update, H27 (00:55 UTC, 24 Oct)

## The headline
- **P1, the core chain, passed in full.** The original two-case run (both cases, including case 2, which was failing at H24) exited green in 141 s. Proof's independent check of that result is under way. When it confirms, P1 is GO and the deletions (A4, G5) can merge.
- **P2 and P3 now fail at the same single point:** the readiness check after startup, before any gesture runs. That's one cause to find, not two. A likely candidate turned up in upstream Agent: a fix for a bootstrap readiness marker and a Linux process race. App is testing it against the saved evidence by 01:30Z.
- **Speed recovered:** 21 merges in the last hour, against 6 an hour at H24.
- **ETA: 25 Oct, about 10:00 UTC (range 02:00Z to 24:00Z on 25 Oct).** That's 6 h later than at H24. P1 is ahead of plan, but P2's 8 gestures have *never* run, so more fixes after readiness are likely. The independent review also pointed out that my forecast has moved about +1 h per hour since H18. I've taken its later middle rather than my own.

## Numbers
| | H24 | **H27** |
|---|---|---|
| **End-to-end proofs** | 2 of 5 (P4, P5); P1 case 1 only | **2 of 5 confirmed, plus P1 full PASS awaiting its independent check.** P2 and P3 fail at readiness. |
| % done | — | **About 80% of the work merged. By proofs, 2 to 3 of 5.** |
| Merges | 14 in 3 h | **31 in 3 h (21 in the last hour)** |
| Live workers | about 1 | **5** (Agent 3, App 2). Viewing and the farm are idle by design, so they now take spare work (below). |
| Upstream | App 65c1771b7 | App b236cbfa3 (2 commits); Runtime 795379a67 (1); Agent 90d469808 (15, one possibly relevant). All deferred to the freeze except the readiness candidate. |
| ETA | ~04:00Z 25 Oct | **~10:00Z 25 Oct** (02:00Z to 24:00Z on 25 Oct) |

## What finished since H24
- **P1:** the full original chain PASSES: split, trim to a new ID, the intervening Agent edit, the lost acknowledgement, restart and exact retry, in both cases.
- **App:** P2/P3 bootstrap lifecycle and reload-readiness fixes; the A2 track projection, video caller and parent-media closure.
- **Agent:** about 14 full-suite fixes (schema oracle, document publish, CLI surface, motion and scene fixtures).
- **Runtime:** the upstream draft U1c passed independent review and is held for the freeze.

## Blockers since H24: how each was overcome, and the deeper cause fixed
1. **P2/P3 looked like two problems.** *Overcome:* one shared readiness row, with App fixing and Proof judging, and no more runs until the cause is named. *Deeper fix:* a **03:00Z time box**; if there's no named cause by then, I re-plan.
2. **Disk:** main fell to 8.4 GB. *Overcome:* compression, plus cleanups on App and Proof. The guarded cleanup tool correctly refused two old environments (1.5 GB), and I didn't force it. *Deeper fix (D34):* above the 8 GB line, disk work stops. Six workers had spent hours on storage tooling that freed nothing.
3. **Unreadable status lines hid stale state.** Three boards still said "P1 NO-GO" after it passed, and my door-port instruction never became a task. *Deeper fix (D33):* plain words, 200 characters or fewer per board cell, every note starting "Ask / Owner / By when", and every cross-lane ask becoming a task the same pass.
4. **No rule for the final full-suite gate.** Agent's full suite has 267 failures. *Decision D32:* each failure is either fixed or proven to fail identically on upstream main, in which case it's listed in the delivery as a known gap. Nothing is skipped. Viewing and Runtime, which are idle, now help write those fixes.

## Opus second opinion (H27), headline
"The critical path is P2/P3 readiness, with no time box, and the gestures behind it have never run. The 04:00Z ETA is optimistic: ~12:00Z on 25 Oct. Owner-less asks are hiding in shorthand, disk micro-work runs above the floor, and there's no full-suite gate decision." **All acted on:** the time box, U2c, the door-port task, D32, D33, D34, failover work for idle lanes and the P1 GO broadcast.

## Your call (still open, optional)
**P2 fallback:** if P2 still isn't green by about 12:00 UTC on 24 Oct, should I (a) keep going, which is my recommendation, or (b) ship with P2 marked partial, its failing gestures listed and the tests left unchanged and visibly failing?
