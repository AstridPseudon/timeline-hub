# Timeline: owner update, H12 (09:50 UTC, 23 Oct)

## The headline
- **Two of the end-to-end proofs now pass or nearly pass:**
  - P5 is done;
  - P4's single edit and its 10-notes-as-one-commit case pass on the integrated code, with all 10 undo/redo steps.
- **P1, the core App chain, is in final review.** Its last two root causes, one Agent and one App, are fixed and merging.
- **What's slowing us:** App's machine (still shut down every ~30–60 min, so it can merge only in short windows) and a frozen dispatcher on the Agent machine (fix ordered).
- **ETA: 24 Oct, 10:00–18:00 UTC, most likely about 14:00Z.** Allowing App's keep-awake saves about 4 hours.

## Numbers
| | H9 | **H12** |
|---|---|---|
| **End-to-end proofs P1–P5** | 1 of 5 | **1 of 5 done (P5), plus P4 mostly passing.** P1 is in review; P2 and P3 wait on App merges. |
| Board rows merged | 105 of 142 | **153 of 204.** New rows include real regressions found by the first full-suite run. |
| Speed | 30 merges in 3 h | **20 merges in 3 h**, 93 since start. The slowdown comes from App's merge windows and the Agent dispatcher freeze. |
| Upstream drift | none | **Runtime moved** (+7 commits: macOS CI fixes and a test skip registry, 3 conflicts). Merge ordered (U1b); the others are unchanged. |
| ETA | 10:00–16:00Z 24 Oct | **10:00–18:00Z 24 Oct, most likely 14:00Z.** |

## What finished since H9
- **App** (built on the Proof machine as failover, merged by App):
  - the head-publication adapter;
  - A3 child placement through occurrence.fork;
  - split authored-provenance;
  - P1's startup seed and environment.
- **Agent:**
  - G2 public command;
  - R2 split inverse;
  - the P4 ten-notes rerun;
  - F-core;
  - the R1 sequential mirror (one of P1's two root causes);
  - its full-suite run with all 380 failures classified: 316 are test-environment (durable fix merged), and every real regression has its own task.
- **Runtime:** the D17 authority, the producer fixture, the stale-envelope fix, and the history work.

## Blockers since H9: how each was overcome, and the deeper cause fixed
1. **App's machine was reclaimed 4 more times, killing every App worker.** *Overcome:*
   - App is now merge-only;
   - the healthy Proof machine builds App's work;
   - App can merge several reviewed commits in one wake (new rule).

   *Root fix needs you* (see below).
2. **The Agent dispatcher froze for about 35 min.** A worker ran a host recovery script inside its sandbox. *Root fixes:*
   - the script now refuses to run in a sandbox;
   - a stale dispatcher now raises an alarm;
   - "host scripts are lead-only" is a rule.
3. **Mail addressed to a lead was filed in the manager's inbox,** so leads never saw it. *Fix:* leads' recovery checks now surface it.
4. **Gates were prose,** so R5 and the deletions waited for a header line. *Fix:* exact, checkable gate criteria. R5 merges the moment A3 is proven; A4 and G5 merge the moment P1 is GO.
5. **Decisions:**
   - D16: earlier refusals keep every test check;
   - D17: cross-timeline duplicate is in scope as a writer migration (Agent command, Runtime verifies source authority);
   - D12a: no-new-invalidity covers cross-field checks.
6. **Row inflation** (142 → 204). *Rule:* new rows only for critical-path, gate or real-regression items.

## Opus second opinion (H12), headline
"App's merge window is the bottleneck. Three fixes wait on it, and every gate (P1, A3, R5, A4, P2, P3) needs it." It also found the Agent dispatcher freeze and the lead-mail gap. **All three of its actions are done:**
- the gate criteria and stacked merges;
- the Agent restart and the kit fixes;
- this escalation to you.

## Needs you (when you wake), in priority order
1. **App's keep-awake (saves about 4 h).** In the Timeline Child 1 (App) session, allow the 2-minute ensure-daemons **Monitor** (refused as "[Auto-Mode Bypass]"). Allow the INBOX archive step there too.
2. **Farm:** in Timeline Child 5, allow `bin/run-manager farm claude-sonnet-5-5` (needed for the final full suites; lanes use a slower fallback meanwhile).
3. **Routine scripts** in each child session (for example via `/fewer-permission-prompts`).
4. **Decision, any time:** support the two deferred anchor-undo cases (D14) later, or leave them deferred?
