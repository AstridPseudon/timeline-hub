# RT08 item witness: second failure diagnosis (1225)

## Finding

**Fixture/oracle error; no missing provider materialization fact demonstrated.**
The witness edits the intended occurrence and opens the intended realm, but its
source is not shared. It expects allocation records for an ordinary own-shot
update. The approved Agent emits those records only for an actual changed
virtual shot slot. The prefix and pin/binding shape in the oracle are correct.
The withdrawn 1157 item-map allegation is not a defect and is not this cause.

No product/test edits, fixture replay, third body, test request, installation,
socket/renderer/browser/native execution, artifact generation, pin or release
was performed. This report is read-only source/history analysis.

## Exact failing evidence

Runtime base `ce066206feefc71fb93853d935f93051333bc799`, tree
`ec34394b5aa9b4fa1b11c8c9e235ade447aca498` (unchanged in this worker).
Agent suite pin `4b7a27127fb9b642be8ad118e6aa663bd7761611`, tree
`a6126ed13a7b4dad8124894ebced1cf1b5977d5f`; confirmed by read-only
`git -C /home/user/work/wt/agt-pin-4b7a2712 rev-parse HEAD HEAD^{tree}`.

Retained result directory under `$ORCH/tests`:
`rt-m2-item7227-fixture-order-repair-1221-private017-agent4b7-integration-1021122226-18290`.
Its recorded command (not rerun):

```sh
env ASTRID_RUNTIME_CHECKOUT="$PWD" ASTRID_CHECKOUT=/home/user/work/wt/agt-pin-4b7a2712 PYTHONPATH="$PWD:/home/user/work/wt/agt-pin-4b7a2712" PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider -m integration tests/test_timeline_projection_occupancy.py::test_startup_provider_materializes_source_items_and_refuses_global_item_occupancy
```

Result: **1 failed in 2.03s**, exit 1, `StopIteration` at line 449 after
`first = editing.commit(...)` succeeds. No global-item negative was reached.
Worker1221's report and log were read; no earlier failing body was replayed.

The retained database is still available:
`/tmp/pytest-of-root/pytest-43/test_startup_provider_material0/precut-music-documents-v31-copy-b/realm.sqlite3`.
It was queried using Python stdlib SQLite with `mode=ro&immutable=1`, without
opening RuntimeService or importing/executing Agent or fixture code.

Accepted publication: `txn-6eb14b3a10f249689aeae3d7641d1ac8`.
Previous parent: `rt08-source-items-parent`.
Accepted parent:
`authoring-parent-revision-dd9202abefa6fe2d95be6475a38c8aa4428e9bea1ebb8e2157960442c862dd27`.
Durable ledger result: `status=accepted`, `id_map={}`.
History command: `clip.move`, version `1`, select
`occurrence:occurrence-3/clip:clip-3`, `on=3.5`.

Exact record dependency keys:
`move.source`, `move.quantization`, `move.images`.
Exact binding keys/refs:

| Key | Ref |
|---|---|
| `move.track` | `occurrence:occurrence-3/track:picture` |
| `move.owner` | `occurrence:occurrence-3` |
| `move.target` | `occurrence:occurrence-3/clip:clip-3` |

The record reads `occurrence:occurrence-3/shot`, path `['shot_id']`, as
`shot-3`. Its `at` write goes from 0 to `0.20000000000000018`, consistent
with global 3.5 seconds minus occurrence origin 3.3 seconds.
SHA-256 of the stored canonical `records_json` matches the accepted event's
`records_digest`; the ledger's commands equal the history commands. Thus
this is an actual retained capture, not an inferred/missing history row.

Before and after acceptance, the parent has exactly these source owners:

| Occurrence | Shot | Before revision |
|---|---|---|
| `occurrence-1` | `shot-1` | `film-shot-revision-1` |
| `occurrence-2` | `shot-2` | `rt08-source-revision-2` |
| `occurrence-3` | `shot-3` | `rt08-source-revision-3` |

Each shot occurs **once**. Only occurrence-3's shot revision changes, to
`authoring-shot-revision-58561e376e8eeef17f8d872a01622bf49f8c47a58fbe4657ec1899de1081df85`;
its shot ID remains `shot-3`. The accepted item remains
`rt08-source-item-3`, with opaque metadata `[null,{"keep":true}]` and
`metadata.source_item_id=rt08-source-item-3`. Shot-2's source item/revision
are unchanged. This proves the test opened and edited its intended shot.

