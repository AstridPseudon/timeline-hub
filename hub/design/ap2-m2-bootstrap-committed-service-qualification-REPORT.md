# AP2-M2 committed-service bootstrap qualification

## Result

**NOT QUALIFIED — central harness selector failure before browser execution.**
The one requested central run completed the exact private normal014 setup and
hosted build, then Playwright returned `Error: No tests found` for the exact new
bootstrap title. No App browser journey ran, so this result is not evidence of
a product failure or a positive App qualification.

The committed App candidate was clean at `ffe9ee82387d704474cc7f09e5d8178467058f1b`
(tree `905803d2a46ee21ce272ef2fa090079c809a4f67`), preserving approved source
candidate `449ae7c00067169f1f6c4db727ac4b0fa702e0e2`. The only product-tree
change remains the new real consumer journey in
`tests/e2e/local/three-products.spec.ts`.

## Private suite and wrapper

Registered the unique App suite
`ap2-m2-bootstrap-committed-service-qualification` in the central test
allow-list. Its worker-record wrapper is
`run-bootstrap-committed-service-qualification.sh`; it is a private copy of
the existing normal014 wrapper and narrows only the Playwright selector to:

```text
M2 real gate 5 bootstrap actual consumer: production initializer uses native create/init, exact retry, restart and guarded undo
```

The wrapper retains the existing source and authority guards: Agent `3c4`,
Runtime `202` plus immutable producer `a0`, artifact `f021`, schema `6ba`,
locked Composition `0.0.13`, private Python imports/collection, private node
graph (`532` packages and `34` bins), vendor-lock checks, generated-file
hashes, hosted build, Chromium check, and browser lock. Its EXIT trap removes
the disposable run root. No public013 source substitution was made.

## Central evidence

Exactly one request was submitted:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-bootstrap-committed-service-qualification \
  ap2-m2-bootstrap-committed-service-qualification)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  ap2-m2-bootstrap-committed-service-qualification-ap2-m2-bootstrap-committed-service-qualification-1020201152-30268
```

Result: **FAIL, exit 1, 154 seconds**. Result directory:
`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-bootstrap-committed-service-qualification-ap2-m2-bootstrap-committed-service-qualification-1020201152-30268/`.

The log proves the private setup ran:

```text
verified artifacts=75 manifest=ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815 schema=6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d
private node graph: packages=532 bins=34
normal014 App PRE-browser: private npm/Vite caches and hosted build output verified
Error: No tests found
```

The committed source contains the exact requested title at line 1141, but the
central Playwright invocation collected no matching test. Per instruction, the
first result was classified and not blindly rerun.

## Other evidence and boundaries

Previously recorded candidate checks remain valid: focused Vitest **158 tests
passed across 6 files**, focused ESLint passed, Playwright collection reported
10 tests including the new journey, and `git diff --check` passed. Those checks
do not replace the missing central App consumer proof.

Not proven by this run: real `AstridRuntimeClient -> RuntimeDataProvider ->
createDefaultTimeline` activation, Runtime native initialization, opaque
`null`/`false`/`[]`/`{}` preservation, reserved IDs, lost ACK/restart/exact
retry/no duplicate init, reload/undo/redo, or zero legacy traffic in a live
App journey. No full suite, public pin/adoption, dependency/DTO mutation, or
product source change was made.

## Recommended next step

Have the orchestrator inspect the exact-title selector/central Playwright
collection mismatch, then authorize a fresh uniquely identified central run
only after correcting that harness issue. Do not treat this first result as
either product red or App qualification green.
