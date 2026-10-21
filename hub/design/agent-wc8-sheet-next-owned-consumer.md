# WC8 next owned consumer — no eligible attached writer remains

Date: 2026-10-21
Worker: `agt-m2-wc8-sheet-next-owned-consumer`
Agent tree: current `tl/integration` at `4467c1c1a`

## Disposition

No product change was made. The current integration already migrated the
connected sheet apply ingress to the existing native adapter and durable
outbox. There is no second eligible attached `SheetClient`/sheet-merge caller
to migrate under the current public013 contract without inventing a basis or
stable row identity, refreshing guards, or changing the retained detached and
mixed behavior.

## Exact census

- `astrid/packs/timeline/cli.py:3599-3604` routes `--native` and every
  connected (`parsed.client is not None`) `apply` invocation to
  `_cmd_commit_edit(..., sheet=True)`.
- `astrid/packs/timeline/cli.py:3943-3953` loads the retained
  `NativeSheet` from the scoped outbox and calls its existing `apply` path.
- `astrid/sdk/timeline_sheet.py:603-846` is the native attached adapter. Its
  already-qualified cells use existing `clip.move`, `clip.set` (source hold
  and explicit clears), `clip.set-params`, `track.set`, `clip.trim`, and the
  parent `clip.delete` capture functions, then one `TimelineSession.commit_many`
  batch. The retained bundle, basis, row `# ref` bindings, opaque values,
  clear semantics, atomicity, and exact in-flight retry identity remain in
  this path.
- `astrid/sdk/timeline_sheet.py:849-870` is the remaining `apply_sheet`
  entrypoint. It rejects native `clips`/`tracks` rows and retains the documented
  detached legacy grammar and local rollback behavior.
- `astrid/sdk/timeline_sheet.py:873-927` retains the documented
  `apply_sheet(..., client=client)` history lookup API; it is not an attached
  native writer. `:938-1012` is the legacy client-side three-way
  `merge_sheet`; `:1015` onward is the legacy `_apply_parsed`/whole-checkout
  mutation path, including the remaining omission handling.
- `tests/editing_conformance/runner.py:388-416` deliberately invokes the
  no-client detached `apply` path for legacy sheet conformance. It has no
  retained native export/basis and cannot be converted to the native path
  without changing its documented detached/mixed coverage.
- A repository-wide source census found no `SheetClient` class or additional
  production `apply_sheet`/`merge_sheet` caller. The only production writer
  call is the detached fallback at `astrid/packs/timeline/cli.py:3607-3612`;
  connected callers do not reach it.

The remaining writer is therefore exactly the detached legacy
`apply_sheet -> merge_sheet -> _apply_parsed -> Checkout.save` path. It must
remain until each unsupported legacy grammar (narration, sound/media,
structure/addition/removal, looks, relational timing, and other mixed rows)
has a native command path and equivalent qualification. This is not a whole
WC8 deletion claim.

## Current pin decision

The current public013 pin already contains the existing native operations
listed above; prior current-public013 HTTP evidence qualifies the attached
native sheet export/apply/reload/retry/undo behavior. The blocker is not a
missing public013 operation for the supported cells. The blocker is that the
remaining caller is detached and its legacy text has no retained native
bundle/basis or stable `# ref` identity. A conversion would require
unsupported identity recovery or a new syntax/carrier, both outside this task.

## Tests

Direct targeted neighbors:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_sheet_native.py \
  tests/packs/timeline/test_cli_native_sheet.py \
  tests/sdk/test_timeline_sheet.py \
  tests/packs/timeline/test_verbs_working_copy.py
```

Result: **122 passed in 9.25s**.

No Runtime HTTP case was run because this worker made no real consumer or
source change. No full, browser, renderer, or passing-suite rerun was run.
The worktree remains clean.
