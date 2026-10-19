# M2 group ownership audit — design only

2026-10-19, `agt-m2-group-audit`. Sources: Agent `a8eb28af525e`, App
`2d8eac72eb59`; Runtime persistence inspected read-only at `82df3cf0f462`.
App advanced to `dd376d5e0389` during the audit; its diff changes only four e2e
files, so all inspected product sources and the offline probe inputs are unchanged.
Read PLAN, edit-recipe, m2-move-draft and Agent STATUS. No product/test edits,
implementation, merge authorization or M1 browser evidence.

## Finding and recommended decision

**The three fixtures own parent clips in an App-authored
`config.pinnedShotGroups` array. That field is neither an override cache nor a
current canonical shot/occurrence group contract.** Main's lossless
`CanonicalDocument` authoring codec can retain it, but the separate canonical
shot-composition graph treats it as migration-only; App's normal canonical
projection omits it. Consequently the draft cannot yet call a parent soft-tag
row the canonical group of an occurrence's children.

**Proposed contract decision, requiring Agent/App owner approval:** for the first
three parent-clip fixtures, reuse the existing authored parent
`config.pinnedShotGroups` rows, with an explicit read-side compatibility view.
Do not introduce another store, persisted group ID, transport field or copy on
each occurrence. This is the smallest storage reuse, but continuing that
migration-only field as editable soft tags must be approved explicitly. If
canonical-only migration wins, the existing alternative is a pinned shot plus
an occurrence, and its group drag is an occurrence-placement edit, which the
current draft excludes. Do not silently substitute that different operation.
Evidence: source map below and both offline probes; actual publication/readback
of these groups is **UNRUN**.

## Source map and concrete shapes

Paths prefixed `A/`, `P/`, `R/` mean the Agent worktree, read-only App integration
and Runtime integration respectively. Line numbers refer to the heads above.

| Boundary | Exact source evidence |
| --- | --- |
| Existing authored App group | `P/src/tools/video-editor/types/index.ts:463` defines ordered `clipIds`, `shotId`, `trackId`, optional mode/name/video/snapshot/pool/lineage. `P/src/tools/video-editor/hooks/useClipDrag.test.tsx:191` constructs the exact group fixtures below. No `memberSelectors` or `ownerOccurrenceId` is declared in this main group type. |
| Group identity | `P/src/tools/video-editor/lib/pinned-group-projection.ts:4` uses `(shotId,trackId)`; `:65` first matches that pair, with UI lane-repair fallback at `:32`. `P/src/tools/video-editor/lib/timeline-domain.ts:344` derives display ID `shotId:trackId`. Neither is a separately persisted stable ID. The pair changes on retrack; `shotId` alone must not be presumed unique across lanes. |
| Group member order versus span | `P/src/tools/video-editor/lib/shot-group-commands.ts:53` builds `clipIds` ordered by live `at`; `pinned-group-projection.ts:151` preserves input order on ties and unknown IDs at the end. `timeline-domain.ts:362` resolves members and `:392` sorts the view by time. There is no authored group start/end/span reference in this type: bounds derive from member intervals. Legacy `start/children` repair is at `timeline-domain.ts:880`. |
| Ordinary clip/lane order | `P/src/tools/video-editor/lib/timeline-data.ts:226` derives rows and per-lane `clipOrder` by walking authored `tracks[]` and `clips[]`; `:296` writes clips in track order, retained per-lane order, then appended IDs. `clipOrder`, row actions/effect IDs and reader `renderGroups` (`lib/timeline-reader.ts:1021`) are projections, not new persistence collections. |
| App encode | `P/src/tools/video-editor/lib/serialize.ts:33` carries pinned groups; `timeline-domain.ts:2706` serializes the pair. However `timeline-domain.ts:292` copies only known group fields: the probe's `opaque:{keep:null}` disappears. `timeline-data.ts:317` reconstructs clip fields and timing. Neither is a lossless M2 authoring materializer. |
| Legacy publication and read | `P/src/integrations/runtime/dataProvider.ts:949` merges config and reconciles parent clips; `:1007` calls `publishParentComposition`. `:1277` reads immutable parent payload; `:1311` returns config and canonical clips. This proves the old source path, not permission to use it: `R/runtime_protocol/service.py:3180` rejects this publisher once the timeline has command history (`timeline_commit_required`). |
| Sole command codec | `A/astrid/sdk/timeline/commit.py:146` opens exact immutable images; `:161` compiles via main and closes reused images. `A/astrid/core/timeline/authoring_bundle.py:1028` copies the full authored parent and adds compiled occurrences. `P/src/tools/video-editor/commands/authoringBundle.ts:100` copies parent bytes and materializes the same scoped owners. Python probe confirms a raw group survives encode→JSON→decode. This proves preservation, not a registered group operation. |
| Undo authority | `P/src/tools/video-editor/commands/commitSession.ts:306` cancels a local unsent intent, refuses uncertain in-flight undo, or emits `timeline.inverse` naming the accepted publication at `:326`. The snapshot-only `CanonicalShotCompositionHistory` at `data/shotCompositionEditor.ts:663` is not guarded accepted history and must not become M2's undo path. Command `group_id` groups undo intent; it is not a shot-group identity. |
| Physical persistence/read | Realm SQLite is `R/runtime_protocol/store.py:712` (`realm.sqlite3`). `R/runtime_protocol/timeline_commit_store.py:600` stores internal/shot JSON, `:629` parent `payload_json`, `:632` occurrence rows with ordinal/placement/track. `R/runtime_protocol/service.py:2530` returns `json.loads(payload_json)` from the exact revision. Schema: `R/runtime_protocol/canonical_schema.py:341`. `project_shots`, `shot_items` and `composition_revision_occurrences` are populated from accepted payload at `timeline_commit_store.py:610`; they are not a soft-tag edit authority. No DB was opened or written by this audit. |
| Canonical ownership is different | `A/astrid/core/timeline/shot_composition.py:340` recursively rejects `pinnedShotGroups`; `:504` invokes that check. `P/src/tools/video-editor/data/shotComposition.ts:96` rejects the root key (not the same recursive check). `P/.../shotCompositionProjection.ts:567` constructs output config without pinned groups; probe confirms omission even when supplied in base config. Do not mistake TS acceptance of a nested opaque field for Python graph acceptance. |
| Migration already exists | `A/astrid/core/timeline/shot_composition_migration.py:408` requires unique, contiguous parent members in authored order; `:828` copies clips to a shot's internal timeline with relative starts; `:846` constructs occurrence provenance; `:866` removes the parent group array and member clips. This is a conversion, not a lossless same-shape group-row move. |

