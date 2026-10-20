# AP2 M2 selected DEV runner preflight repair

## Result

Repaired the retained selected DEV driver at:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh`

The matching own-worktree copy is `run-central-selected-p1.sh` in this worker
worktree. No App product source, provider, DTO, catalog, authority, fixture,
shared dependency, or install was changed.

## Causal diagnosis

The existing central result
`ap2-m2-selected-draft-p1-review-gate-ap2-m2-selected-real-p1-history-fixture-fix-1020214132-29175`
first failed in the test wrapper, before the selected driver could qualify:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/test-run:34` attempted
to write
`/tmp/.../orch/tests/cache/28d9957ea71d4537ad8922522a7fe9a7.running`, but the
parent `tests/cache` directory was absent. Wrapper cleanup repeated the same
missing-path failure at line 49. The retained log therefore contained only the
driver's final trace message.

A safe `sh -x` probe of a clean private App snapshot then identified the first
selected-driver guard: `prepare_private_node_graph` requires
`$RUN_ROOT/private-node-modules` not to exist, while the driver had just created
it in its `mkdir -p` list. The driver now leaves that path absent for the
helper. The driver also now retains `driver.stderr` and emits it to the
original stderr fd before EXIT cleanup removes the private run root.

The next list-only probe found a second pre-collection issue: anchored
`--grep "^$TEST_TITLE$"` matched zero tests because Playwright matches the full
title, including the spec-file prefix. Both collection and execution now use
`--grep "$TEST_TITLE"`, selecting exactly the intended test.

The repaired source retains the actual App2 Python
`/home/user/work/venv-app2-native/bin/python`, Agent `8130a401...`, Runtime
`2c4ac180...`, locked Composition `0.0.13` archive/hash guards, absolute
helper paths, private node graph, and existing DEV environment exports.

## Checks

- `sh -n ./run-central-selected-p1.sh` — passed.
- `sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-draft-p1-review-gate/run-central-selected-p1.sh` — passed.
- Safe private preflight probe with `SELECTED_PREFLIGHT_ONLY=1`, `TMPDIR=/tmp`,
  and clean git snapshot — passed; exact Agent/Runtime commit+tree, archive,
  Composition, Python, private checkout, and private node graph guards passed.
- Safe private collection probe with `SELECTED_LIST_ONLY=1` — passed; exactly
  1 test listed, the selected DEV test. No browser, build, localhost, socket,
  native provider, full suite, or central wrapper was run.
- Own copy and retained external driver are byte-identical after repair.

## Exact next command

After the orchestrator recreates the central cache directory, the one next
qualification command is:

```sh
ORCH=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a
mkdir -p "$ORCH/scratchpad/orch/tests/cache"
R=$("$ORCH/scratchpad/orch/bin/request-test" ap2-m2-selected-draft-p1-review-gate ap2-m2-selected-real-p1-history-fixture-fix --no-cache) && "$ORCH/scratchpad/orch/bin/wait-test" "$R"
```

That command is not run in this task.
