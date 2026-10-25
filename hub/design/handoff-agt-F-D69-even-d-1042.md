# D69 independent READ ONLY semantic review — even-d

Status: **COMPLETE ASSIGNED SUBSET; NOT WHOLE-AUDIT PASS**.

Assignment used the corrected EVEN `function_index` membership from
`handoff-agt-F-D69-residual-even-0945.json`: immutable indexes **98, 104, 112,
114, 124**. These are five disjoint function scopes. Complete old `08e6b905`,
captured-new `d6294843`, and current-normal `d0ecf1d` test sources were inspected;
all five current-normal file blobs and function body hashes exactly equal the
captured-new sources. The residual membership contains 13 units: 5 removed and
8 added. The unchanged `len(writer.calls) == 1` assertion in index 114 is not a
residual unit.

Subset result: **0 PASS, 13 equivalent-approved, 0 FAIL, 0 UNRESOLVED**. No
whole-audit PASS is claimed. Global whole129/113/287 conservation and other
reviewer ownership remain unchanged.

## Per-function decisions

### Index 98 — vendored client root-lock artifact

Function source: `tests/stage1/test_vendored_workspace_client_parity_luna.py`
`test_vendored_client_is_the_locked_runtime_artifact`.

- Source: old blob `1b641d4697e6cf0655c57e5f9c0f2915c01c3269`, body SHA
  `086f93e72b6f1a726d4e3182872049191b8fb8455604769193d72f1c225028c1`, lines
  41–45. Current/captured blob `81b3bc78b8eee65e146a6ac5d16ca3d0560a0a60`,
  body SHA `8140b0575ed75ad7ecdb6535e4379bea6e40147b11e2588312bf0915599f9319`,
  lines 50–55.
- Removed line 43: the locked `astrid_runtime_client/` set was exactly
  `__init__.py`, `generated.py`, and `contract_metadata.py`.
- Added line 52: the exact set additionally requires
  `timeline_commit_types.py`.
- Decision: **equivalent-approved** for both units. The current set strictly
  contains every old member. The generated timeline commit DTO module is the
  approved C0/R0/U4a client surface; current `runtime.lock.json` contains the
  path and `scripts/vendor_lock.py:check` still validates every locked byte.
  No old lock guard is removed.
- Mounted caller: test loader → `scripts/vendor_lock.py:check` and
  `runtime.lock.json`; this is an artifact-boundary predicate, not lexical
  evidence.

### Index 104 — reconciled capability ledger count

Function source: `tests/test_capability_ledger.py`
`test_host_consumes_the_reconciled_ledger_before_readiness_matrix`.

- Source: old blob `5d17a5255578da567d9e86d85a5fb7a7881221b0`, body SHA
  `251db7762bb8c274131d3ad8e9b94f3808801406acf2537027c13b6347604f63`, lines
  55–67. Current/captured blob `51db423220d8a3f06224ec5ce8f1e1348bcd7d7a`,
  body SHA `7ca2c7eff8634d003a062fab1bcaa8faaa47e514fa8039541381ddfc94072c96`,
  lines 55–67.
- Removed line 59: `host.ledger["sources"]["counts"]["pack_labels"] == 107`.
- Added line 59: the same predicate with count `108`.
- Decision: **equivalent-approved** for both units. `GenericPackHost.__init__`
  still loads the reconciled ledger before the matrix. Commit `a521535cc5`
  explicitly admitted `music.duck` and changed the approved count from 107 to
  108; `_reconcile_sources` still derives the count as `len(labels)`. The set
  equality, matrix cardinality, CPU finalizer, and resource-key predicates are
  unchanged. This is an approved current-source count update, not a missing
  ledger behavior.
- Mounted caller: `GenericPackHost.__init__:5545` →
  `load_capability_ledger` → `_reconcile_sources:484–507`.

### Index 112 — one-root Runtime lock coverage

Function source: `tests/test_vendor_lock.py`
`test_one_root_lock_covers_all_known_runtime_paths`.

- Source: old blob `f18124eb4034f2d03b775c043697e2f02237f61a`, body SHA
  `09a0a16c2026231b223a08486b49732d657ed9f05c23c7b67fa0e6e7b5693249`, lines
  62–82. Current/captured blob `0625ca400664dacf633c5edc77352e24c909c0a6`,
  body SHA `8c7f22cb2e42bbb749b14c50c57e834c6d8b36ab02c234717926c17dbfc46d65`,
  lines 62–83.