Actual authored App fixture shape (excerpt of `useClipDrag.test.tsx:194`):

```json
{
  "config": {
    "tracks": [{"id":"V1","kind":"visual"},{"id":"V2","kind":"visual"}],
    "clips": [
      {"id":"clip-1","at":0,"track":"V1","clipType":"hold","hold":2},
      {"id":"clip-2","at":2,"track":"V1","clipType":"hold","hold":2}
    ],
    "pinnedShotGroups": [
      {"shotId":"shot-1","trackId":"V1","clipIds":["clip-1","clip-2"],"mode":"images"}
    ]
  }
}
```

Derived values are `clipOrder:{V1:["clip-1","clip-2"],V2:[]}`, group display ID
`shot-1:V1`, bounding interval `[0,4)`. A local
`pinnedShotGroupsOverride:[{...group,trackId:"V2"}]` is an instruction to replace
the authored array during preview (`P/lib/timeline-mutation-engine.ts:188`, under
`src/tools/video-editor/`); the `Override` key itself is not saved group ownership.

By comparison, actual `commands/fixtures/authoringBundle.json`, case
`trimmed-child` (single-line fixture), contains this canonical occurrence/child
excerpt; these are two ownership levels, not an alternative soft-tag row:

```json
{
  "occurrence": {
    "occurrence_id":"occ-0","shot_id":"source-shot","shot_revision_id":"shot-r1",
    "placement":{"start_ms":10000,"track":"picture"},
    "duration_ms":10000,"source_offset":0,"speed":1
  },
  "internalClip": {
    "id":"raw-child-clip","track":"picture","asset":"media",
    "at":1,"from":2,"to":8,"speed":2
  }
}
```

Parent lane is the occurrence placement's lane; child lane is in the pinned
internal timeline. The child's source window is `[2,8)` at speed 2, not the
occurrence span. Projection creates occurrence-qualified display IDs, preserving
`rawClipId`, `ownerRef`, `clipRef` at
`P/src/tools/video-editor/data/shotCompositionProjection.ts:334`. Probe sample:
`occ-1:alpha-video` → `occurrence:occ-1/clip:alpha-video`. Never parse a display
ID or media alias to infer ownership. Main copies internal bytes unchanged while
materializing independent repeated-shot owners and known item references
(`A/authoring_bundle.py:218`, `:403`, under `astrid/core/timeline/`;
`P/commands/authoringBundle.ts:160`, under `src/tools/video-editor/`). Do not
conflate asset aliases, shot-item IDs, raw clip IDs and occurrence IDs.

