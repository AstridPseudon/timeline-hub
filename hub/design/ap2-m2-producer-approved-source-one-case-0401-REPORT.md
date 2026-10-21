# AP2 M2 producer approved-source actual result

## Result

The one authorized central request was submitted exactly once:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test ap2-m2-producer-explicit-run-mode-source-0354 ap2-m2-producer-existing-graph-command-actual-e2e-integration --no-cache
```

Result packet:

```text
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-producer-explicit-run-mode-source-0354-ap2-m2-producer-existing-graph-command-actual-e2e-integration-1021040015-21671/
```

The central test service recorded `fail`, exit `1`, in 2 seconds. The command was:

```text
sh scripts/testing/run-producer-public13-list.sh "$PWD" run
```

The result packet's `log.txt` and `runner.log` are both zero bytes. No Playwright output, producer assertion, browser journey, or actual body result was produced. This is a preflight/source-ancestry failure, not a product-body failure.

## Preflight identity

The approved source was verified before submission:

- source commit `00bbc22d63b4abe7275cfe9ad5f3762157d7394f`
- source tree `f41a45c01293b0248a27c490bb9e8aa02be33ecd`
- parent `70dec48e88ea036bf160539b58b68bb64c38f3b3`
- body SHA-256 `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`
- helper SHA-256 `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`
- actual config SHA-256 `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`
- run-mode wrapper SHA-256 `11080069b40aab7e9fd9798974cc43d9b244de5f17d930ebc74dc0f935136fc2`
- Agent commit/tree `8130a401bf44a518d5a40ae274d398b8c560be55` / `236c3e57e0265c52b81ba8085de3193026176bff`
- Runtime commit/tree `2c4ac180c2220bdad966bc01e95ad230e99ce26a` / `7ab412cc4bcbe517efcfa806e092336390312e18`
- protected public13 runner SHA-256 `40c25724b502ce5582caf04c6ebf44ab89a509b5f3d629876d599f57c3e5fa7a`
- public13 Composition tarball SHA-256 `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; 77 regular members
- Runtime producer manifest SHA-256 `6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`; 75 artifacts
- protected graph archive SHA-256 `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`

The approved delta review also verified the exact Node/Vite resolver, graph, argv, actual config, `--list` preflight count of one, short private paths, disk threshold, max-two-copy isolation, and no concurrent producer caller before this request. The local preflight observed 15 GiB available on `/tmp`; no other producer/playwright tester was active.

## First-failure cause and preserved evidence

The source runner contains `APP_SHA=4ef89267f00d193273441ff6dbb955f30d27d708` and, for a changed snapshot, requires the snapshot's `HEAD^1` to equal that SHA. The central service correctly snapshot-committed the requested source tree with source head `00bbc22d…`; therefore the snapshot's direct parent is `00bbc22d…`, while that source commit itself has parent `70dec48e…`. The runner compares `00bbc22d…` with `APP_SHA=4ef89267…` and fails before emitting output. The source delta therefore does not satisfy the runner's existing one-parent delta assumption.

This diagnosis is based on the preserved packet, the exact source commit ancestry, and the runner source; no rerun or wrapper modification was made. Original rows/order/reload/lost-ACK/restart/exact-body+key/retry/undo/zero-legacy assertions were not reached and remain unverified.

## Changes and next steps

No product or test-source files were changed in this worker; its worktree remains clean. Per instruction, execution stopped at the first failure: no retry, new source, timeout, full suite, or local browser was run.

Next step requires an orchestrator decision: repair or otherwise qualify the source runner's ancestry guard for the approved `00bbc22d…` delta, then authorize a new single actual run. Do not treat this result as a producer product failure.
