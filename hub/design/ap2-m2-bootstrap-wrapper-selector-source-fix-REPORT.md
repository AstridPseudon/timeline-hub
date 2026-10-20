# AP2-M2 bootstrap wrapper/source selector repair

## Result

**NOT QUALIFIED — the wrapper/source collection failure is repaired, but the
single permitted browser gate failed an existing strict bootstrap identity
assertion.** The run did not return `Error: No tests found`; it collected and
executed exactly the intended bootstrap case. No behavior cut is claimed.

## Minimal cause and repair

The failed 15749 wrapper copied the requested App source and used an anchored
full-title grep. That made the effective wrapper source and selector implicit;
Playwright's displayed title includes the file/line prefix, so the anchored
selector collected no test. The App integration base also does not contain the
qualified bootstrap source.

Added the App-owned wrapper
`tests/e2e/local/support/bootstrap-wrapper-selector-source-fix.sh`. It keeps
the existing normal014 private tuple and guards, overlays only the donor's
exact 16 custody-approved paths onto the requested integration source, and
then proves both conditions in the same disposable overlay:

- donor ref `f487c0ca9a7b916bf842dd7a2cb3fa442ebeda3e`, tree
  `6444fffcaa606bfe83101ccb561c47fbd0d10ce4`;
- effective `tests/e2e/local/three-products.spec.ts` SHA-256 equals the donor
  blob: `df2b88dcebca08a9a1a5970108774b1289579209963da7a8611309fc58c15631`;
- exact path `tests/e2e/local/three-products.spec.ts` plus the unique
  substring `M2 real gate 5 bootstrap actual consumer` lists **1 test in 1
  file** before the hosted build.

The central allow-list received the unique suite
`ap2-m2-bootstrap-wrapper-selector-source-fix-integration`; `integration` is
intentional for the cross-repo cache key. The wrapper now also cleans its own
temporary run root after browser failure.

## One central run

Exact request:

```sh
R=$(/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/request-test \
  ap2-m2-bootstrap-wrapper-selector-source-fix \
  ap2-m2-bootstrap-wrapper-selector-source-fix-integration --no-cache)
/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/bin/wait-test \
  "$(basename "$R")"
```

Result: **FAIL, exit 1, 151 seconds**. Result directory:

`/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/tests/ap2-m2-bootstrap-wrapper-selector-source-fix-ap2-m2-bootstrap-wrapper-selector-source-fix-integration-1020231130-26944/`

The wrapper guards and hosted build passed. The browser ran one test and
failed at `tests/e2e/local/three-products.spec.ts:1360`:

```text
expected projectId: 4dcb2321f23d451091785dec01757b74
received projectId: 36498405a10c4b2ab9a5412eaf22a9a5
timelineId: d0022034-8d26-5584-8a06-ff87ba3b3d6b
```

This is the preserved strict assertion that the URL-selected timeline scope
must equal the project/timeline scope observed from the native create request.
The run stopped there; create/init ordering, lost ACK, restart/exact retry,
guarded undo, opaque values, and zero legacy traffic were not all proven.

Source tuple retained by the central log: Agent
`3c4f6de4fa777323b3386c01c7266b619b86af6d`, Runtime
`202074110717146fc7f08af2306a8dd7f695b0b1`, immutable producer
`a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, artifact `f021…`, schema `6ba…`,
and locked Composition `0.0.13`. No public013 substitution, fallback revival,
credential/custody weakening, shared dependency mutation, local browser/socket
run, full suite, or rerun was performed. The disposable central run root was
removed after the result.

## Targeted checks

- `sh -n tests/e2e/local/support/bootstrap-wrapper-selector-source-fix.sh` — PASS.
- `git diff --check` — PASS.
- Donor exact-16 path comparison, source blob hash proof, and selector proof — PASS in the central wrapper before build.

Recommended next step: investigate the retained project-scope mismatch in the
qualified bootstrap source/fixture pair. Do not rerun this unchanged tree or
claim the bootstrap behavior gate green.
