# App M2 shot-name record-carrier browser gate

Status: **source assertion repaired; central browser qualification blocked by the test-service runner preflight**.

## Contract correction

The previous new assertion looked for `shot.source` under `commands[0].dependencies`. That is not the frozen contract: the accepted wire `EditCommand` is closed and carries no `dependencies` field. Agent records the dependency separately, and App submits only `record.command`.

The assertion now preserves the existing exact command-body checks, explicitly asserts that the submitted command has no `dependencies` property, then uses the existing authenticated Runtime read:

`GET /v1/projects/{project}/timelines/{timeline}/commits?limit=50`

It selects the accepted history entry by the response receipt/publication ID and asserts the same dependency policy on `records.commands[0].dependencies`: `key: "shot.source"`, `policy: "exact"`. No new wire field, guard, endpoint, or production change was added.

Old carrier → new carrier:

`accepted.body.commands[0].dependencies` → `acceptedHistory.body.items[acceptedPin.publication_id].records.commands[0].dependencies`

## Source identity

- Worker base HEAD: `f598b4b8ee7b457991646dfe8f936caaacb3f39e`
- Worker base tree: `6a4284b1c516412b3e528ebc7531472efb8f4d05`
- Final modified source blob (`tests/e2e/local/shot-name-command.spec.ts`): `5927edc5485da93a37c35fd26c698c60f7955ac4`
- Central snapshot tree: `b52120ac0772d1874ed5d1c569c614c556f0033a`
- Frozen Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`
- Frozen Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`
- Public12 source: `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`
- Setup guard: `88888d44ddd375caacb7b45b74001b70428bf4404b76fe11c84a83f8b05a6cfa`
- Chromium 141 binary: `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`

## Verification

Passed locally:

- `node_modules/.bin/eslint tests/e2e/local/shot-name-command.spec.ts --ext ts --max-warnings 0`
- `VITEST_CACHE_DIR="$PWD/.tmp-vitest-cache" node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-file-parallelism src/tools/video-editor/commands/shotSetCapture.test.ts src/tools/video-editor/commands/commitSession.test.ts src/tools/video-editor/commands/shotSetSession.test.ts` — **3 files, 80 tests passed**
- `node --test scripts/testing/current013-integration.test.mjs` — **1 passed**
- `TMPDIR=/tmp/tl-shot-name-discovery-record-carrier PLAYWRIGHT_OUTPUT_DIR=/tmp/tl-shot-name-discovery-record-carrier-output node_modules/.bin/playwright test --config playwright.shot-name.config.ts --list` — **1 test discovered**
- `git diff --check` — passed

Central run requested once:

- Test ID: `app-m2-shot-name-record-carrier-browser-gate-e2e-shot-name-mounted-submit-final-8f27-agent8130-runtime2c4-public12-1020155056-14425`
- Snapshot tree: `b52120ac0772d1874ed5d1c569c614c556f0033a`
- Result: **did not reach the browser case**; service summary reported failure after 201s with no test counts. The result `log.txt` and `runner.log` were empty and the exit artifact was `2`, indicating external runner/preflight failure before Playwright output. No raw-Unicode, reload/undo, lost-ACK/restart/retry, 409 draft, or zero-legacy browser result is claimed.

## Ledger note

No deletion-ledger row was changed or marked `DELETED`. This worker only corrects the evidence carrier for the embedded canonical shot-name gate. Existing fallback/gallery/settings writers remain out of scope, and no MAIN574 join or manager integration was performed.

## Next step / blocker

The central named runner must be repaired or refreshed so its preflight can execute this final source snapshot and emit Playwright logs; then rerun the one browser case. The source assertion itself is ready and the production tree is unchanged.
