# M2 placement contract — bounded branch candidate

Worker: `agt-m2-placement-native`; branch `tl/agt-m2-placement-native`;
base `5b51b9363c7c598f6815594f7cb931ca8c635690`.
Source checkout: `/home/user/work/wt/agt-m2-placement-native`.
The harness assigns the final commit. This is an Agent unit-qualified candidate,
not a Runtime/App qualification or permission to merge. PLAN still records M1
open. No merge is requested.

## Published operation and capture

`placement.move`, version **"1"**, moves one existing raw parent/occurrence clip
to an absolute global time. It preserves duration, source window, speed, raw
track, asset binding, membership, ordering and opaque authored values. It is
separate from occurrence media ADD/SWAP and creates no media, registry binding,
clip, track, shot or occurrence.

Export:
`astrid.sdk.timeline.native_placement_commands.capture_placement(bundle, owner, clip_id, on, *, ownership)`.

* `owner`: exactly `parent` or `occurrence:<raw occurrence ID>`.
* `clip_id`: existing raw clip ID, never a projected display ID or a generation
  ID inferred from a deterministic legacy entry name.
* `ownership`: required adapter argument, exactly `parent` or `occurrence`,
  matching `owner`. `shared` always refuses. The scoped wire selector is the
  authoritative ownership expression; occurrence intent also records
  `ownership: "occurrence"`.
* `on`: finite nonnegative **absolute global seconds**. No frame argument,
  auto-position sentinel, pooled null, implicit lane, or new media selection.

Wire envelope:

```json
{"schema_version":1,"op":"placement.move","version":"1","select":"occurrence:occ-a/clip:clip-a","args":{"on":12.012},"intent":{"ripple":"none","anchor":"fixed","position":"absolute","ownership":"occurrence"}}
```

The capture export returns this command plus the native recorder's complete
`resolved`, `expect`, `authorship`, `reads`, `selections`, `bindings`, `created`.
Capture on the original bundle before preview and preserve it in the outbox;
do not refresh its guards on retry. Parent intent omits `ownership` and retains
the same ripple/anchor/position fields. The provider checks every submitted
recorder claim. A shared intent is rejected by the canonical schema as well as
the adapter. Parent/shared-shot root writes are not alternative selectors.

Schema authority:
`/home/user/work/wt/agt-m2-placement-native/astrid/core/timeline/schema/edit-command.schema.json`.
The new conditional reuses `$defs.ClipMoveArgs` (`{"on": number >= 0}`, closed
keys), constrains version/selector/intent, and adds no media-selection schema.
SHA-256: `372b2c293a0ff458fa75ef0448a184e251a35de94ed05a433a46ca2d700df314`.

## Why a small operation wrapper is needed

The handler delegates **all timing and authored writes** to existing `move` in
`capture.py`; it does not duplicate that implementation. An ordinary thin
`capture_move` alias was tested first. It is insufficient for the ownership
contract: in a detached head with a second occurrence referencing the target's
same authored root, ordinary move replay changes that sibling's child too.
The new operation adds only these observations before delegation:

1. Query `placement.owners`, query_version 1: ordered occurrence references
   whose **authored** `shot_id` equals the selected occurrence's authored root.
   `members` and `order` must be exactly `[owner]`; `boundaries` contains that
   exact `shot:<authored root ID>`; policy `guard-membership`. Multiple owners
   refuse even when a sibling occupies a different parent lane.
2. Full existing asset-binding reads at the raw authored paths:
   parent `registry.assets[asset]` and `config.registry.assets[asset]`, or
   occurrence `/source` at `registry.assets[asset]`. Absence is recorded too.
   Thus stored generation/variant/catalog/object pins, nullable or opaque
   binding fields, and unchanged identity values remain guarded. No tuple is
   manufactured from a URL, file, display ID or newer gallery selection.
3. Require an explicit positive occurrence `duration_ms` and reject a quantized
   child interval extending beyond it, including the last occurrence. The
   existing move's duration evaluator supplies the span; no timing math is
   duplicated.

The query's historical overlap predicate catches occurrence creation/removal
or `shot_id` writes that add/remove a reference to this authored root, including
ABA, and whole parent-occurrence replacement. Unrelated root references remain
disjoint. Inverse rechecks membership before installation, protecting a later
consumer. A changed authored-root boundary conflicts; this bounded version
does not normalize that selection across a different root identity, even where
ordinary move permits a proven source-materialization handoff.

