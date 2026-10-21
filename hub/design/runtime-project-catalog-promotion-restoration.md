# Runtime project-catalog promotion restoration

Status: **PROPOSED / UNMERGED**. Worker `rt-m2-project-catalog-promotion-restore`, base `16acbb6ef94a6d8e226ccdc351ba0d96e0b09ea5`.

Owner14:32/14:34 and MANAGER-COMMON film-vs-catalog precedent authorize the existing project-scoped catalog operation. This changes no Agent command, schema, DTO, client, endpoint, table, journal, release or pin.

## Agent preservation source mapping (staged)

The Agent-side preservation repair is tests-only in
`tests/stage1/test_runtime_client_cutover.py`, against the compatible Runtime
checkout `b92d3e7a05eec65c142294ef4873edd059e9b31d` with the vendored/public
Runtime source pin `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`. The central
snapshot for this repair is Agent tree `63cb7d427685f6a4859f9d6dbe4b2c5028fa59a4`.

| Ledger row | Existing test mapping | Preserved boundary |
|---|---|---|
| AG-CATALOG-PROMOTION / AG-CUTOVER-04 | `test_promote_candidate_receipt_replay_and_foreign_provenance_rejection` | Kept catalog promotion success, fixed-point invalidation, exact receipt/result, replay, foreign provenance refusal, and restart replay. |
| AG-CUTOVER-01 | `test_documented_project_cli_mutations_return_committed_receipts` | Kept unplaced catalog create/add/reorder success and receipt/result equality. |
| AG-CUTOVER-02 | `test_project_shot_scope_stays_with_project_route` | Kept project isolation and unplaced lifecycle success; film-owned writes refuse without mutation. |
| AG-CUTOVER-03 | `test_editor_domain_reads_and_media_relations_use_generated_operations` | Kept catalog reads, stale-version conflict, and unplaced lifecycle success; film-owned writes refuse without mutation. |
| AG-CUTOVER-05 | `test_shot_items_and_reference_associations_use_versioned_routes_and_survive_restart` | Kept catalog CRUD/version/replay/restart and reference receipt assertions; film-owned item/lifecycle writers refuse with unchanged SQL/state. |

`_seed_shot` uses the existing trusted acceptance fixture boundary only to make
film-owned refusal cases reachable; it does not stand in for a product writer,
accepted history, or catalog promotion. The deletion ledger remains staged
until this source is merged and independently reviewed.

## Implementation and authority

Restored Main `29d0954b6d78a7d7937d81bc36567b6dee7ca976`'s `RuntimeService.promote_project_shot_candidate` body unchanged, and `RealmStore.promote_shot_items`. Restored only the two catalog revision helpers the operation needs (one unused Main local assignment removed). The existing shot-scoped internal revision identity is Main's retained child representation; no timeline row or film history is invented. The unused store RetiredRouteError import is removed. Other direct shot/item/text writers remain refused.

The normal operation retains project identity/ownership, exact candidate identity, version CAS, metadata/recipe/provenance/output identity verification, managed object ownership and actual CAS bytes, primary/superseded changes and version advancement in the same durable transaction, transitive plate/proxy/timeline-asset invalidation as a receipt RESULT, and receipt-first exact retry. Catalog revisions/head may advance; existing immutable shot/internal/parent images and accepted film heads/history are not rewritten. Timeline placement/selection/content still require EditCommands.

A real overwrite case exists: an accepted occurrence pin or authenticated historical materialization slot previously authorized a new physical projection even after a catalog promotion advanced that global head. `_check_shot_destinations` now joins the existing current/historical owner proof to the exact current `shot_revision_heads` revision before allowing a new image. Exact immutable reuse never enters this write guard. The historical proof accepts the same physical owner as well as a remapped owner: this preserves normal exclusive move → restore → move, which the old blanket current-membership allowance permitted. A newer catalog head has no matching accepted owner edge and refuses visibly (`destination_occupied`) before persistence. No name/namespace guess, new provenance state, or side journal.

## Tests and setup

The two original generated-client HTTP tests have their strict xfails removed. Only setup changes: the existing `_apply_published_shot_projection` helper bootstraps the original catalog items in each private ephemeral realm because createShot/addItem remain retired. There is no positive SQL fixture, fake provider or synthesized accepted history. Every original assertion is retained: 7 in the atomic/fixed-point/receipt/replay/stale test and 2 in the provenance test (AST comparison confirmed).

Added one corrupted-CAS/receipt-failure rollback control, one exact catalog/accepted-film immutability plus restart/receipt-first control, and one real-provider move/promotion/historical-reuse/overwrite-refusal control. The latter derives its occurrence-owned target from the accepted document; the normal fixture uses an exclusive owner with the same physical shot ID. The separate library shot is explicitly absent from the occurrence closure. There is no silent promotion retargeting and no use of ordinary014 or a private generated cohort. Existing host and real shared-slot/C4 controls are run as neighbors; the new native control does not claim a newly generated shared-slot fixture.

Promotion-specific retirement parameter cases are removed from the retired-writer group under the owner ruling; normal promotion positives replace that classification. Same-primary now has the normal 422 control; auth/read-only/foreign-project assertions still include promotion, and direct-store stale rollback remains covered. No remaining retired CRUD refusal is relaxed.

