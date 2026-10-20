# Agent ordinary014 current-preserving consumer stage

Status: **PRIVATE consumer descendant staged; not merged, published, activated,
or promoted to the integration pin.**

## Exact source and pin

- Base: current `tl/integration` Agent `81873ccf270e1c099c9f76b86103ccf3c9275cf4`.
- Reviewed ordinary source join: clean three-way result of current base and
  approved `ee896821b502ee4e51211b19d064fa44915f5777` ordinary source; its
  source delta is 61 paths and matches merge tree
  `2ca6b5f18ae3abf47063c05529dcf9541106b52c2` byte-for-byte.
- Frozen ordinary source/schema basis: Agent `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`.
- Raw command schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
  55 definitions / 29 operations.
- Runtime producer checkout: `/home/user/work/wt/rt-pin-a0dca169`, verified
  `HEAD a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree
  `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- Runtime package: `0.2.14` (unpublished).
- Runtime wire schema: `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.
- Immutable artifact version: `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`.
- `runtime.lock.json` was updated with the normal `vendor_lock.py update` and
  `check` procedure; all locked consumer bytes match the producer manifest.
- Prospective worktree tree (computed without staging):
  `56b637351f2499a15a31ad09f572cb6de05a0e8d`.
  Commit SHA is pending the required harness commit; this worker did not run
  commit/merge/rebase/checkout.

## Current-source preservation inventory

The 61-path ordinary join was applied on top of current integration; no old
snapshot replaced the current tree. The only additional changed paths are the
five normal consumer-pin files: the four generated Python client modules and
`runtime.lock.json`.

Current preservation files remain byte-identical to base `81873ccf`:

- restore facade/session: `astrid/sdk/timeline/sync.py` (including
  `TimelineSession.restore`);
- retry/error custody: `astrid/sdk/workspace_client.py` and
  `astrid/core/execution/generic_host.py`;
- canonical read/verified-source images: `astrid/sdk/timeline_filmstrip.py`
  and `astrid/core/rendering/verified_source.py`;
- D10 source removals and current rendering boundaries;
- extracted filmstrip cache: `astrid/packs/rendering/actions/timeline_visualize/_filmstrip_cache.py`;
- sheet/cut owner and current Gate3 assertions:
  `astrid/sdk/timeline_sheet.py`,
  `tests/sdk/test_timeline_checkout_facade.py`, and
  `tests/sdk/test_timeline_checkout_history_boundaries.py`.

No private 392/materialization/group/transition/opacity/provenance source was
added. The source allowlist contains no such paths.

## Evidence

- `scripts/vendor_lock.py check runtime.lock.json --producer /home/user/work/wt/rt-pin-a0dca169`:
  passed.
- Static producer-byte/schema/registry/restore checks and `git diff --check`:
  passed.
- Pin/schema/registry suite (`tests/test_vendor_lock.py`, vendored-client
  parity, current union schema): **63 passed in 170.72s**.
- Direct ordinary pure source plus facade/history suite: **350 passed, 54
  skipped in 33.31s**.
- Sheet, restore recovery, accepted history, and publication retry suite:
  **165 passed, 9 skipped in 13.66s**.
- No full/full-* suite, socket/browser journey, registered-render repeat, or
  health override was run.

## Runtime follow-up request

Runtime/App2: please provide the exact current-compatible ordinary014 server
commit/tree and the one exact previously failed hold-clear parent/restore node
selector before any live-node retry. The current server/hold-clear handoff was
not supplied in this worker turn, so those nodes remain unrun and unclaimed.

