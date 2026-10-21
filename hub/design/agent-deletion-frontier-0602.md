# Agent deletion frontier — 2026-10-21

No new zero-caller helper was removed from the current `a08a50007` tree.
The narrow `rg` proof found the apparent post-migration candidates still
live:

- `_duration_sheet` is called by `checkout.py::_stage_sheet` and
  `checkout.py::_pending_sheet` for the retained duration draft/outbox path.
- `_publishable_parent_command` is called by
  `AttachedCheckout.publish()` and still gates the accepted parent move,
  scalar, delete, split, and selected-PARAM commands.
- `apply_sheet` still has the production caller
  `packs/timeline/cli.py::_cmd_apply`; its detached path reaches
  `merge_sheet`, `_apply_parsed`, and `Checkout.save`.

The exact remaining deletion blocker is the detached legacy sheet producer:

```text
_cmd_apply -> apply_sheet -> merge_sheet (versioned sheets)
           -> _apply_parsed -> Checkout.save
```

It remains a Main-positive no-client/local and mixed-grammar path. Its
prerequisite for deletion is a bound `NativeSheet` replacement for the
remaining narration, sound/media, structure/add/remove, look, and relational
timing grammar, with a retained native basis, stable row intent/identity, and
the existing Runtime/outbox target. Until that exists and is qualified, the
local helpers must remain; this frontier does not retire any public or test
behavior.
