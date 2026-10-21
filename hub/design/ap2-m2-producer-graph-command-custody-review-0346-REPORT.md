# Producer invocation graph custody review 0346

## Verdict

The invocation mechanics are sound for the tested snapshot, but I cannot
approve the exact registered suite as a durable command. Its new wrapper
delegates to the existing public13 runner at
`$ORCH/workers/ap2-m2-public13-effective-build-attachment-fix/public13-integration-runner.sh`.
That worker is already marked `recycled` (2026-10-20 19:04 UTC). The file is
still present today, so the recorded central run passed, but the suite is
not safe to retain after the worker directory is reclaimed.

Smallest defect: preserve/lease that existing runner for this suite, or move
the unchanged runner to a durable owned path and update the wrapper's path and
hash. Do not duplicate or relax its source/graph guards. After that path fix,
rerun only the source-only named suite/list preflight as needed; no browser,
actual journey, full suite, or unchanged build is warranted by this review.

## Exact reviewed source and command

The stage0320 source is exact:

- App commit `4ef89267f00d193273441ff6dbb955f30d27d708`, tree
  `8c7393050ded32854503dfb7719a102b5dec94eb`.
- Producer body commit `36dd91257fd13dcad0d58b48c790caa5063b4c8c`, tree
  `d908845dbc8e5ebf96698d08621557e904f20c52`.
- Spec SHA-256 `d91d0c1cce22f68119cd30fcb0a288346474b0ad4b64c84dcee3b730fa468d89`.
- Helper SHA-256 `50cbe5341f24c9a1ecc999018e2c6d975380a3440570abce151f9173c9752016`.
- Selector config SHA-256 `5b880ceff883abce2575a3a85aaa4eda69d3bcb848768ff0e91f337d50cca4c0`.
- New forwarding wrapper SHA-256
  `d382db5b7ddcd9d5dc2420666d340cd2ff7ea97a6f3a1521e4f455a29bbb0354`.

The exact registered suite is:

```text
app ap2-m2-producer-existing-graph-command-e2e-integration sh scripts/testing/run-producer-public13-list.sh "$PWD"
```

Its forwarding path preserves the existing public13 runner's build command,
then matches the exact child argv:

```text
npm run test:e2e:three-products -- --grep "M2 ordinary extension batch"
```

and invokes the existing selector as:

```text
node_modules/.bin/playwright test --config playwright.producer-ownership-current-pin.config.ts tests/e2e/local/producer-ownership-current-pin.spec.ts --list
```

The selector collected exactly one test:
`removes only stale owned transcript output and moves only owned scene output`.
Arguments and paths are quoted; the wrapper uses `exec` for the hosted-build
child and preserves the selector child's exact nonzero status.

## Guards and evidence

The wrapper and existing runner verify, before the hosted build/list:

- Agent `8130a401bf44a518d5a40ae274d398b8c560be55`, tree
  `236c3e57e0265c52b81ba8085de3193026176bff`.
- Runtime `2c4ac180c2220bdad966bc01e95ad230e99ce26a`, tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Public13 archive SHA-256
  `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`, with
  77 regular members.
- Protected graph source archive SHA-256
  `895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`.
- Attached Composition package version `0.0.13`, package SHA-256
  `7c806b078b00bba1593336c49a3d2953b3f8f7afc7fa9919f6d5d7ccc7c1aa61`, and
  `dist/evaluation.js` SHA-256
  `e27ed545e9e0c28cf863e7bccd4a720f61e1002e04f2946dd3afca5e5f478155`.
- Runtime producer artifact digest
  `sha256:6f000bc615a9cb24fb00cc69a97af75eae71006ebfe87e3caa272fcdbbb1af56`,
  with 75 manifest artifacts.

The reused public13 runner's Node `createRequire` and Vite/Rollup resolver
checks both resolved the protected graph's Composition evaluation module;
the earlier build diagnosis recorded the same realpath/hash and required
export. The new runner adds no graph, package, pin, schema, body, or product
change. Its temporary child root, caches, TMPDIR, node_modules attachment,
and App `dist` are cleaned by traps in the forwarding and reused runners.

Planted negatives all behaved correctly in the stage0346 worker:

- wrong graph: rejected;
- wrong source identity: rejected;
- zero-test output / `NoTestsFound`: rejected;
- failing forwarded child: original status `1` preserved.

The named central source-only suite passed twice after the wrapper was staged:

- `...1021034721-16240`: exit 0, 60 seconds;
- final `...1021034858-18751`: exit 0, 59 seconds.

The final log shows the protected resolver PASS, hosted Vite build success
(`built in 49.28s`), and exactly one collected test. It contains no browser
launch or producer journey. The prior public13 build-only repair also passed
(`...2103`, exit 0, 58 seconds) against the same stage0320 source and graph.

Direct review checks here: `sh -n scripts/testing/run-producer-public13-list.sh`
passed; source, ref/tree, graph version, evaluation hash, and wrapper hash
matched the values above. No product worktree was modified, and no browser,
actual, full, or unchanged build was rerun.

## Live callers and next step

No live producer caller changed. The unchanged callers remain the Transcript
Lane extension and Scene Phase Markers extension registered by
`src/tools/video-editor/dev/localExtensions.ts`.

Before using the suite as an approval command, retain the existing public13
runner under a non-recycled path (or have the orchestrator explicitly lease
its worker directory). Then update the wrapper's path/hash and perform the
small source-only verification. The current run is evidence of correctness
of the wrapper mechanics, not durable qualification of the suite registration.
