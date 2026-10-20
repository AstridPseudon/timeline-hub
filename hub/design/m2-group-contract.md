# M2 canonical group migration and existing-lane view candidate — HELD

PLAN option A is settled. Canonical shot/occurrence ownership is the single editable representation; parent `config.pinnedShotGroups` is migration input only. No M2 integration before PLAN's M1 record. Current successor: branch `tl/agt-m2-group-existing-lane-view`, based on reviewed migration `746440c4c4a6bf7dd8a89500c2bef21a3721efef`. Harness commit is pending worker exit; the base is not the final source identity. The migration proof below is retained; current move/view exports and evidence are specified in the successor section.

## Bounded implementation

`timeline.migrate-groups` v1 selects `parent`, takes closed `groups:[{legacy_shot_id,shot_id,occurrence_id}]`, and requires a mapping for every legacy group in authored order. The caller supplies the destination IDs. The handler uses the current native recorder, collection order guards, root creation, source capture and inverse machinery. It does not allocate IDs, manufacture history or publish outside the ordinary provider.

The exact two-clip fixture is c1 at 0 and c2 at 2, hold 2, lane V1. Conversion creates shot `new-shot`, occurrence `new-occ`, a 4000ms interval starting at 0 on V1, and removes only consumed parent rows and the structural legacy array. Full legacy group/mode/snapshot/null/opaque metadata and ordered `{legacy_clip_id,clip_id}` mapping remain under occurrence `provenance.group_migration`. Complete child/track/registry bytes, ungrouped rows/order, rational 30000/1001 fps and immutable source pins survive. The canonical graph walker exempts only the actual token path `occurrences[index].provenance.group_migration.legacy_group`; collision keys and structural legacy data elsewhere still refuse. No sanitizer is used.

Interleaved/reordered membership, duplicate legacy shot identities, missing/duplicate/shared members, occupied destinations, ambiguous aliases, divergent mirrors/registries, nonempty legacy items without an explicit mapping, follow timing and unrepresentable timing refuse atomically. No fixture normalization is authorized. Ordinary edits on a legacy basis refuse; a sole recorded migration or authenticated migration inverse is the admission path. Historical reservation scans may read exact legacy boundaries, without granting ordinary edit admission.

The current staged inverse is retained. A one-line mirror refresh in its existing reconstructed-write loop is necessary to validate destination child bindings without querying a stale derived parent clip mirror. The old 99d inverse implementation was not imported. Pure compiled reload/inverse/exact raw legacy restoration/same-ID redo and detached-provider disjoint-work/ABA/dependency guards pass.

## Source versus official artifacts

