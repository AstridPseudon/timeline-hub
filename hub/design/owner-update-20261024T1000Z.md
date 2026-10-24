# Timeline: owner update, H36 (10:00 UTC, 24 Oct)

## The headline
- **Agent's full suite: 263 of 267 closed, 4 open** (from 65 at H33). **Runtime's: 36 of 36 closed.**
- **The freeze has started:** Runtime's upstream merge and the client regeneration are merged. Agent's upstream merge has passed review and is queued. App's has passed review and waits for P2/P3. Composition is unchanged, and its checkpoint passed.
- **P2 and P3 are the gate, and they are converging only slowly.** In the one informative run since readiness was solved:
  - **P3** got further (past the reset). The next blocker is now fixed and qualified.
  - **P2:** still 3 gestures failing, and 5 not yet run. One cause is in an Agent function, and its fix is being written for the pinned version in parallel now. Another (the element Apply) is still unknown after six read-only passes, so I've ordered recording instead of more reading.
- **ETA: 25 Oct, about 16:00 UTC (range 08:00Z on 25 Oct to 12:00Z on 26 Oct), unchanged.** P2/P3 should pass around 17:00Z today (range 13:00–24:00Z), then 8–12 h of freeze, gates and the final build.

## Numbers
| | H33 | **H36** |
|---|---|---|
| End-to-end proofs | 3 of 5 | **3 of 5** (P1, P4, P5); P2/P3 converging |
| Agent full suite | 65 open | **4 open** |
| Runtime full suite | 0 open | 0 open |
| Freeze | not started | **Runtime merged; Agent and App reviewed; Composition clean** |
| % done | ~87% | **~92%** |
| Merges | 32 in 3 h | 22 in 3 h (the remaining work is narrow) |

## What finished since H33
- **Agent:** 61 full-suite failures closed, including fixes written by Runtime and Viewing. The one regression the farm comparison found (a recorded line count in a code-health test) was fixed without weakening the test.
- **Freeze steps:** U1c, D39 regeneration, Agent U2 review, App U3b review.
- **P3:** the D50 expectation fix, and the setup step through the real gesture.
- **Farm:** a proper test environment built for Agent's full suite; one more missing-package fix is in progress.

## Blockers since H33: how each was overcome, and the deeper cause fixed
1. **The freeze had no owner** (H33 review). *Fix (D48/D49):* Runtime coordinates, and drafts started at once.
2. **"Worker died" with no restart, twice.** *The App lead's diagnosis:* both hit their 18-min time limit. *Deeper bug, fixed:* the worker launcher quit on any Codex error, so failed or timed-out workers lost their saved work, and the automatic usage-limit fallback could never have fired. *Rule:* test-heavy work gets at least 45 min.
3. **The dispatcher blocked every launch while it built an environment.** *Fixed:* builds run in the background.
4. **Disk:**
   - a worker made three copies of a 1.9 GB store: stopped, with a "never copy benches" rule and an alert for large scratch;
   - repeated fetches left 27 pack files in one repository copy: 0.85 GB reclaimed, and now consolidated hourly on every machine.
5. **Sol work silently downgraded to Luna** when a brief lacked a marker (3 times tonight). *Fixed:* intent is read from the worker's name, and any downgrade is reported to the lane's manager.
6. **Viewing's session blocked twice on a "Send Message" permission prompt.** Leads now send routine reports as hub notes instead.

## Opus second opinion (H36), headline
"P2/P3 are converging slowly: 1 informative cycle in 4.5 h, about 2.2 h per cycle, 2–4 more likely. Cut cycles by instrumenting the element failure, writing the pinned-version popup fix in parallel, and releasing P3 alone if it doesn't touch popup. Check the final tuple early on a branch. Fix the silent Sol downgrade." **All acted on.**

## Your calls
1. **P2 fallback (due ~12:00Z):** if P2 still isn't green, (a) keep going, which I recommend and will do by default, or (b) ship with P2 marked partial, its failing gestures listed and the tests unchanged and visibly failing?
2. **Two deliberate test-expectation changes, for your review:**
   - **D44:** when one of two clips sharing a shot is edited, the untouched one keeps its identity.
   - **D50:** P3 expects the `created: []` field the approved contract requires.

   Both keep strict checks, were independently reviewed, and are in the delivery's behaviour-change log.
3. **To prevent another Viewing stall:** in Timeline Child 2, allow "claude-code-remote — Send Message" permanently, or switch to Accept edits.
