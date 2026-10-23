# A3 mounted child-placement review — ap2-A3-child-mounted-review-0805

## Result

**SOURCE PASS.** Candidate `a9dd20390ee32f5a2b79973af63312241c976bda`, tree `c85d0c7bc1e0031368250c7a56e1d0836a247b2f`, cumulative baseline `cffa91c93`, exactly 14 allowlisted files. No product changes were made by this review.

The two prior Luna FAILs (0729/0738) are resolved: the mounted VideoEditorProvider registers acknowledged canonical composition plus project/timeline under the existing selection owner; Gallery, ImageGen, ShotsPage and external-drop callers (plus public mutation wrappers for remaining consumers) derive the concrete canonical `ownerRef`, `timelineRef`, and one fresh destination. The existing placement service forks through LocalSaveSession/outbox, reloads the accepted basis, and performs fresh parent placement.

Empty, foreign, ambiguous, duplicate, non-addressable, data-item, and missing-graph selection cases refuse when canonical mounted context exists. Lifecycle disposal/project reset clears ownership/context; no-context legacy calls retain parent-only behavior. No shot-ID guess, first-match occurrence, array-order/byte-equality inference, broadcast, or TypeScript managed-edge patch exists. Nondefault selected timelines refuse honestly; no retargeting. React Query retry-1 retains the same request identity.

The existing A2 full-v2 carrier is unchanged from `cffa91c93`: request `api_version: 1`, scope, base pair, commands, label, steps patch/reads, merge/reads, dry-run, key, and accepted/merged canonical/head/digest/receipt/records/effects/bindings/dependencies/history/undo/publisher/provider/compiler/conflict/invalid handling remain in production placement. D15 read-only refs: Agent execution `4edc4b321cae5cfc58252d7ed89e3f0408238646` / tree `f17b84c48bae3461dd11cedb8719bd17495a8210`; Runtime/client `34eac0041b0891e9011966b39bcbd26053fde5bc` / tree `9853574865f25e08284e82ffb26c0bdecaa16a30`.

## Evidence

- Exact private targeted command (author’s 13-file list, `--configLoader=runner`, private config/cache): **PASS — 13 files / 181 tests**.
- Root, App, Node `tsc --noEmit --incremental false`: **PASS**.
- Scoped ESLint, `git diff --check`, normal Runtime lock, and Agent producer lock: **PASS**.
- Composition archive SHA-256 `819acf6b3815d6eeabe772a9569581fedbe4f9c9cce35946efca9454e2040234`; package `0.0.14`; 80 regular files byte-identical; all public exports resolve to the exact private graph: **PASS**.
- Cumulative 14 blobs are recorded in the worker report.

The author’s initial default Vitest run touched shared `/home/user/work/app/node_modules/.vite-temp`. I classify this as temporary-cache metadata touch only, with no evidence of candidate source/package/lock/vendor-payload mutation, but do not claim zero initial touch or cleanup. Final review runs were private.

Not run: browser, localhost, HTTP/body, live Runtime/service/socket, build, full suite, central test service, or shared-install mutation. Physical accepted/merged/refused Runtime proof and original P1/P3 journey proof remain unverified and manager-owned.
