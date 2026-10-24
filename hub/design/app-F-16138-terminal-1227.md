# Report: F terminal checkpoint 16138

The existing checkpoint reached terminal; no new request was submitted.

- Request: `app-U3b-F-reviewed-join-1146-full-1024120556-16138`
- Snapshot tree: `3311baa327c8963d007cfc3a1b2f04617085f3b3`
- Actual integration: `d99396bca7c3853435cfa5a5991f5b1073187be4`
- Command: `npm test -- --maxWorkers=3`
- Result: exit `1` after 1665s
- Vitest: 1,343 files / 19,251 tests passed
- Node suite: 257 passed, 38 failed, 26 skipped
- Declared platform skips: 27
- No core timeline failure nodes; final gate is not passed.

Seven bounded `wait-test ... 1` passes returned exit 124; the next same-ID wait returned terminal exit 1.

Failure inventory:

- 33 offline-verifier nodes: non-core, deferred external-pack/landing scope under D52. All share the `#/definitions/Meta` schema-resolution failure; the remaining assertions consequently fail. Upstream execution comparison is unknown. Paths: `scripts/astrid-landing/offline-verifier/verify.test.mjs`.
- 2 extension-evidence nodes: non-core, environment failures. Both fail because `ssh-keygen` is absent (`ENOENT`); `command -v ssh-keygen` also returned nothing. Upstream comparison is unknown.
- 1 known-failures guard node: non-core, ours-live regression candidate. The test expects three authorized markers, but the current drag test contains zero `.fails` markers and the guard reports zero authorized entries. Upstream execution comparison is unknown.
- 2 extension-ship verifier nodes: non-core, ours-live regression candidate. `package.json` removed `test:e2e:chrome-export`, while `scripts/release/verify-extension-ship.mjs:86` still requires it. Upstream execution comparison is unknown.

Recommended next steps:

1. Restore/provision `ssh-keygen` in the test environment.
2. Reconcile the known-failure guard with the current drag tests without weakening the gate.
3. Restore the required Chrome-export package script or update the release profile coherently.
4. Separately verify the offline verifier against matching upstream before deciding whether the `Meta` schema compatibility issue remains deferred or requires repair.

The worktree is unchanged and clean. Commit metadata and `DONE` were written.