Existing move capture supplies exact target membership, track identity and
activity fields, source identity/window and media-ID reads, occurrence map,
parent/child fps, parent/source image provenance and ordered lane-blocker query.
It quantizes once using rational fps and converts global time to occurrence
local time. It clears `on`/`until`/`until_film_end` at app and app.astrid scopes,
and writes fixed_start/for. All original move limitations remain: translation-only
occurrence map, unambiguous positive duration, no unsupported nested/time maps,
nonnegative local start and no crossing the next occurrence. The wrapper also
checks the explicit occurrence end after quantization and refuses a missing
extent.

No new IDs are allocated: `created` is empty. Composition with preceding
track.create/clip.add reuses caller-reserved IDs and the existing staged inverse;
a later track consumer prevents deleting the created lane.

## Real App semantics and the unsupported boundary

Inspected `/home/user/work/app` at
`2bfde69eac32335eae0bc5fa2820940c0b3c694b`, especially
`src/shared/lib/placement/{placementService,documentPlacement}.ts`,
`src/shared/lib/timelineFrameBatchPersist.ts`,
`src/shared/hooks/shots/{useShotGenerationMutations,addImageToShotHelpers}.ts`,
and the callers found by `rg`; read `design/app-writers.md` and
`design/app-popup-command-handoff.md`.

The current shared service is **not equivalent** to a literal move:

* placeGeneration resolves media, merges `gen:<generationId>` registry state,
  infers/creates a pinnedShotGroup, removes the old expression, then pools on
  null or creates `clip-sg-<shotId>-<generationId>` with a **four-second hold**.
  Undefined frame appends after the group's last clip; explicit frames shift
  forward while an equal start frame is occupied.
* unplaceGeneration deletes its clip/pool membership, optionally recreating a
  pooled member if the registry has managed media. It preserves the registry.
* batchUpdatePlacementFrames resolves entries through that read model and
  sequentially removes/recreates media placements. It can promote pooled
  members and silently ignore missing entries; the outer frame-batch adapter
  detects missing results. This is not a source-window-preserving clip move.
* The service selects a default timeline and identifies ownership through
  legacy group membership; its requests lack explicit canonical occurrence/raw
  clip ownership. The new capture must not infer it from shot/generation names.

Therefore this publication covers **existing canonical clip repositioning
only**, with an explicitly chosen owner and literal move semantics. It does
not qualify the legacy place/unplace/frame-batch writers for deletion. Pooling,
generation add/replacement, automatic placement, collision shifting, occurrence
root geometry moves, child retrack and shared-root editing explicitly remain
unsupported. Legacy pinned groups need the separately owned recorded migration.
Relational `shot_generations.timeline_frame` and `metadata.end_frame` are outside
this command and remain untouched. No whole-document or registry upsert fallback
is supplied.

## Golden and evidence

Golden:
`/home/user/work/wt/agt-m2-placement-native/tests/editing_conformance/fixtures/recipe_m2_placement.json`.
SHA-256: `7404b665b2918ebf095abc68bd3a20176afb0589b79cf785887c1da50b68d271`.
Two cases (parent and nonzero occurrence): full original canonical document,
capture request, exact command, authoritative record and compiled output. Fps
is 30000/1001; original source media is already pinned. Neither case introduces
a new media-manifest dependency.

`test_recipe_m2_placement.py` proves deterministic capture/replay/JSON roundtrip,
exact writes equal to clip.move, source-window/opaque/registry/order preservation,
sibling isolation, compile/reload, exact full-document inverse using the
original historical source closure, redo, clears/null/absence, disjoint rebase,
relevant conflict/ABA, source-owner sharing/later consumers, claim/schema refusal,
and reserved track/clip composition with dependency-protected inverse.

Final targeted command:

```sh
PYTHONPATH=$PWD /home/user/work/venv-agent/bin/python -m pytest -q tests/editing_conformance/test_recipe_m2_placement.py tests/editing_conformance/test_recipe_m1_commands.py tests/editing_conformance/test_recorded_graph_roots.py tests/editing_conformance/test_recipe_m2_clip_add.py tests/editing_conformance/test_recipe_scalar_commands.py
```

**319 passed in 7.89s**, exit 0. Changed-file ruff and `git diff --check` pass.
No full suite, installation, browser/socket suite, Runtime/App acceptance,
commit, merge or push was run.

Read the popup worker's published `design/m2-popup-native-contract.md`: its ADD/
SWAP lane is blocked on exact media-manifest inverse across reload. This
placement candidate adds no media pins and its existing-media golden restores
the full document with a historical source closure; it does not solve or bypass
that blocker. Runtime still owns official schema/generated-artifact refresh and
actual provider acceptance; App still owns capture parity, outbox/zero-legacy
traffic and accepted reload/undo qualification before deleting any writer.
