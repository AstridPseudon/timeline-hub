# AP2 M2 selected stale three-hash binding repair 1132

## Result

Corrected the selected local runner's three stale binding hashes. The only
artifact edit is in `verify_scripts_and_scope` in:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-clean-keeper-main-port-1120-runner.sh`

The selected source/keeper remains App `0cc2583aaf07e89190b9344b5ac82849d6279586`,
tree `320e74a93676c781e83885b86ec237b4a1465d80`. No App source, test, docs,
`.gitignore`, shared helper, graph, install, or product file was changed.

## Corrected binding data

| guard | old approved-966 value | computed bound-file SHA-256 |
|---|---|---|
| `OLD_DRIVER` | `a959de6e0041f0d8ee28b949a19f5add97d7fb5de27714da6beaad15abd6ce4f` | `cf4ddff51c86e2be5a1d7bdae705aa3390eaf4c931e6cea7b2369311dadecea7` |
| `SOURCE_COMMON` | `96969ce9ff43b676abb4616009fd1112e93020065483b2a8ae0afac7245ba109` | `647ea22abf9cf452ca9cb1a8a21633dcd33dc201ac0cc8bbc4f65b6f07929b2b` |
| `PARENT_MEDIA` | `1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd` | `ce9e86fab603bd654e572bba67bfca0f9214722f4036cce19840960d9ff6b702` |

The values were computed with `sha256sum` from the exported bytes. No short
hash was pasted and no path or execution logic was altered.

## Computed artifact manifest

| artifact | absolute path | SHA-256 |
|---|---|---|
| runner | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-clean-keeper-main-port-1120-runner.sh` | `6416f65db7b8f247bd8610b504435c8a18c4139ded1b8bbcf4fc7ae3da83e5ed` |
| source helper | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-clean-keeper-main-port-1120-source-common.sh` | `647ea22abf9cf452ca9cb1a8a21633dcd33dc201ac0cc8bbc4f65b6f07929b2b` |
| parent helper | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-clean-keeper-main-port-1120-parent-media-central.sh` | `ce9e86fab603bd654e572bba67bfca0f9214722f4036cce19840960d9ff6b702` |
| selected P1 driver | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-clean-keeper-main-port-1120-selected-p1-driver.sh` | `cf4ddff51c86e2be5a1d7bdae705aa3390eaf4c931e6cea7b2369311dadecea7` |
| protected lease | `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-selected-clean-keeper-main-port-1120-KEEP` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

## Recursive selected-path inventory

Before the preflight, I traced both runner modes and their sourced helper
edges. The runner binds:

- argv: an absolute `APP_ROOT`; selected spec
  `tests/e2e/local/three-products.selected-param-dev.spec.ts`; selected title
  `local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo`.
- keeper/path data: `APP_KEEPER_ROOT=/home/user/work/wt/app-pin-0cc2583a`,
  the empty non-symlink lease above, the three exported helper/driver paths,
  `AGENT_REPO=/home/user/peteromallet/astrid-agent`,
  `RUNTIME_REPO=/home/user/banodoco/banodoco-workspace-runtime`,
  `/home/user/work/venv-app2-native/bin/python`, and the external locked graph
  plus archive paths under the orchestration workers directory.
- preflight environment: `env -i`, `HOME=/root`, `LANG=C.UTF-8`,
  `PATH=/opt/node22/bin:/usr/local/bin:/usr/bin:/bin`,
  `NORMAL014_PROFILE=final95`, `NORMAL014_APP_SOURCE=parent`,
  `NORMAL014_USE_BASE_PYTHON=1`, explicit `NORMAL014_LOCKED_GRAPH` and
  `NORMAL014_LOCKED_GRAPH_ARCHIVE`, keeper path, and
  `SELECTED_FINAL95_MODE=preflight`.
- run environment: the same closed tuple with
  `SELECTED_FINAL95_MODE=run`; the tested stub additionally set
  `SELECTED_FINAL95_LAUNCH_STUB=true`. The original run path retains private
  `TMPDIR`, npm/Vite/Playwright cache paths, `NODE_OPTIONS`, `NODE_PATH`,
  `PYTHONPATH`, Runtime data/realm/door variables, credential/origin variables,
  and the selected Agent/Runtime head exports.
- source/helper recursion: `run_cheap_preflight` and `run_actual` source the
  current `SOURCE_COMMON`. Its final95 tuple is Agent
  `6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, Runtime and producer
  `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`, Runtime manifest
  `a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d`,
  76 artifacts, artifact version
  `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`,
  schema `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
  and wire `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`.
  It clones those exact source refs privately, verifies producer byte parity,
  checks the graph, creates only a private node graph, and uses the base Python
  because `NORMAL014_USE_BASE_PYTHON=1`.
- graph/dependency guards: Node `v22.22.0`; Composition `0.0.13`; Vite
  `5.4.21`; Vitest `4.1.5`; Playwright `1.60.0`; archive SHA
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`;
  embedded Composition tarball SHA
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; 77
  regular archive members; physical, symlink-free graph node_modules.