## Recorder mapping and exact inverse

Existing primitives are `A/astrid/sdk/timeline/_recording.py:43` (read/select/bind),
`:64` (tagged before/after, including unchanged writes), `:85` (create).
`_command_state.py:144` resolves only existing entity kinds; `:204` writes a full
row or a dict property. Array-index mutation is not supported. Current queries
are only `move.target`, `track.create`, `move.blockers` (`_recording.py:15`).
All move-set queries in the draft are therefore proposed, not current APIs.

| Requested effect | Existing support / genuinely needed change |
| --- | --- |
| Add/delete/update/reorder soft tags | A guarded write/clear of `parent`, path `["config","pinnedShotGroups"]`, already represents the entire raw array, including absent/null/empty distinctions and complete objects. It can add/remove/reorder rows without a new store or group ID. Python primitive probe restores exact bytes. This is conservative: concurrent edits to any row conflict. A semantic per-row primitive is needed only to promise independent row concurrency; it is not required by these three fixtures. |
| Group retrack | Translate every selected raw clip once, write each `track`, update the matching group's `trackId` while preserving its complete object, `clipIds`, mode, snapshots and original array position. Do not rebuild through App's lossy clone. If using per-row addresses, bind the original exact `(shotId,trackId)` tuple; old present→absent and destination absent→present must be one guarded relocation. Refuse duplicate keys and occupied destination. Frozen R4 `astrid/sdk/timeline/shot_groups.py:27` encodes that tuple as base64url JSON; it is an address convention, not proof of a main persistent identity. |
| Clip order | The three exact examples already have the required raw clip order: changing tracks yields the expected projected per-lane order without rearranging `clips[]`. The draft's **general** promise to append incoming clips in explicit `members` order needs a reusable owner-scoped collection-order primitive when the existing array differs. Record complete ordered stable refs before/after; reorder full existing objects, not reconstructed rows; derive App `clipOrder`. Do not persist another order map. |
| Row create/delete/order | Existing track create appends and reserves the ID. `State.set` restores a deleted row by append (`_command_state.py:208`); probe `[A,B]→delete A→restore A` yields `[B,A]`. Exact middle-row restoration and explicit reorder genuinely need collection-position/order restoration. Bottom append alone does not need a new lane-order operation. |

For a future order/per-row primitive, record collection membership/order and the
row's absence/presence with ownership edges. Extend overlap checks between a
collection address and its member addresses: current token overlap compares
equal entity refs (`_command_state.py:109`), so replacing `parent.clips` cannot
silently stand in for writes addressed as `parent/clip:c`. Preserve the current
top-level/config clip alias rule and derived mirror compilation
(`_recording.py:113`); do not author two independent clip arrays. Whole-array
group writes and future semantic row writes likewise need common overlap rules
if both address spellings are admitted. These changes are **UNIMPLEMENTED/UNRUN**;
the probes establish current limits, not conformance of a proposed primitive.

Exact guarded inverse must retain first-before/last-after including presence,
full raw group/clip/track objects and order; restore starts/source fields and
group key, then recompile mirrors/timing. Verify original read/selection/identity
guards and complete publication ancestry; overlapping same-value/ABA writes
still refuse. Existing mechanics: `inverse.py:24`, `:46`, `:105`. Do not replace
them with snapshots or a new undo stack.

There is also a concrete composed-batch gap: `inverse.py:138` checks created-track
dependents **before** reversing the batch's moves (`:142`). The primitive probe
of create C + move its own clip to C refuses with `created track has surviving
dependents`. The shared inverse must distinguish dependents removed by the
guarded reversing batch from surviving later dependents, stage that reversal,
then remove the empty track; it must still refuse later clips/references.
This is a required future fix, not evidence that grouped undo currently works.
Keep ID reservations monotonic (`commit.py:317`); retrack does not allocate a new
group, and track create/retry/redo must use the original reserved ID.

## Preserve the three fixtures exactly

All remain `it.fails` in `P/src/tools/video-editor/hooks/useClipDrag.test.tsx`.
No assertions or tests were edited. The offline planner checks use V3 already
present to test geometry; they do **not** exercise track creation or dispatch.

