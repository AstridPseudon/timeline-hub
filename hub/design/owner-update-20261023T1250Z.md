# Timeline: owner update, H15 (12:50 UTC, 23 Oct)

## The headline
- **2 of 5 end-to-end proofs pass** (P4 and P5). **R5 is done**: the old save routes are now rejected, with an integrated proof.
- **Your two permissions worked.** App's machine has been stable since 09:59, the farm is live, and the 3 h from 09:38 to 12:38 brought **45 merges**, the best stretch yet.
- **P1, the core chain, is still NO-GO.** Its runs keep failing in the *test harness* before the real test body runs, one cause per attempt. I've changed how gate runs work (D21) to break that loop.
- **ETA: 24 Oct, most likely about 16:00 UTC (range 12:00–22:00).** This assumes P1 passes by about 18:00 today; every hour later moves the ETA by an hour.

## Numbers
| | H12 | **H15** |
|---|---|---|
| **End-to-end proofs P1–P5** | 1 of 5 | **2 of 5** (P4 and P5). P1 is blocked in the harness; P2 and P3 wait on one Runtime security fix. |
| Board rows merged | 153 of 204 | **200 of 240** |
| Speed | 20 merges in 3 h | **45 in 3 h**, 138 since start. The last hour had only 3, because the remaining work sits behind two gates. |
| Upstream | Runtime moved | App and Runtime moved again (tests/CI only), so they're **deferred** under the new rule. |
| ETA | 10:00–18:00Z 24 Oct | **12:00–22:00Z, most likely about 16:00Z.** |

## What finished since H12
- **R5:** old save routes rejected (the original 20 render scenarios plus 80 legacy cases pass).
- **P4 done:** single edit, 10 notes as one commit with every undo and redo, restart, show/history, conflict and rerun.
- **Upstream:** Runtime merged (U1b); Agent's merge is in review (U2b).
- **App:** about 14 fixes for the farm's full-suite failures, plus the A2 placement and popup work.
- **Agent:** the D17 cross-timeline duplicate (Runtime authority plus the Agent port), undo-v2, the R2 port, and the D09 harness fix.

## Blockers since H12: how each was overcome, and the deeper cause fixed
1. **App's machine** stopped being reclaimed once you allowed the Monitor. Merge-only was lifted, and App is working its own rows again.
2. **The Agent dispatcher froze for 35 min** on a pip install with no timeout. *Fixes:*
   - every pip call is now bounded;
   - a stale-dispatcher alarm;
   - workers can no longer run host scripts.
3. **Main's disk hit its 8 GB floor.** A finished dry run had left a 1.4 GB clone. *Fixes:*
   - removed it (main is back to 10 GB);
   - fresh clones now go in temp folders;
   - **the final delivery build runs on the farm.**
4. **The farm's App full rerun was refused by its worker permissions** (copy, link and unpack while building a private dependency set). *Not worked around (D19):* the run went back to App, whose own workers do this normally.
5. **P1's harness loop.** *Root fix (D21):*
   - test environments are built by the dispatcher, never by hand;
   - every gate run starts with a preflight that reports all problems at once;
   - harness-only fixes, with the test body hash-locked and unchanged, skip the review round. This cuts each P1 attempt from about 1 h to about 15 min without weakening the proof.
6. **Upstream churn:** 3 tests-only upstream moves in 3 h. *New rule:* defer by default. Merge early only if a change touches the contract, schemas, the save path or pins, fixes a failure we're hitting, or is a security fix. Otherwise there's one upstream merge per repo at the final freeze.
7. **Decisions:**
   - D18: a product guard refusing our harness means the harness is fixed, never the guard;
   - D20: same-timeline shared placement is built only if an old writer could create it; otherwise no new API, and no fabricated test data.

## Opus second opinion (H15), headline
"The 45 merges were a burst of independent fixes. What's left sits behind two serial gates (P1 and Runtime's created-child fix). P1 fails in the harness, not the product, so separate harness qualification from the proof." **All three of its actions are done:** D21, provisioned benches and preflight, and the upstream rule with D20.

## Needs you
- **Nothing blocking.** Optional: to let the farm run App's full suites itself, allow file copy, link and unpack inside its own worker folders in the Timeline Child 5 session.
- Optional, for disk headroom: in App (Child 1) allow `bin/recycle` and removing old v1 KEEP markers; in Viewing (Child 2) allow removing old v1 KEEP markers.
- Decision, any time: support the two deferred anchor-undo cases (D14) later, or leave them deferred?
