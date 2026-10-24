# D48 Farm 96 cause classification

Read-only classification of the published Farm26511 packet for Agent `9cd3dbe865a941c052bda04ae0d61306d18f8f26` / tree `57f0231da0d7904ecd8778169973d6384e0ae141` with Runtime `45c3a7f476e1c5f74fafc15956a58b9871eee21f`.

## Source and packet validation

- The manifest reports raw log SHA256 `06d435fed2622a4d9a8680e1071a650d5e34272090b08af5fe3ba0bd274dea06` and `2,089,428` bytes. The raw log remains on Farm; no local rehash is claimed.
- Manifest: `78,899` bytes, SHA256 `dad95d48ae0e2bda28dccb948368a3b3404c9a1b9c20982916b9b0b378fd6ee7`.
- Historical extract: `742,107` bytes, SHA256 `597c7445799991f0b328cd43e25b3726dd86aab2fe25bb20588eb32c64097563`.
- Newer extract: `43,677` bytes, SHA256 `ff2fa869a3d30494c1516f3ee937682649c7a54920612abc1c9ba8746a495e21`.
- Stdlib validation passed: 88/88 and 8/8 headers match manifest membership, zero duplicate node IDs, and 96 total rows.

The Agent source imports `runtime_protocol.platform` at `astrid/core/execution/persistent_supervisor.py:17`; Runtime45c3 contains the `runtime_protocol` package. The repeated child `ModuleNotFoundError` is therefore classified as a Runtime Farm child import-path/recipe failure, not an Agent product regression. The newer external-orchestrator row is a separate verified tuple API mismatch: the Agent fixture imports `runtime_protocol.external_pack_sources` at `tests/helpers/external_orchestrator_owner.py:53`, while Runtime45c3 exposes no such module/API. The one non-environment row is the exact source/docs inventory mismatch: Agent source `generic_host.py` is 14,313 lines while `docs/giant-file-rationale.md:18` claims 13,998.

## Prior closure accounting (corrected after independent review)

Farm excerpts are failure evidence only and are never counted as prior proof. Each row now has an exact prior-closure reference, or an explicit `missing_prior_qualified_proof` record, in both JSON and CSV. The complete official census is `census22ee4d6df217eef1cef60f7e9c646b6f5fe13a45d31163afb2ffe46126facae0` (261 closed / 6 open / 267 total). Historical 202/65/236 counts remain provenance snapshots and are not closure credit.

The 96 Farm members have 96 qualified exact-node prior references and 0 missing references in this packet. References are distributed as follows: `env86_installed` 62, `env_source16` 1, `render_cohort_0013` 9, `render_audio_0013` 1, `render_node_five` 4, `d13_wheel_0039` 1, `env_misc_0020` 3, `cli_surface_0012` 1, `render_wire_27934` 6, `h3_current_0508` 7, and `d40_observed_0551` 1. The independent D40 result review `d40_result_review_0552` corroborates that same exact node and is not duplicate credit.

Every environment label is supported by its bounded source/import/installed scope and relevant source comparison in `counted_closed_proof`; none is inferred from the Farm Runtime45c3 failure tuple. The seven H3 rows use authenticated current Runtime `f3208b26b53c4d7053e5464eaa7c5e15b1505812` and installed Agent `ba8f0bc8bebf6d0e9a8143fed80d31f846cd5b95`, while the Farm failure used Runtime `45c3a7f476e1c5f74fafc15956a58b9871eee21f`. No duplicate credit or automatic reopening is performed.

Exactly one current challenge is recorded: `tests/test_structure_contracts.py::test_giant_file_inventory_matches_rationale`, because current `generic_host.py` is 14,313 lines and the retained rationale claims 13,998. The independent docs source repair is disjoint and unverified here; this packet does not claim it fixed.

## Classification and limits

| Cohort | Environment | Regression | Unknown | Total |
|---|---:|---:|---:|---:|
| Historical closed | 72 | 1 | 15 | 88 |
| Newer closed | 8 | 0 | 0 | 8 |
| Total | 80 | 1 | 15 | 96 |

Unknowns are deliberately finite: five lifecycle marker assertions, two review-observation assertions, six missing `result.json` producer outputs, and two installer child-process exits. Their rows name the exact missing evidence; no cause is guessed.

The newer eight are not backdated. No open-node PASS credit is assigned because the packet has no quiet-log/JUnit exact PASS list. No tests, probes, original bodies, full suite, install, product edit, schema/client/pin change, or v2 caller change was made. The JSON/CSV rows retain the actual Farm section line/byte offsets and the published extract scope for independent review.

## v2 contract limits

This evidence-only packet does not prove implementation or production-caller adoption of v2. The required request remains the full shape: `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, nonempty `commands`, `label`, `steps` (`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`), `merge` (`fields|atomic`), declared reads, `dry_run`, `source`, `rationale`, `group_id`, and a stable idempotency key. Replies remain the full `accepted`/`merged` canonical document/head/revision/digests/records/effects/steps/dependencies/bindings/history/undo/attribution` forms, dry-run `would_status` with null receipt, and structured conflict/invalid forms with reason or code/path/hint/current head/suggested command. No v2 caller test or production-caller proof was run or claimed.
