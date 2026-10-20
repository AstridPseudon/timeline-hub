# Agent native candidate promotion — RT02 / AG-CUTOVER04

Status: **BLOCKED on project-shot acceptance authority**, with an executable
native counterexample. This is a bounded block, not an ordinary-release hold.
No candidate command/schema/artifact was generated or registered. The original
two Runtime promotion positives remain unchanged and open.

## Exact source and peer agreement

Agent source: `310e54840fa5fb8eb7e51bb64ed2c34b7a1063b3`, tree
`c5a8a3ec7e9e01c61c5ae31834da53bed4be406a`. This worker adds only two direct
test files. Runtime native probe source: `7f6dd8920e1ceec41b137358df5e7fecc304888d`,
tree `4cccb2d643194df7df95d624e89a6cd9f6f268fc`.

Reviewed the exact original assertions in Runtime
`tests/test_shot_candidate_promotion.py`, and `origin/main:runtime_protocol/service.py`
`promote_project_shot_candidate` (line 3644 in that ref). The old algorithm:
receipt-first exact retry; expected project-shot version guard; exact candidate
item identity; primary_visual/candidate validation; supplied metadata, recipe,
provenance project/shot/target-role/output checks; managed candidate CAS bytes
verified against digest; at most one old primary; atomic status flips; immutable
shot revision; fixed-point dependency report; result persisted in the receipt.
It does not require a timeline placement or registered generation.

The 14:18:36Z Runtime PEER REPLY in Agent INBOX explicitly agrees that no mutable
unplaced-shot carrier is currently agreed, `shot_closure` is read-only, and C4
must remain intact. It requests no candidate freeze/generation or invented
parent/library timeline/journal. Runtime dispatched
`rt-m2-unplaced-shot-promotion-carrier` to investigate the preservation contract.
This worker's request and executable follow-up are in both manager INBOXes;
the command/arguments below remain a proposal, not peer-approved schema.

## Smallest existing carriers and their limits

- Agent `commit.py:_verify_document` requires exactly the occurrence-reachable
  shot/internal closure: orphan shots are refused. `bundle_from_document` cannot
  open an unplaced project-shot aggregate.
- `authoring_bundle.py:open_authoring_bundle` and
  `_copy_shot_for_placement` retain source identities in `source_mapping`, but
  remap shared project shot S/items I into occurrence-owned S-prime/I-prime.
  Source provenance still names S. Promoting the copies would change ownership
  and item identity; it would not promote the original project catalog item.
- The existing `shot:<id>` recorder root can write a complete
  `{payload, internal_timeline}` aggregate already in the bundle. Ordinary
  recording cannot address item refs directly. The PRIVATE typed carrier
  reviewed at Agent `3730d0bd51686a1692450359482205df64dcc839`
  adds `shot:S/item:I` addressing and source-bound materialization guards;
  `_materialization.source_entity` resolves authenticated immutable sources
  read-only. It still writes occurrence-owned destinations, not unplaced S.
  It is not part of the frozen ordinary source and was not composed here.
- Runtime `RequestCommitPort.shot_closure(shot_id, revision_id)` is the smallest
  existing exact source input: shot revision, internal revision, media and
  document pins. It does not guard the CURRENT global project-shot head.
  Its present store reader also recovers retained inputs from an existing
  parent manifest; a never-placed legacy shot is not guaranteed readable by it.
- Runtime `TimelineCommitStore._validate_closure` (lines 500–513 in tested source)
  already verifies managed project media membership, CAS length and actual
  sha256 for every immutable manifest pin. Reuse that carrier for candidate and
  source digests. Requiring `MediaSelection` instead would lose the old ingest
  object capability: `selected_media` requires a registered generation/variant.
- Runtime acceptance/history is timeline-scoped. Merely reading an old shot
  revision must continue not to repoint the newer global shot head (C4).
  The existing occupied-destination/item-ownership guards remain required.

Project catalog KEEP is preserved: the probe demonstrates that unplacement
retains its catalog shot exactly. No catalog write/read API was reclassified.

## Executable counterexample

`tests/editing_conformance/test_candidate_promotion_scope_runtime.py` uses the
existing ordinary birth test's private normal-generator fixture (unchanged
55-definition/29-operation schema), a new realm, normal trusted startup provider,
authenticated commit callback and these accepted commands:

1. Normal `create_project` and provider-backed `create_timeline` bootstrap.
2. `track.create` then `occurrence.create` for `project-shot` / `occ`.
3. Read exact born canonical shot/internal images and catalog shot.
4. `occurrence.delete` removes the sole placement.
5. Assert catalog shot is byte-equal and exact `shot_closure` remains readable.
6. Assert current canonical closure contains no shot/internal images;
   `State.entity('shot:project-shot')` refuses; adding retained images as orphan
   canonical children refuses; all accepted/current/catalog bytes remain equal.

