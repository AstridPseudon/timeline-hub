**BLOCKED: tooling repair and generated adoption are complete; production compatibility is not.**

The unchanged [localSaveSession.ts:160](/home/user/work/wt/app-U3b-D39-tool-return-sol-1005/src/tools/video-editor/commands/localSaveSession.ts:160) recognizes only the old full-v2 schema digest. Actual D39 metadata therefore blocks `doc.patch` and omits `steps`/`merge` from semantic requests. Repairing that caller exceeds this task’s authorized files.

- Repaired the normal sync tool’s obsolete mapping; adopted canonical `commit_conflict_409` and `retired_route_410`.
- Ran `node scripts/sync-runtime-client.mjs /home/user/work/runtime` against exact Runtime `becfe6db88b2cc034dba3fafa6c050117cdf2b06`.
- Ran `node scripts/astrid-landing/refresh-vendor.mjs --astrid-repo /home/user/work/agent --commit ba55ac1e9e70156f03f7e31cc1b1ef040bb75b84`.
- Retained historical publish recordings/tests, all 20 incoming HOME paths, six dormant blobs, protected specs and D50 tail exactly. No files deleted or generated artifacts manually edited.

Commands and results:

| Command | Result |
|---|---|
| Node20 Vitest, `--config config/testing/vitest.config.ts --configLoader runner --no-cache --maxWorkers=1 --no-file-parallelism`, selecting `recordedResponses.test.ts`, `vendorLock.test.ts`, `client.test.ts` and `fakeWorkspaceRuntime.recorded.test.ts` | **70 passed** |
| Same Vitest command with `$(cat "$TMPDIR/union-files.txt")`: frozen 27-file union plus runtime-elements and the four files above | **729 passed, 43 failed** across four caller suites |
| `TSX_DISABLE_CACHE=1 /opt/node20/bin/node --import tsx --test tests/e2e/local/support/{gate5-reset-precondition,p2-document-oracle,p2-original-owner-ready,p2-parent-oracle,p2-transition-oracle}.test.mjs` | **10 passed, 20 Gate5 hook failures** |
| Vitest with private semantic config selecting `p2-semantic-oracle.test.mjs` | **3 passed, 4 failed** |
| `ASTRID_CHECKOUT=/home/user/work/agent` with `config/testing/vitest.astrid-renderer.config.ts` | **2 passed** |
| Serialized `flock -w600 /home/user/work/.app-tsc.lock env NODE_OPTIONS=--max-old-space-size=4096 /opt/node20/bin/node node_modules/typescript/bin/tsc -p CONFIG --noEmit --pretty false --incremental false` for root/app/node configs | **All passed** |
| Scoped ESLint with `--max-warnings 0`; `git diff --check HEAD` | **Passed** |
| Runtime `generators/generate.py --check` and `scripts/artifact_manifest.py --check` | **Passed** |
| Both vendor-lock checks; `node scripts/build/verify-astrid-vendor-sources.mjs`; Node20 public-boundary tests | **Passed; 9 tests** |

All **79 producer artifacts** match exact committed Runtime bytes and manifest hashes; all **14 locked consumer artifacts** match. Initial new assertion mistakes were corrected; final focused tests pass. Renderer initially failed against the incomplete browser subset, then passed using the required actual checkout.

Harness finalized the retained base as `a721837291dc8b93642e8095b21bb99ddfba11c2`. Current state:

- HEAD: `cd29ff2642ab8241850a2ed3490970771a9c02eb`
- HEAD tree: `7e67ff429569e55140b9563f5f6511117ae359e6`
- HEAD parent: `6f2eb7e04518544dbc43cd9ac53153fc8be6e3f2`
- Pending merge parent: `82cb5c0005df7abe0fcb8673f7be192a6c9e9183`
- Working content tree, computed read-only: `dc3f7fdedf4cd9eeb83a6dffd67a56b438089b19`

Final commit SHA remains harness-owned. `commit-msg` and `BLOCKED` are written; no `DONE`.

Next: authorize the bounded caller compatibility repair, retain every failing expectation, then independently review. No integration merge, full/browser/build/provision run, service request or shared dependency mutation occurred.