Migration predecessor canonical schema: `/home/user/work/wt/agt-m2-group-official-root-proof/astrid/core/timeline/schema/edit-command.schema.json`, SHA256 `47f67cd701ba3d2210d8b3c1f754e00eeace6078e37f610bc7b286ea17df2930`. Standalone review copy: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-group-official-root-proof/notes/edit-command.group-candidate.schema.json`. Removing only its appended migration condition and `MigrateGroupsArgs` restores the exact ordinary Bundle2 schema bytes, frozen SHA256 `472622c45fa6b5c7a425c949516a64a52d83192d3749e78a0f000decd088aee9`. All 16 existing conformance fixtures, including M1 and label goldens, remain byte-identical to a31.

Normal pin delta is exactly Agent `f423074778f4220df808799a4f7b308e56885397` (all six files), consuming Runtime `d691ddadb4ef3f5881a25fa893b4fb812211f102`, client 0.2.3, schema digest `sha256:a435dde3b552999ea75ff593868ff4d56debdd64bd8f79c134fb470a279a05e6`. This artifact contains frozen ordinary 472622 root guards. It is not a group release: migration closed args/typed exports still need a newly reviewed normal generation from the distinct candidate. No Runtime schema override, Runtime edit or fake pin was used.

The direct source pair proves official root-key admission and real CAS/normal segments transcript setup, retained v1 reads after v2/reopen, negative literal `lines` admission, and canonical-document envelope validation. Two positive real migration tests now reach the provider and fail in `_check_reservations`: the Runtime-owned 99-line helper's genuinely stored setup record has `created:[]`, while its command omits `created`; the reviewed identity scan requires exact agreement. Do not infer accepted migration, undo/redo, retry/restart or browser success. Do not weaken the production guard to accept the helper. Runtime owner should supply a reviewed helper successor with complete capture fields through genuine storage acceptance, followed by rerunning the original positive tests. A later provider failure is not inferred.

Helper comes unchanged from explicit Runtime archive `7c6e4eabf88d914d9c98c0097b06ea298ba11866`, `tests/timeline_trusted_bootstrap.py`, SHA256 `c3cdaa6b904f374cee7c17f6d61ba196909bca1e9bab0f6e200d8efe6e227c82`. Runtime code is d691; only the test helper module is imported from that archive. No SQL or invented accepted edge is added by Agent.

## Existing-lane successor: exact exports, captures and read view

The successor adds `occurrence.move` v1, a singleton exact occurrence-root selection with closed args:

```json
{"on":1,"track":"parent/track:V2","child_track":"occurrence:new-occ/track:V2"}
```

`on` is nonnegative GLOBAL seconds, rounded using existing parent fps and half-toward-positive-infinity behavior. The fixed intent is `{ripple:"none",anchor:"fixed",position:"absolute",ownership:"occurrence"}`. Parent and raw child refs must exist, have compatible output kind/activity, and the raw child ref must belong to the selected occurrence. No IDs are derived from legacy display IDs or `(shot,track)` pairs.

SDK exports, owned by `/home/user/work/wt/agt-m2-group-existing-lane-view/astrid/sdk/timeline/`:

- `occurrence_commands.capture_occurrence_move(bundle, select, on, *, track, child_track, new_child_track=None) -> list[EditCommand]` captures once on the original bundle before local preview. It returns the fully recorded authoritative batch, ready for unchanged preview/commit/retry. If needed, the caller supplies a complete `new_child_track` row with its already allocated ID; the helper composes ordinary typed `track.create` for this occurrence BEFORE `occurrence.move` in the same batch/undo. It never creates a parent track. Existing raw IDs may differ from parent IDs and remain explicitly bound on later gestures.
- `group_view.project_group_view(bundle) -> {clips,pinnedShotGroups,bindings,output}` is pure and detached from Runtime/UI. `bindings[i]` belongs to `clips[i]` and has `{occurrence,clip,raw_child_track,parent_track}`. Example: `{occurrence:"occurrence:new-occ",clip:"occurrence:new-occ/clip:c1",raw_child_track:"occurrence:new-occ/track:V2",parent_track:"parent/track:V2"}`. Parent clips use `occurrence:null`, `raw_child_track:null` and an explicit `parent/clip:<id>` ref. Adapters retain these refs; display `id`/legacy `shotId` is never an edit selector.

The command writes only placement start/lane (and existing at_ms alias) and each current canonical child clip's track. Complete canonical child order/membership, ownership, source registry, raw lane definitions, timing and destination lane contents are recorded through existing primitives. `lane.members` is scoped by an exact parent track ref, includes inactive destination members, and records membership/order. Activity reads protect inactive blockers; unrelated-lane activity edits do not conflict. Half-open collision checking ignores inactive rows. Existing inverse/rebase/provider machinery remains unchanged. Authored child track birth is typed; physical materialization is not claimed as semantic creation.

The view derives ordered `clipIds` from CURRENT canonical children, converts local authored starts through current occurrence placement, maps display lanes to the parent track and preserves authored source hold/speed/from/to and rational fps. Legacy `shotId`, mode, snapshots and opaque/null fields remain display/history metadata. Stale legacy member maps/clipIds never determine membership. Ungrouped parent clips and other canonical children remain present; unrelated migrated groups retain metadata and order. The helper does not persist a second editable group collection.

Bounded support: fixed, translation-only occurrences; complete active single-output-lane child groups for move; literal child timing supported by the migration geometry helper. Shared owners, nontranslation/follow timing, unsupported aliases/maps, incompatible or missing lane refs, multi-lane/inactive move members and out-of-extent children refuse explicitly. A positive `xfail(strict=True)` for shared-occurrence isolation retains the required successful behavior, pending the separately owned materialization carrier. No fake shot birth or carrier-WIP edit. New parent-lane and free multi-move slices remain separate.

Portable capture/record/output/read-view golden:
`/home/user/work/wt/agt-m2-group-existing-lane-view/tests/editing_conformance/fixtures/recipe_m2_group_move.json`, SHA256 `488b7f475d0a760a7ba0e268b6b6121c81bf623d60c07958153ba18ca33d5d98`. The existing migration golden remains unchanged at `tests/editing_conformance/fixtures/recipe_m2_group_migration.json`. The new test module additionally reproduces the original App `makePinnedGroupData` authored values (`clip-1`, `clip-2`, `shot-1`, images, 30fps) and asserts V1 empty / V2 `[1,3)` and `[3,5)` / hold2 / order/mode after canonical reload. The rational 30000/1001 case independently asserts 1.001/3.001 quantization; it is not silently normalized to 30fps.

Current source schema:
`/home/user/work/wt/agt-m2-group-existing-lane-view/astrid/core/timeline/schema/edit-command.schema.json`, SHA256 `2c864090806d7dacfe89ff751b0c100f389186e2f7292f4eb2db53cff2ae94d4`.
Explicit candidate copy:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-group-existing-lane-view/notes/edit-command.group-existing-lane-candidate.schema.json`.
Removing only the new occurrence condition/args definition reproduces exact 746440c4 base schema bytes. All 17 pre-existing fixture files and all six ordinary pin files remain untouched. A newly reviewed normal group schema/client generation is still REQUIRED before public release; the normal ordinary d691 artifact's permissive generic admission is only a source probe, not generated group exports.

