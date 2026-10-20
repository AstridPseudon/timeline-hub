# M2 writer bundle 2 — INTERNAL PROVISIONAL source, no release

M2 integration is HELD until PLAN records M1. Frozen Bundle1 remains Agent
`3bf9e5368a956ef562c77e1beb0a745addf23daf` / Runtime
`6be970633cc82ab412428151e6bf42f3e7fc3081`, client `0.2.2`.
This candidate is not popup acceptance, a generated artifact release, or an App handoff.

## Exact source identity

| Field | Value |
|---|---|
| Branch | `tl/agt-m2-popup-foundation-compose` |
| Source worktree | `/home/user/work/wt/agt-m2-popup-foundation-compose` |
| Base commit | `84db8bde88f695fede81f32a2fddb30622c6781f` |
| Final tested source tree | `c401f7720a092d1c1305ed37dea55c7754b8eacf` |
| Composed commit | **PENDING HARNESS COMMIT AFTER WORKER EXIT**; do not use the base SHA as the composed commit |
| Canonical schema | `/home/user/work/wt/agt-m2-popup-foundation-compose/astrid/core/timeline/schema/edit-command.schema.json` |
| Canonical schema file SHA256 | `5e622fb61142501f2c028f639da855ca318600be27a594253641bf9b755aa287` |
| Runtime lock SHA256 | `76509204d81fdeb25dcf3b621a52f0f3ac919c4e53bfe64f0e6c261dbf23ec08` (unchanged) |
| Exact paired Runtime | `6be970633cc82ab412428151e6bf42f3e7fc3081` |
| Paired client/schema/artifact | `0.2.2` / `sha256:89a396aaa10a5ab6c29fb5f053bf12dd031be4a259c33ebc6a53489fcd5878d3` / `sha256:3b805d6946fd73c44144009021f44153b78ceeb5e5b1298cd2397a1f2dc19730` |

The sandbox forbids commits and the harness commits only after exit. Manager TODO:
read `git rev-parse tl/agt-m2-popup-foundation-compose`, verify its tree equals the
final tested tree above, and replace the pending commit cell before freezing source.
The exact tree is already corroborated by the central service's `snap` file.
No commit identity is fabricated in this handoff.

## Reviewed composition and file manifests

- Foundation `84db8bde` is retained, including generic clear batches, staged/own-write
  capture, net-zero handling, semantic reservations, root patterns and original goldens.
- Popup: exact `2f77310e..5528c45c`. Full file manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-popup-foundation-compose/notes/popup-manifest.txt`;
  complete reviewed delta: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-popup-foundation-compose/notes/popup.patch`. New helper/handler, golden and both
  popup test files are byte-identical to `5528c45c`.
- Media provenance: exact `c3da1535..2f77310e`. Manifest: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-popup-foundation-compose/notes/media-provenance-manifest.txt`;
  delta: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-popup-foundation-compose/notes/media-provenance.patch`. Only boundary-proven manifest removal and
  provider forwarding are added to the newer core. The one inverse condition already
  exists equivalently in the foundation (`before.state == present`), so it is retained.
  The missing precursor test module is copied exactly from reviewed `2f77310e`,
  rather than importing the older product core.
- Placement: exact `e4338c48^..e4338c48`; manifest `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-popup-foundation-compose/notes/placement-manifest.txt`,
  delta `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-popup-foundation-compose/notes/placement.patch`. Handler, golden and tests are byte-identical.
  Selection/query and registry changes are manually reconciled with foundation/popup.
- Trim `8de94595` is **not composed**: the base lacks `_trim_commands.py` and its
  fixture/tests. It depends on native trim `d82f6ef7`, outside the supplied exact
  overlay. Manager must explicitly review/include that prerequisite, then apply
  `8de94595`; do not copy its whole older `commands.py` or schema.
- Split `3b03358` is **not composed**: that revision does not resolve in this object
  store. `3b03eee9` exists but is not silently substituted; manager must confirm the
  exact reviewed split SHA and its generic create-after/order changes.