## Why the fixture cannot produce the expected allocation

Committed witness `tests/test_timeline_projection_occupancy.py:70-105`
publishes items for shot-2 and shot-3 and replaces their revision pins. It
never adds a second occurrence of either source. `source_items_agent`
(lines 419-427) fixes setup ordering only. The separate `shared_editing`
fixture (lines 359-390) adds `repeated-third`, but this witness never uses it.
`film` restores the committed music-documents capture. `_start_door` opens
`film.fixture.duplicate_root` with the Astrid startup provider; `Editing`
reads that same daemon's current head. There is no wrong-realm or stale-head
explanation here.

In exact Agent4b7 source:

- `astrid/core/timeline/authoring_bundle.py:350-355,418-449` counts source
  shot IDs. `_authoring_shot_id` (218-228) creates a virtual placement ID
  only when the count exceeds one. `_copy_shot_for_placement` (280-313)
  returns the original item IDs and an empty map for an unshared shot.
- `astrid/sdk/timeline/capture.py:270-273` chooses the command version via
  `_materialization.capture_version`; `_materialization.py:16-26` returns
  v2 only when the occurrence's authoring shot differs from its source.
- `_materialization.py:29-47,93-107` records allocations only for changed
  virtual slots. The retained v1 command therefore correctly lacks them.

For a genuine allocation to destination `D`, the exact approved names are:

```text
dependency: materialization.source:shot:<D>
  kind=entity, policy=exact, pin={parent:{revision_id,content_digest},source:S}
shot binding: shot:<D> -> shot:<S.shot_id>
item binding: shot:<D>/item:<mapped> -> shot:<S.shot_id>/item:<raw>
owner binding: materialization.owner:shot:<D> -> occurrence:<owner>
all three binding forms: policy=fixed, dependencies=[dependency key]
```

`S` includes the exact source shot/revision/digest, internal timeline
identity/revision/digest, and `item_id_map`. Witness prefixes
`materialization.source:` and `materialization.owner:` match exactly.
Changing the oracle to accept absence, v1 or an empty item map would lose
its intended behavior and is not a repair.

## Accepted Agent proof reused

Read exact committed test source at
`e736332f14a07601659285d5fffc4f81a1ef2a44`,
`tests/editing_conformance/test_commit_runtime_identity.py`:

- `identity` (45-64) puts main's real `item-1` carrier on the source shot and
  explicitly points the first **two** occurrences to that same shot and
  `identity-shot` revision. This is the missing fixture precondition here.
- `test_fresh_shared_placement_materializes_own_slot_reload_inverse_and_exact_retry[fresh]`
  (269-353) captures `placement.move` v2 for `occurrence:occurrence-1` /
  `clip-1`. Lines 288-317 assert the one-entry source item map, exact shot
  and item allocation map, dependency, owner binding and item binding.
- Lines 324-336 distinguish fresh reload's own physical source projection
  (empty remap) from the retained original allocation authority. Lines
  339-353 prove own-slot placement/inverse equality and ledger-first exact
  retry. These assertions already have accepted bounded direct-Service credit.

Shared `peer-agent-to-runtime-20261021T1138-reviewed-transition-and-alias.md`
and `handoff-agent-to-runtime-rt08-global-item-proof-1200.md` explicitly
record review1130's acceptance of e736. They also exclude HTTP/public/native/
adoption credit and deny item credit to shot-only20692. The raw remote
`workers/agt-review-private017-item-bearing-source-result-1130/report.md`
is not present on this machine; review acceptance is reused from those
shared summaries, not represented as a fresh inspection of that raw file
or a newly run pass. No accepted proof was rerun.

## Smallest new occupancy case and existing coverage

The genuinely new case is **free destination shot D, but its authenticated
mapped raw item ID J already belongs to a different unrelated shot U**.
Use the same project; cross-project and a second journey are unnecessary.
The sealed current-v2 provider submission must refuse `identity_collision`
and leave the entire durable store (including head, history, retained
closures, receipts, events and sequences) unchanged.

