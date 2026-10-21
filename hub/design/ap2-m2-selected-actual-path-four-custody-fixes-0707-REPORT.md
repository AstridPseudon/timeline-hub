# App2 M2 selected final95 actual-path custody correction

## Result

Corrected the owned runner copied from worker 0658:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-actual-path-four-custody-fixes-0707/run-owned-selected-final95.sh
sha256: a92fded8e01ce622060113d1296ac74e9ccff6a8770a8dcac08e331a0d901964
```

The App worktree is clean. No App source/spec, dependency, lock, generated
file, shared helper, shared graph, Agent source, or Runtime source was edited.

## Four review findings closed

1. The actual path now validates the service-captured App tree and selected
   source bytes immediately before overlay copy. It separately requires
   `APP_KEEPER_ROOT` in run mode, checks that it is physically distinct,
   clean, and exactly `HEAD ba02c8f246ec61cd65d178a1ada686788df3fdab` / tree
   `7fe8c15b56da9944ae31e8273d41d3ceb21b3677`. The own worker `KEEP` marker
   and normal Runtime lock/generated/schema links remain checked.
2. Actual collection now uses the exact selected title and `verify_private_list`;
   zero, no-test, or multiple title matches refuse before launch/build.
3. The actual path controls inherited `NODE_PATH` and `NODE_OPTIONS` before
   any Node helper runs, restores the owned final95 tuple after sourcing the
   compatibility helper, and verifies the actual private Vite/Vitest/
   Playwright/Composition versions plus the Composition ESM entry.
4. The runner owns one physical `RUN_ROOT`; the helper's run-root/trap is not
   invoked. One EXIT cleanup path covers success, failure, HUP, INT, and TERM.

The helper is sourced with its existing `parent` compatibility role only for
its closed source/graph functions; `restore_owned_tuple` rebinds the runner's
selected final95 values so helper role variables cannot replace the selected
registration. No shared role patch was needed.

## Immutable registration

```sh
RUNNER=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-actual-path-four-custody-fixes-0707/run-owned-selected-final95.sh
SERVICE_CAPTURED_APP_ROOT=<clean service-captured App root with HEAD tree 7fe8c15b56da9944ae31e8273d41d3ceb21b3677>
PROTECTED_APP_KEEPER=<separate clean keeper with HEAD ba02c8f246ec61cd65d178a1ada686788df3fdab>
APP_KEEPER_ROOT="$PROTECTED_APP_KEEPER" SELECTED_FINAL95_MODE=run "$RUNNER" "$SERVICE_CAPTURED_APP_ROOT"
```

The selected recipe remains unchanged:

```text
title: local DEV selected PARAM uses admitted P1 through P2 removal, refusal, retry, reload and undo
spec:  tests/e2e/local/three-products.selected-param-dev.spec.ts
spec sha256: 10250fa44db4e2d4423f8d06258105df267e3ba4e29700d700bb1d3182a6def1
```

Final tuple retained:

```text
App HEAD/tree:       ba02c8f246ec61cd65d178a1ada686788df3fdab / 7fe8c15b56da9944ae31e8273d41d3ceb21b3677
Agent HEAD/tree:     6efc81500a0e0688c2bb41e736503f0fc3e04abb / 2ed2b8a12b5b3391ca221ba6ff05390f71a73556
Runtime HEAD/tree:   95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c / d3a290b407fa61e6ab2d476f50c068073f70df00
artifacts:           sha256:54205b3ecb55038e416b31af936c9af26afa30db1d05da16157ee4d861fe05ac
manifest:            a902387c6a2315374f7e73511feea47da30191aba831b48820b3864b773a532d (76)
schema:              6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
Composition tarball: 9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738
graph archive:       895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
```

The artifact line above is the exact retained value from the frozen
registration (`sha256:54205b3ecb55038e416b31af936c9af26afa30db1b05da16157ee4d861fe05ac`); the runner literal is
`sha256:54205b3ecb55038e416b31af936c9af26afa30db1b05da16157ee4d861fe05ac`.

Unchanged control hashes:

```text
normal014-source-common.sh:       d9a691dcaafd7d544a467445a3a020a9ad3d02afc1d527870f00be6948fea848
normal014-parent-media-central.sh: 1d2ebce742bab9a20a911baedab8e7e318e82d6f1043f7f554949855acf646fd
old selected driver:              a959de6e0041f0d8ee28b949a19f5add97d7fb5de27714da6beaad15abd6ce4f
```

## Evidence

Commands and results:

```text
SELECTED_FINAL95_MODE=preflight /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-actual-path-four-custody-fixes-0707/run-owned-selected-final95.sh <selected App root>
  PASS
sh -n /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-selected-actual-path-four-custody-fixes-0707/run-owned-selected-final95.sh
  PASS
preflight result: all ten checks; exact one test in one file
```

Final valid actual-path control used a separate clean detached keeper and a
launch-only stub. It entered the real `run` dispatch with hostile inherited
`NODE_PATH=/tmp/wrong` and `NODE_OPTIONS=--require=/tmp/wrong`; the stub saw
the runner-controlled private values. Trace reached every actual control:

```text
source_refs artifacts locked_graph scripts_scope selected_contract
service_source protected_keeper keep_and_normal_link node_graph list1 launch
```

Result: PASS, status 0, root removed after success.

Final actual-path planted refusals, all before launch:

```text
wrong role/source identity       REFUSED, status 1
wrong service tree               REFUSED, status 1
wrong App lock pin               REFUSED, status 1
wrong locked graph path          REFUSED, status 1
wrong App source root            REFUSED, status 1
dirty protected keeper           REFUSED, status 1
zero/no-test list                REFUSED, status 1
multiple-title list              REFUSED, status 1
```

Cleanup controls through the same actual dispatch:

```text
launch stub exits 17             PASS: status 17, root removed
launch stub sends SIGTERM        PASS: status 143, root removed
```

No browser, hosted build, product launch, daemon, live socket, full suite,
dependency installation, or central actual was run.

## Additional execution evidence

While proving the valid control, the pre-existing actual-path source-manifest
`printf` emitted invalid JSON (three leading quotes around
`runtime_environment`), preventing the real workspace-create step from
reaching the requested launch boundary. The runner now computes the parent
Python environment path separately and emits valid JSON. This is a minimal
runner-only execution correction discovered outside the four custody findings;
it is called out explicitly for orchestrator review rather than silently
relabelled as one of the four.

## Next step

The orchestrator may perform exactly one central actual using the literal
registration above and an immutable selected source/keeper pair. This worker
claims runner custody and offline stubbed-dispatch evidence only, not browser
behavioral qualification.
