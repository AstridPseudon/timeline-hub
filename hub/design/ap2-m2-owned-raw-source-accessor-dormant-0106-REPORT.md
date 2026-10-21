# App2 M2 owned raw source accessor — 0106

## Result

Implemented one dormant, row-local accessor in `src/tools/video-editor/runtime/admitted-elements.ts`.
It scans the existing `current.elements` raw record for the exact project and all four owner-qualified fields: `packId`, `kind`, `id`, and `revision`. On success it returns only the existing `DocumentPin` carrier derived from the raw binding and the existing four-field snapshot object descriptor. It performs no Runtime, catalog, browser-hash, latest, Vite, Provider, session, or save lookup.

Missing binding, missing or malformed snapshot object, foreign element project, foreign binding project, missing owner, and missing exact ref return a visible `{status: 'refused', reason}` result. No caller or add emission was wired; the accessor remains dormant because the current admitted pin does not carry `f83`.

## Tests and checks

- `TMPDIR=<private task temp> ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache src/tools/video-editor/runtime/admitted-elements.test.ts` — PASS, 1 file / 10 tests.
- `./node_modules/.bin/eslint src/tools/video-editor/runtime/admitted-elements.ts src/tools/video-editor/runtime/admitted-elements.test.ts --max-warnings 0` — PASS.
- `./node_modules/.bin/tsc --noEmit --pretty false --skipLibCheck -p tsconfig.app.json` — exit 2 on pre-existing unrelated errors in App/Composition/runtime integration. No diagnostics were reported for either changed file. Examples include generated `ServiceStatus`/`Health` drift, missing Composition exports, and existing `Object.hasOwn` target errors.
- `git diff --check` — PASS.

No full, browser, localhost, live-socket, Runtime-door, pin, activation, or broad 28-test investigation was run.

## Scope and callers

Changed files:

- `src/tools/video-editor/runtime/admitted-elements.ts`
- `src/tools/video-editor/runtime/admitted-elements.test.ts`

Changed export: `admittedElementSource` (dormant). Live product callers changed: none. Test-only callers: the two focused accessor tests. HOME/Vite preservation of `snapshot_object` remains a separate request and was not edited.

## Decisions and blockers

Reused the existing `DocumentPin` and `VerifiedDocumentObject` field types, Agent's existing camel-case binding identity, and the existing status-style available/refused result convention. No new DTO, store, provider/session seam, wrapper, script, framework, or SYSTEM8e path was added.

The supplied `currentHOMEstatus.md` path did not exist. I used the available latest App2 status and HOME peer updates in `managers/app2/STATUS.md` and `managers/app2/INBOX.md`; this did not change implementation scope.

No implementation blocker remains. The app-wide TypeScript baseline remains red as noted above.

## Recommended next step

After the separately coordinated HOME/Vite preservation lands and the current pin contains the approved `f83` field, have its future consumer call this accessor before any capture/submit path and preserve the refusal result. Do not activate it on the current pin.
