# App2 M2 Main95 exact consumer-neighbor check

## Result

PASS. The approved immutable App source was verified as:

- commit `10fa2ff9a8216604aa39e3584f89dc9e7a09080a`
- tree `01fd2a04ff0c383ec5281043c7e5a4c843d1d835`

The exact dependency identities were verified read-only:

- Agent commit `6efc81500a0e0688c2bb41e736503f0fc3e04abb`, tree
  `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`
- Runtime commit `95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c`, tree
  `d3a290b407fa61e6ab2d476f50c068073f70df00`

The App `runtime.lock.json` source commit is the approved Runtime `95bd…`.

## Exact check

Command run from the immutable App tree:

```sh
TMPDIR=/tmp/w-ded2ace1b1 ./node_modules/.bin/vitest run \
  --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 \
  --no-file-parallelism \
  src/integrations/runtime/clientStatus.test.ts \
  src/integrations/runtime/clientSharedSession.test.ts \
  src/integrations/runtime/client.runtimeOrigin.test.ts \
  src/integrations/runtime/connection.test.ts
```

Result: **4 test files passed, 47 tests passed, 0 failed**.

The four files were the only tests run for this check. The already-qualified
`client.test.ts` and `vendorLock.test.ts` suites were not repeated. No updater,
browser/build/full/live-socket/central test service run, historical `26437`
replay, or Composition14 check was run.

## Scope and disposition

No App source, product code, lock, generated file, pin, activation, or
adoption change was made. The prior exact10fa 45-client/schema plus 13-vendor
qualification is carried unchanged. HOME native `timeline.init` activation
remains a separate same-pin/activation proof.

The test runner left a synthetic mount under the worker-private TMPDIR. Exit
cleanup was attempted, but that mount is read-only and busy in the sandbox;
the cleanup failure did not affect the App worktree. The App worktree remained
clean.
