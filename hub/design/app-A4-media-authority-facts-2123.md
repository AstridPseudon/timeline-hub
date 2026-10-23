## A4 report — prepared-media authority audit

Outcome: the exact A4 packet is a harness-only witness, not Runtime-authority-complete. Agent’s four `dependency_changed` refusals are expected. The packet cannot prove a product defect or justify a guard waiver.

### Confirmed

- App HEAD: `d3bec9b4a3ead64d05021e37e5d418884434f2ab`; worktree clean.
- Runtime source: `abd47e68de6d7a36bec8ac4f0f6e0bc01d98d14e`
- Agent source: `07e6d83df69146c7dddea207f32330dc8b58dbc5`
- Packet: 67,120 bytes, SHA-256  
  `33934817ed76afaa7ff32968325e8aa4bc0212bfe9c62adb1c1f382f2dfff8b4`
- Exactly four requests parse and match their recorded byte lengths and SHA-256 values:

  1. `38afc047...c738a1`, 2368 bytes
  2. `a422aaf9...269f1`, 2452 bytes
  3. `99cf8093...17f5`, 2656 bytes
  4. `e1f05b38...27ae5`, 2416 bytes

The request bytes were not changed. The packet contains the expected v2 request fields and no added `reads`, `rationale`, or `group_id`.

### Existing App call chain

- Prepared import caller: `useAssetManagement.ts:363-443`
- Runtime import boundary: `dataProvider.ts:1305-1364`
- Existing Runtime selection capture: `dataProvider.ts:1722-1739`
- Existing prepared carrier: `AssetResolver.ts:31-40`, with optional `mediaSelection`
- Registration drops that field: `commands/provisioning.ts:5-11`; `useAssetManagement.ts:228-246`
- Ordinary prepared placement: `useTimelineCommandsService.ts:442-503`
- Commit transport: `dataProvider.ts:750-766`

App does have an authoritative verification path:

- `getProjectMediaSelection`: `dataProvider.ts:849-859`
- `getProjectVerifiedMedia`: `dataProvider.ts:861-881`
- Existing semantic callers: `placementRequester.ts:162-189`, `nativePlacementCapture.ts:42-61`
- Existing semantic media capture requires exact verified inputs: `parentClipAddCapture.ts:36-57`

### Required authority

For each prepared asset, the authentic Runtime input must include:

- `MediaSelection`: exactly `asset`, `generation_id`, `variant_id`, `object_id`, `catalog_digest`
- `VerifiedMedia`: that exact selection plus `media_type`, `size`, and video duration where applicable

A registry entry, filename, URL, or opaque `media_id` string is not sufficient. The packet’s `media-old-*` / `media-source` values and empty base `dependency_manifest.media` are synthetic and have no Runtime selection or verified-media records.

Runtime validates captured selections and manifest membership in `timeline_commit_port.py:350-357,515-557`; Agent enforces the same boundary in `_doc_patch.py:296-314`.

### Classification and owner

The packet is harness-only missing authority. It is not evidence of a live invalid production emission. However, the source audit confirms that the ordinary App prepared-media path currently drops `PreparedMediaImport.mediaSelection` and does not call `getProjectVerifiedMedia` before placement.

The precise missing input is four authentic Runtime-backed `MediaSelection`/`VerifiedMedia` records bound to the imported assets. Owner/next source: App A2/A3 plus the Runtime media-selection/verified-media boundary. Agent should continue only after those inputs are supplied through the existing provider verification path.

### Safe continuation

1. Preserve all four request bytes and full positive oracles unchanged.
2. Obtain real selections through existing Runtime selection and verified-media reads.
3. Use the existing semantic capture/provider path; do not fabricate `dependency_manifest.media`, `reads`, pins, or APIs.
4. Re-run the bounded Agent witness only with those authentic verified inputs. A changed request must be treated as a new packet, not a replay.

### Checks

Ran:

- packet stat/hash audit — passed
- JSON parse and four-request hash/length audit — passed
- `git diff --check` — passed
- `git status --short` — clean

No tests, typechecks, lint, browser, backend, or full suites were run per the report-only brief.