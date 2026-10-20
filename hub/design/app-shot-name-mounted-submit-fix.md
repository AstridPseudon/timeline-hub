# App M2 embedded shot-name mounted submit fix

Status: **mounted input diagnosis fixed; central browser qualification remains unverified at an assertion contract mismatch**.

## Final source and diagnosis

- App worker HEAD: `8f27c052b6ba6cdeb70066f188d5d5aa72d617ef`.
- App HEAD tree before the uncommitted fixture delta: `f27821adaa105f7e430112ae9a511d8f90c537ff`.
- Central final-source snapshot tree containing the two-file delta: `6a4284b1c516412b3e528ebc7531472efb8f4d05`.
- `tests/e2e/local/shot-name-command.spec.ts`: `ad7a21d80f5711ee08e8fd083b5b551dc5bc1156b5885755574ceff0f8253ce2`.
- `tests/e2e/local/support/app.ts`: `312a9109517aaaf30360313a78465e6666414aeb273e24a308f18020550670a4`.

The previous zero-commit trace did not exercise the shot-name port. The helper selected `dialog.locator('input').first()`, which is the mounted timeline track-label input (`aria-label="Track name"`). Enter therefore followed `track.set`; its alert was `track.set label capture is unavailable.` The production shot-name header input is now selected with `input:not([aria-label="Track name"]):visible`, and the helper verifies its initial seeded value before filling. This is a fixture-only correction to select the actual production input; no native event, readiness guard, basis guard, raw value, unmount guard, or error behavior was changed.

Production path traced: `AstridTimelineEditor` → guarded `useTimelineCommandSession` `shotSet` port → `LocalTimelineShotBrowser` → `ShotEditorView` → `ShotSettingsEditor` → `useNameEditing`. Root readiness remains the existing `commit.data !== null && initialRecoveryChecked` gate in `useTimelineSave.ts`; no automatic pump or general native API was added.

## Central final-source run

Registered suite:

`e2e-shot-name-mounted-submit-final-8f27-agent8130-runtime2c4-public12`

The registered source used frozen Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, frozen Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, public source `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`, setup `88888d44ddd375caacb7b45b74001b70428bf4404b76fe11c84a83f8b05a6cfa`, Chromium 141 (`85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`), and private short temp/cache paths.

Run ID:

`app-m2-shot-name-mounted-submit-diagnosis-fix-e2e-shot-name-mounted-submit-final-8f27-agent8130-runtime2c4-public12-1020154238-7762`

The strict source, frozen-peer, Agent/Runtime artifact, browser, cache, and no-distribution guards passed. The real mounted journey emitted one `/v1/.../commit` request and passed the exact body, base revision, occurrence read, and accepted response setup assertions. It stopped at `tests/e2e/local/shot-name-command.spec.ts:162`:

```text
Expected: commands[0].dependencies contains { key: "shot.source", policy: "exact" }
Received: commands[0].dependencies === undefined
```

This is a serialization-layer mismatch in the existing assertion, not a missing source dependency. Frozen Agent `shot_set()` calls `ctx.dependency(...)`; `Recording` stores that in the separate record field, while `Plan.commands` returns only `record['command']`. App `finishShotSet()` likewise returns `record.dependencies` separately but enqueues `commands: [result.command]`. The HTTP command body consequently has no `dependencies` key by contract. The assertion was left intact to preserve the requested exact-body checks; no unsafe field injection or guard weakening was made.

Because the central test aborts at that assertion, later raw Unicode, reload/Undo, lost-ACK/restart, exact retry, real 409 draft, and zero-legacy assertions were not executed by this run. No browser qualification is claimed.

## Remaining writers

Unchanged and intentionally out of this embedded NAME slice: standalone/canonical fallback writers in `ShotEditorView.tsx` (`enqueueCanonicalShotPublish` / `updateCanonicalShotName`), its legacy `useUpdateShotName().mutate` fallback, gallery/list `VideoShotDisplay.tsx` `useUpdateShotName().mutateAsync`, and the separate canonical settings writer (`updateCanonicalShotSettings` through the whole-graph CAS callback). `MAIN574` layout/display metadata and the current `span[title="Click to edit shot name"]` input remain outside this fix.

## Tests

- Targeted Vitest: 8 files, 149 tests passed.
- ESLint on touched e2e files and relevant neighbors with `--max-warnings 0`: passed.
- `node --test scripts/testing/current013-integration.test.mjs`: 1 passed.
- Playwright discovery with `playwright.shot-name.config.ts`: exactly 1 test discovered.
- `git diff --check`: passed.
- Central final-source browser suite above: setup/build/guards passed; test failed at the documented `commands[0].dependencies` assertion.

No full suite, TypeScript compiler, install, framePCM, renderer, or shared-dependency mutation was run.
