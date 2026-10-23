# Timeline: owner update, H3 (01:05 UTC, 23 Oct)

## The headline
- **Foundations are in.** The contract (C0, C0b and C0c) is finished and Astra approved it. All three upstream merges (Runtime, Agent, App) are complete or nearly so, against the real upstream.
- **The integrated edit path isn't proven yet.**
- **Overnight was slowed by systemic problems,** which I found and fixed at the root; details below.
- **Honest ETA:** 03:00–10:00 UTC on 24 Oct. That is later than the 16–24 hours I'd hoped for.

## Numbers
| | H3 |
|---|---|
| **% done (integrated proofs)** | **0 of 4** proofs pass: P1 is a partial NO-GO; P2, P3 and P4 haven't run yet. I count this, not task counts. |
| Work merged | 14 of 41 board rows: the contract, U1, U2, U3c, U4a, V1 inventory and schema, V3 pack, V4-agent, and test collections. No R, A or G implementation task is integrated yet. |
| Speed | 21 merges in 3 h (about 7 an hour). Live Codex workers dipped to about 4 during the safety holds, and are now recovering. |
| ETA | Best case about 21:00 UTC on 23 Oct; **realistic 03:00–10:00 UTC on 24 Oct**. Confidence is low-to-medium. I'll re-forecast at H6 and H8 from integrated proofs. |

## Hour-3 go/no-go: NO-GO (partial)
- **Proven:** the new patch command handles the real-document corpus (42 tests pass, independently reviewed). App's provenance and local-save modules pass their tests.
- **Not proven:** the end-to-end App chain (split, then an edit, then an Agent edit in between, then a lost reply, then a restart).
- **Why not:**
  1. A2 isn't wired into the editor's real save path yet.
  2. The v2 message shapes haven't been published by Runtime yet.
  3. Safety holds on `rm -f`, now fixed.
- **Deletions (A4, G5) stay locked until P1 passes.**

## Blockers: how each was overcome, and the deeper cause fixed
1. **Leads refused my relayed approval.** You approved in each session. *Root cause:* authority doesn't carry between sessions.
2. **Upstream merges used a stale upstream.** *Root cause:* main's repos fetched only an old branch, and that would also have broken the final ZIP build. It's fixed permanently, and upstream merges must prove they contain the live tip.
3. **Containers restart every 35–45 minutes,** and each restart killed in-flight work. *Root fix:*
   - an automatic recovery script on every machine;
   - durable keepalives;
   - a dead worker's work-in-progress is committed and resumed;
   - tasks are sized to about 30 minutes;
   - manager rounds are cut to 35 minutes.

   (I first thought these were idle reclaims; I was wrong, and the true cause is still unknown.)
4. **`rm -f` safety rejections held whole lanes.** *Root cause, found in my own tooling:* the dispatcher and the shared worker rules told every worker to "clean up temp files". Both are rewritten so scratch files go in a temp folder, with no `rm -f`. A refusal now stops one worker, not the lane.
5. **Workers stopped at sandbox limits** (sockets, git writes). *Root cause:* my one-page rewrite dropped the how-to section. It's restored.
6. **v1 state leaked into the new run** (old inboxes and old farm requests). Both were voided.
7. **Gaps in the plan:**
   - no owner for publishing the v2 messages;
   - no owner for re-adopting the clients;
   - two cross-lane requests nobody owned.

   *Root cause:* cross-lane requests travelled as peer notes. They're now board rows with owners.
8. **"Done" didn't mean wired in** (A2). *Fix:* acceptance now requires the real production caller.

The full log is in `LOOPS.md`, "Root-cause log".

## Opus second opinion (H3), headline
- "14 of 41 merged" overstated progress.
- The biggest bottleneck is Runtime's v2 wire, which every implementation task is waiting on. It's now Runtime's top priority, with 3 or more workers.
- The next risk is App's U3 review, which turns out to depend on Viewing's Composition exports. That dependency is now recorded.
- The farm being down leaves the H6 proofs without a home. Lanes will use their own test service until it's up.

## Needs you (when you wake)
1. **Farm:** in the Timeline Child 5 session, allow `bin/run-manager farm claude-sonnet-5-5`.
2. **Permissions:** in each child session, allow the routine scripts: run-manager, `bin/recycle`, KEEP-marker removal and manager INBOX writes. For example, run `/fewer-permission-prompts`. Several cleanups and writes are being refused case by case.
