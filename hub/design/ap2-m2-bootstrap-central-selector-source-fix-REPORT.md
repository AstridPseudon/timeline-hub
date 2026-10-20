# AP2-M2 bootstrap central selector/source repair

## Result

**NOT QUALIFIED — the central harness selector was repaired, then the first
real App run reached the browser and failed the product assertion before
bootstrap creation.**

The prior result (`30268`) was not product evidence: its private wrapper used
an anchored full-title grep and Playwright reported `No tests found`. The
source was already committed and contains the requested test at
`tests/e2e/local/three-products.spec.ts:1141`.

This worker made no App source or test-source change. It created one disposable
private central wrapper/suite entry, changed only the selector and collection
order, ran one central qualification, then removed both private harness files.

## Causal harness repair

Playwright's grep is evaluated against the fully qualified test title, whose
displayed form includes the file/line prefix. Therefore this selector did not
match:

```text
^M2 real gate 5 bootstrap actual consumer: production initializer uses native create/init, exact retry, restart and guarded undo$
```

The private wrapper now used the unique unanchored selector:

```text
M2 real gate 5 bootstrap actual consumer
```

It also passed the exact source path,
`tests/e2e/local/three-products.spec.ts`, and ran Playwright `--list` after
the private overlay/dependency/runtime environment was assembled but before
`npm run build:hosted`. This proved the selected test survived into the
central copied source before build/serve activity.

The private wrapper retained the normal014 source and authority guards and the
approved tuple: Agent `3c4f6de4fa777323b3386c01c7266b619b86af6d`, Runtime
`202074110717146fc7f08af2306a8dd7f695b0b1`, immutable producer `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, artifact
`sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`,
schema guard `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
and locked Composition 13. No public013 substitution or shared dependency
mutation occurred.

## Central qualification

Exactly one corrected central request was submitted:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-bootstrap-central-selector-source-fix \
  ap2-m2-bootstrap-central-selector-source-fix)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  ap2-m2-bootstrap-central-selector-source-fix-ap2-m2-bootstrap-central-selector-source-fix-1020201909-29453
```

Result: **FAIL, exit 1, 95 seconds**. Result directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-bootstrap-central-selector-source-fix-ap2-m2-bootstrap-central-selector-source-fix-1020201909-29453/`

The first causal log records:

```text
Listing tests:
  three-products.spec.ts:1141:1 › M2 real gate 5 bootstrap actual consumer: production initializer uses native create/init, exact retry, restart and guarded undo
Total: 1 test in 1 file
...
normal014 App PRE-browser: private source collection, npm/Vite caches, and hosted build output verified
Running 1 test using 1 worker
```

The browser then executed the selected App test and failed at
`three-products.spec.ts:1180`:

```text
Error: production bootstrap must create the timeline through Runtime /v1
Received: undefined
```

The observed request list contained no expected POST to
`/v1/projects/<project>/timelines/<timeline>` before the assertion. The
failure is therefore a real product/bootstrap-path failure, not a collection
or source-copy mismatch. Per instruction, this first causal result was not
rerun.

## Evidence and boundaries

- App tree tested by the central service: `905803d2a46ee21ce272ef2fa090079c809a4f67`;
  source candidate remains `ffe9ee82387d704474cc7f09e5d8178467058f1b`, with
  approved production candidate `449ae7c00067169f1f6c4db727ac4b0fa702e0e2`.
- Existing focused evidence remains **158 tests passed across 6 files** and
  focused ESLint passed; it was not rerun because this repair changed no App
  source or test source.
- Wrapper shell syntax check passed before the central request.
- Central private artifact, vendor-lock, Python collection, private node graph
  (`532` packages / `34` bins), hosted build, and Chromium pre-browser checks
  passed.
- No full suite, local browser/script/socket run, public pin/adoption,
  dependency/DTO/product guard edit, Gate 5 rerun, Agent-only proof, or source
  test weakening was performed.
- The private wrapper and suite registration were removed after the result;
  the App worktree remains clean.

## Recommended next step

Investigate why the real New Project flow in this exact private tuple does not
emit the expected Runtime `/v1` timeline-create request, using the captured
browser trace/error context. Do not treat this run as App bootstrap
qualification, and do not rerun the central service without a product-side
causal fix.
