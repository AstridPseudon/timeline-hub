# Producer TSX IPC preflight and five-control verification — 1209

## Verdict

The authorized local-TSXIPC preflight **passed**. The phase-corrected five-control sidecar then stopped on its first new failure while constructing the `after` case. The required five-control result is therefore **not qualified: 1/5 cases completed, 4/5 unreached**. No retry, source change, build, browser, runtime, service, install, or actual journey was run.

## Exact commands and results

Plan read from `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/PLAN.md`.

Preflight, run exactly once with an owned physical short TMPDIR:

```text
TMPDIR=/tmp/tl-ap2-m2-tsx-direct-YX0Vfn TMP=/tmp/tl-ap2-m2-tsx-direct-YX0Vfn TEMP=/tmp/tl-ap2-m2-tsx-direct-YX0Vfn sh P/next-preflight.sh.txt
```

Result: **exit 0**.

- public13 hosted-build resolver: PASS, Composition `0.0.13`, tarball SHA `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`;
- public13 preflight: **11/11 checks PASS**;
- TSX module-format probe: `module-format probe PASS: DirectHarness loaded as ESM; no daemon invoked`;
- the authorized local IPC scope was only TSX's module-loader pipe; no external network was used.

Five controls, invoked exactly once:

```text
python3 P/outer-controls-run.phase-corrected-1150.py
```

`before` completed with the expected early refusal and its assertions passed:

```json
{"label":"before","outer_status":1,"manifest":false,"dispatch":["producer-startup-custody-gate-0717-owned.sh"],"shell_executions":1,"child_count":0,"temps_created":0,"temps_leaked":0,"translation_reverse":"PASS","run_root_removed":true,"dist_removed":true,"node_modules_restored":true}
```

The first new failure occurred while constructing `after`:

```text
AssertionError: producer-startup-only-gate-0717-owned.sh
```

at `outer-controls-run.phase-corrected-1150.py:83`, the fixture reverse-translation assertion. The sidecar exited before dispatching the `after` case, so `after`, `absent-output`, `copy-failure`, and `success` have no control results. Counts: **1/5 completed; 4/5 unreached**. No failure packet or success packet was produced.

## Cleanup and custody

- Preflight-created `/tmp/tla-*` and the owned TMPDIR were absent after exit.
- The sidecar's partial `controls/after` fixture was cleaned by its temporary-directory context; only the retained case directory and `before` evidence remain.
- No run-specific `evidence` or `run_root` remained; no producer/playwright/runtime/TSX child remained.
- The pinned keeper remained clean: `5863411a8c2400db719b5385002b05af0a2b3891`, tree `31b0f77c6ef4e9fdbeff3e4f88cc4705f0891e89`.
- The assigned App worktree remained clean. Shared dependencies were read-only. No product source, spec, pin, guard, `.gitignore`, or original artifact was changed.
- Pre-existing unrelated `/tmp/tla-*` and `/tmp/tl-ap2-producer-existing-*` directories were not touched.

## Artifact hashes

The eight retained positive artifacts remained unchanged:

```text
producer-physical-keeper-gate-0717-owned.sh       d9ecc3ade14746c559c46c68046eec3f71ecac5c37f9218cb575a9e2057a6238
producer-public13-runner-0717-owned.sh             b21d9ccd1dfc31b81d38e2e19c78ca4d53ca3a3a7a5c74f82c7bffb533fe9d13
producer-retain-failure-artifacts-0753.sh          dab4e885cedbde6273139d3b4350cacdd33020e63773f9c71e0289ab78ddea75
producer-runner-0717-owned.sh                      84031e301827518c2b981c585e812c5a5ad3d00727105c1b8515a6e1209a54fa
producer-startup-custody-gate-0717-owned.sh        02d831e05094586d3771424ac43cacb602799c691ec40423fb370891ba1cb16e
producer-startup-module-format-probe-0717-owned.mts d4eeaeb74a582fe9ccb94c1cfba7f66c41ec50eef7823db34f61ed7185e12af3
producer-startup-only-gate-0717-owned.sh           4ce9e7f4fc0eb6c6a7b32b784cd3ea64f598b4169fa49ba2a99126237dc4a5df
producer-startup-only-probe-0717-owned.mts         a062cab11ea3a86ef75ece5a86584d0555040336032ced515d6ac50de9481d8f
```

Custody hashes also remained unchanged: approved sidecar `a4b3f89d9f15f9fbd095e5b6b658605807f7b0099e8337f0cb4dea11ebdf662e`; original harness `ff1ae8404f39d765b01429ce706fa0affb6a163b632c20506a9705f103ec7234`; launch stub `4299795135db4be3b83b41d9034cb1519b529925865222f9af866029df9264b7`.

## Blocker and next step

The first new failure is the phase-corrected sidecar's reverse-translation assertion for `producer-startup-only-gate-0717-owned.sh`. Per the settled instructions, no source or sidecar correction was attempted and no second attempt was made. The next step requires orchestrator review of that exact translation failure before any further verification.