- Removed line 76: `len(bundle["files"]) == 14`.
- Added line 77: `len(bundle["files"]) == 15`; the same expected set now also
  contains `astrid_runtime_client/timeline_commit_types.py` at line 67.
- Decision: **equivalent-approved** for both residual units. The old 14 paths
  remain in the exact set, and the fifteenth path is the approved generated
  commit DTO artifact. Source-commit format, no nested lock, and
  `vendor_lock.check(LOCK) == []` guards remain.
- Mounted caller: the test reads the single root `runtime.lock.json`; the
  production checker is `scripts/vendor_lock.py:check`.

### Index 114 — group move through the canonical commit boundary

Function source: `tests/timeline/test_authoring_bundle.py`
`test_group_move_compiles_and_uses_existing_publication_boundary`.

- Source: old blob `c6084c424890fba59f2786439ad492efaff789d8`, body SHA
  `d83f2fc3c211a246c537ceb37f82c7bb892919187fbd8ccd38e08450dddb60a2`, lines
  382–398. Current/captured blob `4e4c9e61cd94707b3ec7d03f7ad1b862511a9275`,
  body SHA `be11c72526b3b908ab2d7970af63bbd3a496fcbbec1289fa06d09b10837219a0`,
  lines 777–799.
- Removed line 398: `result["publication"]["data"]["new_head"] ==
  writer.calls[0][2]["parent_revision_id"]`.
- Added line 796: `request["base_revision_id"] == "parent-1"`.
- Added line 797: `request["merge"] == "atomic"`.
- Added line 798: `all(command["op"] == "doc.patch" for command in
  request["commands"])`.
- Added line 799: `result["publication"]["new_head"] == "saved-revision"`.
- Decision: **equivalent-approved** for all five residual units. The removed
  predicate was tied to the retired parent-publication response shape, where
  `new_head` was compared to the request's parent revision. D72/C0 approve the
  registered `commitTimeline` boundary: the request carries the exact base
  revision, uses atomic merge, and the group reorder is emitted as guarded
  `doc.patch` commands; the accepted response's new head is the landing
  `saved-revision`. The unchanged one-call assertion still preserves one
  publication boundary but is not counted as a changed unit.
- Mounted caller: `publish_authoring_candidate:1883–1889` →
  `astrid/sdk/timeline/authoring_commit.py:authoring_commit_request:84–187` →
  `writer.commit_timeline`; Runtime validates the canonical operation and the
  Agent provider is registered by `create_runtime_commit_service`.

### Index 124 — navigation editing recipe

Function source: `tests/v10/test_domain_cli_projects_timelines.py`
`test_timeline_navigation_preserves_resolved_scope_and_editing_resources`.

- Source: old blob `06cee01d85e448208e396b690983878b429c2f85`, body SHA
  `ca81ad971f73235bac11f0e01cfc507ea450c99fa3f3e42b2f93bbf4c9154771`, lines
  1103–1140. Current/captured blob `a54c3b729fcb3a8aa7b3578891a64ec8f264997d`,
  body SHA `cf06962b96de33917e4be42049790d1a1e653b8347c905b15925cc5790315054`,
  lines 1111–1148.
- Removed line 1126: workflow `checkout → edit → check → publish`.
- Added line 1134: workflow `checkout → edit → check → commit`.
- Decision: **equivalent-approved** for both units. G5 changes the displayed
  writer verb to the canonical `commit` route. Current `_editing_navigation`
  emits `check` and `commit`; `timeline_document.py` parses `commit` and keeps
  `publish` only as a compatibility alias. Resolved project/timeline/revision,
  guide/script paths, and the check command remain conserved.
- Mounted caller: `_show_navigation_help` and
  `_visualization_navigation_help` → `_editing_navigation:1218–1230` →
  `timeline_document.py` `TimelineSession.commit_many:327–332` with exact base
  pins and `merge="atomic"`.

## Static checks and boundaries

- Membership JSON, runtime lock JSON, and capability config JSON parsed: PASS.
- Old and current target files were AST-parsed statically: PASS. No product
  imports, test collection, helper/body execution, services, or live sockets.
- `git diff --check` on Composition and the read-only Agent worktree: PASS.
- Tests, typecheck, and lint: **N/A by the read-only brief**.
- No product, test, generated, pin, registry, ledger, foreign-output, or
  source file was modified. Detailed machine-readable evidence is in
  `workers/agt-F-D69-even-d-1042/evidence/source-checks.json` and `.txt`.

