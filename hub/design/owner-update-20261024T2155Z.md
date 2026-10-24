# Timeline: owner update, H48 (21:55 UTC, 24 Oct)

## The headline
- **P3 passed for the first time** (20:44), with an independent GO. **P1 and P3 are green on the current code.**
- **The setup hang that blocked every P2 run is fixed** (Runtime, about 21:00).
- **The deeper cause is now pinned down:** Runtime re-checks the WHOLE accepted history on every request, one request at a time. P2's gestures (element, popup, parent), P4's ten-note step and Agent's timeout cases all stall there.
  - The three quick fixes so far gave 4–8% each.
  - A structural fix is now running: check outside the request lock, and only check what's new if needed (D84).
- **ETA: 25 Oct, about 12:00 UTC (range 07:00Z on 25 Oct to 04:00Z on 26 Oct).** That's back from the 06:00Z target I gave at 20:20; that target assumed the wait would be one simple spot, and it's structural. The Opus second opinion says about 13:00Z.

## Numbers
| | H45 | **H48** |
|---|---|---|
| End-to-end proofs | P1 green | **P1 and P3 green.** P4: main cases pass, ten-note 45.4 s against a 45 s budget. P2: 0/8 (stalls in Runtime history verification, plus one App setup bug). P5: green earlier. |
| Agent core | 2 original cases (22 tracked) | **5 tracked** (all timeouts, same Runtime cause) |
| Runtime core | 2 | 1 root cause (history verification) |
| ETA | ~12:00Z 25 Oct | **~12:00Z 25 Oct** (07:00Z 25 Oct to 04:00Z 26 Oct) |

## What finished since H45
- **P3 GO.** All four approved test corrections held (each stricter, or truer to the real product).
- **The setup wait is fixed,** so P2 gestures now actually run.
- **The popup ownership rule is unified** across Agent and Runtime, with a security review.
- **Two history-speed fixes and one decoding fix are merged,** each with a security review.
- **Your elegance plan:** designs came back, and you have the proposal (do E1, skip E2, fold E3). It's paused until the ZIP, to keep all slots on the critical path.

## Blockers hit, and the deeper cause fixed
1. **One wait looked like five separate failures.**
   - *Fix (D83):* treat them as one bug, found from the evidence across runs, and chase it in a seconds-long local loop instead of 7-minute browser runs.
   - *Deeper:* the structural verification fix (D84).
2. **P3 failed one check per 2-hour cycle.**
   - *Fix:* stricter "check both exactly" corrections, now a standing rule.
   - *Fix:* the reviewer applies its own approved correction.
   - *Fix:* NO-GO runs skip their separate verdict.
3. **Hub-sync wedged one machine for an hour** on a single conflicting line. *Fixed in the shared tools:* it falls back to a merge, with an automatic alert if that also fails.
4. **Disk limits App and Agent.**
   - Critical runs now go down to 6 GB.
   - Lossless packing of old test output is added.
   - The rest needs you (below).

## Opus second opinion (H48), headline
"The focus is right: Runtime's history verification gates P2, P4 and Agent. Demand a structural fix (verify outside the lock and only verify new entries), not more micro-gains. Fix App's own two P2 bugs now instead of waiting for Runtime. Free App's disk. ETA ~13:00Z 25 Oct." **All acted on (D84).**

## Your calls (optional, each just gives a lane more workers)
1. **Timeline Child 1 (App):** allow deleting `/home/user/work/app-m3-private13-normal-lock-install-units-r6-owned`. It's 1.1 GB from an earlier version, unused, with no guarded tool for it. App is at 5.3 GB and limited to 1–2 workers.
2. **Timeline Child 4 (Agent):** allow releasing the 38 stale code copies (about 2–3 GB) that the safety check blocked.
3. **The E-plan proposal:** say yes or no to E1 after the ZIP.
