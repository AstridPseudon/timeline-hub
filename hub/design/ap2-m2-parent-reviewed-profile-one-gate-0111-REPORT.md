# AP2 M2 parent reviewed final95 one-gate report

## Result

**BLOCKED before central execution.** The approved final95 profile is present
and independently custody-reviewed, but the only registered genuine
File/media suite still invokes a stale external wrapper. Spending the one
central request would test that stale wrapper/cohort, not this worker's exact
current source. No central request was submitted and no gate result is claimed.

## Exact source and profile identities

Reviewed source pair:

- Row-local App source: `2fb03f7e2a8d70ca552c6417387f03e81686791b`, tree
  `ffbe469ea211df1de3f5ecf57075451ce41c14f5`.
- HOME construction: `32e997454b76378ba04505f894cd60fcddfe95b6`, tree
  `c16379e633e922790206d90d284dadab34c8256b`.
- Existing parent driver source: `780c502368cb6eb379cf3848af7009067c7cd744`,
  tree `8eed52bb7f8555c7765a8b485e00920bbf906639`.
- Disposable approved App candidate tree: `65b04167395f3a13dd63d580df7be706d6403223`.
  This is not present as a Git object or as the current App worktree tree.

Approved final95 profile:

- Agent: `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`.
- Runtime and producer: `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`.
- Runtime artifact: `sha256:54205b3ecb55038e416b31af936c9af26afa30dc1b05da16157ee4d861fe05ac`;
  76 manifest entries.
- Raw shared schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`.
- Final95 wire digest: `sha256:7d4afa05962b8cd61643213fc79cdde41e16046c4e2a777bd299b48af0f31816`.
- Approved normal App pin: `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`,
  tree `01fd2a04ff0c383ec5281043c7e5a4c843d1d835`.

The profile source-common hash is
`1e3708e5dff0b0acc251e9c97d802aa39383fe52435d229448e3517ebbe9a101`.
Its default remains historical `old202`; `NORMAL014_PROFILE=final95` resolves
to the tuple above and rejects unknown profile names.

## Blocking evidence

The current worker App identity is:

```text
HEAD  78fb4d77195e7e633082a2c0aaef139149409b18
TREE  7b39350a0b161dc0acdfa80060e1b8476886b9f4
STATUS clean
```

The worker-local existing driver expects the disposable candidate tree
`65b04167395f3a13dd63d580df7be706d6403223`, so it cannot accept this clean
source tree before the normal private overlay is created.

The registered suite command is:

```text
app ap2-m2-parent-retained-evidence-real-gate sh /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-retained-evidence-real-gate/run-parent-manual-drop-evidence.sh run "$PWD"
```

That external wrapper is not the current driver. Its source hash is
`84d25718c481d6699f2f9adcddbfbe45ea25efb7393a2f820bf0f2f8552c12b2`; it
requires stale App `HEAD 74643bed98fc9bf3102f544bc189e6464510f58b2` / tree
`a75e27930df49a0c4ee9005806d59b14f16d2361`, and does not bind the current
worker's candidate tree. The current driver hash is
`54b6027e506f057465f30061215fba297405a4cf0263e172787399c54afa8788`.

Therefore the registered command cannot prove the requested same-source,
same-tree final95 genuine File/media case. The required next action is to make
the already-registered runner resolve to the current driver/candidate while
preserving its existing source, lock, normal-updater, private public13 graph,
Node/Vite, short-child TMPDIR, cleanup, raw/order/reload/guarded-undo,
lost-ACK/restart/exact-retry, and zero-legacy guards. Then the one intended
request is:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-parent-reviewed-profile-one-gate-0111 ap2-m2-parent-retained-evidence-real-gate --no-cache) && /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test "$R"
```

No retry or alternate old-202/3c4/a0 suite was requested.

## Local checks

Passed without browser, localhost, live socket, dependency installation, or
shared-install writes:

```text
sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe
  failuretrap probe passed: evidence copied before disposable-root cleanup

sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh
node --check scripts/testing/current013-integration.test.mjs
git diff --check
  passed
```

No product source was changed in this worker. No browser or central evidence
exists to retain; no temporary build output was left in the worktree.
