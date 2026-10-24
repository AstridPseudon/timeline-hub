# H30 census review

Verdict: **FAIL for Author0350’s 136 closed / 131 open count.** The exact corrected count is:

- **142 closed**
- **125 open/held**
- **267 total**
- **No full-267 PASS; Farm checkpoint pending**

Six render-wire nodes are valid bounded integrated credit from service `27934` (6 exact selectors, 41.48s). The seven H3 nodes passed historically in service `0137` (3.60s), but D40 subsequently changed `runner.py`, `generic_host.py`, and `generic_host_worker.py`; they require current-source requalification and remain open.

Structural audit: **PASS** — 267 unique IDs and phase rows, all tagged `ours`, 262 call/5 setup, zero body-mapping mismatches, and no unsupported baseline credits.

H30 Viewing cluster: **PASS**, exact 33 nodes independently verified:

- native sheet: 24
- CLI native: 7
- scene dispatch: 2

All remain open under the current Viewing failover lane; Agent owns home merges.

Artifact: [h30-reconciliation-review.json](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-F-census-review-0358/evidence/h30-reconciliation-review.json)

Checks run:

- JSON validation — PASS
- Custom exact census audit — PASS
- Render-wire relevant-source identity check — PASS
- H3 D40 source-drift check — PASS (drift detected)
- `git diff --check` — PASS

No product/test changes or full reruns were performed. Next bounded work is current-source qualification of the seven H3 nodes and the assigned H30 failover rows.