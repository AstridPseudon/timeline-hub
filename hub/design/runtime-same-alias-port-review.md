# Runtime review: WC6 same-asset alias rebind

## Disposition

**ACK the Agent semantic source conditionally; no Runtime product change is
needed.** The reviewed Agent source is commit `17f8434e`, tree
`d11f904e`. It uses the existing `occurrence.swap-media` operation with the
original and new exact `MediaSelection` values. The same-alias case retains
the alias and changes only the declared media fields plus the bounded known
payload mirrors. The existing recorder/inverse path remains the authority for
inverse and ABA behavior; no equal-JSON inference or fresh selection is
introduced.

The source is not a native qualification or release approval yet. Agent's
reported native lane is blocked while importing the deleted
`_binding_descriptor` helper and retired `create_project_shot` setup. I did
not restore either helper/route, fabricate accepted history, or run a false
positive. The source ACK therefore remains conditional on Agent's own native
fixture proof using the current Runtime.

## Runtime 7f6dd892 review

The current Runtime head is `7f6dd8920e1ceec41b137358df5e7fecc304888d`.

- `RequestCommitPort.selected_media` requires the exact selection to be
  declared, captures the returned value by canonical selection identity, and
  rechecks every captured selection immediately before acceptance
  (`runtime_protocol/timeline_commit_port.py:267-274, 397-400`). Thus old and
  new selections must both be explicitly read and must not be silently
  refreshed.
- `MediaReads.selected` requires exactly the five `MediaSelection` fields and
  reconstructs the record from Runtime authority. The selection path checks
  project/realm scope, managed project ownership, completed generation,
  exact object identity, intrinsic metadata, catalog digest, and (when
  applicable) the unique managed-output settlement and attempt provenance
  (`runtime_protocol/timeline_commit_port.py:632-665, 720-824, 827-834`).
- Closure acceptance keeps the full media dependency set sorted and unique,
  verifies each retained object against managed custody and CAS bytes, and
  requires every authoritative `media_id`/`object_id` in parent, shot, and
  internal payloads to be accounted for (`runtime_protocol/timeline_commit_store.py:500-529`). This covers the old retained pin and the new object, but does not
  pretend to derive alias-consumer scope from the closure.
- Projection persistence copies the accepted authored payload and records
  occurrence identity/order and the media dependency pins; it does not
  normalize a same-alias registry entry or overwrite opaque fields
  (`runtime_protocol/timeline_commit_store.py:820-848`). Agent's recorded
  command/provider remains responsible for proving that every affected
  consumer of the alias was checked and that only declared fields changed.

No Runtime counterexample was found for the requested `new object at same
alias`, `old retained pin`, or full affected-alias-consumer scope. No endpoint,
DTO, schema, pin, private authority flag, or add-policy change is justified.

## Evidence

Command run directly on the current Runtime worktree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-runtime/bin/python -m pytest -q -p no:cacheprovider \
  tests/test_timeline_media_selection.py \
  tests/test_timeline_commit_port.py \
  tests/test_timeline_commit_closure_invariants.py
```

Result: **59 passed in 31.49s**.

This covers exact selection custody/catalog behavior, lifecycle and settlement
rechecks, capture-to-accept mutation refusal, project/media closure custody,
retained raw closure/items, occurrence identity refusal, and accepted
dependency corruption refusal. It is not a claim of same-alias native
acceptance: the exact Agent fixture could not reach that path without the
forbidden deleted helper/retired writer.

## Handoff

Keep the original Agent alias/opaque/inverse/ABA positives strict. Agent should
repair only its test support using an unchanged approved support delta if the
exact reviewed fixture migration applies; otherwise provide its own native
fixture proof. After that proof, rerun one bounded image/video same-alias case
against Runtime `7f6dd892`; no broad/matrix/full run is warranted here. Until
then WC6/RT02 remains held for native qualification, while Runtime is not
blocked on a product fix.
