# D141cc P3 controller validation

- Dispatch source: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141cc-submit-owner-sol-1047/evidence/dispatch-recipes.json (SHA-256 d665c4907abd063edc9da0f29c887b56f7b66fb80febbe52f14732ea66e95d0d), dispatches[6], selector p3.
- Native builder and argv were loaded programmatically from the dispatch JSON with cwd /home/user/work/app.
- Pre-submit custody: unchanged inspector returned FIRST_NATIVE_INVOCATION_ONLY; plan, lock, registry rows, and matching requests were absent. Four detached execution checkouts were clean and matched their loaded SHA/tree pins; builder SHA matched 2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f.
- D66 service source used the exact pinned App tree 6a6e49eb4461b5ca1a7fa1247653bc794f26d710 via its unchanged-tree snapshot; the generated snapshot HEAD was 7b70ca03e919b0bc8fd7477a0915a00d3d71c841, with the pinned commit as its sole parent.
- Environment: original dispatch environment, unset keys, and operational keys were loaded programmatically; inherited TEST_KEEP=D141hh p3 was the sole authorized extra.
- Native submit: exit 0. Authentic preflight ID app-pin-82e9e13d-full-d141-p3-82e9e13d-submit-preflight-1026121859-29473 reached pass; authentic normal ID app-pin-82e9e13d-full-d141-p3-82e9e13d-submit-1026121929-6447 reached pass.
- Marker evidence: native request-test created both raw tests/<ID>/KEEP files before queueing: preflight at 2026-10-26T12:18:59.900Z; normal at 2026-10-26T12:19:29.958Z.
- Normal wait: /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-pin-82e9e13d-full-d141-p3-82e9e13d-submit-1026121929-6447 returned exit 0, pass, in 206 seconds.
- Service body: readiness 1 passed; Gate-5 journey 1 passed. The native log reports the lost-ACK/newer-local-gesture/restart/undo journey passed.
- Disk trace minimum available bytes: 4736208896; never at or below the 4,000,000,000-byte stop floor.
- No product, test, generated, pin, kit, registry, queue, or hub source was edited by this worker; service-owned queue/artifacts are retained as evidence.

The initial observer wrapper parse failure occurred before spawning the native process and had no service side effect; it is disclosed rather than treated as a native attempt.
