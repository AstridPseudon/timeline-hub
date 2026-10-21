# AP2-M2 parent viewport exact-one central run

Result: the one permitted central run failed before browser execution. No retry was made.

Suite ID: `ap2-m2-parent-viewport-exact-one-central-1126-ap2-m2-parent-viewport-exact-one-central-1126-e2e-1021113018-1384`

Central result: `fail`, exit `134`, duration `83s`. The hosted Vite build transformed 5,586 modules, then Node22 aborted with `FATAL ERROR: Reached heap limit Allocation failed - JavaScript heap out of memory`. This is the first retained frontier; it occurred before browser launch.

Exact source and custody passed: App `6707a30f14bf3a5ee19cb9e481b7dbd95b77522a`, tree `6ff32d797f0e774b8574274a3494ce8755fa160c`; exact keeper and captured service tree matched; Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`; Runtime `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`; locked graph archive SHA-256 `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`; Composition archive SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

Preflight commands and results:

- `sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-viewport-exact-one-central-1126/record/aggregate-preflight.sh` — PASS. All aggregate checks passed, including exact source, original assertions, keeper/link, graph/archive, Agent/Runtime cohort, Node22, private roots, environment isolation, credential declarations, lock, disk floor, no heavy peer process, exact one-test list, and zero-test retention probe.
- `env -i ... sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-viewport-exact-one-central-1126/record/artifacts/final-keeper-gate.base.sh preflight` with the exact graph/archive, App keeper, Node22, and private roots — PASS. Source preflight passed, 76 artifacts were verified, and Playwright listed exactly `three-products.spec.ts:1410`.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-viewport-exact-one-central-1126 ap2-m2-parent-viewport-exact-one-central-1126-e2e --no-cache` — queued the suite above.
- `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test ap2-m2-parent-viewport-exact-one-central-1126-ap2-m2-parent-viewport-exact-one-central-1126-e2e-1021113018-1384` — FAIL exit 134.

Reached: source/keeper guards, source tuple preparation, locked graph verification, private dependency graph creation, runtime lock checks, exact test collection (`1 test in 1 file`), and hosted build start.

Unreached: browser launch, DOM/viewport assertions, native ADD, reload, lost-ACK, restart, retry, undo, and zeroLegacy body assertions. No browser trace, error context, or request/response/console summary exists because the browser was never launched.

Disk: captured preflight baseline was `13,237,588 KiB` free on `/tmp`; post-run measurement was `12,468,452 KiB` free. The post-run value remains above the 10 GiB floor. A separate earlier aggregate baseline was `13,240,096 KiB`; its post-preflight measurement was `13,239,348 KiB`.

Decision: the inherited bound helper had a POSIX shell-quoting defect in its `${var:?message}` text (`HOME's` / `graph's`), causing `dash` to consume the following archive assignment. I corrected only those two message strings in this worker’s private data-bound copy, updated the helper hash guard, and re-ran preflight successfully. No product code, peer runner, shared helper, shared dependency, or frozen packet was changed. The central OOM then required stopping at the first failure; increasing heap, changing Node/toolchain, or retrying would violate the settled run controls.

Fresh evidence is retained under `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-viewport-exact-one-central-1126/record/evidence-central/run/`. The source/hash manifest is `sourceHASH-manifest.txt`; the central log and summary are retained in the suite result directory. Their hashes and the exact artifact hashes are recorded in that manifest.
