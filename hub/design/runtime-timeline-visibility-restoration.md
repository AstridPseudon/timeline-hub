# Runtime timeline visibility/restoration boundary

Date: 2026-10-20 UTC

Runtime keeps the existing timeline archive and recover operations as
project-scoped catalog mutations. Archive increments the timeline catalog
version and sets `archived_at`; recover clears `archived_at` and increments the
catalog version. Both preserve shots, references, canonical head/publication,
accepted closure/document bytes, CAS, and film recorder/history rows. They use
the existing timeline event and command receipt/idempotency paths, including
expected-version conflicts and exact retries.

`recover_timeline` is unarchive only when `version` is absent or names the
current catalog version. A requested non-current version is a visible 410
refusal before any write, with `timeline.restore` named as the replacement. An
exact receipt produced by the new visibility-only recover remains replayable;
legacy historical recover receipts are not replayed. Canonical historical film
restoration continues through the existing actual-Agent-provider
`timeline.restore` path.

The implementation intentionally does not append `timeline_revisions` or
materialize legacy internal revisions for archive/unarchive. This keeps catalog
visibility outside film history while retaining the existing timeline event and
idempotency receipt semantics.
