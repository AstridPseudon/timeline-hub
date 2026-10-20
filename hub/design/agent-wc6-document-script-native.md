# Agent WC6: native timeline document publication

## Source and schema

- `astrid/packs/rendering/docs/scripts/timeline_document.py` now publishes
  through `TimelineSession.commit_many(..., via="document", base=...)` with a
  source-file `.outbox.json`. The exact base revision/publication pin is taken
  from checkout history or an exact existing history row.
- `astrid/sdk/timeline/document_diff.py` is the bounded typed adapter. It
  validates project/timeline scope, `base_parent_payload`, placement identity
  and order, shot baselines, and stable clip/track IDs against the exact pinned
  Runtime closure.
- The supported raw fields are clip `at`, `hold`, `from`/`to` where the
  registered trim command is valid, declared built-in `params`, and parent
  track `label`. Each command is captured and immediately applied with the
  canonical command runner; no display-ID lookup, prefix guess, client rebase,
  whole-parent replacement, or handwritten mirror rule is used.
- `TimelineSession` retries an existing pending flight from the original base;
  the script reads the unmodified pinned bundle when an outbox flight exists,
  so command capture is not redone from the latest head. The receipt stores
  candidate/command digests and the idempotency key; a same-file key with
  changed intent is refused.

## Held behavior and gaps

- Parent/child structure, placement membership/order, shot creation/deletion,
  narration/text payloads, DSL/opaque fields, child track/registry edits,
  selected-pack parameter schemas, and unrecognized raw fields remain explicit
  holds. The original source and positive behavior requirements remain intact.
- Legacy same-alias media replacement remains held because the existing native
  command set has no lossless recipe for updating the alias/registry/payload
  provenance as one bounded command. The existing catalog import/reuse/readmitted
  source path remains intact and is still covered by `test_authoring_media.py`;
  the legacy document-publication positive is retained as a strict xfail.
- Minimal follow-up owner/dependency: the Agent/Runtime command owner must
  qualify an existing occurrence media command (or an explicitly bounded
  equivalent) for same-alias replacement with exact source/provenance claims.
  Then remove the strict xfail and add the script-level commit/reload/readback
  assertion. This worker intentionally did not add a new endpoint, table,
  journal, schema override, proposal format, or legacy fallback.

## Tests and evidence

Targeted command:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="$PWD" /home/user/work/venv-agent/bin/python -m pytest -q -p no:cacheprovider tests/timeline/test_authoring_feedback.py tests/timeline/test_authoring_media.py tests/sdk/test_timeline_native_frontends.py tests/sdk/test_timeline_sheet_native.py tests/sdk/test_workspace_client_timeline_commit.py
```

Result: `148 passed, 1 deselected, 1 xfailed in 12.77s`.

The focused timeline pair alone also passed: `87 passed, 1 deselected, 1
 xfailed in 6.64s`. Ruff passed on all touched Python files, and `py_compile`
passed for the script and adapter. No full or live-socket suite was requested.
The adjacent native suites provide the existing evidence for guarded undo,
restart/lost-ACK exact retry, rebase, and outbox behavior; the new document
test covers native command emission, exact pinned-base refusal, held narration
and media edits, real feedback mapping, and same-key changed-intent refusal.

## Deletions and product diff

- Deleted the script-local `Writer` and its
  `publish_parent_composition` bridge (14 removed lines), removed the
  `publish_authoring_candidate` import/call, and removed the script's whole
  candidate publication path.
- No legacy publication caller remains in
  `astrid/packs/rendering/docs/scripts/timeline_document.py` (`rg` checked
  `publish_authoring_candidate`, `publish_parent_composition`, and `Writer`).
- Updated the rendering skill, document-checkout reference, and CLI journey to
  describe the native command/outbox route and explicit holds.

## Unverified

The real Runtime/App end-to-end private candidate roundtrip for the migrated
script was not run in this worker because the task forbids full/live suites.
The native client/session targeted suites and the script's fake-session
feedback/retry tests are the available evidence. Same-alias media publication
is intentionally not claimed as closed.
