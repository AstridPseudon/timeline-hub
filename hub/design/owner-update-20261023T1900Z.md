# Timeline: owner update, H21 (19:00 UTC, 23 Oct)

## The headline
- **Honest reset on P1.** It now runs its whole chain up to the restart, but its last failure (no recovery save after the restart) hasn't been fixed. The latest App merge was test-only.
  - Its cause may not be a bug at all. Production recovers automatically, while the test clicks a button that exists only in a test fixture.
  - I've ordered an independent ruling, product bug or test expectation, before anyone changes anything (D25).
- **Disk keeps blocking the proofs.** Each code-version change builds about 1 GB of read-only test environment, and two cleanup tools freed nothing. I've ordered one proper fix: the dispatcher owns the whole lifecycle, with a disk budget and automatic eviction.
- **ETA: 24 Oct, most likely about 20:00 UTC (range 14:00Z on 24 Oct to 08:00Z on 25 Oct).** My earlier "around 14:00Z" was the optimistic end; this is the realistic middle.

## Numbers
| | H18 | **H21** |
|---|---|---|
| **End-to-end proofs** | 2 of 5 | **2 of 5 (P4, P5).** P1 diagnostic; P3 running on the farm; P2 in parallel. |
| Merges | 15 in 3 h | **23 in 3 h**, 177 since start |
| Upstream | App efe83c77e | App d7ace4970 (moving fast, conflicts drafted on a branch); Runtime aa6c5b0cb (deferred) |
| ETA | ~19:00Z 24 Oct | **~20:00Z 24 Oct** (14:00Z on 24 Oct to 08:00Z on 25 Oct) |

## What finished since H18
- **Runtime:**
  - the all-or-nothing safety-check fix;
  - the sequential-edit fix;
  - the retire tool v1, installed (it refused everything, safely);
  - 15 unused checkouts recycled (1.6 GB).
- **App:** P1's corrected test check; restart diagnostics; the A4 deletion draft (now fixing parity).
- **Agent:** undo and occurrence-storage fixes; the G5 deletion draft is nearly ready.
- **Farm:** got the permissions you approved, plus the provisioning tools that were missing from its allow-list; the P3 environment is built.

## Blockers since H18: how each was overcome, and the deeper cause fixed
1. **Proof lane at its disk stop line.** *Overcome:* P3 and P2 runs moved to the farm. *Root fix:* bench reuse rules (D21a–c), and the coming dispatcher-owned bench store.
2. **Main fell to 6.4 GB:** a worker kept 2.5 GB of test fixtures in its own folder. *Fixed*, and a new rule says all scratch goes in temp folders.
3. **Farm permission gaps:**
   - the allow-list didn't cover the provisioning tools;
   - two permission patterns were broken;
   - the recovery script wrongly reported a finished worker as dead.

   All fixed in the kit and pushed.
4. **P1's crossed ownership and test-only fixes.** *D25:* triage before fix; full diagnostics written to files, because the last run's were truncated; and a GO on pinned versions counts, without chasing moving heads.

## Opus second opinion (H21), headline
- "P1's cause is still unknown, and nothing has actually fixed it. The next run is diagnostic. 'No recovery POST' may be a test expectation."
- "Disk patching freed 0 GB. Give the dispatcher the whole bench lifecycle, with a budget and eviction."
- "The end game is unscheduled. A4 and G5 have open failures, and P2 waits on P3 for no reason."

**All acted on:**
- D25;
- the bench-store task;
- A4 and G5 parity fixes as ready work now;
- P2 runs in parallel with P3.

## Needs you
Nothing blocking. Open question, whenever you like: fund relational timing as a follow-up?
