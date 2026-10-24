## A3 report

Read-only investigation completed; no App source/test changes. `DONE` and commit message were written.

### Findings

- Canonical `am-burst` source:
  - Authored manifest: `astrid/packs/astrid_motion/rendering/elements/effects/am-burst/element.yaml`
  - Generated registry: `astrid/packs/rendering/elements/catalog.ts`
  - Revision: `sha256:f4b453923da74f104d41baf34ab9760bc7474d53d7ce034e11e0ec0197babf29`
  - Current Agent source and App vendor catalog/manifest are byte-identical.
- UI normalization preserves the exact identity: `id`, `kind: effect`, `packId: astrid_motion`, revision, schema, defaults, published/admitted state.
- Apply path is complete:
  `ElementsLibraryPanel` → synchronous `captureForTurn()` → `AstridElementOperationAdapter` → `useTimelineSave` element route → `createTimelineLocalSaveHandoff` → persisted outbox → `RuntimeDataProvider.commitTimeline` → generated client POST with `Idempotency-Key`.
- The exact `am-burst` path differs from passing `text-card` only at component resolution:
  - `text-card`/`rendering` resolves through Composition’s registry.
  - `am-burst`/`astrid_motion` resolves through the canonical `@astrid` Vite glob.
  The source file and catalog path are present and matching; persistent failure there is currently an environment/source-selection or module-admission unknown, not a source-proven defect.
- The current outbox path forwards the full v2 request fields required by C0, including commands, steps/patch, optional reads, merge, label, source, rationale, group, and `dry_run:false`. Accepted response envelopes and Runtime error details are retained.
- Contract naming discrepancy: current App/Runtime code accepts `accepted|rebased|merged`; the task wording says `historical_rebased`. This is cross-contract-wide, not motion-specific.

### Fixture/assertion gap

`tests/e2e/local/support/harness.ts` currently seeds parent registry assets but no opaque registry field. The exact motion test’s closure checks are self-consistency checks and do not assert the registry remained unchanged. Prior WIP evidence indicated `registry.opaque.keep` was removed.

Smallest guidance for Sol0557:

1. Restore the opaque registry fixture field if it was removed.
2. Keep the exact `am-burst` journey unchanged.
3. Add a direct unchanged assertion for the parent registry (and existing opaque config/clip/shot fields) around the motion apply.

No adapter/provider rewrite is indicated.

### Verification

- `git status --short --branch` — clean.
- SHA comparison of current Agent and App vendor catalog plus `am-burst` manifest — identical hashes.
- Frozen R4 App candidate catalog — does not contain `am-burst`.
- Tests/typechecks/full/browser/backend were not run, as explicitly prohibited for this investigation.