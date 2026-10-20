# vw-m4-last-app-request-disposition-close

## Result

The remaining `vw-m3-native-frame-fixture-frozen-pair-proof` row is **SUPERSEDED** by App merge `4553d4b8c7a7fdf226b25634660c63da9f0c947a` (source commit `eadcb603a5796e3f4f64443b825d889e63248866`). The merge is present in actual App integration `812a609ee7ee02a6abe2fbf96513408e706c830d`; the current file blob is `b8c1705c3eca6b8b87a94be160aecd6da1e993d6`.

The exact missing guard families from the prior one-still-wanted disposition are all present one-to-one in `tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts`:

- Lines 10–72: separate Runtime server, official Runtime producer, and Agent identities; literal commit, tree, and archive SHA-256 checks; private archive extraction.
- Lines 77–90: `astrid.__file__` and `runtime_protocol.__file__` must resolve under the extracted roots, with ordered explicit Runtime-then-Agent `PYTHONPATH` entries.
- Lines 110–121 and 182–189: pre/post source manifests are compared, with Runtime server and producer kept as distinct identities.

The existing behavior assertions remain in lines 124–179: native `seed: false`, `/v1` restore, three media pins and dependency manifest, forged-task refusal, and unchanged object list/zero legacy-write audit.

The later current canvas successor `0f6220525` was checked directly: its diff against `4553d4b8` changes only canvas imports/profile parameterization and test invocations; it does not alter the guard block. No controller/PCM physical qualification is needed to close this test-only stale request, and none is claimed.

## Verification

Read-only source and integration checks passed:

- `git -C /home/user/work/app rev-parse tl/integration` → `812a609ee7ee02a6abe2fbf96513408e706c830d`.
- `git -C /home/user/work/app show tl/integration:tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts` → current file contains all required guard and retained assertion families.
- `git -C /home/user/work/app diff --check 4553d4b8c7a7fdf226b25634660c63da9f0c947a tl/integration -- tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts` → PASS.
- Direct presence checks for commit/tree/archive pins, module origins, ordered `PYTHONPATH`, before/after manifests, `seed: false`, zero legacy writes, and forged-task/object-list assertions → all PASS.

No test command was run, per the task. No source edits, dependency/cache writes, browser/render/full/install runs, or Git mutations were performed.

## Decision

Close the last table row as superseded by exact SHA `4553d4b8c7a7fdf226b25634660c63da9f0c947a`. This is based on the actual current file and the integrated merge’s source diff, not ancestry alone.

## Blocked / unverified

Nothing blocks this narrow table reconciliation. Browser/render/full qualification and physical frame/audio parity remain outside scope and unverified.
