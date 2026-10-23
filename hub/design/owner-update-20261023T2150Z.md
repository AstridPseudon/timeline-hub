# Timeline: owner update, H24 (21:50 UTC, 23 Oct)

## The headline
- **P1's core chain passes:** case 1 runs the whole chain, including the lost acknowledgement, the restart and the exact retry.
- **The other three checks aren't passing yet:**
  - P1's case 2 (a second chained edit refused inside the App, before it's sent);
  - P2 and P3, which have failed only on the farm. There the App editor never connects or becomes ready.
- **Throughput collapsed this evening** to about 1 live worker and 6 merges an hour. Everything left is behind two serial proof runs, and each environment gap on the farm cost a 45–80 minute fix cycle. I've restructured to break that (below).
- **Honest ETA: 25 Oct, about 04:00 UTC** (range 20:00Z on 24 Oct to 16:00Z on 25 Oct). That's 8 h later than my H21 estimate. I'd been reading the optimistic end of the ranges.

## Numbers
| | H21 | **H24** |
|---|---|---|
| **End-to-end proofs** | 2 of 5 | **2 of 5 (P4, P5)**, plus P1 case 1 passing. P1 case 2, P2 and P3 fail. |
| Merges | 23 in 3 h | **14 in 3 h** (6 in the last hour), 191 since start |
| Live workers | 4–7 | **about 1** |
| Upstream | App d7ace | App 65c1771b7 (U3b-draft keeps up on a branch); Runtime and Agent unchanged |
| ETA | ~20:00Z 24 Oct | **~04:00Z 25 Oct** (20:00Z 24 Oct to 16:00Z 25 Oct) |

## What finished since H21
- **P1 case 1 PASS:** the core chain end to end, on App's own service.
- **A new pre-check** records the environment as evidence and requires "connected" and "owner ready" before any gesture.
- **Runtime:** the restructure-pins fix (unblocks G5); toolchain and child-environment delivery so App can build its own test benches; occurrence projection.
- **Kit fixes:**
  - the farm's provisioning allow-list and the exact Node 20 paths;
  - no more false "worker died" reports;
  - the report-writing rule (a worker's final message is its report, D30).

## What slowed us, and the root fixes
1. **The farm's environment never worked for P2 and P3:** about 6 permission and graph cycles since 18:12, then its rebuilt graph was swept away. *Fix:* **P2 and P3 now run on App's own service**, where P1 connects, side by side on one bench. The farm stands down to the final build.
2. **Stale "blocked" labels:** lanes kept waiting on Runtime fixes that had already merged. Told each lane to clear them; the existing rule re-checks blocked rows every pass.
3. **Undiagnosable runs:** the logs were cut off. *Fix:* full diagnostics now go to files. P1 case 2 gets one time-boxed Sol triage, with its reviewer named in advance.
4. **Deletions all waited on full P1.** *Re-gated:* G5 (the Agent deletions) merges at P1 case 1 + P4 + its own tests, since case 2 fails inside App before any Agent traffic. A4 (the App deletions) splits by whether production still reaches the code (D31).
5. **Disk:** handled. Main has 9 GB and the others 8–19 GB. A dispatcher-owned bench store with a budget and eviction is being built.

## Opus second opinion (H24), headline
"Throughput collapsed because two serial runs gate everything, and each environment gap costs a kit cycle. Fire the P3 A/B on App's service now, move P2 there too, re-gate G5 on case 1 + P4, time-box case 2. ETA ~04:00Z 25 Oct." **All acted on.**

## Your call (optional)
**A fallback deadline for P2:** if P2 (the 8-gesture tour) still isn't green by about 12:00 UTC on 24 Oct, do you want me to:
- (a) keep going until it is, or
- (b) ship with P2 marked partial, its failing gestures listed as a known gap, and the tests unchanged and visibly failing?

I'd recommend (a) unless you need a delivery by a fixed time.
