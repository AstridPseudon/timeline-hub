# How the machines communicate (owner-approved hub: GitHub AstridPseudon/timeline-hub)

## Machines and ownership
| Machine | Who | Areas (managers) | Home of repo (only this machine merges into its tl/integration) |
|---|---|---|---|
| main | orchestrator (Claude) | runtime, agent | agent, runtime |
| app | App area lead (Claude) | app | app |
| viewing | Viewing area lead (Claude) | viewing | composition |

A worker may change a repo that is not homed on its machine. For example, Viewing edits Agent `astrid/packs/rendering/` and App preview/player. That worker's branch is pushed to the hub, and a **merge request** asks the home machine to merge it through its normal queue.

## The hub (https://github.com/AstridPseudon/timeline-hub)
- **Files** go on branch `main`, folder `hub/`. Each machine writes only its own files:
  - `hub/status/<area>.md`: the manager's STATUS.md, prefixed with `machine | UTC time | dispatcher heartbeat age`. Written by the area's machine at least every 30 minutes.
  - `hub/escalations/<area>-<UTC>-<slug>.md`: written by the area's machine. When the orchestrator answers one, it moves the file to `hub/escalations/closed/`.
  - `hub/inbox/<area>.md`: orchestrator decisions, appended only. Written by main; the area machine copies new items into `managers/<area>/INBOX.md`.
  - `hub/design/*`: shared design docs. Edit only docs your area owns, plus coordination sections addressed to you; last writer wins per file. Mirror with `$ORCH/design/`.
  - `hub/merge-requests/<repo>/<worker>`: the asking machine writes one line, `timeline/<repo>/tl/<worker> <sha> <area> <one-line reason>`. The home machine merges with `bin/merge` and writes the result (`MERGED <sha>` or `REFUSED <reason>`) to `hub/merge-results/<repo>/<worker>`.
- **Code** goes in refs `timeline/<repo>/<branch>` on the same GitHub repo:
  - `timeline/<repo>/tl/integration`: pushed by the repo's home only, fast-forward only.
  - `timeline/<repo>/tl/<worker>`: worker branches, pushed by the machine that ran them.
  - Fetch everything with `git fetch hub 'refs/heads/timeline/<repo>/*:refs/remotes/hub/*'`.
  - Workers whose brief says `--base tl/integration` for a non-home repo use `hub/tl/integration`. Each sync fast-forwards a local read-only branch `tl/integration` from it.
- The remote named `hub` is https://github.com/AstridPseudon/timeline-hub. Never push to upstream repos (peteromallet/*, banodoco/*). The final delivery is still the ZIP built on main.

## Sync cadence
Each machine runs `$ORCH/bin/hub-sync <machine>` every ~5 minutes from a loop (`bin/hub-syncd <machine>`). It handles status out, escalations out, inbox in, design both ways, code push/fetch, and merge requests in/out. Git races: `pull --rebase`, then push, retrying 4 times with backoff (2/4/8/16 s).

## Who decides
Only the orchestrator answers escalations, changes PLAN.md and records gates. Area leads keep infrastructure healthy and relay messages. Managers follow MANAGER-COMMON.md exactly as on main.

## Cross-machine handoff of worker evidence (added 2026-10-20)
Worker folders do NOT sync from remote machines to main. Anything another area must read (a REPORT, a proposal.patch, a fixture or a probe) is copied as a FLAT file into `$ORCH/design/handoff-<worker>-<file>`, for example `design/handoff-vw-m3-d09-known-caller-preservation-proposal.patch`. design/ syncs both ways, newer wins. Code for another repo still travels as a hub branch with real commits. Never point another area at a path under workers/ on your own machine.
