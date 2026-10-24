Completed the read-only D21 terminal-packet correction for:

`app-P3-current-integrated-0900-ap2-P3-gate5-h6-0348-1024103234-3896`

### Actual result

- Status: `fail`, exit `1`, duration `268s`
- Readiness: passed
- Original Gate-5 result: 1 failing test
- Assertion: expected `wire.attempts = 1`, received `2`
- Failure: `tests/e2e/local/three-products.spec.ts:1365`
- Caller: `prepareAfterAckLossMountedDocuments` at line `1613`

The failure occurred after the predecessor setup and reset path. Therefore predecessor POST200 and reset were reached/asserted PASS, not NOTRUN. ACK-loss handling, retry, reload, runtime restart, merge/history/undo tail remained NOTRUN.

No browser success was inferred from source ordering alone.

### Source identity

Declared selected source:

- Commit: `82cb5c0005df7abe0fcb8673f7be192a6c9e9183`
- Tree: `6fa0a0f32b212dbdae7c2ecaca1813de68907e67`
- Parents: `182c65242d8228232cde32961fd1948056dd841a`, `f56128d540ff96013c9532d79f3f4e767beba820`
- Full spec blob SHA256: `26c1ae764013f8907ff7f3664dbcee016c88bc17a797f66800d012e618165d5b`
- Static D50 tail hash, lines 1608–1741: `5ede6f374857a66a327da3cea0e85de0457a04267003f3f66e3d40ee4f380912`

The retained `snap` declares only tree `6fa0a0...`, key `d800...`, and a recycled worktree path. Its full commit/parents could not be authenticated. It is not relabeled synthetic or as confirmed `82cb`; actual daemon/provider identity remains UNKNOWN.

### Safe D21 JSON manifest

All retained JSON files parsed successfully with `jq empty`.

| Origin | Size | SHA256 |
|---|---:|---|
| `playwright-output/p3/mounted-readiness/three-products.mounted-rea-54c87-ed-owner-before-any-gesture/d21-environment.json` | 5305 | `1a333c111f399aac03f7aaf9b66f13c01dba41f5d6365832918f3c6e9ab1f88f` |
| `.../attachments/d21-environment-json-90f5eb84b49a2383b1ab65b266edf244221eda71.json` | 5305 | `1a333c111f399aac03f7aaf9b66f13c01dba41f5d6365832918f3c6e9ab1f88f` |
| `.../mounted-bootstrap-lifecycle.json` | 224 | `98ef1621a572cf0da026b45f632f9594214674f6a29da548a36ff580e8f9ffde` |
| `.../attachments/mounted-bootstrap-lifecycle-json-cf3046721821ea2795c42db75b67b918e42b4ff0.json` | 224 | `98ef1621a572cf0da026b45f632f9594214674f6a29da548a36ff580e8f9ffde` |
| `.../mounted-readiness-diagnostics.json` | 926 | `c7ebb186dda699a74301325271c0eca40bfec536aec4c87dd6b2d69d8a6e570d` |
| `playwright-output/p3/mounted-readiness/worker-0/d21-environment.json` | 5063 | `7375b45802ec5200dec9ad37411bef09b1cadd90a63fdb816d9cc6f9d9789bb6` |

These use the existing D21 v1 schema, bounded fact/projector controls, route/path sanitization, correlation through case/stage/source metadata, and private artifact writers. The lifecycle artifact is `UNKNOWN` for diagnostic loss; it is not a success claim. Gestures remain `NOTCAPTURED`.

Private/unqualified trace, logs, summary, and error-context bytes were preserved and not exported. No raw trace, auth, URLs, or request bodies were copied or reconstructed.

The full C0 request/reply contract remains unchanged in source, including all request identity, command, step, merge, read, source, rationale, group, dry-run, and idempotency fields plus `{data, receipt}` response metadata. No actual reply metadata was invented.

### Verification

- Retained readiness command: 1 passed.
- Retained Gate-5 command: 1 failed with the assertion above.
- `jq empty` over all retained JSON: passed.
- `git diff --check`: passed.
- Worktree remains clean.
- No new test suite or `wait-test` request was run.

Commit message written and `DONE` marker created.