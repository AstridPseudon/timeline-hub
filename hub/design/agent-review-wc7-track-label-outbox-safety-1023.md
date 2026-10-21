# WC7 currentpublished014 track-label Checkout outbox-safety review — APPROVE

## Scope and disposition

Reviewed source `5b32b3c2e` (`tl/agt-m2-wc7-track-label-existing-outbox-consumer-1014`),
working-tree patch `381437d57950fa159b04b20219685bf5d4d09b76f2dceb8585f11d0fd49d83e3`,
limited to:

- `astrid/sdk/timeline/native_checkout.py`
- `tests/sdk/test_timeline_native_checkout.py`

The initial review found a concrete HOLD: a manually persisted, valid-shape raw
`track.set` label request with no native `expect`/`reads`/binding capture passed
the new eligibility predicate and was sent. The generated test Runtime then
filled in authoritative capture fields, silently turning the arbitrary record
into a committed intent.

The patch now requires the existing native capture record before parent
track-label publication: explicit resolved target, stable track-id read,
`scalar.target` binding, label expectation, direct authorship, and the complete
native capture-field set. The raw-record regression leaves the record pending,
creates no flight, and makes no transport call. No fallback recapture, schema,
pin, DTO, store, authority, document-diff, or sheet-overlap change was added.

## Verified behavior

- Parent-only stable target uses `capture_track_set` and the existing outbox.
- Absent label, empty-string label, and explicit clear remain distinct.
- Captured base revision/publication, command guards, request body, idempotency
  key, and rationale remain unchanged through lost acknowledgement, reload, and
  retry.
- Conflict keeps the original pending command, flight body, base pins, and
  rationale as a draft.
- Unsupported attached writers remain held; the new raw label-shaped record is
  also held rather than becoming authoritative.

## Evidence

Commands, all from the review worktree with shared read-only dependencies:

```text
PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/sdk/test_timeline_native_checkout.py \
  tests/editing_conformance/test_parent_track_label.py
48 passed in 3.16s

PYTHONPATH="$PWD:/home/user/work/runtime" \
  /home/user/work/venv-agent/bin/python -m pytest -q \
  tests/sdk/test_timeline_sync_native.py
31 passed in 1.63s

git diff --check
passed
```

Not run by instruction/scope: HTTP or live Runtime-door tests, Runtime-native
qualification, browser/e2e, full suites, and broad repeated suites. The report
does not claim those results.

## Follow-up

The harness should commit the two worktree changes with the supplied commit
message. No further product changes are recommended for this bounded consumer.
