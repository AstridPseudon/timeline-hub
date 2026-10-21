# Runtime review: Agent producer clip-leaf source

Status: **SOURCE HOLD**.

The exact Agent source is structurally compatible with the existing Runtime
carrier shape, but it has one data-safety mismatch in the ownership guard that
must be corrected before consumer ACK. This is a source-only review; no
Runtime/App activation, generated output, HTTP, socket, pin, renderer, or
generation claim is made.

## Identity and delta verified

- `HEAD` is `57af3fffe192ad369c4282d9ab3a67efd57dc51c` and its tree is
  `319013e799d244497deac26719282595c213b658`.
- The exact parent is `f448c4b40c60d08f4092e232688b0de99bb07243`, tree
  `d4508b9fa5db9b2a2774fc5acc811fc34814c53d`.
- The delta is exactly four files: the command schema, the clip scalar
  implementation, the producer conformance test, and the schema-union test.
  No live callers changed.
- The current producer schema SHA-256 is
  `0b747d87c763a8f0ba0dcc5027390ab04d6296cfddfffa8c049020334ca3ec92`.
  Removing only the producer additions reproduces the parent schema hash
  `da144e6d1c0d3e2ad6ef8246a63a4d4c5fd379b7a0efbedc0f376987527ef068`.
  The focused union test also reconstructs the exact `84fc0863…` floor.
- Runtime’s current pinned ordinary/public014 command schema remains
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
  The producer fields are therefore not claimed active until the later exact
  source composition updates the Runtime pin.

## Carrier/data-safety review

The source extends existing version-1 `clip.set`; it adds no operation, DTO,
endpoint, ID allocation, or alternate acceptance path. `ClipSetArgs` is closed
at the carrier boundary: top-level `label`, five known `text` leaves, and the
existing-owner `app.managedBy` plus complete `app.__generated__` JSON leaf
(`astrid/core/timeline/schema/edit-command.schema.json:2576-2672`). Unknown
top-level and nested text/app leaves are refused.

Execution writes nested leaves rather than replacing `text` or `app`
(`astrid/sdk/timeline/_clip_scalar_commands.py:154-162`), so existing opaque
siblings survive. `hold` remains the only timing leaf here; `at` and `track`
remain `clip.move` authority, and fresh rows remain on `clip.add`. The command
validator enforces finite JSON before schema validation
(`astrid/sdk/timeline/commands.py:118-130`), while the carrier schema gives the
known numeric `fontSize` its JSON-number type.

The implementation records existing owner/generated leaves and ordinary writes
(`astrid/sdk/timeline/_clip_scalar_commands.py:19-46,49-58`); the generic
recorder/inverse path retains before-values and guards them on replay. The
producer tests prove opaque sibling preservation, strict inverse/redo, and
refusal of user/foreign/identity-adopting metadata
(`tests/editing_conformance/test_recipe_producer_clip_set.py:59-116`).

## Blocking counterexample

`_producer_app` checks only `isinstance(current.get('managedBy'), str)` at
`astrid/sdk/timeline/_clip_scalar_commands.py:21-24`; it does not enforce the
handoff contract’s required non-empty owner. A direct source probe constructed
an otherwise valid mirrored clip with:

```text
app.managedBy = ""
app.__generated__.extensionId = ""
```

and captured `values.app.__generated__` with the same fixed identity. The
capture was **accepted**, even though this is an unowned/malformed clip that
must refuse atomically. The incoming schema’s `managedBy` `minLength: 1`
(`edit-command.schema.json:2622-2626`) does not protect the existing stored
owner when the incoming update carries only `__generated__`.

Required follow-up: reject an existing owner unless it is a non-empty string,
and add a regression case for empty persisted ownership. No product fix was
made in this review.

## Deliberately unresolved caller mapping

The Main witness still uses `duration`/`clip.update`, while this source uses
`hold`/`clip.set`; Main also emits flat caption geometry that this producer
carrier intentionally refuses. I did not invent a translation. Runtime/App2
must separately resolve whether one proposal is split across `clip.move`, this
producer `clip.set`, and the position `clip.set`. These unresolved mappings are
not evidence against the carrier shape itself.

## Evidence

Commands run:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/editing_conformance/test_recipe_producer_clip_set.py
3 passed in 0.71s

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" /home/user/work/venv-agent/bin/python -m pytest -q -o addopts= -p no:cacheprovider tests/sdk/test_timeline_materialization_schema_union.py -k 'only_carrier_additions or private_remove or private_extent_floor or literal_three_union or extent_proposal or voiceover_property or complete_reviewed_private_s2'
7 passed, 17 deselected in 1.01s
```

The first suite passes all source-local producer behavior tests. The second
reconstructs the exact parent/floor relationships, including `84fc0863…`.
No full suite, sockets, browser, renderer, generation, pin, activation, or
native Runtime claim was run.
