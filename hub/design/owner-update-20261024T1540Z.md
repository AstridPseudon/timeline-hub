# Timeline: owner update, H42 (15:40 UTC, 24 Oct)

## The headline
- **All final upstream merges are in** for Runtime, Agent and App, on the tips you pushed. Conflicts were resolved on Luna/Sol, keeping upstream's behaviour and adapting ours.
- **The regression check against upstream ran for real.** Agent's 276 failing tests were compared with a full run of unchanged upstream Agent:
  - **One real regression was found and fixed** (an environment-variables check). It's merged and passing.
  - **No other regression is proven.** 66 fail on upstream too; 199 are new tests of our own code.
- **P2/P3 are still the gate.** On the refreshed code, both died in 1 second at App's own test launcher before any test ran, so we have no product result. I've cut the extra launcher machinery App was building (D64, D66).
- **ETA: 25 Oct, about 08:00 UTC (range 03:00Z to 22:00Z on 25 Oct).** That's 4 h later than at H39. No P2 gesture has run on current code in about 10 h, and each P2 fix cycle has taken 3–4 h.

## Numbers
| | H39 | **H42** |
|---|---|---|
| End-to-end proofs | 3 of 5 (P1, P4, P5) | 3 of 5; P2/P3 blocked at the launcher (no tests ran) |
| Upstream merges | freeze merged | **final refresh merged in all 3 repos** |
| Agent core | "276 failing", being sorted | **7 core open** (all waiting on one Runtime change); regressions: 1 found and fixed, 0 open |
| Runtime core | 0 open | 3 open: the D62 work below |
| Merges | 24 in 3 h | about 25 in 3 h (from the lane clones I can see here) |
| ETA | ~04:00Z 25 Oct | **~08:00Z 25 Oct** (03:00Z to 22:00Z 25 Oct) |

## Decisions this hour (all mine, no change to strict tests)
- **D62: no new cross-repo trust layer.** Runtime asked to seal every recording run so a dishonest Agent couldn't drop data. I declined:
  - it's new security surface, and it only guards against our own logged-in Agent;
  - Runtime instead labels each commit's recording-format version when it accepts it, which is enough for the 4 failing fork tests.
  - *Known gap, logged:* a malformed new-format commit is rejected when someone first forks or undoes from it, not at submit.
- **D63: sorting the comparison with upstream.** Tests that don't exist upstream are our own and follow the core rule. Ones that fail on upstream too are pre-existing. Ones that pass upstream but fail on ours are regressions, and must be fixed.
- **D64/D66: P2/P3 launcher.** App kept building ever-stricter checks on how its own test runner starts, and that is what failed. It now stops that work: the runner starts the normal stack, runs the original tests unchanged, and records which commit and test files ran. P1 runs first as the control, then P2 and P3 in parallel.
- **D65: the install manifest.** App's installer pins exact upstream Runtime and Agent commits. Those can't be our final commits until you merge our patches (see your calls).

## Opus second opinion (H42), headline
"P2 is the risk: five gestures have never run and fix cycles take 3–4 h. App is still building launcher machinery; cut it, along with Runtime's separate proof stage. Pin the manifest only after the D62 regeneration. Also check the other way: upstream tests missing from ours. ETA ~09:00Z 25 Oct (03–24Z)."

**All acted on in D66.** The reverse check (upstream tests missing from ours) is the direct answer to "will we lose functionality?", and it's now running.

## Your calls
1. **A release step for you, at delivery (D65).** The ZIP will say:
   1. merge Runtime;
   2. merge Agent;
   3. run one included command in App, which points its install manifest at your new commits and checks the interface fingerprint matches;
   4. merge App.

   Nothing for you to do now.
2. **Possibly one known gap behind a refused permission (D66 item 5).** One Agent core test may need a source that sits behind an earlier access refusal. I've asked for the exact detail. If that's the case, I'll ask you to accept it as a known gap or grant access.
3. The Viewing session (Timeline Child 2) is still blocked by the safety check. That's low urgency, since it has stood down.
