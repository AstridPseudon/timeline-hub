# App parent-delete MAIN574/public13 gated port

Status: code port complete in the worker tree; current-source central browser proof is pending manager/integration execution.

## Exact qualification source

The READY gate was present at `managers/app/notes/root-main574-public13-READY` before the port was composed.

- App qualification source: `ea38656fe62950440b36cafee780698cff2c3f9c`, tree `8bd8f741f7c8b28b8682aa960a658417f70c8522`.
- Agent: `8130a401bf44a518d5a40ae274d398b8c560be55`, tree `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Composition 13 archive: SHA256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
- Runtime 013: official all-75 artifact `6f000bc`, schema `8de823`.
- Browser/source target: Agent 8130, Runtime 2c4, public13 archive 9412, all-77 App lane, all-75 Runtime lane, peers/source/cache enabled, Chrome 141, short temporary directory.

The worker started at App `3e69e44f5fdfd1ea27f5f8ac677b4d385db2cba5` and composed the reviewed MAIN574/public13 integration delta in the working tree without git mutation. Because the worker must remain uncommitted, there is no final tree object for the combined source; the exact pinned integration tree is the READY App tree above.

## Source chain and port

The frozen writer cut is based on `3599fc49ad76dfdd7847ab4c813fc9317a0304eb` (tree `74130f681f6b0c87a7c61cb33d4ae6a092c03046`), with:

- parent-delete writer source from `82dd3d769` (tree `99847a8452ee6eef26b0d1318335a43b3427defa`);
- native-owner routing from `295641487` (tree `7b86b7aff415007f679c29ffa71a1d16f8551e24`);
- the frozen final wrapper lineage at `ccf537dd409259c4a88d0938675bf3e4deb32553` (tree `d64759dc62dcbe83d98c1a0421df2b73a2c2b8a9`), preserving the old qualified source tree `06121fff` (tree `06121fff1735a708671aa483f9e9eb19c5282e9b`).

The port includes only the frozen delete capture/gesture/commitSession sections and their required hook routing, tests, fixture, Playwright config, and existing current013 wrapper/spec support. It preserves the reviewed integration delta, including MAIN Inspector/tabs/metadata/cold-readiness work, PCM13 progress/pins, and the four App2 helper additions. No new App2 port was authored.

Product behavior retained:

- native owner-aware routing for a single parent clip;
- occurrence and group fallback behavior, including original group 261 behavior;
- opaque/raw JSON keys and Playwright inspector own-key preservation;
- durable capture/finish/submit flow with corrected idempotency and receipt carriers;
- additive conflict metadata and no fallback after a native product failure.

Legacy writers remain intentionally present for non-native paths. Remaining caller families are the group/multi/occurrence branches in `hooks/clip-editing/useClipDeletion.ts`, the legacy keyboard-delete builder in `lib/keyboard-delete.ts`, group-delete helpers in `lib/shot-group-commands.ts`, prepared media removal in `commands/media.ts`, metadata deletion in `useTimelineCommit.ts`, and the existing provider/save paths. This port makes no writer-retirement or deletion claim.

## Evidence

Nearest controls passed directly in the worker, using the existing private Vitest preload only for the repository's known `__dirname` setup requirement:

```text
6 files, 119 tests passed
12 files, 401 tests passed
ESLint: passed
git diff --check: passed
check-known-failures: 3 authorized expected-failure markers, 0 forbidden markers
```

The exact Vitest file lists were the delete capture/gesture/commitSession/ops/session tests plus their neighboring move, label, semantic gesture, commit, state, keyboard, and media tests. The original grouped-delete positive (`useClipEditing.test.ts`, group 261 coverage) was included.

Offline wrapper controls passed with:

```text
NODE_OPTIONS=--experimental-vm-modules node --test --test-reporter=spec \
  scripts/testing/current013-parent-delete.test.mjs \
  scripts/testing/current013-integration.test.mjs
# 2 passed, 0 failed
```

Historical central evidence for the old qualified source, not evidence for this dirty current worker tree:

- `app-m2-delete-browser-json-observation-gate-e2e-parent-delete-observation-two-case-tree06121fff-agent8130-runtime2c4-e2e-integration-1020155819-20141`: pass, exit 0; both fresh cases passed (lost-ACK/restart exact-key receipt and real 409 original-intent recovery).
- `app-m2-delete-browser-json-observation-gate-e2e-parent-delete-observation-conflict-tree06121fff-agent8130-runtime2c4-e2e-integration-1020155541-5006`: pass, exit 0; conflict case passed.

The required new central two-case run against the exact current MAIN574/public13 source was not run here. The known strict wrapper checks a clean committed App SHA/tree, while this worker is required to leave the composed port uncommitted and the central service snapshots that dirty worker tree. A manager must run the existing wrapper after harness commit/integration, with the exact source tuple above; no duplicate checker was introduced and no current-source qualification is claimed.

## Handoff

Do not mark the parent-delete writer or ledger as deleted. First commit/integrate this worker with the reviewed MAIN574/public13 delta, then run the existing strict two-case central suite with the pinned Agent 8130 / Runtime 2c4 / public13 archive 9412 / App all-77 / Runtime all-75 / Chrome 141 tuple. Hold on any concrete product error; routine harness/setup/carrier errors should be fixed equivalently and rerun.