- Scalar worker `agt-m2-clip-scalar-fields` was still uncommitted when final source
  was frozen for paired tests. Its WIP is excluded; manager adds only its committed,
  passing source in a later composition. This is why this source remains INTERNAL PROVISIONAL.
- Params/word/root-stage/materialization WIP is excluded. Params' three strict xfails
  and the foundation's two new root inverse strict xfails remain byte-identical.

The only additional Python glue beyond reviewed overlays is replacing the existing
seven-line `TRACK_CREATE_PARAMETERS` literal with its one-line canonical-schema lookup.
Its exact existing closed args become `TrackCreateArgs` plus one normal operation
condition in the canonical schema. This closes a generator gap without adding a
handler or behavior. All registered args now have normal closed definitions.
Exact semantic-union and 22 byte checks: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-popup-foundation-compose/notes/audit.py`, `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-popup-foundation-compose/notes/final-manifest.json`.

## Operations and capture exports

Every registered operation is version `1`, schema_version `1`. Engine/provider
operations `timeline.inverse` and `timeline.restore` remain available separately.

| Operation | Capture export | Args definition |
|---|---|---|
| `clip.move` | `astrid.sdk.timeline.capture.capture_move` | `ClipMoveArgs` |
| `clip.delete` | `astrid.sdk.timeline.capture.capture_clip_delete` | `ClipDeleteArgs` |
| `clip.add` | `astrid.sdk.timeline._clip_commands.capture_clip_add` | `ClipAddArgs` |
| `clip.set-params` | `astrid.sdk.timeline._scalar_commands.capture_clip_set_params` | `ClipSetParamsArgs` |
| `track.create` | `astrid.sdk.timeline.capture.capture_track_create` | `TrackCreateArgs` |
| `track.set` | `astrid.sdk.timeline._track_commands.capture_track_set` | `TrackSetArgs` |
| `placement.move` | `astrid.sdk.timeline.native_placement_commands.capture_placement` | `ClipMoveArgs` |
| `occurrence.add-media` | `astrid.sdk.timeline.native_occurrence_media_commands.capture_occurrence_add_media` | `OccurrenceAddMediaArgs` |
| `occurrence.swap-media` | `astrid.sdk.timeline.native_occurrence_media_commands.capture_occurrence_swap_media` | `OccurrenceSwapMediaArgs` |

Published `_track_commands` remains a thin re-export of the sole scalar handler.
Native session ingress stays `astrid.sdk.timeline.sync.TimelineSession.queue/commit`.
Popup signatures/ownership/refusals are detailed in `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/m2-popup-native-contract.md`.
The immutable five-field `MediaSelection` and ABI1 `selected_media` seam are unchanged.

Portable goldens are absolute under `/home/user/work/wt/agt-m2-popup-foundation-compose/tests/editing_conformance/fixtures/`.
Popup golden contains add/swap input, verified_media, exact commands/records/output;
placement golden contains parent/occurrence cases. M1 and parent-label capture +
records + output serialization remains exactly **87776 bytes**, SHA256
`b7f84a929716c9fc479fff1ea99e26daeeeb49b72ddc7594562b929f0feb3ff8`.
Frozen-base/composed parity outputs compare equal.

| Golden filename | SHA256 |
|---|---|
| `recipe_m1_move.json` | `e1dc5fc72e42fa90aed3e46ccd3bb95e219004bddd2917dc99f0154cf768dba0` |
| `recipe_m1_occurrence.json` | `dba00dff12f8322f8613869170abd15cd8c8e330bbbee8a6da675270fda3a7bc` |
| `recipe_m1_shared.json` | `0828ae13255897d8bea25ba5fd28445835f374189e837b41b9f818bb017577d7` |
| `recipe_m2_app_track_label.json` | `5aa9aed23a9764e4a9fb0d56fd5efc47368711933adbfaa224f2f725a766ed00` |
| `recipe_m2_clip_add.json` | `5e9a54e75a0901724dedd3e62c0f37f78840a8edee001f30b92306383800479b` |
| `recipe_clip_delete.json` | `091bc1c7fa9c57583dde8fcc6d6af9226513bf4f214369ef0892cc1db492f0aa` |
| `recipe_m2_scalar_track.json` | `f982beb0493fbda9196d99c2dfb5200c26cb82d58cd23535b87eb7295747c75d` |
| `recipe_m2_scalar_params_absent.json` | `9687956ee3850c5d873580a28cd6e8354f0b76dcb9a17bf56eb6ae0213f24b36` |
| `recipe_m2_scalar_params_null.json` | `15e945496b805af2554d78777be4585aa684615de575960352376f1dd4eaba74` |
| `recipe_m2_scalar_params_object.json` | `ae9f96e55432d0cf892f6045285e56265c6adc66058caf146bf4a7d7b1869638` |
| `recipe_m2_scalar_disjoint.json` | `0aab88bff6040ad741771fe8ed2198c141347970420ede78a981ba1416f6e866` |
| `recipe_m2_placement.json` | `7404b665b2918ebf095abc68bd3a20176afb0589b79cf785887c1da50b68d271` |
| `recipe_m2_occurrence_media.json` | `e30ed3303532e3d73adfd07670e04d1312003b7e10d2c5c008629b8b9bffad46` |

## Qualification and explicit limits

Final bounded nonnetwork lane: **1196 passed, 4 existing platform skips,
64 integration deselections, 5 strict xfails** in 84.56s.
Actual direct Runtime `9f9b25c000485e919f30f1411831fe2d5a3c1316` service/SQLite/CAS lane:
**42 passed, 12 strict xfailed** in 21.47s. No socket listeners or schema overrides.
All twelve popup positive/race expectations remain unchanged; only the specific
old scoped-asset schema error can trigger their strict xfail. Params' invalid
selected-schema cases and two root inverse gaps remain visible too.
Ruff passes; mypy passes for all ten touched product modules. Vendor lock verifies
against exact `6be9706`; canonical schema semantic union and capture byte parity pass.

Exact-pair central run (one request, final tree only):
`agt-m2-popup-foundation-compose-bundle1-runtime6be9706-integration-1020010632-18598`.
Result path: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/agt-m2-popup-foundation-compose-bundle1-runtime6be9706-integration-1020010632-18598/`.
**Result pending at initial handoff write; manager must use final summary below / worker report.**
The suite asserts exact Runtime HEAD and uses the existing frozen client pin, including
parent label/M1/identity/provider/client cutover plus scalar/first-clip/add-delete/popup/provenance files.
No full suite, install, network fetch, App/browser journey, artifact generation/version
selection, commit/merge/push or integration edits are performed here.
Detached popup greens do **not** prove Runtime popup acceptance or App readiness.

