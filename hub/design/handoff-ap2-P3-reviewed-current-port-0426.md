# ap2-P3 reviewed current-port handoff

## Result

PASS for the authorized source-only port. Starting at current tl/integration base 66b87816e4ce3aa953f2abd53f7ff98cd29b1608, port the complete independently reviewed P3 one-file delta from source tl/ap2-P3-assertion-sol-0409 at 645ded5ecb61014a4ceef014cd87df1ca8c99454.

Only tests/e2e/local/three-products.spec.ts changed: 337 additions and 3 deletions. The worktree file is byte-for-byte equal to the reviewed source file. The current-to-donor diff is exactly equal to the applied diff. Outside-path blob check passed.

The reviewed expectV2History and recordedSite helper/native-physical alias delta, ordered patch and dependency/boundary/selection/digest/history/receipt checks, and all original Gate-5 assertions are present. No stale product ancestry or unrelated donor changes were imported.

## Exact evidence

Working directory: /home/user/work/wt/ap2-P3-reviewed-current-port-0426

- ASTRID_APP_TIMELINE_PORTS_ALLOCATED=1 PLAYWRIGHT_PORT=19409 FAKE_RUNTIME_PORT=19410 PLAYWRIGHT_OUTPUT_DIR=/tmp/w-5a548548c2a/playwright-output npm run test:e2e:three-products -- --grep 'M2 real gate 5 \(M1 real mounted path\): Agent edit, lost ACK, newer local gesture, exact retry, restart and undo preserve intent$' --list — PASS; 1 test in 1 file; exit 0.
- npm exec tsc -- --noEmit — PASS; exit 0.
- npx eslint tests/e2e/local/three-products.spec.ts --max-warnings 0 — PASS; exit 0.
- git diff --check — PASS; exit 0.

## Qualification boundary

UNEXECUTED body. No browser, socket, service, body, build, or full suite was run. Production-caller behavior and behavioral Gate-5 qualification remain unverified. The central service must run the exact Gate-5 body only after the separately owned environment/public-export resolver correction is ready.

Request/reply obligations remain asserted by the port: full v2 base/commands/label/steps with patches and optional reads, merge/optional reads, dry_run and key; accepted/merged canonical/head/digest/receipt/history/dependencies/merge_mode; and original lost-ACK/restart/undo/zero-old-traffic assertions. Conflict/invalid/preview forms remain contract obligations and were not invented in success-only tour cases.

No product/schema/DTO/generated/pin/lock/config/launcher/suite changes; no new executor or guessed authority; no skips, xfails, weakened assertions, or timeout increases. No commit, merge, checkout, fetch, push, or branch/ref change was performed.
