# Agent sheet legacy cut native gate

## Scope

This gate repairs the `timing.for.card` integration fixture only. It does not
add a public writer, schema field, migration API, or product behavior.

## Fixture and setup provenance

- Main source: `tests/fixtures/timeline_editing/tiny.json`,
  `shots.B.internal_timeline`. The admitted parent preserves the original
  `b-type` ID, `clipType`, `track`, `at`, `hold`, `params`, and exact
  `app.cut=c2`, `app.layer=card`, `app.for=1.0`; the sibling Main clips and
  registry are retained as well.
- Media P/Q/R are created with ordinary Runtime ingest in the test realm.
  The P transcript is created as an ordinary `media.transcript/v1` Document
  with valid `segments`, then pinned by the canonical document manifest.
- Setup uses Runtime's existing test-only
  `seed_trusted_legacy_parent(service, document, idempotency_key=...)` from
  Runtime commit `382f523ef957afb2bd299c5e21424ca821b23f05`, helper SHA-256
  `5e152bfa716b9003b831648cad16f6adb9c334cd18a6a7cf32a31accefe82617`.
  The helper is loaded from its Runtime archive; its private persistence
  acceptance is used only in the ephemeral test realm.

## Gate sequence

1. Seed the exact legacy parent through Runtime's trusted setup helper.
2. Restart Runtime and open the timeline through the authenticated public SDK.
   Assert the accepted setup head, exact parent clips, and exact `b-type` row
   before any NativeSheet edit.
3. Export NativeSheet, edit only `hold` from `1` to `1.5`, and assert the
   existing `clip.set` capturer produces the command while preserving
   `app.cut` and changing `app.for` to `1.5`.
4. Commit a disjoint `type` track label from a peer, then submit the stale
   NativeSheet edit over authenticated Runtime HTTP. Assert `rebased`, exact
   target app metadata, and retained peer label.
5. Restart, read back through the public SDK, and undo the NativeSheet receipt.
   Assert the exact original `b-type` row is restored and the peer label
   remains. `Checkout.save` and legacy projection construction are tripwires;
   neither may be used.

## Evidence

Central named lane, final semantic test node:

```text
native-script-current-integration
tests/editing_conformance/test_native_sheet_current_runtime.py::test_http_legacy_cut_native_for_admits_rebases_reads_and_undoes
1 passed in 2.98s
```

Static checks after the final import-only formatting cleanup:

```text
PYTHONDONTWRITEBYTECODE=1 /home/user/work/venv-agent/bin/python -m ruff check --no-cache tests/editing_conformance/test_native_sheet_current_runtime.py
git diff --check
```

No full suite or other live-socket suite was run. No product/schema changes
were made.
