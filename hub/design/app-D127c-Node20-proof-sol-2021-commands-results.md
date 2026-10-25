# Commands and results

All commands ran from `/home/user/work/wt/app-D127c-Node20-proof-sol-2021` unless identified as the service snapshot. Environment overrides for the three-control commands: `TSX_DISABLE_CACHE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime`. Other environment values were preserved; safe values are in the interpreter stdout files.

## node20-interpreter-fork

```sh
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node -e 'console.log(JSON.stringify({version:process.version,execPath:process.execPath,execArgv:process.execArgv,env:Object.fromEntries(['"'"'NODE_OPTIONS'"'"','"'"'NODE_TEST_CONTEXT'"'"','"'"'NODE_PATH'"'"','"'"'NODE_V8_COVERAGE'"'"','"'"'TSX_DISABLE_CACHE'"'"','"'"'ASTRID_RUNTIME_CHECKOUT'"'"','"'"'TMPDIR'"'"'].map(k=>[k,process.env[k]??null])),child:require('"'"'node:child_process'"'"').spawnSync(process.execPath,['"'"'-p'"'"','"'"'JSON.stringify({version:process.version,execPath:process.execPath})'"'"'],{encoding:'"'"'utf8'"'"'})}))'
```

Exit: 0; duration: 0.319 seconds. Parent interpreter exits 0; child spawnSync error EPERM with no stdout. Child status0 is NOT proof of successful execution.

Raw stdout: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127c-Node20-proof-sol-2021/evidence/node20-interpreter-fork.stdout.txt`; stderr: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127c-Node20-proof-sol-2021/evidence/node20-interpreter-fork.stderr.txt`.

## node22-interpreter-fork

```sh
/opt/node22/bin/node -e 'console.log(JSON.stringify({version:process.version,execPath:process.execPath,execArgv:process.execArgv,env:Object.fromEntries(['"'"'NODE_OPTIONS'"'"','"'"'NODE_TEST_CONTEXT'"'"','"'"'NODE_PATH'"'"','"'"'NODE_V8_COVERAGE'"'"','"'"'TSX_DISABLE_CACHE'"'"','"'"'ASTRID_RUNTIME_CHECKOUT'"'"','"'"'TMPDIR'"'"'].map(k=>[k,process.env[k]??null])),child:require('"'"'node:child_process'"'"').spawnSync(process.execPath,['"'"'-p'"'"','"'"'JSON.stringify({version:process.version,execPath:process.execPath})'"'"'],{encoding:'"'"'utf8'"'"'})}))'
```

Exit: 0; duration: 0.156 seconds. Parent interpreter exits 0; child spawnSync error EPERM with no stdout. Child status0 is NOT proof of successful execution.

Raw stdout: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127c-Node20-proof-sol-2021/evidence/node22-interpreter-fork.stdout.txt`; stderr: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127c-Node20-proof-sol-2021/evidence/node22-interpreter-fork.stderr.txt`.

## node22-supplemental

```sh
/opt/node22/bin/node --experimental-test-isolation=none --import tsx --test --test-concurrency=1 '--test-name-pattern=^(D127c source guard accepts every reviewed arm and rejects wrong hash or source|D127c reviewed-profiler validator enforces the exact safe cProfile projection|D127 reviewed-new validator rejects field, lifecycle, phase, truncation, and safety mutations)$' --test-reporter=tap tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts
```

Exit: 0; duration: 0.762 seconds. PASS: three intended named nodes, pass 3, fail 0, skipped 0; supplemental only

Raw stdout: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127c-Node20-proof-sol-2021/evidence/node22-supplemental.stdout.txt`; stderr: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127c-Node20-proof-sol-2021/evidence/node22-supplemental.stderr.txt`.

## node20-actual

```sh
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test --test-concurrency=1 '--test-name-pattern=^(D127c source guard accepts every reviewed arm and rejects wrong hash or source|D127c reviewed-profiler validator enforces the exact safe cProfile projection|D127 reviewed-new validator rejects field, lifecycle, phase, truncation, and safety mutations)$' --test-reporter=tap tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts
```

Exit: 124; duration: 30.033 seconds. NOTPASS: timeout after 30 seconds, TAP header only, zero named inner nodes

Raw stdout: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127c-Node20-proof-sol-2021/evidence/node20-actual.stdout.txt`; stderr: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/app-D127c-Node20-proof-sol-2021/evidence/node20-actual.stderr.txt`.

