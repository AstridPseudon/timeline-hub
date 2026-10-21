# WC8 detached source — smallest preservation plan

Date: 2026-10-21 UTC  
Worker: `agt-m2-wc8-detached-source-smallest-recipe`  
Current tree: `ed3ec7395` (Agent worktree)

## Decision: NO bounded native replacement is implementable here

The only remaining normal detached sheet/save caller is still a real Main
positive and must remain held:

```text
_cmd_apply -> apply_sheet -> merge_sheet (when the sheet is old)
           -> _apply_parsed -> Checkout.save
```

The current connected/native caller is already complete and is not this row.
There is no way to make the detached caller emit the existing `NativeSheet`
commands at author time without first supplying a native basis, captured
intent/row identity, and a Runtime/outbox target. Adding those implicitly
would be a new carrier or a renamed whole-document writer, both outside this
task and unsafe for the retained detached grammar.

## Original authoring base and user-visible behavior

The original user flow is `timelines show --as sheet`, edit the displayed
legacy sheet, then `timelines apply ... FILE`. `print_sheet` renders that
projection and advertises the apply flow at
`astrid/packs/timeline/cli_show.py:88-123`.

Its authoring base is a detached `Checkout` draft. `render_sheet` computes a
short `v` from the entire `tl.document()` and keeps up to five complete local
bundles in `_exported` (`astrid/sdk/timeline_sheet.py:38-60`). A new draft is
fetched and given `base_parent`, base placements, and base shot payloads/
internal timelines by `Checkout.draft`
(`astrid/sdk/timeline/checkout.py:383-408`). This is local whole-document
provenance, not the native sheet's revision/publication pin or row capture.

The supported legacy edit is deliberately broader than native clip-cell
editing: the parser accepts `lines`, `sound`, cut headers, layer rows,
`why`/`hold`, and the legacy sections (`astrid/sdk/timeline_sheet.py:306-378`).
`_apply_parsed` then edits narration/gaps, sound, cuts/layers, omissions,
looks, and related timing through the Checkout API
(`astrid/sdk/timeline_sheet.py:995-1085` and its continuation). Existing
detached tests assert these positive behaviors, so replacing them with a
refusal or a narrower renamed writer would violate the Main-positive rule.

The actual no-client CLI writer is unambiguous:
`astrid/packs/timeline/cli.py:3599-3616` takes the detached branch,
constructs/loads the Checkout with `_edit_checkout`, calls `apply_sheet`, and
saves the local draft. It does not open a `TimelineSession` or enqueue a
command.

## Existing native attachment, Runtime target, and outbox carrier

The already-qualified connected path has all three pieces:

- `NativeSheet.export` captures the untouched bundle and exact
  `revision_id`/`publication_id` basis, then stores them (plus selection) in
  the scoped session outbox (`astrid/sdk/timeline_sheet.py:664-680`).
- `NativeSheet.load` reconstructs from that retained artifact, not from the
  current head (`astrid/sdk/timeline_sheet.py:682-689`). Its `# ref` rows are
  stable owner/clip/track bindings (`:619-660`).
- `NativeSheet.apply` checks project, timeline, and unchanged basis, then sends
  the generated existing commands through one atomic `commit_many` batch
  (`astrid/sdk/timeline_sheet.py:805-826`). `TimelineSession.open` derives the
  scoped outbox and `/v1/.../commit` target
  (`astrid/sdk/timeline/sync.py:124-168`), while `_flush` persists the exact
  request and retry identity before sending it (`:334-359`).
- CLI connected/default-with-client calls already use this path
  (`astrid/packs/timeline/cli.py:3599-3604` and `:3937-3948`).

The detached caller has none of that carrier. Although `Checkout.draft` may
remember a client for fetching the draft, the detached branch does not use it
to create a session or outbox. `Checkout.save` writes the local draft under a
file lock and performs its own local save merge
(`astrid/sdk/timeline/checkout.py:151-169`).

## Exact missing pieces

1. **Native base:** the legacy sheet has only the whole-document `v` digest
   and optional local `_exported` snapshot. It has no retained native bundle
   paired with a verified Runtime publication pin. `NativeSheet` requires that
   pair and rejects a mismatch (`astrid/sdk/timeline_sheet.py:604-613`).

2. **Native intent and identity:** legacy rows do not carry the native `# ref`
   bindings or captured read/selection/order/created-ID claims. The detached
   path instead reconstructs a parsed projection and applies omission and
   mixed-shape semantics in `_apply_parsed`; an adapter would therefore need a
   whole-snapshot diff/three-way merge or a new syntax/carrier to recover the
   missing intent. The existing native entrypoint explicitly rejects legacy
   rows (`astrid/sdk/timeline_sheet.py:829-846`).

3. **Target and durability:** the detached path targets the local Checkout
   file, not the Runtime commit route, and has no `TimelineSession` outbox
   state in which to retain the original bundle, pending commands, rationale,
   flight body, and idempotency key. `NativeSheet.load` cannot be used without
   that state (`:682-689`).

These are structural gaps, not a missing existing native operation for one
cell. The current native operations already cover the qualified attached
subset; the remaining producer is the detached legacy/mixed producer.

## Smallest safe plan for the manager

- Keep the connected `NativeSheet`/`TimelineSession` route unchanged.
- Keep the detached `apply_sheet`/`merge_sheet`/`Checkout.save` route for its
  documented legacy and mixed grammar, including its local rollback and
  three-way behavior.
- Do not add a snapshot diff, hidden writer, new public API/framework, client
  rebase, schema/pin/generated change, or refusal that would replace a Main
  positive.
- Revisit only after an existing authoring entrypoint supplies the native
  bundle/basis and stable row refs before mutation. A future bounded YES slice
  can then reuse `NativeSheet.preview/apply` and the existing commit/outbox
  path, with the required draft/rationale/save/retry/inverse qualification;
  until then, the detached row is not eligible for migration.

## Net consumers and evidence

- Current cumulative WC8 cleanup removed one dead private `_clip_row` helper
  (20 lines; commit `b5ab828ef`). It had no production callers. This worker
  makes no additional product deletion because the remaining caller is live.
- Remaining row: `astrid/packs/timeline/cli.py:3607-3612` →
  `astrid/sdk/timeline_sheet.py:829-846,918-1085` →
  `astrid/sdk/timeline/checkout.py:151-169`.

Targeted evidence on the current tree:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_sheet_native.py \
  tests/packs/timeline/test_cli_native_sheet.py \
  tests/sdk/test_timeline_sheet.py \
  tests/packs/timeline/test_verbs_working_copy.py
```

Result: **122 passed in 9.18s**.

No Runtime HTTP, full, browser, renderer, or live-socket suite was run: this
worker made no product-source change and the task forbids `full*` requests.