- selected source/pin guards: App source `0cc2583a…`, tree `320e74…`, base
  commit `32b74fdea165816226b6f0727a16817a6a1a79c3`, base tree
  `a3ddc2997e6460bab77d1e4ef7c1ac98ee21ad65`, selected spec SHA
  `2cd9703de2282282a477f5661d600049c8507fb93df1ef0424a06e7978a8b6a0`,
  harness SHA `bdd9b30b025c87097a99e5e67117ee01612f50b4f5a7c11f8f8dbe1ddb13f64a`,
  Vite config SHA `5f26c8fa9beae5691c7c94ae11d008eb6c548eb28aaa2b66887b7512efe6c70d`,
  and discovery proxy SHA `93989e634008d1c9a6aaeddbca7b0aa0f97c40a7ce232860157d04bc6b2155c0`.
- original behavior guards: credential file/origin/project scope, Runtime
  receipt/idempotency assertions, exact P1/P2/action/body/argv, reload and
  inverse/undo assertions, zero legacy posts, partial trace/context retention
  with no DOM retention, explicit child return-code propagation, and the
  single-copy/private-cache controls remain unchanged.

The parent helper and selected P1 driver are included in the four-export
integrity set and pass syntax/hash checks. Their standalone parent-media and
P1 build/e2e bodies were not invoked by this task; the selected runner only
sources `SOURCE_COMMON` and checks the other two by path/hash/syntax. Their
graph/archive paths and retained dependency guards were nevertheless included
in this inventory.

## Why 1120 PASS was withdrawn

The 1120 log shows its preflight PASS occurred before the later export patch
that replaced the helper/driver bytes with the current explicit graph/archive
path bindings. The subsequent 1120 packet hash inventory recorded the new
`647e…`, `ce9e…`, and `cf4d…` files, but the runner's internal guard literals
remained the old approved-966 values. Thus 1120 PASS was valid only for the
then-bound old files; it did not validate the final exported bytes. Review 1128
correctly withdrew that readiness after recomputing the actual bytes. The
earlier list1 result is reused only for its exact source/graph/list scope, not
as current run-hash qualification.

## Reverse proof

The reverse diff was generated by replacing only the three corrected values
with the old values in a process substitution and diffing against the final
runner. It produced exactly three changed data lines at
`verify_scripts_and_scope`; all other runner logic, paths, pins, body,
assertions, argv, and guards were unchanged.

## Exact checks and results

```text
sh -n <runner>; sh -n <source-common>; sh -n <parent-media-central>; sh -n <selected-p1-driver>
PASS

sha256sum of all four exports and KEEP
PASS; manifest recorded above

One existing cheap LOCAL preflight, after aggregate-list setup:
PASS; all 12 aggregate checks and Playwright `1 test in 1 file`
PASS; wrong role/tree/pin/path/argv/zero-test and wrong-artifact refusal probes

Existing run-path control with SELECTED_FINAL95_LAUNCH_STUB=true:
PASS; real run dispatch reached the stub and returned 0 before build/browser/test

private exact-0cc source copy cleanup
PASS; removed after controls

assigned App worktree status
PASS; clean
```

The preflight and run-stub commands used the existing runner only. No browser,
build, Runtime service, socket, daemon, install, full suite, selected actual,
or MAIN qualification was run or claimed. MAIN remains HOLD for the recorded
Node20 versus required Node22/locked-graph qualification. Manager
authorization remains subject to the stated parent-slot/fresh-floor/lock
conditions.
