# Agent video unplace: command handoff

Status: blocked on the current Agent command surface. This is a design and
evidence handoff, not a claim that video unplace is implemented.

Source SHA: `ba5f2756f50a84f570aa9699ef621873f7521abc`

## Intended capture

For an explicit canonical owner and raw child ID:

```text
owner       = occurrence:<raw-occurrence-id>
clip_id     = <raw-video-child-id>
target      = occurrence:<raw-occurrence-id>/clip:<raw-video-child-id>
media       = exact five-field selected-media pin supplied by the caller
commands    = [existing guarded clip.delete(target),
               optional existing shot.pool add(owner, media)]
```

The builder must capture against the original bundle, retain the reserved raw
identity, execute the first command on a temporary bundle only to capture the
second command, and return one ordered batch. The inverse must restore the
whole video row and its exact source window while retaining the registry/media
binding. `keepAsPooled` adds the exact pin to the pool; it does not delete or
rewrite the binding. The image path remains `placement.unplace`, and no owner
or display ID is inferred.

## Current command evidence

The real `test_recipe_m2_shared_auto_placement.build('video')` fixture produces:

```text
occurrence:occ-a/clip:placed
clipType=video asset=reserved-new at=9.017 hold=4 from=0 to=4 speed=1
```

The exact current calls are:

```python
unplace_shared(created, 'occurrence:occ-a', 'placed', ownership='occurrence')
# CommandError: unplace requires one placed media clip

execute(created, [{
    'schema_version': 1, 'op': 'clip.delete', 'version': '1',
    'select': 'occurrence:occ-a/clip:placed', 'args': {}, 'intent': {},
}])
# CommandError: clip.delete v1 requires one parent clip identity
```

The existing delete handler in `astrid/sdk/timeline/_delete_commands.py` only
accepts `parent/clip:<raw-id>`; the existing capture helper is likewise scoped
to that command. `placement.unplace` in
`astrid/sdk/timeline/native_placement_commands.py` explicitly rejects video
rows. No registered existing command removes one occurrence child.

## Required cases once the existing command surface is unblocked

1. Video unplace restores the exact video row, including `from`, `to`, `hold`,
   `speed`, opaque fields, and child order; registry and dependency media stay.
2. Video `keepAsPooled` returns one batch in exact order: guarded delete, then
   `shot.pool add`; absent and empty pools remain distinct, and an existing pool
   member preserves ordered semantics/refusals.
3. Inverse, redo, exact retry, changed-row/source-window refusal, child-window
   guards, and shared-occurrence isolation remain covered.
4. Image unplace and image `keepAsPooled` retain their current positive
   outcomes.
5. Parent/display/derived owners and any legacy-group state refuse without
   mutation; no registry/media deletion or legacy writer traffic occurs.

The brief forbids adding an alias/op/schema branch, recreating the child under
the same ID, deleting the registry asset, or changing low-level inverse code.
Therefore the next decision must be to make the existing guarded
`clip.delete` handler accept this already-schema-shaped explicit occurrence
selector, or to provide an existing occurrence-child delete command. Until
then, the requested builder-only change cannot produce an executable,
invertible batch.