| Exact test name / line | Required authored outcome |
| --- | --- |
| `commits a config edit when a free multi-clip drag drops onto a new bottom track` / 827 | Create V3 once; ordered selection/members `[clip-2,clip-1]`; anchor clip-2 from 2/V2 to 3/V3, clip-1 from 0/V1 to 1/V2; hold 2 each, lanes V1,V2,V3, no pinned override, secondary ghosts, one transaction. |
| `updates pinnedShotGroupsOverride when a pinned group is dragged across tracks` / 1173 | Both parent clips move V1→V2 by +1: `[1,3)`, `[3,5)`; V1 empty, V2 order c1,c2; same group at V2 with ordered membership/mode preserved; one transaction and selection. |
| `updates pinnedShotGroupsOverride when a pinned group is dragged onto a new track` / 1283 | Create V3 once; group moves by +3: `[3,5)`, `[5,7)` there; group track V3, ordered membership/mode retained. Existing test checks config/group; draft's extra geometry and accepted-readback coverage remains required. |

Planner evidence: `P/src/tools/video-editor/lib/multi-drag-utils.ts:193` computes
row delta and expands complete groups; `:224` explicitly leaves group-row update
to caller; `:351` applies moves; `:480` derives clip order. Its collision path can
change source windows (`:470`); do not port that as fixed-window move semantics.
`clip-drag-planner.ts:329` also resolves UI targets/snaps/routes; these are not
authoritative replay choices. Keep the draft's original frozen basis, common
translation/relative offsets, source windows, explicit collision refusal and
original guards. Runtime local door, dependent B, sole recorder and no-receipts
decisions are unchanged.

## Owner handoff and verification limits

1. Agent/App: approve or reject continued **authored soft-tag** use of the existing
   parent array versus canonical occurrence conversion. Main has no demonstrated
   canonical persisted soft-tag contract after migration. Do not add the draft's
   `memberSelectors`/`ownerOccurrenceId` fields by assumption. The three fixtures
   need only parent clips; occurrence-local free selections retain scoped refs
   and main materialization. For a parent group naming occurrence children,
   explicit persisted scoped provenance and its codec/migration are missing;
   fail ambiguous repeated IDs. Evidence: type/projection/migration/codec rows
   above. Such publication and occurrence-group interoperability are **UNRUN**.
2. Agent: choose conservative whole-array group conflicts for this first slice,
   or require per-row concurrency now. Prefer existing whole-array recording for
   the three fixtures; order restoration is a separate real shared-primitive
   gap. Before implementing the draft's broader append/order claim, add the
   collection-order and composed-inverse proofs to the existing conformance
   suites, including exact unknown fields/absence, reordered membership,
   same-value/ABA publications and later dependents. Evidence: primitive probes
   and recorder/inverse lines above. Those suite proofs are **UNRUN**.
3. App: preserve original success assertions; observe the command service's
   preview/accepted result rather than restoring legacy publication authority.
   Current single move refuses groups/retrack
   (`P/src/tools/video-editor/commands/semanticGestures.ts:62`, `:77`). Flip the
   exact three expected failures only with capture→preview→commit/readback→grouped
   inverse coverage. Evidence: fixture lines and three planner probes above.
   Hook suites and real browser coverage are **UNRUN** by this audit.

Offline commands run (both final runs exit **0**); set
`W=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/agt-m2-group-audit`:

```bash
# cwd /home/user/work/app; installed tsx loader, no IPC/servers/install
TSX_TSCONFIG_PATH="$W/tsconfig.json" node --import /home/user/work/app/node_modules/tsx/dist/loader.mjs "$W/probe.mts"
# cwd /home/user/work/wt/agt-m2-group-audit
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/home/user/work/wt/agt-m2-group-audit /home/user/work/venv-agent/bin/python "$W/probe.py"
```

Final output: `W/probe-ts.log`, `W/probe-python.log`. TS: known group-field
round-trip, observed unknown-field loss, stable equal-time ordering, three drag
plans, canonical group omission and scoped clip identity. Python: lossless raw
group encode/decode, graph rejection, unsupported group entity, nonexact row
restore order, exact whole-group-array primitive inverse, composed-track inverse
refusal. Scripts assert observations; they are external audit probes, not tests
of an implemented M2 command. Initial TS attempts exposed missing bundler aliases
(external tsconfig now mirrors existing workspace aliases), probe track/signature
mistakes (corrected), and the real opaque-field loss (retained as a finding).

No pytest/vitest repository suites, full suite, sockets, live publish/readback,
crash/restart/outbox, browser, renderer or macOS tests were run. No full test
request was submitted for this design-only task. Product worktree remains clean.
