# D108/D69 applied source audit continuation

Read-only audit. No product, test, pin, generated, ledger, registry, or
foreign-crosswalk files were changed. The independent script is
`evidence/d108_applied_audit.py`; JSON output is `d108_applied_audit.json`.

## Exact rehearsal identity

The script reconstructed each tree from its approved upstream tip and recorded
patch, then compared the temporary Git tree object. All checks passed.

| scope | applied commit | applied tree | patch bytes | patch SHA-256 | recorded diff SHA-256 |
|---|---|---|---:|---|---|
| Runtime | `62040eeab98747dfb65abb6366236bf213109d6c` | `a522511414947e48e317a5e5c2103483b121a750` | 14,928,733 | `c93c3a1d00ddd9bb44ca51af3fdc71ab8311051846b07465d76183457f1b38b0` | same |
| App | `5391d71d871c73458ef27710fc132694d57983dd` | `204a9216697953f765b5bd550aefa5822503a44c` | 9,741,492 | `6ea5ce83b888a3f789c1b38d53f0180195ce27cf6248286116d22ff11c9a19a1` | `e9897f363f5ee5971316d2dee9b00e68a864774a1bdd541f3e85ae8d0dd61f45` |
| Composition (unchanged scoped PASS) | `ccd3a1084a9a4adc8f391befe01828ca7f9612e8` | `5ab5191a296980a0a6bcd1178ab6902d6478a148` | 501,162 | `14f43521a1423d00fad4ac12774ed80e20ed3d5f4f0e235aec9cf5fff265aad3` | same |

Manifest SHA-256: `37e559e6e176f4d9b4c20db27cdf6de8b4f5ef532b5abedf35533caffb2a4504`.

## Scope A — Runtime

Verdict: **FAIL with exact residual**. The ten changed/missing Runtime units
are source-mapped below, while aggregate assertion signals remain uncited.

| original selector group | applied replacement group | preserved source purpose | verdict |
|---|---|---|---|
| `test_canonical_render_admission::...legacy_version...` | `...::...current_metadata_version` | stale-head refusal, current metadata/version admission, no-write | exact-function equivalence |
| `test_runtime_domains::generated_domains_preserve...` | `...project_media_and_task_listing`; `...historical_timeline_recover_refuses_before_writes` | live catalog plus explicit historical recovery refusal | exact split equivalence |
| `test_runtime_domains::project_media_mutations_roll_back...` | `...project_reference_mutations...`; `...project_shot_mutations...` | retained catalog rollback-before-replay; no film writer | exact split equivalence |
| `test_runtime_e2e::project_shot_reference_crud...` | `...project_shot_crud...`; `...project_reference_crud...` | isolated project-scoped CRUD, idempotency, restart durability | exact split equivalence |
| `test_runtime_exact_idempotency::timeline_shot_and_reference_creation...` | `...project_reference_creation...` | reference half retained; retired film half not claimed | split with retired film half |
| `test_runtime_p1_blockers::project_updates_require_idempotency_keys...` | `...project_reference_updates...`; `...project_shot_updates...` | retained service-boundary idempotency requirements | exact split equivalence |
| `test_shot_composition_contract::materialized_canonical...` | `...pinned_compiled_timeline_schema_remains_strict` | strict canonical nested schema boundary | exact-function equivalence |
| `test_shot_composition_contract::materialized_timeline_schema_provenance...` | `...provenance_and_compatible_raw_field_reuse` | provenance, role extension, nested hashes, raw-field reuse | exact-function equivalence |
| `test_shot_composition_contract::schema_declares_two_owner...` | `...raw_container_boundary_without_a_second_compiled_schema` | two-owner/raw-container boundary | exact-function equivalence |
| `test_spec_reference::working_copy_uses_cas...` | `...without_candidate_is_admitted_uncertified...` | CAS/base-bound, uncertified-without-candidate admission | exact-function equivalence |

The script independently parsed the applied Python source and matched every
replacement file blob and function-body SHA-256 against the cited crosswalk:
10/10 rows passed. Approval sources are
`workers/rt-U1-D69-test-audit-1603/evidence/audit-classification.json`
(reused only after exact body equality),
`workers/rt-m2-keep-split-live/report.md:7-18`, and
`design/deletion-ledger.runtime.md:D04/RK01/RK02/RT02/RT03/RT09`.

Exact residual: **113 changed bodies, 72 removed assertion fingerprints, 205
added assertion fingerprints, 5 equality decreases, 3 membership increases,
0 added skip/xfail decorators, 0 dropped parameters**. These aggregate signals
have no per-assertion selector map and remain unresolved; counts and pass/fail
results did not clear them, and no alias was cleared without source.

## Scope B — App

Verdict: **PASS, source-mapped on the applied rehearsal tree**. The script
found all six history/restore/current-head-CAS positive/negative groups and all
three label/signature groups. Its App checks are deliberately lexical; the 77
explicit syntax limits are **not a TypeScript AST or semantic proof**.

History/restore applied-source anchors:

- `src/integrations/runtime/dataProvider.test.ts:856-857`: project/timeline
  history scope;
- `:858-863`: accepted restore/new head and incomplete-closure refusal;
- `:864-867`: both current-head guards;
- `:868-870`: no fallback immutable readback;
- `:873-893`: missing/unverified/empty revision/publication refusals;
- `:895-908`: foreign project/timeline refusals; and
- `:910-930`: stale Runtime 409 without refresh/fallback.

Production `dataProvider.ts:212-262` keeps project/timeline-scoped history,
verified-head restore, both `expected_head` and `expected_publication_id`, and
accepted-closure consumption. Canonical load/save paths remain at
`:996-1010`, `:1065-1078`, `:1081-1220`; `commitTimeline` remains at `:751-767`.

Label/signature applied-source anchors:

- `timeline-save-utils.test.ts:214-268`: resolved-config identity/signature;
- `timeline-data.test.ts:575-586`: display-label positives/negatives;
- `timeline-save-utils.test.ts:622-637`: full unprojected signature;
- `timeline-save-utils.test.ts:640-688`: repaired pinned-group order/geometry
  and full-config signature; and
- `timeline-data.ts:498-533`, `timeline-mutation-engine.ts:141-173`,
  `useTimelineCommit.ts:341-363,560-573`: derived-label view boundary,
  authored-label retention, and save stripping.

The seven scoped App source blobs are equal between applied capture `0b6cee…`
and current `6e21b74ff9`; this is source comparison only, not recapture or
qualification of later code. No UNAPPLIED mapping was found. D01 remains
**OPEN/in-progress** at `design/deletion-ledger.app.md:6`; this mapping does
not retire whole-document savers or unrelated writers.

Approval sources: `design/app-contract-review.md:11` and `baacef5d66f` for
history/restore; `design/app-main574-derived-label-reconciliation.md:24-35,48-62`,
`design/app-label-reconciliation-final-review-r2.md:7-13,45-74`,
`design/app-U3b-final-review-0738.md:1-30` (ancestors `5404ca470e`,
`cd29ff2642`) for labels/signatures; and
`design/app-U3-D69-home-and-preflight-1704.md:21,31` for D69.

## Checks and limits

- `python -m py_compile evidence/d108_applied_audit.py` — PASS.
- `python evidence/d108_applied_audit.py` — PASS: exact trees/patches,
  10/10 Runtime source rows, and App lexical checks.
- No pytest, Vitest, TypeScript, lint, provider, browser, live socket, build,
  render, or full suite was run.
- No Composition suite was duplicated; only unchanged scoped tree/patch
  identity was checked.
