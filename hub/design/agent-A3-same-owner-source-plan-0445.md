# A3 / R1 / G3 same-selected-owner source proposal — 0445

**Design PASS; carrier/production acceptance FAIL — NO-CARRIER, NOT DONE.**
This is an unapplied proposal, requiring orchestrator freeze/contract disposition.
No product, test, schema, generated artifact, producer, lock or pin was changed.
PLAN §§1,3; C0 §§1–5; BOARD-HEADER frozen Runtime34e/ad823 and mounted-caller rule govern.

## Identity and reused evidence

Worker: `agt-A3-same-owner-plan-0445`.
Inspected worker Agent HEAD `9729c07b764ba6cce1bb31686cb93d29fc72b14d`;
read-only integration snapshots: Agent `f95f1e1691b82dce74a49eb7ca444f97eb364037`,
Runtime `62c454ac07fb46a1a67847d933f1ed5f53043e30`.
Agent `runtime.lock.json` still names `34eac0041b0891e9011966b39bcbd26053fde5bc`.
These source snapshots are not claims about an installed new producer.

Reuse independent0422 exactly: `design/agent-A3-fork-carrier-review-0422.md`,
worker `agt-A3-fork-carrier-review-0422/log.txt`, evidence at lines 8503–8539.
Its native command was `PYTHONPATH=. /home/user/work/venv-agent/bin/python - <<'PY'`
over `tests/editing_conformance/fixtures/recipe_m2_occurrence_duplicate.json`.
Recorded result: count **2 → 3**, order **[occ-0, occ-1, occ-copy]**, created
`shot:shot-copy` and `occurrence:occ-copy`. The probe was NOT repeated here.
The independent worker's final report is only a summary; its log retains the
actual command and output. This is prior evidence, not a test run by 0445.

Required same-owner shape instead:

```text
before: occ-0 -> shot-image S0 -> internal-image I0
        occ-1 -> shot-image S0 -> internal-image I0
after:  occ-0 -> shot-image S1 -> internal-image I1   (selected gesture only)
        occ-1 -> shot-image S0 -> internal-image I0   (exact original)
```

Also require distinct shot images S0/T0 sharing I0: only selected S0's owner
gets S1/I1; T0/I0 remain exact. Closure images have revision identity; an entity
ID is only an alias (C0c). Preserve occurrence count/order, occurrence IDs,
existing shot/entity IDs, raw clip/track/item/asset IDs, occurrence timing/map,
unmodified source windows and every opaque/authored field. Only the actual ADD,
SWAP or placement operands change; ADD naturally introduces its reserved clip
and possibly asset alias. Fresh physical revision IDs and managed pins are the
necessary provider outputs, not an exception allowing unrelated ID changes.

## Source finding and smallest proposed semantic surface

`astrid/sdk/timeline/commands.py:operations()` registers occurrence create,
duplicate, add-media, swap-media and placement commands; there is no registered
same-owner fork command. `native_occurrence_duplicate.py:occurrence_duplicate()`
calls `create_entity()` twice, deliberately creating another occurrence.
Do not alter its meaning, compose duplicate/delete, or patch managed edges.

`native_occurrence_media_commands.py:_exclusive()` guards authored shot owners,
not all physical internal-image owners. ADD calls it. Source correction to
0418/0422's broad wording: `_swap()` does **not** itself call `_exclusive()` in
this worker snapshot; do not claim a newly observed SWAP rejection or passing
shared SWAP witness. Neither fact supplies the missing, ID-preserving physical
isolation contract. `native_placement_commands.py` guards shared ownership in
move/create/unplace. Distinct shots sharing one internal image must be handled
from the verified closure, not inferred safe from `placement.owners`.

Recommended smallest surface: an explicit OPTIONAL
`args.materialize: "selected-occurrence"` on the existing registered
`occurrence.add-media`, `occurrence.swap-media`, `placement.create` and
occurrence-selected `placement.move` families. This spelling is **PROPOSED,
currently unsupported**, not an existing App command. No new op, standalone
fork transaction, producer or caller capability is introduced by this document.
Omission retains the current command contract; reject the marker for parent
selection and for unrelated operations. This gives one authenticated semantic
gesture/step, avoiding an independently undoable preparatory fork with a live
consumer. If the orchestrator requires a separate registered fork command,
that is a different schema decision and needs a follow-up brief.