Existing direct guards do not establish that specific case:

- `test_occupied_destination_refuses_before_any_write` at lines 149-166
  occupies the *shot* `occupied`. Its `refuses` helper (122-133) asserts
  `destination_occupied`, a pre-persistence tripwire and exact whole-store
  equality. Its item belongs to that already occupied shot; it does not
  collide solely with the item of a free destination shot.
- `test_historical_slot_requires_exact_accepted_occurrence_source_proof`
  and `test_verified_inverse_reuses_only_its_actual_historical_owner`
  establish retained shot-owner reuse, not unrelated raw item occupancy.
- Current approved helper
  `test_item_bearing_materialization_uses_validated_destination_pairs`
  (integration Runtime source `52e6c01c...`, lines 321-376; absent from this
  private witness base) asserts exactly
  `allocations == {'destination': ('occ-0', {'parent': ..., 'source': source})}`.
  It exercises `materialization_join`, not `_check_shot_destinations`, and
  has no unrelated occupant or atomic-refusal assertion.

Source inspection of the exact private42a tests and this witness base found
no separate direct assertion for the new free-shot/occupied-item case.
Runtime already has the relevant product guard:
`timeline_commit_store.py:789-798` looks up raw item IDs globally in both
`shot_items` and retained shot revisions and refuses a different owner.
Lines 806-824 also protect retained recorded births. This is an unqualified
behavioral case, not evidence that those guards are missing or defective.

## Minimal source-only repair plan (not applied)

Keep source setup before renderer tripwires and all mapping/source/opaque/
retention/occupancy expectations. Repair only the witness fixture and its
candidate target in `tests/test_timeline_projection_occupancy.py`:

1. During the existing `publish_source_items` setup publication, append
   `rt08-repeated-second` pointing to exact `shot-2` /
   `rt08-source-revision-2` at 6000 ms, and `repeated-third` pointing to
   exact `shot-3` / `rt08-source-revision-3` at 9000 ms. Copy the respective
   occurrence's other fields. This uses existing publication/closure
   authority and leaves the original opaque data/items intact. No fake
   accepted history, schema override or new product carrier is needed.
2. Preserve first/second positive target
   `occurrence:occurrence-3/clip:clip-3` at 3.5/3.6 seconds. Resolve `D3`
   from the authoring bundle's occurrence-3 placement, never by a guessed
   ID. Require current v2 and the exact keys
   `materialization.source:shot:<D3>` and
   `materialization.owner:shot:<D3>`, owner `occurrence:occurrence-3`, shot
   source `shot-3`, and item binding
   `shot:<D3>/item:<item_id_map['rt08-source-item-3']>` ->
   `shot:shot-3/item:rt08-source-item-3`. Retain the existing inverse,
   source-map, id-map, physical-item and opaque equality assertions.
3. The current later candidate `occurrence:occurrence-2/clip:clip-2` at
   2.5 seconds is also wrong: it is unshared in today's fixture, and
   `2.5 + 1.8 > 3.3` crosses the next occurrence boundary in
   Agent4b7 `capture.py:233-247`. With the repaired source fixture, target
   `occurrence:rt08-repeated-second/clip:clip-2` at 6.2 seconds instead.
   Its 1.8-second clip ends at 8.0, before `repeated-third` at 9.0.
   Both shot-2 occurrences remain shared after shot-3's positive steps.
4. Resolve `D2` and its exact `rt08-source-item-2 -> J2` mapping from the
   sealed capture/records; require owner binding
   `materialization.owner:shot:<D2>` ->
   `occurrence:rt08-repeated-second` and item binding
   `shot:<D2>/item:<J2>` -> `shot:shot-2/item:rt08-source-item-2`.
   Occupy only `J2` on existing-API catalog shot
   `rt08-unrelated-item-occupier`, with `D2` still free. Keep exact
   `identity_collision` and `rows(service) == before` assertions.

This plan repairs the existing source witness without replacing any passing
behavior expectation. The accepted positive remains reused evidence; only
the unrelated global-item negative adds qualification. **No execution is
authorized or proposed as part of this task; stop source-only.** No missing
carrier counterexample was found. The orchestrator decides any later repair
assignment; no third body or new journey was requested here.
