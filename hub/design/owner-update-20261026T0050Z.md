# Timeline: owner update, H75 (00:50 UTC, 26 Oct)

## The headline
- **The final versions are locked in.** All four repos are frozen on the upstream versions we recorded at 23:42, and each contains all of upstream's work: Agent 28e56cac, App 867cb273, Runtime 6a011d58, Composition 635f4de0. I've given the go for every rerun.
- **Two regressions were caught and fixed while merging upstream,** before any of them could reach the ZIP. App's merge had silently dropped a check that keeps chat features off during a guided tour, and the review caught it (13 of upstream's own tests failing, now fixed). The D100 fix that 153 tests depended on is in.
- **Honest odds for the ZIP:** about **15% by 10:00 UTC** and about **45–50% by 16:00 UTC**. The independent reviewer and I agree that the 50%-by-morning I gave at midnight was too optimistic. The full chain runs one heavy job at a time per machine, and that's what takes the hours.

## What runs now (in parallel where machines allow)
| Step | Where | Expected |
|---|---|---|
| Plain-upstream comparison for Agent (the baseline for regressions) | Agent machine | ~01:10 |
| Ship-grade Agent full test suite on the final versions | Farm | ~03:30 (instructions still being finalized) |
| Runtime full suite plus plain-upstream comparison | This machine, once ~240 MB more is freed safely | ~03:00 |
| App full suite plus comparison, then P1, P2's 6 gestures, P3 | App machine, one at a time | ~04:00–05:00 |
| P4 (Agent), P5 (Runtime) | their machines | ~03:00–04:00 |
| Per-test regression comparison | all | ~05:00 |
| Fix regressions only, re-prove the affected tests | — | 0 h if there are none, 2–4 h each otherwise |
| ZIP build, check against fresh upstream, notes | Runtime, Farm | +1.5–2 h |

## What I decided tonight (you delegated the cuts at 23:55)
- **D141:** SWAP and Element ship as documented known gaps. The only fix gate is zero regressions against plain upstream. Our own failing tests that aren't regressions stay unchanged and visible, listed in the notes. The investigations stopped, upstream was frozen, and review rounds were reduced.
- **D141b:** compare only tests that exist upstream (17 of 22 groups), with a plain, reviewed command.
- **D141c:** "environment parity". If an upstream test fails because of the environment, it's rerun in a matching environment before we call anything a regression, so a different setup can't hide or invent one. The ZIP is built only from the final, receipted versions.

## Blockers this window, and the deeper fix
| Blocker | Handling | Deeper fix |
|---|---|---|
| App's merge dropped a tour check | Caught by review, restored, 89 related tests pass | The review step on every merge earned its keep; no change needed |
| Not enough disk for heavy runs on this machine and Agent's | Removed working copies that the cut made unnecessary (history kept) | Disk limits stay as they are |
| Lanes couldn't see the plan files at first | Confirmed they were on the hub and waited for the normal sync | — |
| My message headings had hand-typed times that didn't match the real clock | Fixed: headings now use the system clock | Lesson recorded |

## Your calls
- **None are needed.** Thanks for sending the scoped message to each session.
- **One thing was blocked, for your information.** I tried to delete the three old test environments on this machine on your "approve whatever you need". The automatic safety checker blocked it as an irreversible deletion, so I stopped. If you want it, you'd need to add a permission rule for it. We're working around it with safe cleanup instead.

## Opus second opinion (headline)
"Best case ~08:30, realistic 11:00–13:00. The riskiest step is the Farm child-plus-core chain, and the longest unknown is the regression-fix loop. Start the comparisons now, keep the environments the same, and build only from receipted final versions." All acted on.