No SQL, prepared provider, patched semantic provider, old writer, legacy
publication, fabricated acceptance/history, socket, renderer or baseline is used.
This is a reachable native state demonstrating missing authority, NOT a promotion
positive. It does not fabricate candidate items through an unsupported writer.
The original old fixtures require precisely the additional unplaced-project-shot
capability; they are not narrowed to placed or generated candidates here.

The pure neighboring file additionally proves shared S/I remapping, canonical
orphan rejection, and exact full-root recorded status-flip undo/redo with
same-value intervening-write refusal. Its manual recorder experiment deliberately
claims no candidate provenance, byte validation, accepted history or public op.
No pure inverse result is presented as a supported Runtime promotion inverse.

## Smallest contract proposal (not implemented or frozen)

Proposed single CLOSED `EditCommand` operation `shot.promote-candidate`, version
`"1"`, `select: "shot:<exact project-shot id>"`, no intent override. Proposed
required argument set, with no extras:

```text
shot_revision_id: exact immutable source revision
shot_content_digest: source payload sha256
internal_timeline_revision_id: exact source internal pin
candidate_item_id: exact authored stable item id
superseded_item_id: exact old primary id, or null when absent
```

Project identity comes from authenticated commit context. Media/source descriptors
come from the exact shot closure and manifest, never caller-supplied authoritative
payloads. Candidate/old primary selection must preserve authored IDs and reject
ambiguity, missing/changed status, provenance/recipe scope, role, supplied output
identity or digest mismatch before any write. Capture complete item membership,
source descriptors and timeline-asset identity/selection guards. Atomically record
primary/superseded status and the deterministic plate -> proxy -> timeline-asset
fixed point through the existing record/result/history path. Keep generative
invalidations distinct, as the existing analyzer does. Do not merely swap a clip.

The missing contract is explicit, guarded project-shot publication authority in
the SOLE recorder: compare the source against the current project-shot head at
acceptance and distinguish this deliberate project mutation from C4's immutable
historical linking. Its accepted history must represent an unplaced shot without
a dummy parent, hidden library timeline, new table/journal/endpoint or fallback
writer. Reuse immutable shot/source/media images and existing recorded facts.
The precise carrier/output/history representation needs Runtime/Agent agreement;
current CanonicalDocument cannot express it. No extension to public DTOs is
assumed authorized. If it requires such an extension, that is the exact bounded
contract decision for the managers/orchestrator, not an implementation shortcut.
Never-placed legacy source closure retention and the exact scope of dependent
timeline assets also need definition; neither is supplied by inventing document
roots or treating arbitrary caller descriptors as authored authority.

## Tests and limits

Exact commands, from this worker checkout:

```sh
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider tests/editing_conformance/test_candidate_promotion_scope.py tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_recipe_occurrence_delete.py tests/editing_conformance/test_recipe_internal_stages.py tests/sdk/test_timeline_commit_provider_document.py
```

**198 passed in 8.18s.** Includes staged inverse/F1 neighbors.

```sh
PYTHONDONTWRITEBYTECODE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -B -m pytest -q -p no:cacheprovider -m integration tests/editing_conformance/test_candidate_promotion_scope_runtime.py
```

**1 passed in 5.86s** after final fixture-import cleanup. Direct service-only
probe, no localhost/browser/live sockets; no central/full suite requested.

```sh
/home/user/work/venv-agent/bin/ruff check --no-cache tests/editing_conformance/test_candidate_promotion_scope.py tests/editing_conformance/test_candidate_promotion_scope_runtime.py
git diff --check
```

Both passed. Test files are below 150 lines each; no snapshot/golden copied.
No original Runtime test or marker was changed. No promotion fixed-point,
provenance-negative, exact receipt/retry, changed-guard zero-write, Runtime
promotion inverse/restoration or candidate native acceptance is claimed green.
Those original requirements remain open until the missing carrier is agreed.

Ordinary schema bytes remain SHA-256
`6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`:
55 definitions, 27 registered recipes plus inverse/restore = 29 operations.
F1 product code, public013, all product sources and shared dependencies remain
unchanged. No integration edit, git mutation, public generation, release or pin.

Next: Runtime carrier reviewer should use this native witness to settle the
smallest project-shot authority/history representation. Then implement the one
closed command on a separate private candidate cohort and port both original
positive assertions through the real sole recorder before closing RT02/AG-CUTOVER04.