## One actual outside-service request

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test app-D127c-Node20-proof-sol-2021 d127c-node20-three-controls-2021 --no-cache
```

Request accepted, exit 0. ID: `app-D127c-Node20-proof-sol-2021-d127c-node20-three-controls-2021-1025202505-11856`. Exactly one request; `--no-cache`; no cache hit.

```sh
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test app-D127c-Node20-proof-sol-2021-d127c-node20-three-controls-2021-1025202505-11856
```

Terminal service status **timeout**, exit **124**, 48 seconds total; the unit command had a 45-second timeout. This is terminal, not still queued/running. No second request was made.

Exact registered command (the service uses this row):

```sh
app d127c-node20-three-controls-2021 env TSX_DISABLE_CACHE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node -e 'console.log(JSON.stringify({version:process.version,execPath:process.execPath,env:Object.fromEntries(['"'"'NODE_OPTIONS'"'"','"'"'NODE_TEST_CONTEXT'"'"','"'"'NODE_PATH'"'"','"'"'TSX_DISABLE_CACHE'"'"','"'"'ASTRID_RUNTIME_CHECKOUT'"'"','"'"'TMPDIR'"'"'].map(k=>[k,process.env[k]??null]))}))' && sha256sum tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts && env TSX_DISABLE_CACHE=1 ASTRID_RUNTIME_CHECKOUT=/home/user/work/runtime timeout 45s /home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test --test-concurrency=1 '--test-name-pattern=^(D127c source guard accepts every reviewed arm and rejects wrong hash or source|D127c reviewed-profiler validator enforces the exact safe cProfile projection|D127 reviewed-new validator rejects field, lifecycle, phase, truncation, and safety mutations)$' --test-reporter=tap tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts
```

Actual service stdout confirmed v20.19.4 and the required source SHA-256, then emitted only `TAP version 13`. There were no Subtest, ok, skip, or count events. No intended Node20 tests can be credited.

Service files copied byte-for-byte to `service-{status,exit,summary,log.txt,snap,request}` in this evidence directory.

## Read-only checks

- Static full-title extraction: seven registered titles; old author regex matches **zero**. Corrected exact pattern matches precisely the three controls and excludes all bootstrap tests.
- `bash -n -c <exact registered command>`: exit 0.
- `git rev-parse HEAD HEAD^{tree}`: `fd586440a626fc49a35a9dd0ac7e838d5fe55a4b` / `6d2744e271f016206854ab33f57b3cfc737ad54d`.
- `git rev-parse 466c921f40fb9c08e50928df6dea27dfdfb45d15^{tree}`: the same tree.
- `git status --porcelain=v1`: empty before and after.
- `git diff --quiet HEAD -- .`: exit 0.
- `git diff --check`: exit 0.
- `sha256sum tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts`: `59a4d116683f88d415024b6d9236e578cf03c11e2c913b56278f9d57448b40ef`, also emitted by the service.
- `git -C /home/user/banodoco/banodoco-workspace-runtime rev-parse fb4addba95ca4bae0482c93be94e5cae2770ca09^{tree} 368f53f4454d5908c86de53d174f0bedcf23781c^{tree}`: both `8d5683702f36034f27ee7f49737665d66dbc2b75`.
- SHA-256 of `git show fb4addba95ca4bae0482c93be94e5cae2770ca09:tests/helpers/p2_commit_phase_capture.py`: `095c252b111a6d43cb5b4b9ed284b5a445b8b6fe69ca0ad4ee6950f1383c352d`.
- All six mounted-path hashes matched review2013, and the entire App tracked/untracked status stayed clean.
- Event checker: requires one Subtest and non-skipped ok per intended full title and pass=3/fail=0. Node22 satisfies it; sandbox Node20 and service Node20 fail it. Persisted result: `test-event-check.json`.

## Registry publication

Appended one bounded unit row via the documented existing bench-store mutex/full-byte CAS/atomic replacement route (`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-P2-P3-current-install-1429.md`). Outside 718208 bytes retained exactly. Before SHA-256 `90bf27689647f3cf0e97c6028b745a0f4f233ba1a8634ecff3b2959121973ba2`; after `e934b46aa9c6bc1d5d727d7f39c33adbd3b836f1b9ba4532939e7a09fb54d80a`.

The first attempt to atomically replace from TMPDIR returned EXDEV before any registry mutation. The normal same-directory temporary-file replacement then succeeded. No dispatcher code or other suite row changed; the new row remains registered. No cleanup/deletion was performed.

No Runtime61, lint, TypeScript, whole unit file, full suite, bootstrap, live sockets, browser, original-element, profile, native, tour, install, or acquisition was run. Node22 and Node20 commands requested only the three exact no-live controls.
