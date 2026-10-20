# Runtime size census (tl/integration ef731cb vs origin/main 8c1830d)

Read-only. Counts = lines per `git grep -I -c ""` at each rev (blank lines included). Net = `git diff --numstat origin/main tl/integration`. Generated = generated clients/DTO copies, contract JSON/OpenAPI, bundled schema. Tests = `tests/` + `packages/typescript/test/` + conformance fixtures/responses.

## Table 1 — product lines by family

| Family | Lines now | vs main (main → now) | Net | Owner / ledger row |
|---|---:|---:|---:|---|
| Core service/store/server/daemon/door/auth/platform/upgrade/backup (`runtime_protocol/*`) | 25,399 | 25,878 → 25,399 | −479 | D04, RT01, RT02, RT04 (deleted bodies); RK01 KEEP (project catalog) |
| Timeline commit path + timeline read/inspection (`timeline_commit*`, `timeline_inspection`, `timeline_view`, `timeline_cutover`, `snapshot_refs`, `shot_dependencies`, `managed_render_snapshot`) | 5,380 | 1,872 → 5,380 | +3,508 | D04 / D13 (commit path, slim KEEP); RT03 held |
| Visual seam + capture (`visual_seam`, `visual_boundary`, `seam_intent`, `capture_validation`) | 930 | 779 → 930 | +151 | capture KEEP; seam evaluator serves See |
| Local/remote workers, execution, handoff (`local_*`, `remote_worker_*`, `verified_host_launch`) | 8,410 | 8,410 → 8,410 | 0 | main infrastructure (no R4 delta; no ledger row) |
| `astrid_runtime/` (custody, bootstrap, relocation, operator upgrade) | 6,189 | 6,189 → 6,189 | 0 | main infrastructure (no R4 delta) |
| `generators/` (codegen; incl. `timeline_commit_types.py` 196, `timeline_commit_resources.py` 74, `command_schema_compatibility.py` 116) | 2,231 | 1,697 → 2,231 | +534 | R4 additions; D13 family |
| `scripts/`, `tools/`, `conformance/` harness, hand-written `packages/` | 1,173 | 1,150 → 1,173 | +23 | main |
| **Product total** | **49,712** | **45,975 → 49,712** | **+3,737** | |
| Generated: `contract/` (OpenAPI, schemas, manifests, digests), `runtime_protocol/schemas/timeline-commit-bundle.json` (4,085), `contract_metadata.py`, `conformance/typescript/generated.ts` | 11,376 | 4,278 → 11,376 | +7,098 | R4 (timeline-commit schemas + bundle) |
| Generated clients + DTO copies (`packages/python/.../generated.py`, `timeline_commit_types.py`, `packages/typescript/src/generated.ts`, `timeline-commit-types.ts`, `runtime_protocol/timeline_commit_types.py`) | 1,994 | 1,730 → 1,994 | +264 | generated from generators |
| Tests + fixtures (`tests/`, `packages/typescript/test/`, `conformance/fixtures|responses`) | 68,990 | 45,725 → 68,990 | +23,265 | 88 new test files = 22.1k lines (4.5k of it `published-command-schemas` fixtures) |

Reading: the Runtime's **main baseline alone is ~46k product lines**; the ~20–26k end-state target in PLAN §3 cannot be met by Runtime cuts in this census (the worker/custody/platform bulk is main infrastructure the PLAN keeps). Either the target is for R4-added Runtime code only (then the number is ~3.7k net now, ~3.5k of it timeline commit path) or it is re-scoped. **Orchestrator decision needed on the measurement boundary.**

## Table 2 — largest files (product, now)

