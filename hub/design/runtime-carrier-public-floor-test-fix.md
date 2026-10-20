# RT08 public-floor test fix

## Result

Replaced the unapproved blanket `xfail` direction with two bounded tests in
`tests/test_timeline_projection_ownership.py`:

- The original typed item-creation refusal remains unconditional, but now
  validates the exact tracked published S2 artifact
  `tests/fixtures/published-command-schemas/agent-26ef2bbb.json` before the
  normal Runtime validation. No frozen schema was copied or changed.
- Added a current-schema positive that accepts the exact typed claim,
  preserves it in accepted history, and refuses a later reuse atomically with
  `identity_collision`.
- Existing occupied-destination, item-ownership, and invalid materialization
  controls remain unchanged.

## RT08 evidence: original -> new test IDs

| Original test ID | Replacement/current test ID | Evidence |
|---|---|---|
| `test_frozen_artifact_does_not_yet_carry_typed_item_creation_claims` | Same ID, now pinned to exact public `agent-26ef2bbb.json` negative | Public floor rejects `shot:new/item:new`; refusal and zero-write assertions remain. |
| No current-positive test | `test_current_typed_item_creation_claim_is_accepted_and_reserved` | Matched f802 typed claim accepts, is recorded, and remains reserved on reuse. |
| `test_other_timeline_occupied_shot_and_compiler_slot_refuse_atomically` | Unchanged | Occupied destination still refuses atomically, including claimed destination. |
| `test_complete_item_write_set_refuses_before_any_revision` | Unchanged | Existing invalid/occupied item write-set controls remain strict. |
| `test_checker_rejects_each_join_concern[wrong-owner]` (materialization neighbour) | Unchanged | Existing wrong-owner materialization refusal remains strict. |

The RT08 ledger remains HELD; this patch makes no public pin, product schema,
provider, or source-authority change.

## Tests

- `PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-runtime/bin/python -B -m pytest -q -p no:cacheprovider --basetemp=/tmp/rt-m2-carrier-public-floor-final tests/test_timeline_projection_ownership.py -k 'not current_typed_item_creation_claim_is_accepted_and_reserved' tests/test_timeline_projection_occupancy.py`
  - **68 passed, 4 deselected** on the parent ade60 tree.
- Isolated f802 probe, using committed Agent3730 schema SHA256
  `f80215f272bc2cf302d772d619cb8248108eb597a654e01ab89c3a332204d94f` in an
  in-memory registry with the current Runtime code:
  `tests/test_timeline_projection_ownership.py -k 'frozen_artifact or current_typed_item_creation_claim_is_accepted_and_reserved'`
  - **2 passed, 52 deselected**.

The ordinary parent tree cannot run the new current-positive because its
installed schema is intentionally still public013; the direct failure is the
old `ScopedId` pattern rejecting `shot:new/item:new`. The isolated f802 run
verifies the positive without modifying the worktree or shared dependencies.

No full, matrix, browser, or live-socket suite was run.