## Official Runtime generation request — source and definitive TODO

1. Manager reviews this source, resolves the missing trim/split identities and optional
   scalar overlay, and records the harness commit + tested tree above. Any source
   additions require a new reviewed schema SHA and bounded qualification; do not call
   this incomplete source a final ordinary/popup bundle.
2. After manager freeze, Runtime copies the exact canonical source path and SHA above
   onto a NEW candidate and performs normal official root/export generation. Keep one
   union of foundation shot/occurrence root patterns and scoped `asset` patterns in
   `ScopedId`, `EntityRef`, `TargetKey`, `AnchorIdentity`. Include all nine registered
   args schemas and `MediaSelection`, including the relocated `TrackCreateArgs`.
   Cover PreparedCommit recorder/created/guard sites through normal generation.
3. Runtime owns generated Python/TypeScript artifacts, normal package-root exports,
   artifact manifest and version choice. Agent/App then consume that exact same
   official tuple and refresh pins together. This worker generates no Runtime files,
   chooses no release version, uses no raw-schema override and bypasses no pin.
4. Rerun the unchanged 12 strict positive/race popup expectations through actual
   managed media selection/production provider; remove markers only after acceptance,
   reload, restart/exact retry, changed-key refusal, undo/redo and lifecycle races pass.
5. Resolve selected-pack params' three strict failures and root inverse's two strict
   failures under their assigned owners. Qualify App popup captures/browser use and
   zero legacy writer traffic; never infer acceptance from unit counts.
6. Keep Bundle1 frozen and all M2 integration held until PLAN records M1. This handoff
   is an official generation **request source**, not authorization to release artifacts.
