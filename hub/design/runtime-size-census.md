# Runtime timeline-core size census

Boundary approved at 08:00Z and recorded in PLAN decisions: count authored product code implementing timeline **Read/See/Edit**. For Runtime, the manifest below includes the mixed timeline integration files (`canonical_schema`, `cli`, `server`, `service`, `store`) and the hand-written timeline commit/read/See modules. It excludes untouched worker/execution and generic `astrid_runtime` infrastructure, generated contract/schema/client/DTO outputs, and tests/fixtures. Counts are committed-blob lines, including blank lines, from the same path set at both revisions.

Revisions: `origin/main` `8c1830d1ca64a3934c37611a28ffe8db7df879ea` (tree `e8f7bf1c6c3493b05faee2513cb093bda4fb7f46`) → exact current Runtime `6023cfb10307b4c0004642b5fa1995d72ba4f6d1` (tree `bb2d3b6235cc7bf819373d2078d7437360c322d4`).

## Authored timeline-core paths

| Path | main | current | delta |
|---|---:|---:|---:|
| `runtime_protocol/canonical_schema.py` | 418 | 439 | +21 |
| `runtime_protocol/cli.py` | 399 | 401 | +2 |
| `runtime_protocol/server.py` | 1,024 | 1,226 | +202 |
| `runtime_protocol/service.py` | 8,880 | 7,990 | −890 |
| `runtime_protocol/store.py` | 6,540 | 6,796 | +256 |
| `runtime_protocol/capture_validation.py` | 0 | 151 | +151 |
| `runtime_protocol/managed_render_snapshot.py` | 217 | 217 | 0 |
| `runtime_protocol/seam_intent.py` | 88 | 88 | 0 |
| `runtime_protocol/shot_dependencies.py` | 155 | 155 | 0 |
| `runtime_protocol/snapshot_refs.py` | 224 | 278 | +54 |
| `runtime_protocol/timeline_commit.py` | 0 | 55 | +55 |
| `runtime_protocol/timeline_commit_baseline.py` | 0 | 440 | +440 |
| `runtime_protocol/timeline_commit_execution.py` | 0 | 115 | +115 |
| `runtime_protocol/timeline_commit_inputs.py` | 0 | 707 | +707 |
| `runtime_protocol/timeline_commit_port.py` | 0 | 887 | +887 |
| `runtime_protocol/timeline_commit_producer.py` | 0 | 285 | +285 |
| `runtime_protocol/timeline_commit_producer_checkpoint.py` | 0 | 163 | +163 |
| `runtime_protocol/timeline_commit_provider.py` | 0 | 93 | +93 |
| `runtime_protocol/timeline_commit_store.py` | 0 | 940 | +940 |
| `runtime_protocol/timeline_commit_validation.py` | 0 | 103 | +103 |
| `runtime_protocol/timeline_cutover.py` | 217 | 217 | 0 |
| `runtime_protocol/timeline_inspection.py` | 845 | 844 | −1 |
| `runtime_protocol/timeline_view.py` | 214 | 214 | 0 |
| `runtime_protocol/visual_boundary.py` | 228 | 228 | 0 |
| `runtime_protocol/visual_seam.py` | 463 | 469 | +6 |
| **Total authored timeline core** | **19,912** | **23,501** | **+3,589** |

The zeroes are justified: those hand-written modules do not exist at `origin/main`; they are current authored timeline-core additions, not omitted paths. `runtime_protocol/timeline_commit_types.py` is deliberately absent from this authored table because it is a generated DTO copy.

## Reproducible count

The following uses one explicit manifest for both revisions; it does not inspect a checkout or silently use a different path set:

```sh
paths='runtime_protocol/canonical_schema.py runtime_protocol/cli.py runtime_protocol/server.py runtime_protocol/service.py runtime_protocol/store.py runtime_protocol/capture_validation.py runtime_protocol/managed_render_snapshot.py runtime_protocol/seam_intent.py runtime_protocol/shot_dependencies.py runtime_protocol/snapshot_refs.py runtime_protocol/timeline_commit.py runtime_protocol/timeline_commit_baseline.py runtime_protocol/timeline_commit_execution.py runtime_protocol/timeline_commit_inputs.py runtime_protocol/timeline_commit_port.py runtime_protocol/timeline_commit_producer.py runtime_protocol/timeline_commit_producer_checkpoint.py runtime_protocol/timeline_commit_provider.py runtime_protocol/timeline_commit_store.py runtime_protocol/timeline_commit_validation.py runtime_protocol/timeline_cutover.py runtime_protocol/timeline_inspection.py runtime_protocol/timeline_view.py runtime_protocol/visual_boundary.py runtime_protocol/visual_seam.py'
for rev in origin/main 6023cfb; do
  for path in $paths; do
    git show "$rev:$path" 2>/dev/null | wc -l
  done | awk -v rev="$rev" '{sum += $1} END {print rev, sum}'
done
```

Expected totals: `origin/main 19912` and `6023cfb 23501`.

## Scope exclusions

- `runtime_protocol/local_*`, `remote_worker_*`, `verified_host_launch.py`, `astrid_runtime/`, and unrelated auth/backup/CAS/platform/lifecycle code are main execution/custody infrastructure, not timeline Read/See/Edit authored code.
- `contract/`, `runtime_protocol/schemas/`, `conformance/typescript/generated.ts`, generated Python/TypeScript clients, `runtime_protocol/contract_metadata.py`, and generator outputs are generated contract/client data. They remain covered by RT05/D13 evidence but are not authored-line counts.
- `tests/`, conformance fixtures/responses, and package test trees are test evidence, not product lines. Their behavior evidence remains explicit in the deletion ledger; no test expectations were changed for this census.

The mixed integration files are included conservatively because they contain the Runtime’s timeline route, schema, service, projection, and commit integration alongside generic code. This avoids undercounting newly added core while keeping unchanged execution infrastructure out of the approved boundary.

## Current architectural debt

- D04 remains held: `publish_parent_composition` is restored, but App D01 and Agent whole-candidate/`clip.set-element` migrations are both still required; parent-media replacement remains retired.
- Timeline reference/placement mutation bodies remain retired. RK01 project reference catalog is live KEEP infrastructure; catalog-positive tests do not certify timeline placement migration.
- Text-binding clear and text first-use set/rebind remain capability debt with original strict xfails. Candidate promotion remains OPEN with original strict xfails. These are not refusal-as-success claims.
- Legacy timeline revision history still coexists with commit history (`timeline_revisions`, `diff_timeline`); it is not cut-ready while PLAN Read keeps history/diff and Agent consumers remain.
- The migration-only `timeline_cutover.py` audit and scene evaluation in legacy save paths remain held behind D04. Imported-baseline receipt re-verification is a later owner decision, not an approved cut.
- RT05 and RT06 are merged; D13 is merged at 6023cfb. Their default-filter full results are baseline-only and must not be relabeled as marked-integration proof.

## Evidence status

I read each cited result’s `request`, `status`, `snap` tree and `summary` before recording it in the ledger. `rt-m2-commit-path-dedup-full-restore-integration-1020082220-2410` is status `fail`, tree `9fe71e4`, with 4,967 passed / 7 baseline failed / 25 xfailed / 18 skipped. `rt-m2-d13-regen-full-restore-integration-1020082104-3297` is status `fail`, tree `d9dcf842`, with 5,111 passed / 7 baseline failed / 25 xfailed / 18 skipped. Both are the default-filter `full-restore-integration` command from `suites.conf`, not `-m integration`. The D13 targeted result `rt-m2-d13-regen-restore-integration-1020081919-31156` is status `pass`, tree `d9dcf842`, 430 passed / 46 deselected / 1 original xfail. The RT06 marked commit lane `rt-m2-commit-path-dedup-commit-integration-1020080701-23900` is status `pass`, tree `9fe71e4`, 9 passed.

No tests or full suites were run by this docs-only worker.
