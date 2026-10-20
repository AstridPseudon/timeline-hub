# App current013 unique-C final gate

## Result

Changed only Gate 5's independent track identity in `tests/e2e/local/three-products.spec.ts`:

- Gate 5 create request: `f2-independent-C` -> `f2-gate5-independent-C`.
- Gate 5 exact track assertion: updated to `f2-gate5-independent-C`.
- Original M1's `f2-independent-C` create, position, history, and undo assertions remain unchanged.
- The existing six-line real UI reset remains unchanged.
- No product or pin changes.

The reserved Gate 5 ID avoids the worker-scoped identity collision while preserving Gate 5's position 5/7, receipt, guard, history, restart, opaque, and zero-legacy assertions.

## Verified environment

- App base commit: `0ea368432267f1f3e712c91822d6ea4961d40e78`.
- Final central snapshot tree: `00e9e2a92d80ee103a94fab1d976babe3ca918e1` (includes the uncommitted test edit).
- Agent source: `d8749a9ce12a699672faf3ad96b4e4cbea9245c2`, tree `75354d38c898729bac09619679f5421faba319ed`.
- Runtime source: `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Public source SHA256: `fe380bc3280b1f5efa7ecde7cc55a5415a498f2b35af8fb693d11123aa289a28`.
- Composition archive SHA256: `0a7b61529099ce994f807c6d7b1078303a09e7c0219144cc4b07467977f0f1a3`, 77 files.
- Runtime artifact manifest: 75 artifacts.
- Chromium: 141.0.7390.37, SHA256 `85918a9937192b78da8edb51c38a7af4920ac6bd9ba19939ecb0bb724d5a1a95`.
- `ASTRID_PUBLIC_CHECKOUT` and `ASTRID_APP_DIRECT_DIST` were unset; literal `TMPDIR=/tmp/tl13-reset-b1` was used.
- Private module/cache overlay was used. Vite was copied into that private overlay after the first guarded run proved that Vite's realpath-based cache default would otherwise mutate shared `.vite-temp`.

All central lanes reported unchanged all75 artifacts, normal locks, tracked public-browser bundle, all77 public12 files, peers, source, and shared caches at the final guard.

## Tests

- `env -u ASTRID_PUBLIC_CHECKOUT -u ASTRID_APP_DIRECT_DIST npm exec -- eslint tests/e2e/local/three-products.spec.ts --ext ts --max-warnings 0` — PASS.
- Playwright discovery with exact Agent/Runtime source heads and the verified environment — PASS, 7 tests discovered.
- Initial central native3 TestID `app-m3-current013-unique-c-final-gate-e2e-unique-c-current013-bb7fe564-setup88888-e2e-integration-native3-1020142425-11925` — preflight failure: stale expected app tree; no product assertion.
- Correct-tree native3 TestID `app-m3-current013-unique-c-final-gate-e2e-unique-c-current013-00e9e2a9-setup88888-e2e-integration-native3-1020142522-19724` — preflight failure: suite registration had a 41-character Runtime head with an accidental trailing `2`; no product assertion.
- Correct-tree native3 TestID `app-m3-current013-unique-c-final-gate-e2e-unique-c-current013-00e9e2a9-setup88888-e2e-integration-native3-1020142626-14888` — 3/3 product tests passed, but postflight correctly failed because shared `.vite-temp` mtime changed. Repaired the private overlay and did not qualify this run.
- Repaired native3 TestID `app-m3-current013-unique-c-final-gate-e2e-unique-c-current013-00e9e2a9-setup88888-e2e-integration-native3-1020143017-10189` — PASS, 3 passed in 2.5m. This included original M1, Gate 5, and the serial conflict case.
- Labels3 TestID `app-m3-current013-unique-c-final-gate-e2e-unique-c-current013-00e9e2a9-setup88888-e2e-integration-labels3-1020143350-29067` — PASS, 3 passed in 2.2m.
- Separate fresh cold-open1 TestID `app-m3-current013-unique-c-final-gate-e2e-unique-c-current013-00e9e2a9-setup88888-e2e-integration-cold-open1-1020143727-26993` — stopped after the first actual product assertion and failed: `tests/e2e/local/track-label-command.spec.ts:558` timed out waiting for `hold.requests.length` to become 1 (expected 1, received 0). Guard/source/cache checks passed. No retry or test weakening was made.

No full suite, install, tsc, frame, or PCM run was performed. The cold-open lane is therefore an explicit partial/unverified limit for the overall qualification.

## Handoff

The required source-tree result is ready for the imminent root merge. The harness should commit the worktree using the supplied commit message; no commit was run here.

