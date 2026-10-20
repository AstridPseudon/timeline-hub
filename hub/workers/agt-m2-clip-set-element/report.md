`clip.set-element` is registered and the targeted tests pass. I did not run `make check`.

## What I did
- **Handler:** `clip_set_element` is in `astrid/sdk/timeline/_clip_scalar_commands.py`, next to `clip.set`, with a `capture_clip_set_element` helper. It is registered as a singleton in `commands.py`.
- **Identity guards:** the clip is targeted by stable id (`parent|occurrence:…/clip:…`). Both `elementRef` and the `element_ref` alias are read, so replay guards them. The command refuses if no ref exists, or if the new `id` or `kind` differs from the existing one.
- **Write:** it records one `elementRef` write. If the clip carries the retired `element_ref` alias, that is cleared in the same record. The inverse, ABA protection and rebase all come from the generic recorder.
- **Schema:** I added `ElementRef`, `ClipSetElementArgs` and an op dispatch entry to `edit-command.schema.json`, all additive. The args are closed: `{elementRef}` only.
- **Tests:** `tests/editing_conformance/test_recipe_clip_set_element.py` has 22 tests and a golden at `fixtures/recipe_m2_clip_set_element.json`.
  - They cover round-trip, replay, unchanged writes staying history edges, A→B→A, rebase over a disjoint `clip.set-params`, closed-args refusals and a grouped `set-params` + `set-element` batch.

## Decisions
- **Clear policy:** `elementRef` is not clearable, so there is no `clear` arg. Removing it would change which element the clip is, which the same-identity guard forbids. Absent is only a refusal case ("requires an existing element ref").
- **Ref shape:** the stored field is `{packId?, id, kind, revision}`, not `{owner,…}`. The code reads `packId`; draft refs have none. The schema requires `id`, `kind` and `revision` and allows `packId`.
- **Order matters in a grouped commit:** `clip.set-params` validates against the clip's current element. Replaying a `set-params` captured on the old ref after `set-element` moves the ref is refused by design (the test asserts this). `update_parent_element` should therefore send `clip.set`, `clip.set-params`, then `clip.set-element` in that order, as the brief says.
- **Not touched:** the vendored `astrid_runtime_client/timeline_commit_types.py` is pinned by `runtime.lock.json`. It gets `ClipSetElementArgs` when Runtime regenerates its projection.

## Proposal for the legacy entries (not implemented)
`clip.set-element` does not touch `config.app.elements[<id>]` or the `config.clips` mirror. Both belong to the legacy parent-bundle shape in `update_parent_element`.
- **`config.app.elements[<id>]`:** the caller removes it when no other clip still references the old ref. That is the `remaining` check in `timeline_elements.py`. It is a document-level cleanup, not a clip edit, and should become its own command, or be dropped if the native document no longer carries it.
- **`config.clips` mirror:** the commit service already regenerates the mirror through `compile_mirrors` when it equals `parent.clips`. The hand sync in `update_parent_element` goes away on the commit path.
- **`parent/clip:direct` test:** I added one that checks the command leaves `parent.config` unchanged.

## Tests
- **Direct run:** `pytest tests/editing_conformance/test_recipe_clip_set_element.py` gave 22 passed.
- **Test service:** `request-test agt-m2-clip-set-element targeted --files "tests/editing_conformance tests/timeline tests/sdk tests/core/test_timeline_element_publication.py"` gave 3672 passed, 6 skipped, 14 xfailed in 12.5 minutes.
- **Schema superset guard:** I did not find a dedicated test named for it. The existing schema-validating goldens across the batch passed, and the change only adds definitions and a dispatch entry.

The commit message is written and `DONE` is created. I left no build output or temp files in the worktree.
