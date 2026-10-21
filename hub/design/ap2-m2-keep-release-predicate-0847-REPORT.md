# App2 KEEP / lease inventory — 2026-10-21

Scope was read-only inventory and own-finished-scratch eligibility. No App code,
tests, `.git`, shared dependency, source/evidence file, lease, KEEP marker,
worktree, or `/tmp` copy was changed.

## Authority and live state

- Authoritative App ref: `hub/tl/integration`
  `32b74fdea165816226b6f0727a16817a6a1a79c3`, tree
  `a3ddc2997e6460bab77d1e4ef7c1ac98ee21ad65`.
- Final live App2 worker markers: `ap2-m2-keep-release-predicate-0847`,
  `ap2-m2-producer-retained-diagnostic-once-0846`,
  `ap2-m2-transcript-text-decision-consumer-fit-0847`, and
  `ap2-m2-parent-projection-original-proof-freeze-0849`.
  The latter is the current parent source consumer, based on
  `tl/ap2-m2-parent-reviewed-projection-delivery-0844` (`b1e3547e4`).
- Final active central test: `ap2-m2-producer-retained-diagnostic-once-0846`
  run `ap2-m2-producer-retention-recover-review-0838-run-b7c6f480`, status
  `running`, snapshot key `acb9155ec7d74cc0d2fcd6c10d09f83d`, source tree
  `c1ac3383624322ae8d67b10dee36965670d91cd7`, worktree
  `/home/user/work/wt/ap2-m2-producer-retained-diagnostic-once-0846`.
- Its exact suite predicate is `tests/suites.conf:156`: it checks keeper
  `ap2-m2-producer-helper-expect-import-0717` at HEAD
  `6b0267c62aa8773132f1496d5014279e6c1edf61`, tree
  `c1ac3383624322ae8d67b10dee36965670d91cd7`, clean status, KEEP marker,
  shared `node_modules` link, wrapper SHA
  `b7c6f4806c02d8315b3eb69c4b4c469e7b908375603a5a0c967df5bbae60efb9`, and
  a nonblocking browser lock. This is an active source/graph/process
  dependency, not releasable.
- No local process other than this worker’s Codex/shell had a relevant App2
  keeper, `/tmp/ap2-*`, or producer-retention cwd/argv. The active test is run
  by the external central service; its `running` record and snapshot are the
  live references.

## KEEP worktrees and detached App pins

All rows below were checked with `git status`, `HEAD`, `HEAD^{tree}`, and
`git merge-base --is-ancestor HEAD hub/tl/integration`. Every row was clean and
returned `ancestor=no`; none meets the release predicate. Existing KEEP markers
and source authority remain in force.

