# AG01/WC7 native rationale-note consumer cut

## Disposition

Blocked with no repository changes. The qualifying native accepted-history
consumer is already migrated in the assigned tree. The remaining local
`publish` note is the detached whole-document legacy writer, not a duplicate
native accepted-history consumer, so deleting it would remove a live original
behavior without an equivalent sealed flight.

## Exact source/tree

- Repository: Agent worktree
  `/home/user/work/wt/agt-m2-ag01-native-rationale-note-consumer-cut-1026`
- Base/source commit: `b3c96a758c1cfa2a609d1498e0e9ee401b32cc40`
- Source tree: `3467b7bffb0fe6edf9178c9a9de4d446c8ab8857`
- Worktree status: clean; no product or test files changed.

## Existing native proof

`astrid/sdk/timeline/native_checkout.py:199-233` is the qualified attached
`AttachedCheckout.publish()` path. It seals the original `message` into the
existing outbox `rationale` before `TimelineSession._flush()` and returns the
accepted revision/receipt plus the retained rationale. `astrid/sdk/timeline/sync.py:348-416`
persists the exact serialized flight before transport, retries that exact body,
rejects changed retry identity/body, and clears rationale only after the
accepted response. Runtime's existing history facts are the accepted revision,
publication/receipt identity, previous head, source, label, and rationale.

The existing native tests already exercise the relevant behavior, including
the original rationale, exact retry after reload/lost acknowledgement, and an
unrelated local outbox remaining untouched:

- `tests/sdk/test_timeline_owned_move_publish.py`
- `tests/sdk/test_timeline_native_checkout.py`
- `tests/editing_conformance/test_owned_move_publish_runtime.py` (existing
  HTTP qualification; not run here)

## Exact remaining live caller

The only remaining accepted-specific local-note writer is
`astrid/sdk/timeline/publish.py:82-88` inside `_PublishMixin.publish()`:

```text
before = _journal.document_digest(self.document())
self._reset_base(client=client)
_journal.record_or_note(... kind="publish", reason=message, ... evidence=new_head)
```

This method is the detached `Checkout.publish()` path (also reached by the
existing CLI publish caller at `astrid/packs/timeline/cli.py:2983`). It first
sends arbitrary `stored_document()` whole-document state through
`store.publish_bundle()` and then resets the local working copy. It has no
native command capture, explicit outbox target, or request-level sealed
rationale. Its local note remains the original visible reason/evidence behavior
for unbound and legacy writers. Local draft save/edit journal records are also
outside this cut and remain needed.

## One missing existing fact / blocker

The missing fact is a **lossless native command capture for the arbitrary
detached whole-document authoring path**. Without that capture there is no
original sealed native flight whose rationale can be preserved, and no accepted
command/publication fact that can replace the detached note. Creating that
bridge here would overlap the held WC7 whole-writer migration and would invent
new authority or metadata, contrary to the settled plan.

Therefore the local note was deliberately not deleted and its passing original
assertion was not rewritten or weakened. The exact next step is for WC7 to
convert the detached/mixed/unsupported whole-document writer to lossless native
commands and the existing outbox rationale carrier; only then can this
post-acceptance local note be removed and replaced by accepted history/receipt
assertions.

## Validation

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_native_checkout.py \
  tests/sdk/test_timeline_owned_move_publish.py \
  tests/sdk/test_timeline_journal.py \
  tests/sdk/test_timeline_checkout_history.py
```

Result: **62 passed in 5.35s**.

No full suite, browser/socket suite, or central Runtime HTTP suite was run.
