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

## D48 bounded per-node cause review (F-farm15-causes)

Independent read-only review of the 15 unknown rows resolved **0/15**. The
classification remains **80 environment / 1 regression / 15 unknown**; no
unknown was relabeled from a missing artifact, an aggregate prior PASS, or a
different qualified tuple. The packet's existing per-row `source_citations`,
`earliest_causal_boundary`, `owner`, `finite_missing_fact`, and Farm line/byte
offsets remain authoritative.

| Group | Nodes | Retained primary evidence | Exact missing finite fact and owner | Farm offsets |
|---|---:|---|---|---|
| Generic-host shutdown markers | 5 | Assertion at `tests/core/execution/test_generic_host_actions_v3.py:1770` or `:1816`; the expected worker-entry marker is absent, with no child stderr in the retained section | Child stderr/launch outcome, or a matched qualified tuple proving whether the worker started; **Agent execution/host with Runtime Farm child qualification** | Lines `18643–18884`; bytes `1116945–1128618` |
| Generic-host observed-owner markers | 2 | Assertion at `tests/core/execution/test_generic_host_actions_v3.py:1497`; observed-owner set is empty, with no child/process launch outcome in the retained section | Child/process observation and launch outcome on a matched qualified tuple; **Agent execution/host with Runtime Farm child qualification** | Lines `18547–18642`; bytes `1111819–1116945` |
| Render-wire missing outputs | 6 | Consumer assertion at `tests/core/rendering/test_conformance.py:87` sees missing `workspace/result.json`; no producer-side exception is retained | Producer command status/stderr and the exact result-path creation decision for each node; **Agent rendering harness/backend** | Lines `21779–22031`; bytes `1301577–1315775` |
| Installer repair child exits | 2 | Wrapper at `astrid/installer/backend.py:57` reports child Python exit 1; child output and command are absent | Captured child stdout/stderr and the exact failing child command before assigning Runtime or Agent ownership; **Agent installer/service harness** | Lines `33148–33335`; bytes `1981277–1991865` |

The exact node-specific offsets, source citations, and finite-missing-fact
strings remain in both `farm96-causes.json` and `farm96-causes.csv`. No
production caller, v2 request/reply execution, test body, subprocess probe,
full suite, new checkpoint, or raw-log reconstruction was performed.

The newer eight are not backdated. No open-node PASS credit is assigned because the packet has no quiet-log/JUnit exact PASS list. No tests, probes, original bodies, full suite, install, product edit, schema/client/pin change, or v2 caller change was made. The JSON/CSV rows retain the actual Farm section line/byte offsets and the published extract scope for independent review.

## CSV custody correction (F-farm96-csv-custody)

The returned CSV at `856de6e3f2` omitted all 288 Farm tuple cells. Restore `agent_commit`, `agent_tree`, and `runtime_commit` for each of the 96 rows from the unchanged JSON `source_tuple`, cross-checked against each JSON `failed_farm_tuple` and original CSV at `cf0218cf5ef137b8e24fc2678a2de8a5de25ce1a`: Agent `9cd3dbe865a941c052bda04ae0d61306d18f8f26`, tree `57f0231da0d7904ecd8778169973d6384e0ae141`, Runtime `45c3a7f476e1c5f74fafc15956a58b9871eee21f`. These are the Farm failure identities; the separate qualified prior-proof scope columns retain their exact values, including authenticated Runtime `f3208b26b53c4d7053e5464eaa7c5e15b1505812` where applicable.

The same serialization also omitted 96 `source_citation` cells. This additional explicit correction restores the original CSV strings, each independently reconstructed from JSON `source_citations` as `repo path:line (note)` joined by `; `. Both authoritative sources agree for all 96 rows. The complete before/after cell diff is exactly 288 tuple cells plus these 96 citation cells; all other CSV cells, column order, row order, proof references, and every JSON byte remain unchanged.

Standalone stdlib validation checks every one of the 31 mapped CSV fields against JSON for all 96 rows, including tuple, citations, offsets, hashes, prior-proof scopes and optional values. Required cells have zero blanks. Optional blanks retain their JSON meaning: 15 unknown changed-source values are null, 81 rows have no finite missing fact because their classification is not unknown, and all 96 qualified rows have no prior-missing reason. Exactly one current docs challenge remains; neither its repair nor a future home tuple is qualified here.

The published manifest still reports 288 failure sections but only 281 short-summary FAILED lines: the seven-line discrepancy remains unknown and receives no inferred node identities or PASS credit. The 187 ERROR sections are separate evidence and are not reclassified by this CSV repair. The raw Farm hash and byte count remain manifest-reported only; the raw log was not locally rehashed.

Final data artifact SHA256 values after the CSV correction:

| Artifact | SHA256 |
|---|---|
| `farm96-causes.json` (unchanged) | `9b9bc96bc6309c8b98d5afa8c3582a88d38d2895f97438f407e1c5044668b896` |
| `farm96-causes.csv` | `d0dd5e799b1d18a6f051642e55077f650af068da6c5a4675b4e5e7c717913da4` |

## v2 contract limits

This evidence-only packet does not prove implementation or production-caller adoption of v2. The required request remains the full shape: `api_version`, `project_id`, `timeline_id`, `base_revision_id`, `base_publication_id`, nonempty `commands`, `label`, `steps` (`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`), `merge` (`fields|atomic`), declared reads, `dry_run`, `source`, `rationale`, `group_id`, and a stable idempotency key. Replies remain the full `accepted`/`merged` canonical document/head/revision/digests/records/effects/steps/dependencies/bindings/history/undo/attribution` forms, dry-run `would_status` with null receipt, and structured conflict/invalid forms with reason or code/path/hint/current head/suggested command. No v2 caller test or production-caller proof was run or claimed.
