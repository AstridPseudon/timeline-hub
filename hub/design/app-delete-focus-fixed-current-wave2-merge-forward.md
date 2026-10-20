# App delete/focus fixed current-wave2 merge-forward

## Source handoff

- Working source base: `e13800f1f2a174d46ec3990bbd47fb8c76cd3838` (`test(timeline): focus selected clip before parent delete`).
- Frozen delete product parent: `1981ce9801b661a9a335201b0ebd4fcdf1d8aad1`.
- Common source: `3e69e44f5fdfd1ea27f5f8ac677b4d385db2cba5`.
- Current wave2 merge parent: `0d5009e18bee8e29f894dabf5db501a0fcea750f`, parents `3e24e0632669375a84e75c8ff0da315bdc88a45c` and `b58f4f1b53f85fa6c2f15a8aabf144460a75300c`, tree `b323667662d565526d7c2395733f26e2c6380378`.
- Candidate working tree: `92fd62f4adecdb3f93acf92a5444bf035d6aa19e` (computed with a temporary index/object store from the final worktree; the harness must create the committed two-parent candidate with `0d5009e…` and the delete/focus source parent).
- Candidate commit SHA is intentionally pending the harness commit; this worker did not mutate git refs or commit.

## Changes

Applied the current wave2 root forward and resolved only overlap wiring. The resulting source retains parent clip delete, generic patch, and element command ports together; generic mixed/unsupported classification remains atomic; the delete port remains parent-only and guarded; legacy unsupported/group/occurrence routes remain unchanged. The focus fixture asserts selected production clip, focused production clip action, and sends the real Delete key; it does not inject a command.

## Tests

- `PRIVATE13_NODE_MODULES=<private extracted 0.0.13 overlay> NODE_PATH=<same> ./node_modules/.bin/vitest run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1` with the delete/generic/element/session/hook/keyboard/group/occurrence controls: **15 files, 289 tests passed**.
- Same private13/public13 runner with root preservation cohort (bootstrap, selection/media import, generic/element, App2 helpers, PCM/audio, composition, and TimelineOps controls): **16 files, 267 tests passed**.
- `node config/vite/timelineCompositionPackage.test.mjs` under the private extracted 0.0.13 overlay: **9 subtests passed**.
- `node --test scripts/testing/current013-integration.test.mjs`: **passed**.
- `NODE_OPTIONS=--experimental-vm-modules node --test scripts/testing/current013-parent-delete.test.mjs`: **passed**. The same command without the flag failed at Node startup because `node:vm` did not expose `SourceTextModule`.
- `--configLoader=runner --no-cache` was attempted and reached the known repository config limitation (`__dirname is not defined`); no source test was collected in that attempt.
- `git diff --check`: **passed**.

The shared node_modules install was not changed. A first broad run against the stale shared Composition package failed at import time (`0.0.10` lacked public13 media exports); the private extracted public13 rerun above is the qualifying result.

## Remaining actual gate

No browser/local-socket/e2e run was performed here. After the harness creates the strict declared commit/tree, the central test service must run the dedicated fresh two-case current013 parent-delete journey against this exact committed candidate. It must prove both real UI Delete cases, including focus/selection, retry/reload/runtime restart, inverse restoration, conflict draft retention, opaque/prototype/raw mirror preservation, idempotency-key versus receipt identity, and zero legacy writes. Until that central run passes, this handoff makes no mergeretirement or end-to-end qualification claim.
