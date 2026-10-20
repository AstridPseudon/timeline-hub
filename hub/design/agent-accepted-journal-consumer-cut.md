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

## Follow-up consumer migration — 2026-10-20

The follow-up worker migrated the first remaining real accepted-history consumer:
legacy sheet basis lookup in `astrid/sdk/timeline_sheet.py`. With an
authenticated client, `find_version` now uses the existing `RuntimeRevisions`
adapter and opens exact retained revisions through `Checkout.open`; it no longer
uses local exported/undo snapshots to answer an accepted-history lookup. The
no-client local draft journal/stack path is preserved. This closes the
consumer/equivalence gap without adding a journal, snapshot writer, API, or
second outbox/history.

The integration module’s ephemeral Runtime locator is now explicitly
`/home/user/work/runtime` by default and still honors `ASTRID_RUNTIME_CHECKOUT`.
The locked producer remains `2c4ac180c2220bdad966bc01e95ad230e99ce26a`.

Final central targeted result `agt-m2-ag01-runtime-history-preservation-targeted-1020172115-28733`:
**27 passed, 2 deselected**, exit 0, tree
`3190b22e8f5425077a8a788ef9e69c181ade65d0`. Direct focused results: history 5,
journal/revisions 46, sheet/native 73 passed. AG01 remains **in progress**
until integration; WC7/WC8 remain held.
