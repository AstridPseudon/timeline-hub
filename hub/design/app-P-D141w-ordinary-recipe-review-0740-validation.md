# D141w validation

## Result

Pure-builder binding: **PASS**. Controller-plan qualification: **FAIL** on `D141w-C1`, `D141w-C2`, and `D141w-C3`. This review made no product, test, generated-file, pin, registry, queue, hub, or Git metadata changes.

## Read-only commands and results

1. `git -C /home/user/work/app status --short --branch; git -C /home/user/work/app rev-parse HEAD HEAD^{tree}` — PASS; clean `tl/integration`, `82e9e13ddf1d7ec6c736521b2eb091dca9877598`, tree `6a6e49eb4461b5ca1a7fa1247653bc794f26d710`.
2. `git -C /home/user/work/agent status --short --branch; git -C /home/user/work/agent rev-parse HEAD HEAD^{tree}` — PASS; clean `tl/integration`, `ecdc242ed9b673f641759ecf029f95e89a2c6f92`, tree `d362fe9dfdbd0c1fc8e0739c193ed2b74a7d2735`.
3. `git -C /home/user/work/runtime status --short --branch; git -C /home/user/work/runtime rev-parse HEAD HEAD^{tree}` — PASS; clean `tl/integration`, `95d98f038320d5d46bd679ac000ab3e15825c935`, tree `78df31d62c5b9ba4c84dee4ea346e43a767718c1`.
4. `git -C /home/user/work/composition status --short --branch; git -C /home/user/work/composition rev-parse HEAD HEAD^{tree}` — PASS; clean `tl/integration`, `635f4de06fda22a85fc2e4cfc764d0153a4c9f40`, tree `5ab5191a296980a0a6bcd1178ab6902d6478a148`.
5. `sha256sum /home/user/work/app/scripts/testing/d66-plain-stack.mjs; git -C /home/user/work/app rev-parse HEAD:scripts/testing/d66-plain-stack.mjs; git -C /home/user/work/app cat-file blob 59b65214bc74c1ca118b097bc3b13c0ffe480a93 | sha256sum; git -C /home/user/work/app cat-file -s 59b65214bc74c1ca118b097bc3b13c0ffe480a93` — PASS; current and historical blob `59b65214bc74c1ca118b097bc3b13c0ffe480a93`, SHA-256 `2032f3087faab5bc1037b54faa593cb32536de15b748809601731ad5f6a7602f`, 49,914 bytes.
6. `python3 -m json.tool /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141w-final-head-binding-0736/evidence/binding.json >/dev/null && python3 -m json.tool /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-P-D141w-final-head-binding-0736/evidence/source-manifest.json >/dev/null` — PASS.
7. Supported Node pure-import comparison using `/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx` and the exports from `/home/user/work/app/scripts/testing/d66-plain-stack.mjs` — PASS; eight selectors, 16 commands, 16 rows, zero mismatches in command/row bytes, lengths, or SHA-256 values.
8. `git -C /home/user/work/app diff --check 5344c53e3063001bb3255bd0c9cd32cc5e77967f 82e9e13ddf1d7ec6c736521b2eb091dca9877598` — PASS.
9. `git -C /home/user/work/composition diff --check 635f4de06fda22a85fc2e4cfc764d0153a4c9f40` — PASS.
10. `sha256sum /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/suites.conf` — PASS; unchanged preimage `e100f177f029aedc17b5e4ad3fb697e1c9e98142ca88e6c91101c5f0046ac5f7`, 733,192 bytes; all 16 prospective names and all historical 0545 names absent.
11. `rg -n` source inspection of `/home/user/work/app/scripts/testing/d66-plain-stack.mjs`, `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test`, `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test`, `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-checkout`, and `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run` — PASS as evidence; confirms the three controller findings.
12. `rg -n` C0 field inspection of `/home/user/work/runtime/contract/commit-v2.md` — PASS; request, command, step, merge, idempotency, accepted/merged, conflict, invalid, and preview field families are retained; no wire change identified.

## Not run

No App/Agent/Runtime/Composition tests, unit tests, typecheck, lint, browser, localhost/live socket, `request-test`, `wait-test`, `test-run`, `request-checkout`, registration, preflight, body, checkout materialization, full suite, collector, or provider execution was performed. The packet remains source-only and prospective for App `82e9e13d` and Agent `ecdc242e`.