| keeper | HEAD / tree | compact KEEP reason / exact blocker |
|---|---|---|
| `ap2-m2-parent-complete-current-proof-source-0455` | `a304dce02a185a4774ff514d5aa451c9702aa46f` / `a3c82aa91f1336b86491191acf857d88c56179b2` | Parent proof source; detached work is ahead of and not an ancestor of current integration. |
| `ap2-m2-parent-newborn-current-proof-source-0748` | `af1605a28f31a53b5a3472251493d44941b618fe` / `b0cb1f973c0e1b465241ebef38bd267fd39f0434` | Current newborn/source packet named by App2 status and parent `0849`; non-ancestor. |
| `ap2-m2-parent404-current-envelope-exact-source-0556` | `86f765532d25181a1f3e953fb08f79587d328f85` / `5f1d1d06432350eacbdd3d37ae8956b9fe2f756b` | Exact parent-404 envelope source; non-ancestor. |
| `ap2-m2-parent404-door-body-exact-correction-0604` | `acb582c2c3b08481d43853b8526894ac60d074bc` / `141724b56736be40a269f60aa8bfc060914ebd29` | Current corrected parent-404 body material; non-ancestor. |
| `ap2-m2-producer-final-external-hash-binding-0416` | `97187ce3c1576559239f869067a9cef8ffb5f357` / `4acab858b0f12a1878fc231a33f3d06af9b0bdc0` | Explicit `producer-exact-source-keeper.lease`; exact producer source/tool chain. |
| `ap2-m2-producer-frozen-delta-luna-resume-0453` | `17d2518c341c47a2d8634047b400399886da3a2a` / `d63fe4f1e1f32a01acfc9d11cda6c29066fce162` | Frozen producer diagnosis/source chain; non-ancestor. |
| `ap2-m2-producer-helper-expect-import-0717` | `6b0267c62aa8773132f1496d5014279e6c1edf61` / `c1ac3383624322ae8d67b10dee36965670d91cd7` | `KEEP` + `SOURCE_LEASE`; directly required by active central run and suites predicate. |
| `ap2-m2-producer-physical-keeper-startup-preflight-0545` | `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` / `fd16d32fd3487e56c9fe1ff16582dba240f63b77` | Producer startup/keeper source used by exact suite wrapper predicates; non-ancestor. |
| `ap2-m2-producer-realm-physical-path-diagnosis-0538` | `b8cc7e1c79ec5516b9eee3832b5c33d62dac1aa7` / `fd16d32fd3487e56c9fe1ff16582dba240f63b77` | Producer diagnosis source and retained wrapper ancestry; non-ancestor. |
| `ap2-m2-selected-actual-path-four-custody-fixes-0707` | `ba02c8f246ec61cd65d178a1ada686788df3fdab` / `7fe8c15b56da9944ae31e8273d41d3ceb21b3677` | Selected actual/source custody packet; non-ancestor. |
| `ap2-m2-selected-final95-owned-driver-source-0658` | `ba02c8f246ec61cd65d178a1ada686788df3fdab` / `7fe8c15b56da9944ae31e8273d41d3ceb21b3677` | Selected final95 driver source; same protected identity as `0707`. |
| `ap2-m2-selected-normal-dev-frozen-source-0651` | `ba02c8f246ec61cd65d178a1ada686788df3fdab` / `7fe8c15b56da9944ae31e8273d41d3ceb21b3677` | Exact selected suite source and status-named `ba02` keeper; non-ancestor. |
| `app-pin-25155ccb` | `25155ccb22728780a3ecd6379a929cad75cc1400` / `972d2ed2e4f85f334eb9f2e6ca40d9bfbce9eac7` | Detached frozen parent App pin with KEEP; no active queue/test direct reference found, but no release authority and non-ancestor. |
| `app-pin-7fafee1f` | `7fafee1f67aa7b42e3997d2c30b4ee8e1bad42c5` / `9d5ba429c703da57203e01d13e5a5fe4cc7ee014` | Detached frozen producer short-alias App pin with KEEP; no active queue/test direct reference found, but no release authority and non-ancestor. |

The parent, selected, producer keepers, and the `0822` producer wrapper/tool
artifacts remain protected. The manager leases also explicitly retain:

- `workers/ap2-m2-producer-final-external-hash-binding-0416` while the exact
  producer command/preflight is reviewed;
- `workers/ap2-m2-public13-effective-build-attachment-fix/public13-integration-runner.sh`,
  `workers/ap2-m2-locked-app-test-graph/artifacts/app-ap2-m2-locked-graph`,
  and its `app-ap2-m2-locked-graph-source.tar` while the public13/locked graph
  runner is protected.

The historical terminal test snapshots for parent/producer/selected were not
treated as live; only the current `running` record above was used for active
test retention. No stale status-only release decision was made.

## Scratch, disk, and action

- Free space at final check: `13,912,342,528` bytes (about `12.96 GiB`; `14G`
  rounded by `df`).
- Normal App copies: `0` `/tmp/timeline-normal014-app.*` directories.
- Named private App2 temporary copies: `4`, all retained and not touched:
  `/tmp/ap2-afteranchor-agent.qb8qXO` (115M),
  `/tmp/ap2-afteranchor-parity.3WyoFF` (128K),
  `/tmp/ap2-m2-parent-complete-0455.kIk398` (1.8M), and
  `/tmp/ap2-m2-transcript-origin-0535-zCx7Rc` (4.0K).
- App2 worktrees: `17`; worker-record private/scratch directories matching
  the approved app/private naming patterns: `4`. These are other workers’
  evidence, dependency/graph material, or leased/protected artifacts, not this
  worker’s finished scratch.
- This worker is still running and has no private App copy or finished scratch
  eligible for `compact-scratch`. No archive/hash-manifest comparison or
  recycle was therefore performed. No `bin/recycle`, `rm-own`, test, build,
  browser, install, or arbitrary `/tmp` cleanup was run.
- Manager action list: after the active run and all named wrapper/source/lease
  references end, recheck ancestry, active processes, queued/running tests,
  leases, and KEEP authority before using only the prescribed recycle/compact
  tools. Do not remove the four named temporary copies or any protected
  worktree in this report from this worker.

