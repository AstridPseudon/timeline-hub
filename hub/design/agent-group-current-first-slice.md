# Current canonical group first slice — PRIVATE CANDIDATE, publication held

Owner: agt-m2-group-migration-current-first-slice. PLAN option A and the October
19 group review are unchanged. This is recovery of the reviewed first slice,
not a new group design. No integration checkout, public schema, client/pin,
Runtime source, original App test, shared dependency or history was modified.

## Exact source and packaging

Base Agent `ee896821b502ee4e51211b19d064fa44915f5777`, tree
`aa0b15850d4b777b77f54faec189cf7e4c60a7b6`. Ordinary schema is still byte-identical
at SHA256 `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`
(**55 definitions / 29 operation clauses**).

Recovered intent/source: migration `746440c4c4a6bf7dd8a89500c2bef21a3721efef`
and existing-lane/view `4a1dc1a84080effdc6a30c740303e75d9d189295`. The actual
worktree adds only `astrid/sdk/timeline/{new_group_commands,occurrence_commands,
group_view}.py` and `tests/editing_conformance/test_group_read_view.py`. These
handlers are deliberately **unregistered** in the ordinary command engine.
The pure read view and direct tests work on current ordinary code.

Executable private source is
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-group-migration-current-first-slice/notes/candidate`.
The reproducible generator is `notes/prepare_candidate.py`; it archives the
exact current base, copies those worktree helpers, and adds the reviewed
registration/admission/inverse seams only inside that private source. The
complete source delta is `notes/private-candidate.patch`, SHA256
`74f657c0308d931334361426925851a9413657d688f1261e3195e80d519a573d`.
`notes/source-audit.txt` gives the exact changed file hashes. No artifact was
normally generated or published and no compatibility of this candidate is
asserted by its generic Runtime schema admission.

Private schema: `notes/edit-command.group-private.schema.json`, SHA256
`c51d71e687e9962fd5309528d6d69d266e319ebffe9a1dc46af20be7add8afc3`,
**57 definitions / 31 clauses**. It appends only `MigrateGroupsArgs`,
`OccurrenceMoveArgs` and their two reviewed clauses. Removing them reproduces
not merely equivalent values but the exact frozen ordinary schema bytes. All
55 prior definitions/29 clauses, the four generated Python client files,
`runtime.lock.json` and the existing pin qualification test remain unchanged.
No withdrawn 10c/partial schema, private f802 carrier schema, or staged014 pin
was substituted.

## Operations and mapping

Private `timeline.migrate-groups` v1 selects `parent`, takes closed
`groups:[{legacy_shot_id,shot_id,occurrence_id}]`, and maps every group in
original authored order. IDs are supplied once by the caller. It guards the
full original group array, ordered parent membership, all consumed rows,
registry declarations, tracks and rational output, and retained input pins.
It uses the existing `Recording.create_entity` for real semantic shot and
occurrence births. The bounded shot has `items:[]`; nonempty legacy items
refuse until an explicit reviewed semantic item mapping exists. There are no
fake physical-slot creation records or caller-authorized id_map entries.

Complete group metadata, mode, snapshots, null/opaque fields and ordered
`{legacy_clip_id,clip_id}` mapping remain under the occurrence's
`provenance.group_migration`. Parent ungrouped rows, unknown fields and order
survive. Member rows become canonical children with local starts; exact raw
original restoration uses accepted recorded writes and existing collection
order/inverse machinery, never a second editable group store or a converter.
The sanitizer is not called. The graph exception matches only the exact token
path `occurrences[index].provenance.group_migration.legacy_group`.

Interleaved/reordered/duplicate-shot-ID groups, duplicated/shared/missing
members, nonempty legacy items, occupied destinations, divergent mirrors or
registries, ambiguous lane aliases, following timing/maps, and unrepresentable
geometry refuse without changing the supplied document. Ordinary edits cannot
use a legacy basis; migration is a sole command, and legacy inverse admission
requires authenticated migration/inverse history.

Private `occurrence.move` v1 selects an exact occurrence root and takes closed
`{on,track,child_track}`. `on` is global seconds quantized with the existing
parent rational-fps policy. Parent/raw child destination refs are explicit and
existing; the whole-group temporal move writes occurrence placement and
atomically retracks current raw children. It records membership/order and
lane occupancy, with half-open collisions. Ordinary movement never rewrites a
whole parent/group array. Shared-source derived owners explicitly refuse until
the materialization carrier is qualified; display IDs or `(shotId,trackId)`
never infer ownership. The recovered optional typed child-lane composition is
kept internal; no new-parent-track or free multi-drag milestone is claimed.

`project_group_view(bundle)` is pure. `pinnedShotGroups` in its return is a
read-side compatibility projection, not persisted editing state. Current
canonical child membership supplies clipIds; provenance supplies display
metadata only. Parallel bindings explicitly carry occurrence, scoped raw clip,
raw child track and parent track. Canonical children without migration metadata
remain visible without invented legacy groups. Parent/child duplicate display
IDs remain distinguishable through the bindings. Unsupported maps and legacy
unmigrated input refuse. Source windows/hold/speed, metadata and rational output
are retained.

## Current-code corrections, not a new framework

1. New canonical occurrence records explicitly include `gain:1`, matching the
   current `occurrence.create` birth. The recovered old omission was accepted
   but Runtime materialized gain=1 while retained payload omitted it, causing
   `occurrence_field_mismatch` and refusal on reopen. Adding the default at the
   NEW birth fixes integrity without modifying the legacy input or its inverse.
2. Current `_validate_inputs.proven_sites` needs one `staged.compile_mirrors()`
   after each reconstructed forward write. The existing reverse-stage refresh
   already exists. Without the forward refresh, restoring removed parent clips
   fails against a stale config.clips mirror. This change is PRIVATE only.
3. Private selections `migration.groups` and `lane.members` and the reviewed
   lane-selection overlap support are restored onto current recorder/collections.
   No generic authoring context, journal, DTO, SourceFactory, endpoint or root
   replacement API is introduced.
4. Shared-source authoring owners are recognized through the existing canonical
   `/shot` mapping and refuse before writes/births. Merely opening a repeated
   source into independent authoring owners does not qualify physical ownership.

## Real source/setup and tests

Real Runtime product probe: archived
`a51af885ea631c695a857985239c7fe7bf2e871f`, tree
`7c6ab6700307309a7942e64eb4d0c6c7cc42b681`, through the normal locator. This
is a source probe with the unchanged ordinary provider/client pin, not a new
matched generated cohort. It uses actual Runtime acceptance and retained reads;
no live socket/HTTP, SQL, fabricated accepted history, retired writer or guard
override is involved.

The explicitly requested helper382f was tested first, unchanged:
**7 passed / 2 failed** at `semantic identity boundary differs from writes`.
It does contain both `created:[]` lists, but its raw parent-root write remains
incompatible with authored State. This is evidence the requested helper source
is stale; no Agent guard was relaxed.

A previously reviewed Runtime-owned successor already exists:
`54db299d6ebb9ec98649895760a4cd37cee6c147`, helper SHA256
`9f61af7be9518aa9d2442091257d6cdae99c65db0773377a53244f8807b30e13`.
It changes only trusted TEST SETUP to existing whole-closure timeline RootPins
before request/record acceptance; full legacy bytes and created arrays stay
intact. This successor was selected explicitly in the PRIVATE candidate only.
It is not silently adopted as a public pin or a product operation.

Final actual Runtime lane: **11 passed in 4.90s**. This includes the original
nine cases with every positive assertion live, plus two current-source cases:

- Real managed PNG CAS and real media.transcript/v1 `segments` Document exist
  BEFORE the exact 30000/1001 legacy parent + DocumentPins setup.
- Accepted migration, canonical reload, transcript-v2/reopen retention, exact raw
  original guarded undo and same-ID redo. Both normal and opaque variants pass.
- Existing authored V2 move displays c1 at1.001/c2 at3.001, both hold2 onV2,
  current ordered images membership, retained pin, healthy integrity, restart,
  grouped migration+move exact raw undo and redo.
- Two migrated groups commit independently; a stale first-group move actually
  returns `rebased` after the other group's move, preserving that group's exact
  children/metadata. Removing the touched canonical owner then submitting a
  previously captured move refuses and leaves accepted head/closure unchanged.

Current ordinary worktree tests: **37 passed**, including ten new pure-view /
geometry / shared-owner guard cases and document neighbors. Private inverse /
root / semantic-reservation neighbors: **204 passed**. Private recovered group
suite plus current-policy tests: **83 passed / 2 failed**. Both failures retain
old spike assertions that ordinary equal-state activity/selection ABA must be
refused. Current settled replay intentionally uses identities-only intervening
checks and validates values/membership on final head. No code changed this
policy and neither assertion was removed/weakened/marked. New direct cases
prove changed birth/removal/order/lane membership conflicts, and strict undo
continues to reject same-value writes/lane ABA. The two diagnostic failures
remain explicit for orchestrator review, not an all-green recovered suite claim.

Ruff (product plus isolated direct test checks), schema/pin byte audit and git
diff check pass. Fixtures are generated at test time; no giant golden is added.
All new test modules are under500 lines. Commands and logs: worker
`notes/report.md`. No full*, HTTP/browser/App, renderer, macOS, or public normal
artifact-generation lane was run.

## App outcomes and open dependencies

Original App three `it.fails` stay byte-identical and unrun:

| Original outcome | This slice |
| --- | --- |
| Existing-lane pinned drag: V1 empty, V2 clip1[1,3),clip2[3,5), hold2, images order/mode, effect IDs, selection, one transaction | Exact30fps authored fixture values pass privately through canonical compile/reload/view. Real rational fixture additionally passes1.001/3.001 onV2. App effect/selection/transaction adaptation is UNQUALIFIED. |
| New-lane pinned drag ontoV3: [3,5),[5,7), same ordered images metadata | Not this existing-lane slice; original positive remains open. |
| Free multi-drag onto new bottomV3: V1/V2/V3 once, clip1[1,3)onV2,clip2[3,5)onV3, selection[clip2,clip1], ghosts, one transaction | Not this occurrence-owned group slice; original positive remains open. |

Peer carrier source is now reviewed private Runtime
`7b8d6d9afe963e2b7a6c6b32fd4e3797451090da`, tree
`d20b745c26a33c2ea4e20863f846335c8cf33e1e`, preserving current catalog-head
fences on81f over83fe. Its Agent counterpart remains3730/f802 (**48/22**),
not the full ordinary55/29 floor. It was NOT substituted here. No reviewed
full55/29+group+carrier union or matched normal artifact currently exists.
`notes/peer-coordination.md` records the exact dependency request and probe update.

Before public source/schema freeze, peers must agree the exact full current
carrier/sourceRef join and normal generation. This read view exports explicit
owner bindings, but does not invent a new public `sourceRef` contract. Shared
physical remapping and semantic item births remain outside the supported slice.
Public release, App adapter/browser qualification and the other two drag
outcomes are OPEN. The worker leaves BLOCKED for this final cohort dependency;
the private executable recovery and pure worktree code are complete/reviewable.
