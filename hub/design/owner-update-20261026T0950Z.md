# Timeline: owner update, H84 (09:50 UTC, 26 Oct)

## The headline
**About 70% done. No regressions remain in Runtime or App's unit tests. Everything left is blocked on disk.** Your hub-repack approval is the only unblock. After it, the ZIP is about **5.5 hours** away (range 5–6.5 h; add 2–3 h for any new regression).

## What's left
1. Agent's full test run on both sides, plus P4. This is the last regression check.
2. App's P1, P2-six and P3 runs on the final App version.
3. The final pin pass, the final ZIP build, and the check that the ZIP applies to upstream.

## Disk now
| Machine | Free | Needs |
|---|---|---|
| Agent | 4.66 GB | 4.71 GB (full pair), 5.0 GB (P4) |
| App | 4.45 GB | 5.0–5.2 GB |
| This machine | 4.25 GB | 4.86 GB (final build). It reaches the 4.0 GB stop in roughly 4–7 h |

## Your calls
1. **Hub-repack.** Paste the line from `design/owner-ask-20261026T0450Z-hub-repack.md` into each session, in this order: **Agent → this one (area = runtime) → App**.
2. **The final apply check.** Either allow Farm to run it, or say "run it on main".

## Since 06:50
- App caught up with the latest upstream (head 82e9e13d). Its unit-test comparison shows **zero regressions**.
- Agent has its final version (ecdc242e) and its full-run command passed review.
- Fixes to stop errors recurring:
  - Stale "running" markers no longer block the repack tool.
  - The stop tool can now cancel queued requests.
  - Sealed files are skipped by cleanup.
- A practice ZIP build dipped this machine to 3.93 GB for a moment. The final build is now treated as a heavy job, and its stop is being fixed so it reaches every process.

## Opus headline
"The ZIP cannot finish without the owner's hub-repack; every remaining body is disk-gated and waiting costs disk." Everything else is being pre-staged so the work starts the moment you approve.
