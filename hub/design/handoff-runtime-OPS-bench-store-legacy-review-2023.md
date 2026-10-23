# OPS-bench-store legacy review 2023

## Verdict: FAIL as written

The exact-seven proposal is a valid bounded *proposal* (PASS for scope), but the
2017 assessment is not factually acceptable as the Runtime recommendation. It
correctly observes that the installed core has no public legacy
unregister/adopt/migrate operation, but it incorrectly treats the shared
Remotion key as ruling out a registration-only transaction, calls the relief
optional under the superseding 18:46 lifecycle, and invents `/proc` executable,
cwd, and FD scans as a future requirement.

## Findings

1. **1841/1847 proposal scope: PASS.** The author packet says the patch is one
   seven-row suite deletion plus seven exact env-file deletions and preserves
   non-target rows/env bytes ([1841:43-47](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-OPS-retired-registrations-1841.md:43>)).
   The independent review confirms the private result has exactly seven target
   rows and seven target env files absent, with current/P1/P2/P3/F inputs
   protected ([1847:30-37](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-ap2-OPS-retired-registrations-review-1847.md:30>)).
   This changes neither the seven legacy runtime directories nor the protected
   `agent-remotion-ap2-current-079-2a9-1743` registration.

2. **Shared Remotion key: the assessment overclaims.** The seven rows sharing
   one Remotion tree/key only prevents representing seven distinct historical
   paths as seven independent *managed bench entries*. It does not prevent a
   registration-only operation whose result is: delete the seven exact suite
   rows/env files, preserve all outside/current bytes, and leave every legacy
   runtime path untouched. The assessment's path/key observation
   ([2017:28-32](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-bench-store-legacy-assessment-2017.md:28>))
   is true only for managed-entry adoption, not for this intended result.

3. **Current API gap: real, but narrower.** Installed core `6d936820…`
   initializes only a new root and explicitly refuses adoption of an existing
   root ([bench_store.py:117-131](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/bench_store.py:117>)).
   Its public mutating path is `ensure`, which creates/reuses a keyed managed
   entry and then adds a registration ([bench_store.py:579-644](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/bench_store.py:579>));
   `registered`, `registration_entries`, `names_for_suite`, `acquire`, and
   `run` do not unregister an unmanaged name ([bench_store.py:654-715](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/bench_store.py:654>)).
   `_evict` can delete only indexed, store-owned entries and their dependent
   registrations ([bench_store.py:430-480](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/bench_store.py:430>)).
   Therefore the current API cannot perform the seven-row/env result, but the
   reason is **missing registration-only API**, not the shared key.

4. **Relief is mandatory for this 18:46 whole-lifecycle row, not optional.**
   The 18:46 owner direction orders one OPS-bench-store lifecycle including
   transactional bench + suite/env handling ([owner:3-5](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/peer-runtime-to-app2-20261023T1850-bench-store-owner.md:3>)).
   The prior assessment's “optional legacy relief” conclusion
   ([2017:44-48](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-bench-store-legacy-assessment-2017.md:44>))
   applies only to its earlier dedicated-store interpretation and is
   superseded here. It does not authorize a live run: the exact proposal and
   prior FS/guard refusals remain STOPPED.

5. **Liveness boundary: no `/proc` requirement.** D21c keys the components by
   content identity ([BOARD-HEADER:78](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/BOARD-HEADER.md:78>));
   the 18:46 lifecycle direction uses flock per-run liveness
   ([owner:3](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/peer-runtime-to-app2-20261023T1850-bench-store-owner.md:3>)).
   Installed `acquire` holds stable entry locks and `run` passes those FDs to
   descendants ([bench_store.py:691-715](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/bench_store.py:691>)).
   The assessment's proposed `/proc` executable/cwd/open-FD scan
   ([2017:46](</tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/handoff-runtime-OPS-bench-store-legacy-assessment-2017.md:46>))
   is not a requirement and must not become a recurring superseded process
   scan. The genuine gap is one-time: legacy registrations are not indexed, so
   the current flock API cannot establish a prelease/cutover boundary for
   those seven names.

6. **No extra permission question.** The task/orchestrator instructions already
   authorize routine OPS source/API review work; no new approval prerequisite
   is stated. That authority is for this read-only analysis and a future
   narrowly reviewed source/fixture seam, not for live deletion, retry, host
   operation, or bypassing the existing guards.

## Smallest next owner action

Runtime should add and independently review one narrow registration-only
transaction seam/private fixture (not legacy adoption): under the existing store
mutex and pending-journal rules, accept the seven exact names plus expected
suite/env bytes, verify the exact current baseline and target hashes, remove
only those seven rows/env files, and prove byte equality for outside/current
inputs and all seven legacy runtime paths. The seam must expose a one-time
prelease/cutover check using the lifecycle's flock model; it must not scan
`/proc`, adopt the seven paths as managed entries, evict them, or authorize a
live operation. Keep the proposal's current STOPPED/NO-GO status until that
source/fixture proof and the already-required guarded owner run exist.

## Checks run

- `sha256sum .../handoff-ap2-OPS-retired-registrations-1841.patch` — PASS,
  `5984d485a2840c780c00a6461e3d6cb98462cef21428e8a9bbc233d18bf18b6a`.
- `sha256sum .../orch/bin/bench_store.py` — PASS,
  `6d9368207947aa316e1ed6486c5fa7ef843a84f50163114bb958011b538712a8`.
- Read-only AST/source check — PASS: seven suite deletions, seven env-file
  deletions, no public retire/adopt/migrate/unregister method; installed public
  methods are `initialize`, `recover`, `ensure`, `registered`,
  `registration_entries`, `names_for_suite`, `acquire`, and `run`.
- `git diff --check` and `git status --short` on assigned Runtime worktree —
  PASS/clean.

No product source, tests, generated files, configuration, stores, benches,
leases, processes, or host state were modified. No full suite or live operation
was run. Prior guard/FS refusals remain STOPPED.
