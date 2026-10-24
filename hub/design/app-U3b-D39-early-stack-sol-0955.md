**BLOCKED — U3b merge verified; U4p D39 adoption incomplete.**

- Retained sanctioned merge state: HEAD `cd29ff2642ab8241850a2ed3490970771a9c02eb`, MERGE_HEAD `82cb5c0005df7abe0fcb8673f7be192a6c9e9183`.
- All 20 incoming paths match HOME exactly. Strict P2/P3 helpers, D50 spec/tail, outbox/transport/door behavior, C0v2 caller and six D31/D37 blobs remain intact.
- Upstream `2a288e629c47` ancestry, conflict-marker scan and `git diff --check HEAD` pass.
- No worker-authored source, assertion, generated-file or pin changes.

Adoption failures:

- `node scripts/sync-runtime-client.mjs /home/user/work/runtime` fails because D39 removed `conformance/responses/publish_conflict_409.json`; the producer now supplies `commit_conflict_409.json`. The tool restored the original lock.
- `node scripts/astrid-landing/refresh-vendor.mjs --astrid-repo /home/user/work/agent --commit ba55ac1e9e70156f03f7e31cc1b1ef040bb75b84` fails with `spawnSync git EPERM` under Node 22 and Node 20. No workaround attempted.

Verification:

| Command | Result |
|---|---|
| `bash "$TMPDIR/union.sh"` — frozen 27-file union plus runtime-elements, vendorLock, recordedResponses and client tests | **756 passed, 11 failed**; all failures are unchanged vendorLock fixture `git init` calls denied with EPERM |
| Node20 Vitest with private P2 semantic config, `--configLoader runner --no-cache --maxWorkers=1 --no-file-parallelism` | **7/7 passed** |
| `/opt/node20/bin/node --import tsx tests/e2e/local/support/gate5-reset-precondition.test.mjs` | **20/20 passed** |
| Node20 `--import tsx --test` over the five Gate5/P2 Node control files | **5 files passed** |
| Actual renderer config run with `ASTRID_CHECKOUT=/home/user/work/agent` | **2/2 passed** |
| Serialized `flock -w600 /home/user/work/.app-tsc.lock … tsc -p CONFIG --noEmit --pretty false --incremental false` for root/app/node | **All passed** |
| Scoped Node20 ESLint, `--max-warnings 0` | **31 paths passed** |
| Astrid conformance, local Runtime lock and vendor-source verification | **Passed for existing pins** |

My initial P2 semantic invocation used Node instead of Vitest and failed during module loading; the correct runner passed unchanged assertions.

All **79 D39 producer artifacts** match exact Runtime `becfe6db88b2cc034dba3fafa6c050117cdf2b06` and its committed manifest. Consumer provenance remains Runtime `34eac004…` and browser Agent `3f1ceaed…`; no final adopted tuple is claimed.

`commit-msg` and `BLOCKED` written; no `DONE`. Resolve the fixture mapping and subprocess denial, resume normal adoption against reviewed Agent home, then independently review before the manager requests App full checkpoint. P2/P3 GO still gates integration. No full, browser, HTTP, service, build or provisioning run occurred.