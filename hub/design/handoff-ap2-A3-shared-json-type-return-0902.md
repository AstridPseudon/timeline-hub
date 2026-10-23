# A3 shared JSON type return handoff

- Source commit: `2d3d14d998be2b59fb017b4c0f2458c3a7340423`
- Source tree: `7cd3b112b824711cebb87a6e25ce249461d574cc`
- Source file blob: `2a710a34cf6ffd16e8b4bc8a3abaebb7210ef09f`
- Final working file blob: `7414e29b369448ff900370fb2a53644a740472b8`
- Changed file: `src/tools/travel-between-images/components/shotTimelineDataProvider.ts`
- Change: shared popup ADD now sends the complete row through the existing `toOutboxJson` finite-JSON boundary before generated `EditCommand.args`; no fields, guards, receiver binding, fork ordering, or SWAP behavior changed.
- Scope controls: no generated schema/client, executor, route, move/undo/handoff/child/provenance/spec/support, fixture, lock, package, shared install, or deletion changes.
- Verification:
  - `./node_modules/.bin/vitest run --config config/testing/vitest.config.ts src/tools/travel-between-images/components/shotTimelineDataProvider.a3.test.ts --no-cache` — 25 passed.
  - `./node_modules/.bin/eslint src/tools/travel-between-images/components/shotTimelineDataProvider.ts --max-warnings=0` — passed.
  - `./node_modules/.bin/tsc -p tsconfig.app.json --noEmit` — passed.
  - `git diff --check` — passed.
- Not run: full suite, HTTP/body/browser/socket/build/service tests, per task limits.
