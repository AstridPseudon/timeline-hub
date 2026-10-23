Implemented the P3 harness repair in two permitted files: `support/app.ts` and `mounted-readiness-safety.test.ts` (+102/−1 lines).

The bootstrap now waits for a readonly observation of a settled production owner matching the seeded project and timeline before closing. It uses the existing 5-second assertion timeout. The later 90-second fresh-owner poll, connected checks, original journeys, and D28 body remain unchanged.

Observed in actual11562’s retained trace:

- `call@22`: bootstrap outbox inspection returned `[]`.
- `call@24`: bootstrap page closed.
- `call@28`: blank-page database-existence probe returned `false`, without throwing. The subsequent database read was never called.
- Final exit was 2; connected-selection and fresh-owner stages were unreached.

The source establishes the ordering defect: track visibility precedes asynchronous verified-basis/identity reads and durable owner creation, while the old helper could close after an absent-database empty fallback. **Why production had not created storage by that point remains unverified.** The trace does not distinguish missing storage from an empty database at the earlier `[]` inspection.

Validation:

- `node --import tsx tests/e2e/local/mounted-readiness-safety.test.ts` — **10/10 PASS**. Actual bootstrap helper and production outbox writes, with mocked page/locators and vendored IndexedDB fake; covers absent, empty, unrelated, dirty, settled, timeout, and rejected-probe states.
- `node --import tsx "$TMPDIR/bootstrap-before.test.ts"` — reconstructed original helper: **8 PASS, 2 expected FAIL**.
- `node --import tsx tests/e2e/local/d21-environment.test.ts` — **7/7 PASS**.
- Typechecks below — **exit 0**:

```bash
flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 bash -c 'node node_modules/typescript/bin/tsc --noEmit -p tsconfig.app.json --pretty false && node node_modules/typescript/bin/tsc --noEmit -p tsconfig.node.json --pretty false && node node_modules/typescript/bin/tsc --noEmit -p tsconfig.json --pretty false'
```

- `node node_modules/eslint/bin/eslint.js tests/e2e/local/support/app.ts tests/e2e/local/mounted-readiness-safety.test.ts --max-warnings 0` — **PASS**.
- `git diff --check` — **PASS**.
- All four named actual-run source blobs equal the supplied `cdd262c6…` baseline.

Artifact SHA-256 values, under actual11562’s `playwright-output/` directory:

| Artifact | SHA-256 |
|---|---|
| `worker-0/d21-environment.json` | `b9af80a1ae8b6fd9bfa3d45faa59a17e5cb9e0d241abb3362be77685ff1fb989` |
| Test `d21-environment.json` | `523c3a9a349494b709847f1bb7d36ff0ce328b51392e6c7b46d5791813dd5be7` |
| Test `mounted-readiness-diagnostics.json` | `e946d77075875151ef4e99f135d43945feb4e04bab3f1f134d7173473616ebd5` |
| Private `trace.zip` | `a54d89d0876a17bc1c1324dacced39f2e7b11e58ab9fc21ad5082adad7c1d0e1` |
| Private `error-context.md` | `e658a41d5094f9848b475d3223238549f5dc5a83811c52d55df21786a01f9974` |

Trace extraction exported only finite call metadata and allowlisted results; no headers, credentials, principals, full URLs, or response bodies.

Protected D28 body SHA-256 remains `5d36c124aa3b6bcc7c5b2bea702566fedd4801d8b55602dd8f771c2ac5369696`; original Gate-5 file remains `0e69b561a0c750669f45e54259021179b355bde41a52e265b7ea198be7318f14`.

No live run or product readiness verdict was attempted. Next: copy source, bind the row, then run the single live qualification. P3 commit message and `DONE` were written; no Git mutation was performed.