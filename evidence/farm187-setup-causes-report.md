# Farm 187 setup-cause classification

## Verdict

The published setup export accounts for all 187 unique errored node IDs. The literal exception families sum exactly to 187:

The retained checkpoint summary was **17,335 passed, 288 failed, 187 errored (all setup), and 4 skipped** on Agent `9cd3dbe865a941c052bda04ae0d61306d18f8f26` with Runtime `45c3a7f476e1c5f74fafc15956a58b9871eee21f`. These are historical reported counts, not a current working-tree full-suite claim or retrospective closure of the seven missing failure lines.

| Cause | Classification | Owner | Count |
| --- | --- | --- | ---: |
| `external_pack_sources` import missing on Runtime `45c3a7f4` | other: Runtime pin tuple mismatch | Runtime pin/tuple owner | 47 |
| `ASTRID_REMOTION_PROJECT_DIR` missing | environment | Farm lead / renderer provisioning | 33 |
| provisioned renderer peers missing | environment | Farm lead / renderer peer provisioning | 33 |
| Node `v20.19.4` absent; only `v22.22.0` reported | environment | Farm lead / Node toolchain provisioning | 29 |
| provisioned Remotion React peer missing | environment | Farm lead / Remotion dependency provisioning | 42 |
| composition14 runtime directory missing | environment | Farm lead / composition14 runtime provisioning | 3 |
| **Total** |  |  | **187** |

Each record in [farm187-setup-causes.json](farm187-setup-causes.json) retains the exact node ID, phase, published exception excerpt, line range, byte range, classification, and owner. The CSV is the flat export.

## Evidence and limits

- TSV: 187 rows and 187 unique IDs; exact set match with the published original 187-line errored-ID file; manifest reports 187 listed/found and zero unknown. Every per-node manifest line/byte offset maps to the JSON and CSV row, and the JSON/CSV exports have exact 187-record mapped-field parity.
- The raw farm log is not local. Its SHA-256 `06d435fed2622a4d9a8680e1071a650d5e34272090b08af5fe3ba0bd274dea06` is retained as farm-reported only. Excerpts come from the published TSV and offsets from the published extract manifest; no raw-log verification is claimed.
- The seven failed-summary lines with no `FAILED` node line remain unidentified and are neither invented nor assigned here.
- Exact PASS IDs are unavailable: no JUnit artifact exists and the quiet log lists failures/errors only. Open-node PASS credit is zero; a missing ID is not treated as a pass.
- No Node/runtime/provision/process/environment/network/cache probe, new test, or full run was performed.

The 47 import failures are deliberately not labelled generic environment failures. Read-only Runtime tree inspection found no `runtime_protocol/external_pack_sources.py` at `45c3a7f476e1c5f74fafc15956a58b9871eee21f`, while the exact same file is present at `1d9ddba546f8fb1300f55ff62607ed492719cbaa` and `f3208b26b53c4d7053e5464eaa7c5e15b1505812` (Git blob `0a5bdbbebeb9c00043115b44bede0ae53e98aa44`, byte SHA-256 `8931d2ae530ff1d6eccbb28dadec4349641fd4e1c19f231dba2616b93be2234e`); this supports the tuple-mismatch owner assignment.

## Contract boundary

This artifact is a farm-lead checkpoint classification, not product code or HTTP proof. It preserves the v2 boundary in the JSON: the request includes `api_version`, project/timeline scope, exact base revision/publication, nonempty commands, label, complete step fields (`id`, `label`, `intent`, `tags`, `command_ordinals`, `patch`, `reads`), `merge` (`fields` or `atomic`), declared reads, `dry_run`, `source`, `rationale`, `group_id`, and a stable HTTP idempotency key. Reply coverage remains accepted/merged with canonical document/head/revision/digests/records/effects/steps/dependencies/bindings/history/undo/attribution; dry-run `would_status` with null receipt; conflict reason/current head; and invalid code/path/hint/suggested command.

The production caller relevant here is the Farm lead’s existing checkpoint, not a new product caller. No product, kit, census, registry, schema, client, pin, or M5 change was made.
