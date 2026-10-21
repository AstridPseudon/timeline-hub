# AG01/WC7 rationale carrier boundary report

## Disposition

Blocked at the existing detached whole-document publication seam. No product
code or tests were changed, because the only remaining local publication note
is still required by an unbound legacy checkout and its original positive
assertion. The bounded native route already carries the message through the
existing outbox rationale field, so adding another adapter here would create a
second migration path.

## Evidence read

The settled plan, repository instructions, the AG01 ledger, and
`runtime-AG01-WC7-rationale-carrier-response.md` were read. The Runtime note
confirms that request `rationale`, `group_id`, `source`, and `label`, plus
command rationale, are existing carriers. It explicitly says the Agent may
retire the local publication note once the native request supplies rationale
and accepted consumers use existing history identity.

## Exact remaining consumer and blocker

The local note is in `astrid/sdk/timeline/publish.py:82-88`, inside
`_PublishMixin.publish()`. That method still accepts arbitrary detached
`Checkout` authoring, calls `store.publish_bundle()` with a whole stored
document at line 47, retires local draft history, and only then resets the
working copy and records the `kind="publish"` note. Its note contains the
original message as `reason` and the new head as local `evidence`.

The existing native carrier is already correct but belongs to a different
entrypoint: `astrid/sdk/timeline/native_checkout.py:199-233` handles an
explicitly attached checkout with exactly one supported parent command. It
seals the original message into `state['rationale']` before
`TimelineSession._flush()`. `astrid/sdk/timeline/sync.py:348-416` serializes
that rationale in the durable flight body, retries the exact body after
reload, and clears it only after the accepted Runtime acknowledgement.

There is no safe way to make the detached `_PublishMixin` note use that
carrier without first converting its arbitrary whole-document grammar into
native captured commands. That would overlap the held WC7 whole-writer
migration, risk losing unsupported/unbound authoring fields, and violate the
instruction to preserve local-only grammar. `NativeSheet.apply()` is already
the separate connected native path and is outside this bounded task.

The original visible behavior remains required by
`tests/sdk/test_timeline_journal.py:160-186`: it asserts that detached
`Checkout.publish("move the rocket")` records a local publish note with the
message as `reason` and the accepted head as `evidence`. Removing that note
now would lose a passing behavior test rather than replace its producer with a
native command/flight. The AG01 ledger likewise records this exact dependency:
the detached/mixed/unsupported WC7 consumer remains held until WC7 is native.

## Required owner dependency

The WC7 owner must first migrate the detached/mixed/unsupported
`Checkout.publish()` / `_publish_narration` whole-document consumer to a
lossless native command producer and explicit outbox, including a rationale
parameter captured at authoring time. Once that replacement exists, the local
`_journal.record_or_note(..., kind="publish")` hunk can be removed and its
original rationale assertion can move to a compact serialized-flight,
reload/retry, refusal, and draft-retention regression. Until then, the local
note is not duplicate accepted history for this path.

No new journal, metadata field, producer identity, authority path, endpoint,
schema, or Runtime change is justified.

## Validation

Focused command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider \
  tests/sdk/test_timeline_journal.py
```

Result: **20 passed in 1.61s**.

The same command without `/home/user/work/runtime` first failed during
collection with `ModuleNotFoundError: No module named 'runtime_protocol'`;
this was an environment locator issue, not a test or source failure. No full,
browser, socket, Runtime-service, or native-sheet acceptance suite was run.

## Files and ledger status

No repository files were modified. The AG01/WC7 row must remain in progress;
it must not be marked DELETED before the detached whole-writer replacement is
merged and qualified.
