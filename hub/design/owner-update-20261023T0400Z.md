# Timeline: owner update, H6 (04:00 UTC, 23 Oct)

## The headline
- **The core plumbing landed.**
  - Runtime's v2 commit wire is published and proven.
  - The App's real save path is mounted in the editor.
  - The Agent has its patch, undo and dry-run pieces merged.
- **No end-to-end proof passes yet.** The first proof (P1) hit a genuine design gap, which I've now ruled on (D13, below).
- **Honest ETA:** 06:00–12:00 UTC on 24 Oct. That is about 3 hours later than at H3.

## Numbers
| | H3 | **H6** |
|---|---|---|
| **% done (end-to-end proofs P1–P5)** | 0 of 5 | **0 of 5.** This is the real measure. |
| Plan tasks done (merged with proof) | 4 of 24 | **10 of 24**: C0, U1, U2, U3, R1, R2, R3, V1, V3, A2. U4 is half done; V4 is mostly done. |
| Board rows merged | 14 of 41 | **48 of 75.** Rows were split into smaller pieces. |
| Speed | 21 merges in 3 h | **22 merges in 3 h** (about 7 an hour), 43 since start. Only 4–5 live Codex workers at a time, which is too few (see the fixes). |
| ETA | 03:00–10:00Z 24 Oct | **Realistic 06:00–12:00Z 24 Oct; best about 01:00Z.** Confidence is low-to-medium. The remaining critical path is about 12 h of work, times a slip factor of about 1.6–2. |

## What finished since H3
- **Runtime:**
  - the full v2 wire (R2r, 02:14Z), then its client checks and an envelope correction (34eac, 03:27Z);
  - the contract amendments.
- **Agent:**
  - the native-read fix (R1-native);
  - guarded undo (R2);
  - dry run and structured errors (R3);
  - metadata reload;
  - one shared Composition artifact.
- **App:**
  - the upstream editor merge (U3);
  - v2 client adoption (U4p-v2);
  - **the A2 production save funnel, mounted in the editor**;
  - the trim fix.
- **Viewing:** the schema copies to every repo, and the Composition artifact adopted by both consumers (V1, V3).
- **Upstream:** no upstream drift in any of the four repos.

## Blockers since H3: how each was overcome, and the deeper cause fixed
1. **Old legacy timing data blocked unrelated edits** (V2). *Ruling D12, "no new invalidity":* a commit is refused only for declarations it creates, changes or breaks. Existing documents stay editable. No test was weakened; new negative tests were added.
2. **P1 couldn't pass as designed.** The App's saves declared no reads, so every save was all-or-nothing and the "merged" case was impossible. *Ruling D13:* gesture saves declare what they read, and send a field-level merge. Unknown edits stay all-or-nothing. It's a new App task, on Sol.
3. **Decisions waited about 1.5 h for me.** *Root cause:* escalations reach me only when I scan for them. *Fix:*
   - my hourly check now answers owed decisions first;
   - leads message me at once for any row that waits on me.
4. **Runtime published 5 client versions in 2 hours.** Each one forced the consumer lanes to re-adopt and re-review. *Root fix:*
   - the version is **frozen until P1 passes**;
   - future corrections are bundled into one release;
   - producer reviews must run the consumers' negative tests, because a consumer found the last gap.
5. **Rows stayed "blocked" after their dependency landed** (6 rows across 4 lanes). *Root fix:* a new manager rule. Every pass, each blocked row is re-checked against the owner lane's board and dispatched as soon as it's free. Gate holds are labelled separately from decisions.
6. **Peer requests sat as inbox text.** *Rule:* a peer request becomes a board row with an owner within one pass.
7. **A container restart killed a recovery pass.** I edited the recovery script while it was running. *Fixes:*
   - the script now has a single-run lock;
   - scripts are replaced atomically, never edited in place.

   The interrupted worker's work was saved and resumed.
8. **Main's disk was reported as a blocker** against a 15 GB floor that main can't physically reach. *Fix:* the floor is now set per machine; main's is 8 GB.
9. **The farm is still down.** *Workaround:* the Proof lane now runs P1 and P3 itself on the test service, instead of waiting.

## Opus second opinion (H6), headline
- **The three bottlenecks:**
  - the P1 design gap (now ruled, D13);
  - the Agent lane joining G2 → G3 → G4 one after another (now one combined join, with G4 no longer waiting on G3);
  - no home for heavy proofs (now the test service).
- Unfixed systemic causes it named:
  - producer churn (now frozen);
  - long review loops (A2 needed 7 rounds);
  - stale labels (new rule).

  I acted on all three of its recommended actions, and also started a draft of R5 (the final removal of the old save routes) on a branch, so it's ready when A3 and G4 merge.
- Its ETA agrees with mine: 06:00–12:00Z 24 Oct.

## Needs you (when you wake)
1. **Farm:** in the Timeline Child 5 session, allow `bin/run-manager farm claude-sonnet-5-5`. Every hour without it costs proof capacity, and it pushes the ETA out.
2. **Permissions:** in each child session, allow the routine scripts: run-manager, `bin/recycle`, KEEP-marker removal and manager INBOX writes. For example, run `/fewer-permission-prompts`.