Proposed command fragments (NOT HTTP bodies; do not send to frozen Runtime):

```text
occurrence.add-media v1 select=occurrence:occ-0
  args={row:<existing exact raw ADD row>, media:<verified MediaSelection>,
        consumed:<raw IDs actually consulted>, materialize:"selected-occurrence"}
occurrence.swap-media v1 select=occurrence:occ-0/clip:<raw-id>
  args={old_media:<exact old MediaSelection>, media:<verified new selection>,
        materialize:"selected-occurrence"}
placement.create v1 select=occurrence:occ-0
  args={id:<reserved raw clip ID>, on:<absolute seconds>, hold:<seconds>,
        media:<verified image selection>, consumed:<consulted raw IDs>,
        materialize:"selected-occurrence"}
placement.move v1 select=occurrence:occ-0/clip:<raw-id>
  args={on:<absolute seconds>, materialize:"selected-occurrence"}
```

All retain `schema_version:1`, `version:"1"` and their current intent (including
move's full existing intent), captured claims and guards. Fresh physical roots
are provider-derived revisions, not caller-created entities: command `created`
contains ONLY the actual ADD/placement clip and new registry alias when born;
SWAP-to-existing-alias and move create no entity IDs. No created occurrence,
shot or item claim, fabricated revision ref, nonidentity `id_map`, or request
allocation proof is allowed. Reserve raw births once across outbox retries;
physical successors derive deterministically from verified source image,
selected owner and sequential gesture result. A no-op must not fork for its
own sake. Do not mutate payloads merely to force a different digest.

## Exact implementation boundary after authorization

| Repo / canonical file | Narrow proposed change |
| --- | --- |
| Agent `astrid/core/timeline/schema/edit-command.schema.json` | Add optional const marker to the two occurrence media arg schemas and PlacementCreateArgs; give placement.move its own PlacementMoveArgs instead of expanding shared ClipMoveArgs. OccurrenceSwapMediaArgs is also used by parent clip.swap-media: constrain that branch to forbid the marker (or split the occurrence-only args). Keep closed properties and all existing requirements. |
| Runtime `contract/schemas/edit-command.json` | Publish identical authorized semantic schema additions; this is a contract/producer change, not a consumer-only edit. |
| Agent `astrid/sdk/timeline/commands.py` | Point placement.move registry parameters to its new args definition; retain operation names, versions, singleton cardinality and existing intent. |
| Agent `astrid/sdk/timeline/native_occurrence_media_commands.py` | Recognize explicit marker before ADD/SWAP mutation; capture selected physical owner and source. Apply existing verified media, map, timing, registry, consumed-input and alias guards unchanged. Keep the shared refusal unless this exact isolation path was requested and recorded. |
| Agent `astrid/sdk/timeline/native_placement_commands.py` | Carry the same marker through placement.create's call into add_media; use the same selected-owner isolation for move. No timing, global/local conversion or automatic lane algorithm change. Unplace is outside this brief. |
| Agent `astrid/sdk/timeline/_recording.py` / `_command_state.py` | Record source/owner observations and a provider-private per-owner projection marker; preserve existing raw state and IDs. Do not turn the marker into caller-authored binding authority or use shot-ID owner counts as physical-image evidence. |
| Agent `astrid/sdk/timeline/_doc_patch_materialize.py` and `commit.py:document_from_bundle()` | Extend the existing physical-image projection boundary with an occurrence-semantic mode. Unlike remember(), which expands all owners, target exactly the selected owner. Reverse virtual item remaps back to original raw IDs before publishing, retain source shot and internal entity IDs, and emit only S1/I1 plus selected reattachment. Existing generic patch projection retains shared-image semantics. |
| Agent `astrid/sdk/timeline/_commit_patch.py` | Use effect_diff and materializations with actual physical before/after images; capture selected owner lineage even when old images stay reachable. Preserve authored field captures, step boundary, exact bindings and complete structural effects. Do not bypass the current skip for authored shot_id replacement; this proposal keeps shot_id unchanged. |
| Agent `astrid/sdk/timeline/inverse.py` | Restore/replay selected physical edge through authenticated step boundaries; do not let inverse's remember(all owners) broadcast a selected-owner inverse. Reuse original IDs, allocation provenance and later-history scans. |
| Runtime `runtime_protocol/timeline_commit_auth.py` | Authenticate source/successor relation against exact selected occurrence edge and step/effect boundary. Its _physical_owner currently returns the first matching owner: replace that inference in the new path with the recorded exact owner plus full verified owner set. Equal payloads or first match are not provenance. |
| Runtime `runtime_protocol/timeline_commit_store.py` | Audit _check_shot_destinations/_same_materialization_slot against two reachable revisions of one shot and repeated raw item IDs across its revisions. Preserve foreign-project/catalog-head occupancy, global allocation reservations, ancestry, publication CAS and receipt checks. If multiple same-shot writes are required, distinguish immutable revision images from new entity allocations without relaxing cross-shot item ownership. |
| Runtime `runtime_protocol/timeline_materialization.py` | Existing materialization_join requires destination shot != source shot and remapped item allocations. Do NOT force this same-entity revision turnover into that format or weaken its checks. Use the C0c commit.materialization lineage for revision turnover, authenticated by timeline_commit_auth; preserve the older allocation join unchanged. |
| Runtime `runtime_protocol/timeline_commit_port.py`, `timeline_commit_execution.py`, `timeline_commit_validation.py` | Preserve existing request-private input verification, coordinator, CAS, idempotency and schema validation. No second executor/store/route. Extend only if exact new physical-boundary verification requires it. |

Important compiler obstruction: `authoring_bundle.py:_copy_shot_for_placement()`
remaps item IDs when the authoring shot differs from the source;
`compile_authoring_candidate()` then uses the authoring shot as a new entity.
`commit.py:document_from_bundle()` currently restores unchanged original pins.
Calling these paths unmodified is not the promised isolation. Reuse the
physical projection boundary above instead of changing all authoring callers
or treating virtual authoring IDs as new requested entity IDs. This remains
an implementation proposal, not a claim that the listed edits are sufficient
without the bounded tests below.

Generation AFTER exception only: Runtime `generators/generate.py`,
`generators/timeline_commit_types.py`, `generators/timeline_commit_resources.py`
produce the clients and `runtime_protocol/schemas/timeline-commit-bundle.json`;
validate artifact manifest through existing tooling. Agent adopts using
`scripts/refresh_runtime_client.py` and its `runtime.lock.json`; App adopts
through its own refresh tools. Do not hand-edit vendored generated copies or
published schema floors. No generation or pin advancement is authorized here.

## Reads, effects, replay, undo and full v2 preservation

Capture at the sequential command boundary: selected occurrence row and exact
shot pin, shot wrapper/source binding and complete shot/internal authored
payloads; the complete physical owner set/path for each source image; clip and
track membership/order actually consulted; all consumed media/registry/window/
timing/lane inputs already required by the recipe; exact verified media pins.
Whole-source reads are conservative but honest for a copying transform. A
shared-source change may conflict even when a later optimization could merge.
Caller gesture reads remain declared, not inferred from a byte diff. Persist
owner-bound input/output bindings and `commit.materialization` source/successor,
owner, edge_before/edge_after, evaluated head, step and command ordinals.

Effects: create I1 payload, create S1 payload (with its managed I1 pin), then set
only `parent/[occurrences,occurrence_id:occ-0,shot_revision_id]` from S0 to S1.
Use revision-qualified root refs in the physical union. Retain S0/I0 if any
other owner reaches them; remove only roots actually leaving this boundary.
Record complete ADD/SWAP/move authored changes with both physical bindings and
causal step. No parent occurrence list replacement/order mutation and no
authored shot_id write. Wrappers, digests and manifest pins remain Runtime-owned.
Submitted step patches can be empty semantic assertions; they cannot authorize
root creation or managed-edge writes as doc.patch. Same C0 final validation,
including D12 preservation of unrelated legacy declarations, applies.

Rebase: execute/verify at base then replay against authenticated landing head.
Guard occurrence existence, exact source binding and source content, reads,
collections and all written fields across intervening history including ABA.
Only uniquely proven same-owner successors may continue a binding; another
owner's fork leaves the original binding on its still-reachable image. Ambiguous
aliases, unrelated reattachment, missing provenance and unknown history refuse
with existing structured reasons. Compare full physical owner sets explicitly;
never normalize a shared old root globally to the selected successor.
Exact retry/key returns the original durable envelope, without extra revisions,
allocations or history; unknown outcome retries the unchanged request/key first.

Undo uses the existing timeline.inverse v1 (`select:null`,
`args.publications:[<accepted publication>]`, optional
`args.steps:{<publication>:[<step-id>]}`). Persist records.undo_of and
records.undo_steps. Reverse the complete gesture and reattach only the selected
owner to authenticated S0; do not remove I1/S1 if a surviving consumer needs
them. Scan later writes/reads/edge consumers and ABA, use actual landing before
values for merged commits, and preserve unrelated sibling work. Redo is inverse
of this accepted inverse with inherited provenance. Grouped/per-step boundary
records must survive even for intermediate roots absent from final closure.

The entire existing request remains intact: api_version, project_id, timeline_id,
base_revision_id, base_publication_id, commands, label,
steps(id,label,intent,tags,command_ordinals,patch,reads), merge(fields|atomic),
reads, dry_run, source, rationale, group_id and stable scoped idempotency key.
Omitted reads on doc.patch still force conservative atomic scope dependencies;
no empty-read fabrication and no field, assertion or guard dropping.

Keep full `{data,receipt}` replies: accepted/merged, exact authentic historical
rebased replay, canonical document and evaluated/previous/accepted head/revision
identities, document/content/records digests, normalized commands, records,
effects, steps, dependencies, history, undo_of/undo_steps and authoritative
publisher. Conflict retains reason/head; invalid retains code/path/hint/suggested
command. Preview MUST retain would_status accepted|merged, evaluated_head,
complete candidate/effects/steps with receipt:null and no durable effects.
No schema-version bump or historical receipt rewrite is inferred.

## Bounded implementation and acceptance proposal — NOT RUN

1. Agent lane: implement the four existing-family opt-ins and physical projection,
   plus native same-owner/ID preservation cases beside
   `tests/editing_conformance/test_recipe_occurrence_media.py` and
   `test_recipe_m2_placement.py` and
   `test_recipe_m2_placement_create_unplace.py`. Cover shared shot and distinct shots
   sharing one internal image; opaque sentinels and raw source windows;
   ADD/SWAP/move/create; unchanged sibling/membership/order/timing/IDs; no-op;
   missing/ambiguous owner, foreign input, unsupported map and old args unchanged.
   Each acceptance also requires the production caller uses it.
2. Agent/Runtime lanes: targeted cases beside
   `tests/editing_conformance/test_commit_runtime_occurrence_media.py`,
   Runtime `tests/test_timeline_commit_authentication.py`,
   `test_timeline_commit_acceptance.py`, `test_timeline_commit_closure_invariants.py`.
   Cover accepted, disjoint merged, overlap/ABA conflict; sequential step reads;
   lost ack/restart stable retry; changed-body key mismatch; preview no writes;
   exact physical effects and provenance; historical rebased replay; guarded
   whole/per-step undo/redo, surviving consumer and corrupted provenance.
   Multi-revision same-shot item ownership must pass without loosening collisions.
   Each acceptance also requires the production caller uses it.
3. Runtime lane: generated schema/client compatibility checks retain frozen
   published floors. Agent: scoped Ruff, direct scoped
   `/tmp/astrid-u2-typecheck/bin/python -m mypy`, normal `make ruff` and
   compare_mypy_baseline ratchets with worker-private cache paths, no budget rises.
   No full/browser/HTTP/native14 suite is proposed in this task.
4. App lane after authorized tuple adoption: production
   `src/tools/video-editor/commands/occurrenceMediaCapture.ts`, `commitSession.ts`,
   `sessionPlacement.ts` and their mounted popup/placement callers must submit the
   explicit marker through the persisted A2 outbox, adopt canonical replies and
   preserve dependent intents on restart/refusal. Keep semantic execution in
   Python, no TS executor or App edge patch. Targeted caller tests then show the
   selected identity and sibling survive reload and undo. A provider-only unit
   pass cannot close A3: **the production caller uses it** is required.

Current acceptance: **FAIL / explicit NO-CARRIER / production caller uses it NOT
MET**. Design delivery is complete; implementation is not. Orchestrator must
authorize the named semantic/schema + producer tuple exception and cross-lane
adoption, or explicitly disposition the promised shared occurrence-local scope.
Escalation: `escalations/agent-20261023T0445Z-same-owner-carrier.md`.
