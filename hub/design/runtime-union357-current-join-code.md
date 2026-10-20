# Runtime union357 current source join

Date: 2026-10-20T17:16:51Z (`date -u`).
Status: **source-stage implementation complete; normal generation and native qualification HELD**.

## Exact sources and scope

- Assigned Runtime base: `7d1cfa6b1da0c50bb8a9d3430dcaa6272b20b55e`.
- Reviewed carrier product source: `a18022d765859135fb24deadaf885ce2eed83ea9`.
- Final central snapshot tree: `331c5922ee45265751f55e4f0371482888bd0e55`.
  No repository source changed after that snapshot. The harness supplies the
  eventual commit SHA; none is invented here.
- Intended Agent counterpart: `357230816c86da65d5f8cc92b10a3a90d29874e0`,
  actual Git tree `94692ec85167d5c606626c4ec678fe2a63ee0aa6`.
  Direct `git show` verifies schema SHA-256
  `613123b2760150f9f33e23485516d757359c3eaebfe02d552bc97155309aaad3`,
  55 definitions / 29 operation clauses / reviewed 13 v2-capable operations.
  The earlier Runtime review's tree ending `aa5` is a documentation error;
  the committed 357 tree ends `aa6`.

Six paths change, all within the existing reviewed 17-path allowlist:

- `runtime_protocol/timeline_commit_port.py`: add the private source join,
  closed-port refusal and exact sealed-request binding comparison. Only
  `validate` and `_prepared` change among existing methods; all other methods
  are AST-identical to 7d1. Raw `media_info`, declared/exact-BASE pin authority,
  request memo, acceptance revalidation, selected-media CAS verification and
  single-descriptor WAV verification/parsing remain current.
- `runtime_protocol/timeline_commit_store.py`: apply only the reviewed carrier
  diff to 7d1. The result is byte-identical to a180's store, including its
  project-scoped catalog-head fences at current, inverse-source and accepted
  historical ownership sites. Authenticated source/owner/item joins, same-slot
  reuse, global current/retained item occupancy, semantic creation reservations,
  inherited inverse provenance and ledger-first accepted replay are preserved.
- `runtime_protocol/timeline_materialization.py`: the unchanged reviewed
  183-line pure join helper, byte-identical to a180.
- Three retained test files: materialization join, authority review and
  projection ownership. Added seven source-stage cases explicitly prove held
  schema admission and all three catalog-head fence sites without schema
  substitution or native-provider claims.

Product delta: **440 additions / 59 deletions**, net **381 lines**.
No service, route, DTO, table, framework, ID allocation policy, generated client,
schema, manifest, public fixture or version changes. No scene/read bypass.

## Current-tree preservation

An exhaustive SHA-256 comparison against 7d1 finds **416 tracked paths outside
that 17-path allowlist, zero mismatches**. All **254 existing tracked test and
fixture paths** are byte-identical to 7d1, including raw BASE/single-FD tests,
CAS tests, current C4/catalog/metadata tests, historical render retry and strict
parent swap coverage. No existing assertion was removed or changed; no new
xfail, skip or weakened expectation was added.

Inventory, including every compared outside blob:
`workers/rt-m2-union357-current-join-code/source-inventory.json`.

The current generated artifacts are unchanged:

| Artifact | SHA-256 |
| --- | --- |
| `contract/schemas/edit-command.json` | `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d` |
| `runtime_protocol/schemas/timeline-commit-bundle.json` | `6d707cb84a232f6ecd7e17c09c8722a379bb76b6a9d2869efea691d6bd8366e3` |
| `contract/artifacts.json` | `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815` |

This remains ordinary schema 14. New v2 commands and typed item-created claims
are refused before execution. Pure/private helper proofs do not override that
wire gate. The old private f802/48/22 artifacts, compatibility helper changes,
generated clients and manifests were not imported. Normal generation was not
run, including no generator-based version mutation.

The old private-only positive tests
`test_complete_captured_join_previews_original_map_without_writes` and
`test_current_typed_item_creation_claim_is_accepted_and_reserved` were not
imported into this source-only stage: their positive admission requires the
held normal schema generation. Their passing expectations were not rewritten
to refusals or marked xfail. The original current 7d1 suite is fully retained.
The prior continuation/native tests are not substituted for a new 357 pair.

## Exact tests and results

