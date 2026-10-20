# App placed-shot prompt browser journey source

Worker: `app-m2-shot-prompt-real-journey-source`.

This test owns only `tests/e2e/local/shot-settings-prompt-command.spec.ts`. It consumes the producer's committed D01 contract; it does not change product code, the shared fixture, or the existing M1 journey.

## Exact UI and helper contract

- The case opens the existing placed occurrence through `openEmbeddedCanonicalShot(page, seed.occurrenceId, 'F2 canonical shot')`.
- The prompt control is the existing production `Textarea` with `id="batchVideoPrompt"` in `BatchSettingsForm`. The test uses that DOM selector only; it does not inject React state, provider ports, authority, IDs, or a fake transport.
- Seed/readback uses the existing `seedThreeProducts(referenceAt?)`, `revisionBody`, and direct Runtime raw shot read pattern already used by `shot-name-command.spec.ts`.
- The new case calls the existing optional contiguous geometry `seedThreeProducts(3)`. The helper's default and the original M1 journey remain at `THREE_PRODUCTS_REFERENCE_AT = 15`; no fixture file or default was changed.
- No unplaced catalog shot path is opened. That path remains outside this film-history acceptance case.

## One acceptance case

The single serial case covers, in order:

1. A placed-shot Unicode prompt edit, exact `occurrence:{id}/shot` `shot.set` request, accepted history dependency, raw `settings.prompt`, complete shot opaque/root preservation, and unchanged parent config.
2. Reload followed by the real Runtime inverse, restoring the initially absent `settings` root.
3. A lost acknowledgement, durable outbox retry after Runtime restart, identical request body/idempotency key, and identical accepted receipt; then Runtime undo.
4. An explicit empty-string prompt write, asserted as `settings: { prompt: '' }` rather than absence, with raw readback and opaque preservation.
5. A relevant Runtime conflict while the App request is held, retaining the dirty Unicode draft and observing zero legacy composition-revision POSTs.

The browser gate is intentionally deferred until the producer commit is composed with the exact Agent/Runtime source tuple. Discovery and lint do not qualify the browser journey.
