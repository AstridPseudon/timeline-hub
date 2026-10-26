# D141 App full/pristine validation

## Authority and source guards

- Read `PLAN.md`, the app manager INBOX MAIN GO D141c at 00:42Z, the D141 full/pristine recipe and handoff, independent packets review 0003, and receiver 0007 receipt/recipe.
- Final tuple admitted: App `867cb2737af1b46dc608c7cd37c349e920fe9422` / `2b44a46ca51d880c6a00da4c19aa8629b55eb7dd`; Agent `28e56cacb42d3da85b02e5b3543895b44f3d0f70`; Runtime `6a011d58e69173d70e2e9bb3ac434ac8f9e87d8d`; Composition `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`.
- Normal pre/post integration guard: `/home/user/work/app` was clean and remained at the exact final App head/tree.
- Pristine metadata base and receipt target: exact `7ca61bb3280beca21d98a854af266a382f7ce5df` / `974de7cd08900872eeb0bd6f6004d44323e01fab`; the service-created snapshot was clean while running and had the exact tree and required commit as parent, but its synthetic HEAD was `4bb696aceae83a3843df47ff1ff99c9717a3e0aa`. The service removed the snapshot after completion, so post-cleanup `git status`/HEAD cannot be rechecked.
- The live `/home/user/banodoco/reigh-app` checkout was not used or assumed.

## Exact service commands

Normal, submitted first and waited to terminal:

```text
PATH=/opt/node20/bin:/usr/local/bin:/usr/bin:/bin /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test integration:app full --no-cache
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-full-1026004326-12174
```

Pristine, submitted only after normal terminal completion:

```text
PATH=/opt/node20/bin:/usr/local/bin:/usr/bin:/bin /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-D141-pristine-receiver-0007 full --no-cache
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-D141-pristine-receiver-0007-full-1026010029-23581
```

Both service runs reported the unchanged registered command `npm test -- --maxWorkers=3`, Node `v20.20.0`, npm `10.8.2`, and no cache hit. The effective npm script was `npm run test:app && npm run test:node --maxWorkers=3`; because Vitest failed, Node was `NOTRUN` in both runs.

## Terminal results

| ID | status/exit | Vitest files | Vitest tests | Node | expected failures |
| --- | --- | --- | --- | --- | --- |
| `app-full-1026004326-12174` | fail / 1 | 5 failed, 1356 passed, 1361 total | 33 failed, 19734 passed, 19767 total | NOTRUN | 0 |
| `app-D141-pristine-receiver-0007-full-1026010029-23581` | fail / 1 | 3 failed, 1276 passed, 1279 total | 18 failed, 17856 passed, 17874 total | NOTRUN | 0 |

The full per-test failure records, source applicability, and raw-output hashes are in `normal-result.json` and `pristine-result.json`. The comparator result is in `reg-diff.json`: finite classification is REG 0, nonREG 0, UNKNOWN 8. No failure was called REG, upstream-present, or expected.

Raw result directories were retained with `KEEP` files. No repo, test, fixture, generated, pin, script, or Git metadata files were changed.

The service emitted no JUnit/XML artifact in either result directory; the complete `log.txt`, request, status, exit, summary, snap, and `KEEP` artifacts are retained and hashed in the JSON evidence.
