# Ordinary disjoint-label fixture repair

## Result

Repaired the ordinary journey fixture in `tests/e2e/local/three-products.spec.ts`.
The real capture-order gate had already emitted and accepted the full ten-command
ordinary batch; its later retry failed because Agent C and local B both wrote
`parent/track:V1`.

The retained gate response was:

```json
{"code":"conflict","details":{"base":{"publication_id":"txn-9535c6959bac4249aaf4650d2566b87e","revision_id":"authoring-parent-revision-874d84daad595b04fbc9859272c1a60040fc4351527084fc82ca8865eed2f7a4"},"conflicts":[{"base":{"state":"present","value":"V1"},"choices":[],"kind":"dependency_changed","ours":{"state":"absent"},"path":["label"],"ref":"parent/track:V1","theirs":{"state":"present","value":"F2 Agent ordinary sibling"}}],"current":{"publication_id":"txn-c472596830e34b95baf2e56c48d017b7","revision_id":"authoring-parent-revision-7f8e5a502bed10cbe02ab1160ec38f014c828f9cef5485c559070ce2e83c7e7a4"},"reason":"dependency_changed","status":"conflict"},"message":"original authored guard changed","request_id":"bdebdd896d344241a10193a04e8b280c"}
```

The approved duplicate repair establishes the intended independent seed: C
now labels real seeded `S1`; local B remains the unchanged `V1` label command.
No production, guard, recapture, schema, API, or negative-test change was made.

## Assertion map

- Lines 1153–1180 retain marker admission, one emitted public patch, and all
  ten native records/order assertions (two parent clips plus three occurrence
  clips, each move/hold pair).
- Lines 1191–1196 make Agent C write `S1`, preserving the accepted ordinary
  state and transition/placement checks.
- Lines 1204–1208 retain local B exactly as `track.set` on `parent/track:V1`.
- Lines 1212–1239 retain lost-ACK, reload, restart, persisted outbox, and
  byte-identical retry checks.
- Lines 1244–1254 now assert both retry labels: local B on `V1` and Agent C on
  `S1`, while retaining rebasing, opaque data, positions, and outbox closure.
- Lines 1256–1279 retain both guarded undos; the first undo explicitly asserts
  C's `S1` label survives, and the grouped ordinary undo still checks the
  complete Agent result, opaque data, immutable closure, and zero legacy traffic.
- The dependency-conflict negative beginning at line 1287 is unchanged, so the
  genuine same-field refusal and retained B guards remain covered.

## Checks

Passed:

```text
./node_modules/.bin/eslint tests/e2e/local/three-products.spec.ts --max-warnings 0
./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/tools/video-editor/commands/ordinaryRealBatch.test.ts
  1 file, 1 test passed
./node_modules/.bin/playwright test --config playwright.three-products.config.ts --list --grep 'M2 ordinary extension batch'
  1 test listed; no browser/socket run
git diff --check
```

No request-test, browser, localhost, live socket, runner, full suite, or
dependency/shared-install operation was run. The repaired real journey is
therefore not centrally qualified by this worker.

## Later gate

After the harness commits this candidate, run exactly one authorized ordinary
gate:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-ordinary-disjoint-label-fixture-fix e2e-m2-ordinary-committed-driver-gate) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

