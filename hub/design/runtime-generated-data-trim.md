# Runtime generated / frozen data trim (rt-m2-generated-data-trim)

Read-only analysis on `tl/rt-m2-generated-data-trim` (HEAD 9f59dd4, tree = tl/integration content).
Scope: every tracked generated or frozen data file over ~300 lines. Line counts are `wc -l` on the
committed file. Consumers from `git grep` in Runtime, and in Agent and App for vendor locks.

Bottom line: **no file can be trimmed safely in this pass. Lines saved now: 0.** Every candidate is
either (a) a byte-pinned vendored artifact (Agent/App lock, or a sha256 in a test or `sources.json`),
(b) a frozen oracle whose whole content is what the test asserts, or (c) a public ABI surface
(`validate_commit_value` accepts any root `$defs` name). The one real win (about 1.3-1.5k lines in the
commit bundle) needs an ABI decision and a re-vendor, so it is listed as a decision, not an action.

## Table

| File | Lines | Producer | Consumers (Runtime / Agent / App) | Derivable? | Needed-by-test portion | Proposed action | Lines saved | Risk |
|---|---:|---|---|---|---|---|---:|---|
| `runtime_protocol/schemas/timeline-commit-bundle.json` | 4,085 | `generators/timeline_commit_resources.py` (run by `generate.py`) | Runtime: `runtime_protocol/timeline_commit_validation.py:_schema_resources`; tests: `test_timeline_commit_validation.py` (byte equality, wheel contents, `len(resources) == 6`). Agent/App: none. In `contract/artifacts.json`. | Yes from `contract/schemas`, but the wheel must ship it (`pyproject.toml` ships `schemas/*.json`) and the artifact manifest pins its bytes. | Validator accepts any of the 62 root `$defs` names. Tests validate at least 9 names (`CommitRequest`, `PreparedCommit`, `CommitFailure`, `RestoreParentCompositionRevision`, `DocumentPin`, `Digest`, `MediaSelection`, `NarrationTakeRefs`, `VerifiedDocumentObject`). | Keep. Decision needed (see below). | 0 now; about 1.3-1.5k only with an allowlist | High (ABI + re-vendor) |
| `contract/schemas/edit-command.json` | 1,330 | Hand-authored canonical schema | `generate.py:validate_command_schema` (candidate); `tests/test_command_schema_compatibility.py`; bundle; `generators/timeline_commit_types.py:32` | No (authored) | Whole file: the guard compares complete schemas | Keep | 0 | - |
| `contract/schemas/timeline-commit.json` | 1,454 | Hand-authored | Bundle root; `timeline_commit_types.py:29`; generated TS and Python DTOs | No | Whole (root of bundle) | Keep | 0 | - |
| `contract/openapi/workspace-v1.yaml` | 1,642 | Hand-authored | `operation_index` (both clients); bundle receipt fragment; `test_contract_fixtures.py`; `test_schema_validation.py` | No | Whole (operation projection plus receipt) | Keep | 0 | - |
| `contract/schemas/worker.json` | 497 | Hand-authored | `tests/test_schema_validation.py` (many pointers), openapi | No | Several pointers, but authored contract, not generated | Keep (not generated data) | 0 | - |
| `packages/python/astrid_runtime_client/generated.py` | 1,489 | `render_python_client()` from `generators/python_client_template.py` | Agent: `runtime.lock.json` pins its sha256; Runtime: `test_generated_client.py`, `test_client_parity.py` | Yes, from template. Agent pins committed bytes. | Whole | Keep | 0 | - |
| `generators/python_client_template.py` | 1,489 | Hand-authored source | Source of `generated.py` (same content except placeholders) | No | Whole | Keep | 0 | - |
| `packages/typescript/src/generated.ts` | 287 | Typed TS source, patched by `render_typescript_client()` | App: `runtime.lock.json` pins it; TS package | Partly (patch step), but it is the TS source | Whole | Keep | 0 | - |
| `conformance/fixtures/visual-boundary-v1.json` | 2,701 | Authored vectors | Runtime: `test_visual_seam_admission.py:33` (all vectors, at least 10), `:109` (one). Agent: `runtime.lock.json` pins it; `tests/visual-boundary.test.mjs` iterates all vectors. Integration test checks byte equality with Agent's copy. | No | Whole. Runtime's own test uses all vectors, and the Agent copy must match. | Keep | 0 | Trimming would break Agent's pinned copy |
| `tests/fixtures/published-command-schemas/runtime-0.2.3.json` | 1,330 | Frozen publication (historical) | Floor for `generate.py:validate_command_schema`; `test_command_schema_compatibility.py`. Digest pinned in `sources.json` and tests. | No (frozen bytes) | Whole. `compare()` only checks keys present in the old schema, so dropping any definition or operation makes the guard strictly weaker. | Keep | 0 | Weakening the guard |
| `tests/fixtures/published-command-schemas/runtime-0.2.2.json` | 729 | Frozen publication | `test_command_schema_compatibility.py` (exact 5-error count, unchanged-pass). Digest pinned. | No (frozen bytes) | Whole | Keep | 0 | Changes the pinned digest and the 5-error expectation |
| `tests/fixtures/published-command-schemas/withdrawn-10c.json` | 889 | Frozen withdrawn publication | Negative fixture: exact counts (8 missing definitions, 7 missing operations), regex tests, generator refusal test. Digest pinned. | No (frozen bytes) | Whole, because the tests assert the exact error set | Keep | 0 | Changes asserted error sets |
| `tests/fixtures/published-command-schemas/producer-guard-1bffd.json` | 1,510 | Snapshot of Agent D13 producer schema (historical) | `test_actual_d13_guard_is_a_complete_ordinary_superset` only. Passes the whole file as candidate; sha256 pinned in the test. | No (frozen bytes) | Whole. A subset candidate would fail on "missing definition", so the superset claim needs the whole file. | Keep | 0 | - |
| `tests/fixtures/capture_authority.json` | 354 | Hand-authored template (already has omitted duplicates) | `test_capture_candidate_actual.py:83`, `test_snapshot_authority_refusal.py:54` | No | Not measured | Keep; revisit only with a per-test subset | 0 | - |