## Verification

All central requests snapshot source tree `67f0f65ff6df9595b452f23c2c0fbbf262898cee`. No full suite requested.

Central commands (O is `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch`):

```sh
$O/bin/request-test rt-m2-project-catalog-promotion-restore targeted --files "tests/test_shot_candidate_promotion.py tests/test_project_reference_catalog.py tests/test_timeline_shot_authority.py tests/test_timeline_commit_closure_invariants.py tests/test_timeline_projection_occupancy.py"
$O/bin/request-test rt-m2-project-catalog-promotion-restore occupancy-integration --files "tests/test_shot_candidate_promotion.py tests/test_timeline_projection_occupancy.py"
$O/bin/request-test rt-m2-project-catalog-promotion-restore commit-integration
$O/bin/request-test rt-m2-project-catalog-promotion-restore restore-integration --files "tests/test_project_reference_catalog.py"
```

Results (all exact tree above, no source changes after requests):

| Request ID suffix | Result | Qualification |
|---|---|---|
| targeted-1020144341-17230 | exit1; **156 passed, 3 deselected, 34 setup errors** | Both original HTTP positives, rollback and authority/C4 host neighbors pass. All 34 errors are the existing catalog fixture's missing ASTRID_CHECKOUT (`/home/user/work/wt/astrid` unavailable), not assertion failures. |
| occupancy-integration-1020144341-27357 | exit0; **3 passed, 20 deselected** | Both new normal-provider controls plus the existing real shared-slot rematerialization control. |
| commit-integration-1020144342-12993 | exit0; **9 passed** | Requested real-provider commit lane. |
| restore-integration-1020144538-23227 | exit0; **35 passed** | Complete bounded catalog neighbor file in its existing Agent-aware environment; resolves all 34 setup errors above and includes its accepted-film immutability control. |

`wait-test` was run against each of those exact IDs and returned the statuses above. The three named integration requests record external Agent `130b4937856872b7abac35128cdf66222cf67165`, App `41fff23a29f13bd9aede6343592ffba8adebe1a3`, Composition `5a4e9b72f1916c4da01fa370ec5fe8d46b6da8e8`. Local native controls initially ran with Agent `acc17162dd57b2cafc966098e44625ea25bfe461`. These are existing normal startup providers, with no private generation or pin changes by this worker.

The catalog follow-up selects the existing Agent-aware environment because neutral targeted lacks ASTRID_CHECKOUT, required by those existing catalog fixtures. No suite was skipped or weakened to resolve the environment. No remaining task blocker.

Direct checks, from the worker root:

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider -m integration tests/test_shot_candidate_promotion.py
# 2 passed, 2 deselected (before adding the third non-integration rollback control).
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider tests/test_shot_candidate_promotion.py::test_catalog_promotion_checks_bytes_and_rolls_back_before_receipt
# 1 passed.
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider tests/test_timeline_shot_authority.py -k 'not http and not historical_text' tests/test_timeline_projection_occupancy.py
# 65 passed, 77 deselected; final product source.
PYTHONDONTWRITEBYTECODE=1 ASTRID_CHECKOUT=/home/user/work/agent PYTHONPATH=$PWD:/home/user/work/agent /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider tests/test_project_reference_catalog.py::test_catalog_stale_version_refuses_atomically
# 8 passed; confirms Agent-aware fixture environment before central catalog follow-up.
/home/user/work/venv-agent/bin/ruff check --no-cache --select F runtime_protocol/timeline_commit_store.py tests/test_shot_candidate_promotion.py tests/test_timeline_shot_authority.py
git diff --check
# Both pass.
```

An earlier pre-final guard run of authority/C4/occupancy was 76 passed / 77 deselected. Ruff across service/store also reports exactly the seven pre-existing F issues (2 service, 5 store); checked against 16acbb6 with the same --select F command. The one newly ported unused Main local was removed; no new F issue remains. Shared dependencies/caches were not changed; direct pytest uses -B/no cacheprovider and ruff uses --no-cache.

## Exact size and next step

Physical product line counts for the three changed authored paths (includes blanks/comments, excludes tests/generated code):

| Path | Main29d0954 | Base16acbb6 | Proposed | Task delta |
|---|---:|---:|---:|---:|
| runtime_protocol/service.py | 8,880 | 8,063 | 8,198 | +135 |
| runtime_protocol/store.py | 6,544 | 6,814 | 6,826 | +12 |
| runtime_protocol/timeline_commit_store.py | absent | 995 | 1,008 | +13 |
| Total changed paths | 15,424 | 15,872 | 16,032 | **+160** |

Diff product additions/deletions: **167 / 7**; net **+160**. Main restoration is +147 net, prewrite proof +13 net. This is this task's exact changed-path count, not an updated whole Runtime timeline-core census. Test net +131 lines; the promotion test file is 207 lines; no new large fixture/file.

Next: manager reviews the bounded existing-operation restoration and prewrite proof, merges if approved, and updates RT02/RK02 from PROPOSED. Manager batches the post-merge full suite. No merge, push, pin, publication or release performed. Unrelated retired positive replacements remain open; no global writer-migration completion claim.
