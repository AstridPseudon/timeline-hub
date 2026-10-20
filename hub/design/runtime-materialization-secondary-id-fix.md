# Runtime materialization secondary-ID fix

Worker: `rt-m2-materialization-secondary-id-fix`  
Base/recovered carrier: Runtime `3c917378a6dc2b48362fd1bc152cb13a5fd6b84a`

## Decision

The recovered Runtime guard now allocates item identity exactly as Main and
the Agent codec do: `item_id` when present, otherwise `id`. It still refuses a
missing canonical identity or two writes with the same canonical identity.

The removed check required a present `id` to equal `item_id`. That was too
strict: a distinct secondary `id` is opaque payload and must survive without
becoming an allocator key. SQL projection remains keyed by the canonical
identity only. Existing global `shot_items.id` occupancy, retained-source
reservation, source joins, and old source/bystander rows are unchanged.

## Permanent controls

`tests/test_timeline_projection_ownership.py` now covers:

- missing, equal, and distinct `id` mirrors, preserving the input payload;
- a distinct secondary ID equal to an existing bystander row, proving it does
  not move or overwrite that row;
- an actually occupied canonical `item_id` with a free secondary ID, which
  still refuses atomically;
- the existing duplicate, empty/malformed, cross-owner, and retained-ID
  refusal controls.

The prior `conflicting-alias` refusal expectation was removed because it was
the false refusal. The real malformed empty-ID negative remains. The original
audit probe and its unchanged acceptance evidence were not edited.

## Qualification boundary

No public schema/013 change, codec normalization, ID renaming, native typed
carrier claim, pin, merge, publication, or full suite was performed. The two
original strict schema-boundary xfails in
`tests/test_timeline_materialization_join.py` remain unchanged.
