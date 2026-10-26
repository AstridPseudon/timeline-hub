# D141 validation — read-only

## Commands and results

No tests, imports, typecheck, lint, browser, preflight, service request, package install, or product/fixture/mock/assertion/generated-file edit was run by this worker.

Read-only source and receipt checks performed:

- `sed` of `PLAN.md`: governing plan read first.
- `jq` of prior 0120 `join.json`: consumed the qualified `normal-033-shot-group-pack` source-presence and pristine-PASS row.
- `git show`, `git rev-parse`, `git grep`, and `git diff` in `/home/user/work/app` at cut `867cb2737af1b46dc608c7cd37c349e920fe9422` and pristine `7ca61bb3280beca21d98a854af266a382f7ce5df`: exact test, mock, production caller, placement-service blobs, and source diff read without checkout.
- `rg` of normal raw receipt `tests/app-full-1026004326-12174/log.txt`: exact failure `expected 3 to be 2` at test line 397.
- `rg` of pristine raw receipt `tests/app-D141-pristine-receiver-0007-full-1026010029-23581/log.txt`: exact file receipt `shot-group-pack-commands.test.ts (6 tests)` and no matching failure.
- `sha256sum` of both raw logs and their request/status/exit/summary/snap files: hashes recorded in the working inspection; no receipt files were changed.

Raw receipt hashes:

- cut log `fcc5e73b9fa41f7ff7afc8f91813a126495d52358f5d32d1505874b546349fd6`;
- pristine log `636457440c919df79760fe2a9e5e5c008491e283b97ca2b10c475f2b1ffa9ba6`;
- cut summary `1e46e5871efed11d611cee5da547f4611e3c5f36018e2f62b40a24e95f66ec1e`;
- pristine summary `b022e07e50170bcf4be675a2c4c07b770cdb1fb603f646b66d5b87f5b304b118`.

## Receipt summary

| source | receipt | result | relevant case |
| --- | --- | --- | --- |
| cut | `app-full-1026004326-12174` | full FAIL, 5 files/33 tests failed; Node NOTRUN | exact case FAIL, expected 2/received 3 |
| pristine | `app-D141-pristine-receiver-0007-full-1026010029-23581` | full FAIL, 3 files/18 tests failed; Node NOTRUN | shot-group file PASS, 6 tests |

The full-suite failures are not reclassified here. This packet qualifies only the finite requested ID. The prior custody packet remains immutable and supplies the synthetic-pristine tree/parent proof and dependency caveat.

## Scope guard

Own worktree status remained clean. No repository, Git metadata, shared dependency, test, fixture, assertion, generated, pin, kit, hub, or service state was modified. Permanent output is limited to this evidence directory plus the required worker completion markers.
