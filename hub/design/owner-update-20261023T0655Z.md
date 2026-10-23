# Timeline: owner update, H9 (06:55 UTC, 23 Oct)

## The headline
- **The first end-to-end proof passes:** P5, the Runtime acceptance checks (native 14 plus the crash/retry points, on the integrated code).
- **The Agent lane is almost complete.** All its writer migrations (G4) are merged, as are the fork command and the patch, undo and dry-run work.
- **The App lane is now the bottleneck,** and the main cause is environmental. App's machine is shut down about once an hour, killing its workers, because its keep-awake was refused (details below). **This is your #1 to-do.**
- **ETA has slipped to 10:00–16:00 UTC on 24 Oct.** That is more than 20% past target, so I applied the plan's cut order: V4 (the optional cleanup) is cut.

## Numbers
| | H6 | **H9** |
|---|---|---|
| **End-to-end proofs P1–P5** | 0 of 5 | **1 of 5** (P5). P4 is partly passing; P1 is running; P2 and P3 wait on App. |
| Board rows merged | 48 of 75 | **105 of 142.** Rows were split further. |
| Speed | 22 merges in 3 h | **30 merges in 3 h** (10 an hour), 73 since start. |
| ETA | 06:00–12:00Z 24 Oct | **10:00–16:00Z 24 Oct**, low-to-medium confidence. It comes in earlier if App stays awake. |
| Upstream drift | none | none (all 4 repos unchanged) |

## What finished since H6
- **Runtime:** the D12 contract text (C0d), R2r client and envelope repairs, assembly/archive/isolation landings, and **P5 proven**.
- **Agent:**
  - U4a-v2 adoption, R2 undo, V2 timing with D12;
  - G2 (open/commit), G3 (document emitter and show) and **all G4 writer migrations**;
  - **occurrence.fork (D15)**, the P4 reader and the single-edit HTTP pass.
- **App:**
  - U4p envelope;
  - A3 popup and placement;
  - D13 declared reads for split and trim;
  - the P1 spec port and the P3 resolver.
- **Proof:** P1 isolated environment and seed; P2 and P3 ports.

## Blockers since H6: how each was overcome, and the deeper cause fixed
1. **The Agent lane stalled for 30 min** with its daemons "alive". *Cause:* the manager's inbox grew past Codex's 1 MB prompt limit, so every round crashed instantly. *Root fixes:*
   - managers now send only the newest 200 KB of their inbox;
   - the recovery script reports "MANAGER FAILING";
   - the keepalive filter can no longer hide warnings.
2. **Duplicate managers on the Proof machine.** *Cause, my bug:* the recovery script started managers inside the caller's process group. *Fix:* managers start detached, and a running round counts as alive.
3. **An unreviewed 29-file merge** got into Agent via a "test-only" request. *Fix:*
   - an audit was ordered;
   - merge requests may now carry only the worker's own commits.
4. **17 escalations in one hour hid the 2 real decisions.** *Fix:* escalation files are now only for decisions I owe. Requests between lanes become board rows.
5. **Decisions I made:**
   - D13: gesture saves declare their reads;
   - D14: two old anchor-undo tests are deferred, visibly failing, never claimed as passing;
   - D15: the per-occurrence fork is in scope;
   - D16: when v2 refuses earlier than v1, tests are adapted with every check kept;
   - D12a: no-new-invalidity also covers cross-field checks such as frame-rate parity.
6. **Producer churn and stale "blocked" labels** (from H6). *Fixes:*
   - the Runtime version stays frozen;
   - blocked rows are re-checked every pass.
7. **Review churn** (about 8 workers per merge on Runtime). *New rule:* a conflict-free merge-forward needs only a targeted re-run, not a new review.
8. **Main's disk was down to 9 GB.** *Fix:* old worker logs are compressed losslessly, giving 9.9 GB.

## Opus second opinion (H9), headline
"App is the single point of failure. P1, P2, P3, A3 and R5 all wait on it, and its machine is off between hourly wakes." It also noted:
- two App rows were ready but still labelled blocked;
- two needs had no owner row (App's guarded Undo, App's head adapter);
- R5 was gated on a G4 condition that was already met.

**Acted on:** the rows are fixed and assigned. The healthy Proof machine may now build App-repo work as a failover. G4 is marked done, so R5 merges as soon as A3 lands. V4 is cut.

## Needs you (when you wake), in priority order
1. **App's keep-awake.** In the Timeline Child 1 (App) session, allow the 2-minute ensure-daemons **Monitor**. It was refused as "[Auto-Mode Bypass]". Without it, App's container is reclaimed about once an hour and every running App worker dies (5 at 06:40). I have not worked around this. Also allow the INBOX archive step there (it's 659 KB; the new cap keeps it safe).
2. **Farm:** in the Timeline Child 5 session, allow `bin/run-manager farm claude-sonnet-5-5`. The final full suites need it, or else a slower fallback on each lane's test service.
3. **Routine scripts** in each child session (for example via `/fewer-permission-prompts`).
4. **Decision, any time:** do you want the two deferred anchor-undo cases (D14) supported later (option a), or left deferred?