Final targeted neighboring suites: **704 passed, 1 existing integration deselected, 1 new strict shared-isolation xfailed**, 52.15s. Ruff and targeted five-file mypy pass. The unmodified normal d691 source pair admits the new move command/canonical output (**1 passed**). The unchanged actual migration probe still has **7 passed, 2 failed** at the trusted bootstrap `command.created` omission described above. Actual accepted migration→move/retry/reopen/readback remains blocked before the first migration acceptance. No SQL, validator override, helper repair, full suite or browser was run. Exact commands and limitations:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-group-existing-lane-view/notes/report.md`.

The successor is 203 net Python product lines plus schema/tests, exceeding the <120 target because the task includes a separate pure projection, explicit same-batch typed child birth/capture and lane-membership safety. No old provider/schema/physical-birth framework was imported. Reviewed held reference is `154a70a9a2591a86f3c3f2d4b1d3f393c4a5c172` on `tl/agt-m2-retrack-recover`; its shared `notes/report.md` and source were inspected read-only.

## App outcomes and remaining boundaries

The existing-lane SDK values are now proven; App row/effect-ID/selection/one-transaction adapters, outbox accepted readback and real browser qualification still belong to App. All M2 integration remains HELD.

All three original App `it.fails` assertions in `src/tools/video-editor/hooks/useClipDrag.test.tsx` are untouched and unrun:

| Original test | Exact visible outcome still required |
|---|---|
| `commits a config edit when a free multi-clip drag drops onto a new bottom track` | V1,V2,V3 once; clip-1 at 1 on V2 and clip-2 at 3 on V3, hold 2 each; no pinned override; selection `[clip-2,clip-1]`, secondary ghosts, one transaction. |
| `updates pinnedShotGroupsOverride when a pinned group is dragged across tracks` | V1 empty; V2 ordered clip-1 `[1,3)`, clip-2 `[3,5)` with original effect IDs; both metadata lanes V2; derived group retains legacy shot-1, mode images, ordered members; selection `[clip-1,clip-2]`, one transaction. The old override assertion maps to a derived compatibility view, never a parent writer. |
| `updates pinnedShotGroupsOverride when a pinned group is dragged onto a new track` | One config gesture exposes the same ordered images group on newly created V3. The fixture drop at 3 additionally requires clip spans `[3,5)` and `[5,7)` through accepted readback; those geometry assertions are not in the original test and must be added without weakening its existing assertions. |

No App/browser or full-suite pass is claimed. Detailed exact commands and counts are in the worker `notes/report.md`.

Agentmanager02:23 actualmigrationboundary: reviewedcurrentcorecandidate746440c4 648purePASS/38registry+48actualpopup; normal0.2.3rootkeyvalidationpasses. Twooriginal/opaque positivecases remainrealFAIL at trustedbootstraprecorderhistory: record.created=[] while command.createdmissing. Runtimehelperownerrequested completeoriginalcommandcapture BEFOREaccept, no history/SQLrepair/guardweakening. No acceptedmigration/reload/undo/redo claim. Existinglane/readderivedAppview next, occurrence.deleteworker activewithstableO only. All13ops source union completeordinarydefs unchanged; newpublicgroupartifactpendingnormalfreeze.