| File | Lines | Main | Note |
|---|---:|---:|---|
| `runtime_protocol/service.py` | 8,015 | ~8,880 | −865 net; retired stubs + commit wiring |
| `runtime_protocol/store.py` | 6,643 | ~6,540 | +103 net |
| `runtime_protocol/local_worker.py` | 1,968 | main | out of census scope (main infra) |
| `runtime_protocol/upgrade.py` | 1,919 | main | main infra |
| `astrid_runtime/custody_broker.py` | 1,678 | main | main infra |
| `runtime_protocol/local_execution_supervisor.py` | 1,668 | main | main infra |
| `runtime_protocol/timeline_commit_store.py` | 957 | new | commit persistence |
| `runtime_protocol/timeline_commit_port.py` | 856 | new | commit port/reads |
| `runtime_protocol/timeline_commit_inputs.py` | 751 | new | document inputs |
| `runtime_protocol/timeline_commit_baseline.py` | 443 | new | imported-baseline verifier |

## Top 10 deletion/simplification candidates (beyond D04, RT01–RT06, RK01, D13)

Estimates are product lines removed. "Guard" = existing test that pins the behaviour.

1. **Commit-path canonical-JSON helpers are duplicated.** `detached` in `timeline_commit_port.py:38-54` and `timeline_commit_store.py:25-41` is the same finite-check + deepcopy; `digest` in `port:34-35` and `store:44-45`; plus `timeline_commit_baseline._digest:51` and `timeline_commit_inputs.content_digest:150`. Keep one set in `timeline_commit_types`/`util`. **~35 lines, low risk.** Guard: `test_timeline_commit_port.py`, `test_timeline_commit_validation.py`, `test_timeline_commit_acceptance.py`.

2. **Three finite-JSON validators on the commit path.** `timeline_commit_validation._finite_json:13-38`, `timeline_commit_inputs._finite_json:130-148`, and the `finite` nested in (1). Collapse to one. **~30 lines, low risk.** Guard: `test_timeline_commit_validation.py`, `test_timeline_commit_inputs.py`. (Leave `server._validate_finite_json` alone; it guards HTTP body parsing.)

3. **Parent-clip reconciliation is written three times.** `visual_seam.parent_clips:78-84` (raises ConflictError), `timeline_inspection._canonical_parent_clips:393-404` (ConflictError, different message on the non-list branch), and inline in `store.py:1824-1829`. Consolidate to one helper, but preserve each caller's error class and details. **~15 lines, low-medium risk.** Guard: `test_timeline_inspection*`, `test_shot_composition_runtime.py`, the visual seam tests.

4. **PreparedCommit schema is validated twice per commit.** `timeline_commit_store._check_shot_destinations:563` runs `validate_prepared`, then `_validate:519` runs it again on the same object (preview and accept both call the preflight first, lines 636 and 678). Keep the preflight (its ordering is intentional, per the comment at 560-561) and drop the second call. **~6 lines plus one schema pass per commit, low risk.** Guard: `test_timeline_commit_validation.py`, `test_timeline_projection_occupancy.py`.

5. **Test-only wrapper and dead helper live in production.** `timeline_commit_inputs.persist_document_input:740-751` has one caller, `tests/test_timeline_commit_acceptance.py:103`; the production path uses `persist_document_input_links`. `document_input_schema_sql:125-128` has no caller at all. Move the wrapper into the test and delete the function. **~16 lines, low risk.** Guard: `test_timeline_commit_acceptance.py`, `test_timeline_commit_inputs.py`.

6. **Retired-route stubs are one-liner methods.** Seven direct-shot writer stubs, `service.py:3103-3169` (each a `@_durable_mutation` plus a `raise RetiredRouteError`), plus `promote_candidate = promote_project_shot_candidate` at `:3169` (no references anywhere). Replace with one table-driven refusal, keeping every 410 refusal and its test expectation (gate 6). **~35 lines, low-medium risk.** Guard: `test_timeline_shot_authority.py`, `test_timeline_legacy_authority.py`, `test_timeline_document_authority.py`.

7. **Imported-baseline verifier re-derives receipt chains.** `timeline_commit_baseline.py` `_publication_events:269`, `_verify:286-365`, and `verify_baseline:366`, with about 22 receipt-consistency assertions (lines 228-353). PLAN keeps ancestry and intervening-write checks, not a full receipt re-derivation. Cut to the ancestry check. **~60–100 lines, medium-high risk.** Guard: `test_timeline_commit_baseline.py` (503 lines), `test_timeline_commit_crash.py`. Needs an owner decision on whether any live project still needs baseline import.