Working directory for every direct command:
`/home/user/work/wt/rt-m2-union357-current-join-code`.
Shared dependencies remained read-only; direct pytest disabled bytecode and
cacheprovider and used private `/tmp` basetemps.

Final focused source-stage lane:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-union357-final-focused tests/test_timeline_materialization_join.py tests/test_timeline_materialization_authority_review.py tests/test_timeline_projection_ownership.py
```

**199 passed, 3 deselected in 73.06s**, exit 0. The three deselected tests are
retained actual-provider integration tests, intentionally held here.
An earlier run before adding seven stage controls was **192 passed, 3
deselected**; do not add overlapping counts. The five added join/catalog tests
also passed independently (**5 passed**), and the door pre-provider v2/typed
controls passed independently (**2 passed**); these are included in 199.

Retained raw/ordinary acceptance neighbors (final product code):

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-union357-raw tests/test_timeline_raw_audio_port.py tests/test_timeline_projection_occupancy.py tests/test_timeline_commit_acceptance.py tests/test_timeline_current_union_contract.py
```

**148 passed, 2 deselected in 29.21s**, exit 0. Includes exact-BASE pin denial,
WAV descriptor rename/in-place race controls, raw tamper refusal, ledger-first
raw retry, ordinary14 union contracts and immutable/projection acceptance.

Central socket-capable neighbor lane:

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test rt-m2-union357-current-join-code targeted --files "tests/test_door_transport.py tests/test_timeline_commit_port.py tests/test_timeline_clip_replacement.py tests/test_shot_candidate_promotion.py tests/test_timeline_commit_closure_invariants.py"
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test rt-m2-union357-current-join-code-targeted-1020171519-10996 1
```

**65 passed, 16 deselected, 10 xfailed in 57.75s**, exit 0, exact final tree
`331c5922ee45265751f55e4f0371482888bd0e55`. All ten xfails are the unchanged
D04 direct-replacement retirement baseline in `test_timeline_clip_replacement.py`;
none was introduced by this task. Central results:
`tests/rt-m2-union357-current-join-code-targeted-1020171519-10996/`.

```sh
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/ruff check --no-cache --select F runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_store.py runtime_protocol/timeline_materialization.py
# All checks passed.
git diff --check
# Passed.
```

No full suite, broad matrix, native pair, hand render, publication, integration
merge, public release/pin, or normal generation was run. Native public-v1 103/3,
obsolete-private-v1 draft/outbox behavior and dependent-B ACK identity are not
newly qualified by these detached/helper tests.

## Remaining minimal gates

No implementation blocker remains for this authorized source-only task.
The following are deliberate manager/orchestrator holds, not native approval:

1. Agent manager freezes/ACKs exact 357 (or names its exact committed successor)
   and Runtime/Agent review the harness's actual counterpart commit plus tree
   `331c5922...`. Owners settle the normal private generation/version decision.
   Prior 3730/f802 or 83fe/7b8 approval does not cover this pair.
2. Through the existing normal generation flow only, carry the complete
   613/55/29 schema plus the same 13 v2 operations into Runtime's command
   resource, bundle, generated clients/metadata and manifest. Retain syntactic
   v1 so durable accepted retries still reach the existing ledger. Run normal
   generator/manifest checks and existing compatibility/floor tests; restore
   the two retained private-admission positive tests verbatim at this step.
   No manual version override or old f802 artifacts.
3. Coordinate **ONE** central native pair on that exact generated Runtime and
   frozen Agent tuple. It must cover genuine public-v1 complete 103-read/
   3-selection behavior; accepted-v1 lost-ACK/restart exact retry before live
   guards, inverse/redo/history/restore; obsolete new-private-v1 visible refusal
   with exact draft/outbox preservation plus equivalent v2 success; source/
   owner/item binding, own-slot/sibling/current and retained global-item
   occupancy; all three catalog-head fences plus C4 immutable reuse; original
   dependent-B capture/ACK identity; retained ordinary14 parent-media/text/
   init/word/assembled-target operations and P1/F1 guards; raw exact-BASE,
   declared pin, single-FD and selected-media CAS safety. Use retained real
   provider tests and the Agent lifecycle suite; no caller-map authority,
   fabricated accepted rows or physical-allocation-as-birth shortcuts.

Public release, adoption and merge decisions stay with the orchestrator.
