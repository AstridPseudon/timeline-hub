## Report

- No source, fixture, test, or assertion changes.
- Classification: **D18 fixture owner**.
- Input verified: 8,957 bytes; SHA-256 `e61c49fe…3b01d`.
- Invalid field: `canonicalDocument.parent_revision.payload.config.tracks[2].opaque`.

Evidence:

- App bridge feeds raw canonical config into `buildTimelineData` (`preparedImageRequestProducer.ts:127-149`).
- Preview reconstruction preserves `base.tracks` unchanged (`media.ts:538-546`; `timeline-data.ts:404-407`).
- App validation rejects any track key outside `id`, `kind`, `label`, `role`, `scale`, `fit`, `opacity`, `volume`, `muted`, `blendMode`, and `app` (`timeline-domain.ts:202-214, 2607-2620`).
- Pinned Runtime and Agent contracts likewise define a closed track shape; `opaque` is unsupported. Extension data belongs in the permitted `app` bag.

Therefore this is not a testbridge-only defect and does not establish an App A2 defect rejecting supported unknowns. The production path would reject this same malformed track before output, as previously recorded.

Tests:

- No tests run; task was read-only and explicitly prohibited full producer/provider/browser/HTTP runs.
- One finite offline probe was attempted but stopped at environment setup: missing `@astrid/packs`; no product conclusion was based on it.
- Prior unchanged producer report: failure before output with `invalid_placement: Serialized track 'visual' has unexpected key 'opaque'`.

Smallest owner action: Agent/fixture owner should reissue `design/agent-A4-image-live-2315-input.json` with a contract-valid track shape. Do not add a guard waiver or blanket opaque-field deletion.