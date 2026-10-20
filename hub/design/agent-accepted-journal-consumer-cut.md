# AG01 accepted-journal consumer cut — worker note

On current Agent `79b33f8a` / public013 baseline, the remaining live
accepted-specific local-history consumer was `_PublishMixin.publish()`'s
post-acceptance `journal.record_or_note(..., kind="publish")` call. It was
removed after the existing native `TimelineSession`/Runtime-history retry,
reload, guarded undo/redo tests remained intact. The local JSONL reader and
draft records remain for legacy visibility and unsent working-copy history.

Touched only:

- `astrid/sdk/timeline/publish.py` — delete accepted duplicate journal append.
- `tests/sdk/test_timeline_journal.py` — preserve receipt/head assertion and
  assert no duplicate local accepted record.

Targeted result: **139 passed**. The central Runtime-paired test request was
not qualified because its test environment had no Runtime checkout (one skip,
exit 5). AG01 stays **in progress** pending manager ledger update after merge;
WC7/WC8 remain held.
