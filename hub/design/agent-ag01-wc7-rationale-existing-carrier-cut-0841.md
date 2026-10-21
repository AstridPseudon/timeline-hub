# AG01/WC7 rationale existing-carrier cut

## Worker disposition

This bounded cut is blocked at the existing detached whole-document writer.
The native attached command path already carries the original publication
message through the existing request/flight `rationale`; the remaining local
note is not a duplicate on that path.

## Owned hunk

The exact remaining local note consumer is
`astrid/sdk/timeline/publish.py:82-88`:

```text
before = _journal.document_digest(self.document())
self._reset_base(client=client)
_journal.record_or_note(... kind="publish", reason=message, ... evidence=new_head)
```

This code is reached by `_PublishMixin.publish()` after the arbitrary detached
`stored_document()` has been sent through `store.publish_bundle()` at line 47.
It is therefore still the authoring path for unbound/local-only checkout
grammar, not the native attached checkout consumer.

The replacement carrier exists at
`astrid/sdk/timeline/native_checkout.py:213-227` and
`astrid/sdk/timeline/sync.py:348-416`: the attached path seals the original
message into outbox `rationale`, persists the exact serialized flight before
transport, refuses changed rationale on retry, and clears it only after the
accepted response. It does not refresh capture. NativeSheet is a separate
connected adapter and was intentionally not touched.

## Why no deletion was made

The detached publisher has no native command capture, explicit outbox target,
or request-level rationale argument. Deleting its local note before migrating
the arbitrary whole-document grammar would remove the original passing
behavior asserted by `tests/sdk/test_timeline_journal.py:160-186` and would
not provide an equivalent accepted-history consumer. A new bridge or metadata
field would violate the settled Runtime response and create duplicate
authority.

The precise dependency is WC7's held detached/mixed/unsupported whole-writer
migration: first produce lossless native commands from that authoring path and
carry the original message as the existing flight rationale; then delete only
the post-acceptance local publish note and replace its visible assertion with
one compact serialized outbox/reload/retry/refusal/draft-retention regression.

AG01/WC7 remains in progress. Do not mark the row DELETED before that
replacement is merged and qualified.

## Validation

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_journal.py
```

`20 passed in 1.61s`.

No full or native-sheet acceptance suite was requested or run. No repository
product/test files changed.
