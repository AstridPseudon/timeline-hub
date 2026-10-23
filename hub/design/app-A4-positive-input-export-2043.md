# App A4 positive input export

## Result

PASS. The reviewed synthetic App input packet was parsed and copied unchanged to:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-A4-positive-input-2043.json`

This is an App-emitted input witness only. It is not a Python/provider acceptance result, expected Python output, golden, new executor, live Runtime/authentication proof, or raw old-positive parity claim.

## Exact source and export identity

- Source: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-A4-after-positive-mounted-2019/a4-after-positive-input-packet.json`
- Export: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-A4-positive-input-2043.json`
- Whole-file bytes: `67120`
- Whole-file SHA-256: `33934817ed76afaa7ff32968325e8aa4bc0212bfe9c62adb1c1f382f2dfff8b4`
- Git blob ID of both source and export (computed with `git hash-object`, not added to the repository): `8d12f9615ee9dc8d4396e9e7c4fb59035ee17896`
- `cmp -s source export`: exit `0`
- JSON parse: passed; top-level shape is `{ "cases": [...] }` with exactly four cases.

## Provenance

- Test donor: `src/tools/video-editor/hooks/useTimelineCommandsService.persistence.test.tsx`.
- Mounted candidate/reviewed head: `001145ce1dcba562ab082620e965e73bac1857d1`.
- Donor parent: `da7f25f0546ada65c224c650488a79a9ff0e1440`.
- Independent review: `app-A4-after-positive-review-2033`, report PASS, reviewed candidate `001145ce1dcba562ab082620e965e73bac1857d1`.
- Author report: `app-A4-after-positive-mounted-2019`, four actual prepared-media mounted cases through `addClip` → `useTimelineSave`/local outbox → `RuntimeDataProvider` → generated transport → accepted canonical adoption.

## Packet mapping

All cases use request identity `api_version=1`, `project_id=project-commit`, `timeline_id=timeline-1`, `base_revision_id=r0`, `base_publication_id=p0`, `label=Edit timeline`, `dry_run=false`, `merge=atomic`, and `source={"via":"app"}`. Each has one `doc.patch` command, one step, created ID `parent/clip:clip-0`, `list.insert` into `parent.clips` after `anchor`, and pre-insert order `[anchor, later, sibling]`. The base closure has schema version `1`, empty `shots`, `internal_timelines`, `media`, and `documents` dependency lists. Source pins include the `anchor`, `later`, `sibling`, and `source_asset` records.

| Case | Request bytes | Request SHA-256 | Source-pin distinction | Patch mapping | Base closure parent digest |
|---|---:|---|---|---|---|
| old video with missing hold | 2368 | `38afc0473df1616da071f35c3362fcfb7a01dc3fe904a0a7b49b2a0c66c738a1` | `anchor.hold` absent | insert `clip-0` at `3`, no inserted `hold`; `later.at` `5 → 7`; asset registry key `asset-old-video-with-missing-hold` | `sha256:445b8013f7a0db22f5c961f041598012a265d025aa4557b2294df237da8e3431` |
| old video with explicit null hold | 2452 | `a422aaf915d72edb848029e74a394a8ba43897bc3551882a7982b00e268269f1` | `anchor.hold = null` | insert `clip-0` at `3` with `hold=null`; `later.at` `5 → 7`; asset registry key `asset-old-video-with-explicit-null-hold` | `sha256:6c97876532b4ac508b20824295a6ce2f4feed2387c922ec17ac9442083eda313` |
| old video with subminimum duration | 2656 | `99cf8093817631e9df49a4093c3086522419009f58e855fc287bcb62603f17f5` | `anchor.hold = 0.01` | App normalization: insert at `1` with `hold=0.0667`; anchor hold `0.01 → 0`; `later.at` `5 → 5.0667`; asset registry key `asset-old-video-with-subminimum-duration` | `sha256:e0f6d16e3d8891e0d338222a52af2c7990bc1bda5ee9dc16b81c193f1b08526f` |
| old video with incoming transition | 2416 | `e1f05b38f044d4557f0e28c12c644d077f85e617590a1b2b9050fb4c93527ae5` | `anchor.hold` absent; incoming transition opaque `[false, null]` | insert `clip-0` at `3`, no inserted `hold`; `later.at` `5 → 7`; asset registry key `asset-old-video-with-incoming-transition` | `sha256:94cf0261c216274f2559d9ac0b31b8d5a4782a0db8d53124ebf052d13f602825` |

For every case, the embedded request bytes parsed back to the corresponding `request_json`, and recomputed request length and SHA matched the packet’s recorded values. The source pins retain `later` on `V1` at `5` with hold `1`, `sibling` on `V2` at `5` with hold `1`, and source asset `source.mp4` / `media-source`.

## Security and scope limits

- Synthetic identifiers and fixture media names only; no credentials, bearer/auth material, cookies, secrets, private keys, or API keys were found.
- No `http://`, `https://`, `ws://`, or `wss://` URL strings were found.
- No headers, bearer tokens, full URLs, live HTTP, browser, body capture, seed, service, or runtime-auth material is exported.
- The packet contains request data, canonical base closures, source pins, and per-request hashes only; it contains no response receipt or claim of accepted/merged/rebased/invalid behavior.
- The observed subminimum mapping is App normalization `0.01 → 0`, inserted `0.0667`, ripple `5.0667`; raw old-positive parity is not claimed.
- Existing implementation and tests remain unchanged; A4/P1 deletion and broader parity remain HOLD per the reviewed report.

## Verification

Report-only checks performed for this export:

- Node JSON parse and structural audit: passed.
- Per-case request JSON/bytes/length/SHA audit: passed for 4/4 cases.
- Credential/auth/full-URL scan: zero matches.
- `cmp -s` source/export: passed.
- `sha256sum` source/export: identical above.
- `git status --short`: clean.
- `git diff --check`: passed.

No browser, live socket/HTTP, full, provision, seed, service, or App type/lint suite was run for this report-only export; the author/reviewer supplied their own targeted evidence in the provenance reports. No repo product code or test file was edited by this worker.

