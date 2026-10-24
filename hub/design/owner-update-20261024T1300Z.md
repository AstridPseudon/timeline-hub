# Timeline: owner update, H39 (13:00 UTC, 24 Oct)

## The headline
- **Your speed-up is in effect** (D54–D57, plus the regression guard D54a):
  - The freeze merges are **in** for all three repos.
  - Proving happens once, on the final versions.
  - Independent review is now only for security code, protected tests and core product code.
  - The ZIP will be built on main, and Proof, Viewing and the farm have stood down.
- **The lanes took the principles on within an hour:** Agent is at 6 of 6 workers, App at 5 of 6, and about 89% of the work runs on Luna.
- **ETA: 25 Oct, about 04:00 UTC (range 22:00Z today to 16:00Z on 25 Oct).** That's 12 h earlier than at H36, with no functionality loss compared with upstream.
- **The gate is P2: all 8 gestures are core** (D55b), so it needs all of them. Three fail, each with a proven cause and an owner now. Five have never run, so they're the biggest risk, and they'll be exercised on the current code at once instead of after other work.

## Numbers
| | H36 | **H39** |
|---|---|---|
| End-to-end proofs | 3 of 5 | 3 of 5 (P1, P4, P5); P2/P3 now run on the current integrated code |
| Agent full suite | "4 open" (one-test-at-a-time count) | **276 failing in a real full run.** Being sorted by 6 parallel workers into core / regression / environment / pre-existing / dead |
| Runtime | 0 open | **core 0, regressions 0**; building the delivery pipeline on main |
| Freeze merges | Runtime only | **all three repos merged** |
| Merges | 22 in 3 h | 24 in 3 h (12 in the last hour) |
| ETA | ~16:00Z 25 Oct | **~04:00Z 25 Oct** (22:00Z 24 Oct to 16:00Z 25 Oct) |

## Will we lose functionality? (your question)
No, apart from deliberate removals of code nothing uses. **The regression guard (D54a)** means a failure can be a known gap only if it:
- comes from the test environment;
- fails the same way on upstream main;
- belongs to a deliberate deprecation;
- is scope you deferred.

Anything that works upstream and fails on ours is fixed or reverted, core or not. The process changes trade a little robustness (fewer independent reviews, no second clean-environment run on the farm) for speed. Strict gates and test bodies are unchanged.

## What finished since H36
- **Freeze:** App's U3b and D39 merged; Agent's U2 and D39 merged.
- **P3:** the strict retry-accounting fix (D53) is qualified.
- **Runtime:** its full suite is clear of core failures and regressions; the delivery pipeline is being updated.
- **Agent:** removals of dead code under D52 are under way, written by Runtime.

## Blockers, and the deeper causes fixed
1. **Worker finalization broke at 09:40, and it was my own edit.** A check I added made the worker launcher quit before it committed its work or cleaned up. Workers piled up, and App's disk filled. *Fixed and tested.* Automatic recovery now commits and cleans up any stuck worker. *Lesson:* changes to the launcher get a proper test run, not just a syntax check.
2. **A one-test-at-a-time count looked like "4 open"; a real full run showed 276.** *Fix:* real full runs on each lane's machine, plus a sort of every failure under the regression guard.
3. **Proof setups going stale,** which lost 2 P2/P3 attempts. *Fix:* a quick check of identities and bindings comes first for every setup, before review.
4. **Low parallelism.** *Fix (D57):* measurable limits, plus a board line showing live workers, the limit and ready work waiting.
5. **Decisions made:**
   - **D53, D58:** two more exact test corrections, each with independent review and a log entry. **D58 is conditional:** only if the contract confirms that Runtime's receipt ID is not the client's de-duplication key.
   - **D59:** when the final combination is cut (all lanes at 0 core failures and 0 regressions, and P2/P3 passing on it), plus which gates re-run after which change, and where each final rerun happens.

## Opus second opinion (H39), headline
"The freeze merges are already done, but there's no cut rule, so 'prove once' could keep repeating. Two proven P2 defects have no owner. Run P2/P3 on the current code now, so the 5 never-run gestures surface. ETA ~04:00Z 25 Oct." **All acted on** (D58, D59, owner rows dispatched).

## Your calls (optional)
- Tell me when your merges to upstream main are done, so I can schedule the final refresh (D51).
- The Viewing session (Timeline Child 2) is still blocked by the safety check. That's low urgency now that it has stood down.
- The `banodoco/astrid-agent` access request is no longer needed, since the farm stood down.
