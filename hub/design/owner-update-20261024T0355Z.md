# Timeline: owner update, H30 (03:55 UTC, 24 Oct)

## The headline
- **P1, the core chain, is GO** (00:43). Both cases pass on pinned versions, with independent verification. App's deletions (A4) are merging.
- **P2 got past its readiness step for the first time.** Its gestures finally ran: 3 failed and 5 haven't run yet. The 3 failures are App-side (a guard, a popup target, a parent move), and App is fixing all three in parallel now.
- **P3's readiness has a found root cause (D42).** Runtime re-checks the whole 21-command starting commit on every history read while holding its single global lock. That's 2 s per read even after tonight's first fix, and P2 also read twice. The proper fix is written and in security review: check each exact commit once per process, keyed by its content.
- **A second long pole:** Agent's full suite has about 80 of 267 failures still open, and the fix rate is falling. The farm (idle, 18 GB free) now runs a checkpoint full suite for an exact count, and Viewing takes two clusters of Agent fixes.
- **ETA: 25 Oct, about 14:00 UTC (range 06:00Z on 25 Oct to 06:00Z on 26 Oct).** That's 4 h later than at H27. The independent review is right that my estimate has been slipping about 1 h per hour, so I'm taking its later middle again.

## Numbers
| | H27 | **H30** |
|---|---|---|
| **End-to-end proofs** | 2 of 5 + P1 pending verdict | **3 of 5 (P1, P4, P5).** P2 past readiness (3 fail, 5 not run); P3 readiness root cause found. |
| % done | about 80% of the work | **about 83%.** By proofs, 3 of 5. Agent full suite: ~185 of 267 fixed (estimate). |
| Merges | 31 in 3 h | **46 in 3 h** (App 19, Agent 19, Runtime 8) |
| Live workers | 5 | 10 (App 6, Agent 4) |
| ETA | ~10:00Z 25 Oct | **~14:00Z 25 Oct** (06:00Z 25 Oct to 06:00Z 26 Oct) |

## What finished since H27
- **P1 GO**, with independent result and custody checks.
- **App:** most of A4 (the deletions); the readiness restart-deadlock fix; per-run port allocation.
- **Runtime:**
  - history-read cost cut about 3x, plus a version of the fix on the pinned code (the run that got P2 past readiness);
  - the corrected interface description (D39);
  - the private source-authority check (D40);
  - the D42 fix source.
- **Agent:** the client-code alignment; the full-suite census; about 20 fixes.

## Blockers since H27: how each was overcome, and the deeper cause fixed
1. **Every machine was losing disk at about 0.3–1 GB/h.** *Cause:* Codex saving the full history of every run, which nothing ever reuses. *Fix (D36):* Codex no longer saves it, and manager loops now reload when the shared tools change. App's loss fell from about 1 GB/h to about 0.25 GB/h. Leftover temp folders are now swept hourly on every machine.
2. **Decisions waited 1–2 h for me.** *Fix:* main's keepalive now flags every new escalation to me within 2 minutes. Four decisions were made: D37 (keep dormant code, listed for your review), D38, D39 and D40.
3. **Lost edits:** my decisions D38–D40 vanished from the shared header. *Cause:* the sync tool trusted file timestamps, which git resets. *Fix:* files I author are now synced by content and never overwritten by the hub.
4. **A stale "App is merge-only" flag** and **false "worker died" alarms**: both fixed in the tools.
5. **A fix landed on a newer Runtime whose client code differs,** so P2/P3 needed a 2-lane re-check. *Fix (D41):* fixes needed by a pending test go onto that test's pinned version first; everything else is adopted at the freeze.
6. **A fix that didn't clear P3.** *Fix:* an independent whole-path investigation found the real cause within 8 minutes. It's now a rule: after one failed fix, investigate the whole path at once, in parallel.

## Opus second opinion (H30), headline
"Agent is a single funnel with about 80 failures open, no current count, and full runs rationed by disk while the farm sits idle. P2's three failures are App-side, not D42. ETA ~14:00Z 25 Oct." **All acted on:** the farm checkpoint run (D43), an "N of 267 open" count, Viewing failover clusters, App authors for all 3 P2 failures, and the D42 pin released only with measured timing.

## Your calls (optional)
1. **P2 fallback:** if P2 isn't green by about 12:00 UTC today, (a) keep going, which I recommend, or (b) ship with P2 marked partial and its failing tests visibly failing?
2. **D37:** two old pieces of App code that production no longer calls are kept, unchanged and listed, as follow-up deletions for your review. Tell me if you'd rather they be deleted now.