8. **Seam evaluation inside the legacy save path.** `service.py:3002-3006` (publish, result at `:3084`) and `:1843`/`:1855` (compacted replay), plus `store.py:1801-1821` `admit_closure`. PLAN §3 cuts "scene evaluation inside the save path". The evaluator in `visual_seam.py` stays because See needs it. **~25 lines in service plus ~20 in store, held.** Blocked until D01: App still calls `composition-revisions` (`createDefaultTimeline.ts:50`, `dataProvider.ts:282,1008`), and `visual_seam_report` is a response field.

9. **Legacy version history is a second history beside the commit log.** `timeline_revisions` table (`canonical_schema.py:172`), `_record_timeline_revision:1580`, `_timeline_revision:1587`, `_record_legacy_timeline_revision:1378`, `_legacy_timeline_payload:1370`, `list_timeline_history:3366`, `diff_timeline:3383`, routes `server.py:637-640`. This contradicts decision 6 ("the Runtime holds the only accepted history"). **~90–110 lines, high risk, NOT cut-ready.** Agent SDK still exposes `diff_timeline` (`astrid/sdk/remote.py:1560`), and PLAN §1 Read keeps `history` and `diff`. Candidate only once those verbs are re-pointed at commit history.

10. **Read-only cutover audit is migration-only.** `timeline_cutover.py` (217 lines, main-era), reached only from `cli.py:183-197`. It audits legacy documents that D04 is retiring. Delete after D04 closes and the legacy documents are migrated. **~235 lines, low-medium risk.** Guard: `test_timeline_cutover.py`.

### Not in the top 10 (decisions, not cuts)
- **Published command-schema floor** (`generators/command_schema_compatibility.py` 116, `generate.py validate_command_schema` ~25, `tests/test_command_schema_compatibility.py` 251, fixtures `runtime-0.2.2` 729 / `withdrawn-10c` 889 / `producer-guard-1bffd` 1,510 / `runtime-0.2.3` 1,330 / `sources.json`). About 3.9k lines of guard and fixture, and a PLAN "ceremonial digest" candidate. It is the only compatibility guard on the Agent-owned edit-command schema, so this is an owner decision, not a deletion.
- **`timeline-commit-bundle.json` (4,085, generated)** could drop only if the contract dir were packaged. `pyproject.toml:32` ships only `schemas/*.json`, so keep it.
- **Triple-generated DTOs** (`runtime_protocol/timeline_commit_types.py` 103 + Python 103 + TS 101) are generated and not cut-ready. The `runtime_protocol` copy could import from the packaged client, which would be a structural change rather than a deletion.
- **Structural moves (no net change):** the commit service methods (`commit_timeline`, `_execute_timeline_commit`, `list_timeline_commits`, `get_project_verified_*`, ~300 lines) could move from `service.py` into `timeline_commit_port.py`. That reduces the 8k-line `service.py` without deleting anything.
- **`timeline_commit.py` `RuntimeCommitPort` Protocol** (lines 30-53) is only the interface of the one implementing class. Keep it: the provider ABI is a contract.

## Keep-list check
Not proposed for cut: RK01 project reference catalog, the UTF-8 text capability (`text_selection`, `verify_text_object`), the render checkpoint, capture certification (`capture_validation.py`, Decision 2026-10-20), and the refusal stubs themselves (gate 6).

## Verification of the census
- Counts: `git -C <wt> grep -I -c "" <rev> -- <paths>` and `git diff --numstat origin/main tl/integration`; family sums by `sed`/`awk` pipelines. Python was not usable in the sandbox, so no script output is archived here.
- Dead-code checks: `git grep -w` and `Grep` over `runtime_protocol`, `astrid_runtime`, `generators`, `scripts`, `tests`. Helpers with zero non-test callers are called out explicitly.
- Not verified: no test run (read-only task). Runtime ledger has **no RT06 row** in `deletion-ledger.runtime.md` (the brief lists it); flagged for the orchestrator.