Below threshold, noted only: `contract/schemas/timeline-config.schema.provenance.json` (19 lines) has no
code consumer, only `contract/artifacts.json`. `docs/plans/astrid-naming/README.md:668` already marks it
as a decision ("delete or replace with a neutral path"). Deletion would change the manifest version, which
forces Agent and App re-vendor. Not done here: not "clearly safe", and the decision is owned elsewhere.

Binary fixtures (`tests/fixtures/precut-*.tar.{gz,xz}`, about 240 KB total) are frozen v31 snapshots read by
`tests/precut_realm_fixture.py` and `tests/test_precut_variants.py`. Not line-counted; kept.

## Why nothing can be pruned safely now

1. **Byte pins outside Runtime.** Agent's `runtime.lock.json` pins `generated.py`, `timeline-config.schema.json`,
   `visual-boundary-v1.json` and the `conformance/responses` files. App's pins `generated.ts`,
   `timeline-config.schema.json` and the responses. Agent's `scripts/vendor_lock.py:66` requires
   `manifest.version == lock.producer_version`. **Any change to any file matched by `scripts/artifact_manifest.py`
   PATTERNS, including the bundle, changes the manifest version and makes both locks stale.** So even a
   Runtime-internal trim forces an Agent and App re-vendor.
2. **Frozen oracles.** `sources.json`, `test_frozen_fixture_digests` and `test_command_schema_compatibility.py`
   pin the sha256 of each historical tuple. Compaction or subsetting changes the pin. Proof that a subset gives the
   same result: not possible. `compatibility_errors(prev, cur)` reports only differences on the keys of `prev`, so
   removing any `prev` definition or operation removes checks. The results can only become weaker. The four frozen
   files stay whole.
3. **Bundle is an ABI.** `validate_commit_value(value, definition)` accepts any root `$defs` name (`_validator`
   raises only for names not in the bundle). Pruning root `$defs` therefore changes the accepted name set, which
   is a provider-facing surface (`timeline_commit.py` "provider ABI" per the census).

## Measured closure of the commit bundle (node, pointer-level, cross-resource refs followed)

Script: `scratchpad/orch/workers/rt-m2-generated-data-trim/analysis/closure_nine.js` (entries = the 9 names tests
validate). Numbers are upper bounds because nested subtrees overlap.

| Resource | Full lines (bundle, pretty) | Reachable from 9 names (upper bound) | Reachable from all 62 root `$defs` |
|---|---:|---:|---:|
| timeline-commit.json | 1,454 | 800 | 1,446 |
| edit-command.json | 1,330 | 1,346 (all) | 1,346 |
| shot-composition.json | 505 | 363 | 363 |
| timeline-config.schema.json | 535 | 54 | 904 |
| document.json | 195 | 0 | 303 |
| workspace-v1.yaml (receipt) | 61 | 0 | 51 |

With the name set fixed to those 9 names, a pointer-pruned bundle would save roughly 1.3k to 1.5k of 4,085 lines.
With the full 62-name ABI kept, the saving is about zero.

## Decisions for the orchestrator

1. **Commit-bundle allowlist (the only sizeable win).** Decide whether `validate_commit_value` keeps accepting all
   62 root names (no saving) or an explicit allowlist of the names callers use (about 1.3-1.5k lines, after a
   closure-pruning step in `timeline_commit_resources.py`). The allowlist also needs a provider-ABI review, and
   Agent and App must re-vendor (manifest version changes). Batch it with the next contract change that already
   forces a re-vendor.
2. **Python client duplication.** `generated.py` is a rendered copy of `python_client_template.py` (1,489 each).
   Agent pins the rendered bytes. Dropping the committed copy means Agent vendors the template or a release and
   runs the render. A cross-repo change, about 1.5k lines.
3. **`timeline-config.schema.provenance.json`.** Zero code consumers, 19 lines. Decide in the astrid-naming plan.

## Not verified / not done
- No file deleted, no code changed, so no RT07 ledger row (the brief's condition for a pure deletion was not met).
- Targeted run on this tree (the test service, see Report): `test_artifact_manifest.py`, `test_generated_client.py`,
  `test_client_parity.py`, `test_command_schema_compatibility.py`, `test_visual_seam_admission.py`,
  `test_timeline_commit_validation.py`: 242 passed, 1 deselected.
- `generate.py --check` was not run here (Python is not allowed in this sandbox without approval). It is covered by
  `test_command_schema_compatibility.py::test_normal_generation_preserves_all_current_artifact_bytes[check]`, which
  passed in the targeted run.
