# D127c Node20 whole-path diagnosis

## Result

F002 has a finite execution cause. The reported Node20 run used:

```text
--test-name-pattern='^(D127c source guard|D127c reviewed-profiler validator)$'
```

The exact committed App source registers these top-level tests:

```text
line 540: D127c source guard accepts every reviewed arm and rejects wrong hash or source
line 715: D127c reviewed-profiler validator enforces the exact safe cProfile projection
```

The anchored alternatives require end-of-string immediately after `source guard` or
`validator`, so neither registered title matches. This explains the file-wrapper-only
result and zero intended inner nodes. It is expected filtering, not a proven fork,
sandbox, or Node20 spawn failure. F002 remains unqualified because the corrected
Node20 command was not run by this worker.

## Source-to-runner trace

1. The App command enters Node's `node:test` runner with the `.ts` file as the test
   target and `--import tsx` as the TypeScript ESM preload. The exact App lockfile
   resolves `tsx` 4.21.0.
2. The file imports `node:test` and registers seven top-level `test()` calls. The
   source-only TypeScript AST map has zero parse diagnostics and identifies the two
   D127c controls at lines 540 and 715.
3. Node applies `--test-name-pattern` to the complete test name. The bad anchored
   pattern matches zero of the complete names. The corrected anchored full-title
   alternation matches exactly both intended controls.
4. Reporters consume the resulting test events; reporter selection cannot turn a
   zero-match pattern into a selected test. `--test-reporter=spec` is supported by
   Node20 and makes the selected/skipped counts visible. The custom App skip-guard
   reporter is not part of the failed command.
5. Node20 v20.19.4 supports `--test`, `--test-name-pattern`, `--test-reporter`, and
   `--import`, but its help has no `--experimental-test-isolation` option. Node22
   v22.22.0 exposes that option. The Node22 passing control therefore cannot prove
   that Node20 needs or lacks isolation; it differs in both isolation flag and title
   selector.

The prior exact-title Node20 control is useful independent evidence: the profiler
title-only command used `--test-reporter=spec` and reported 1 passed / 5 skipped.
It demonstrates that the supported Node20 interpreter, TSX preload, and test-file
registration route can execute this control. It does not qualify the two-control
F002 proof or any live/bootstrap behavior.

## Command comparison

Failed Node20 command (recorded, not rerun here):

```sh
/home/user/work/runtimes/agent-remotion-app-p1-787-2a9-1830/.toolchain/node-v20.19.4-linux-x64/bin/node --import tsx --test --test-concurrency=1 --test-name-pattern='^(D127c source guard|D127c reviewed-profiler validator)$' tests/e2e/local/support/p2-runtime-phase-bootstrap.test.ts
```

Passing Node22 controls (recorded prior evidence; not rerun here) used exact/full
title patterns, `--experimental-test-isolation=none`, `TSX_DISABLE_CACHE=1`, an
explicit Runtime checkout, and `--test-reporter=tap`. Those controls passed one
named node each, but are supplemental to the required Node20 proof.

## Boundaries

No unit/test body, Node20 proof, localhost/socket/service/bootstrap, browser,
profile, native, full suite, tour, source change, Runtime rerun, Git write, or
upstream operation was performed. Runtime PASS61 remains unchanged. D130 SWAP,
WAL/recovery, and full-tour hold remain untouched.
