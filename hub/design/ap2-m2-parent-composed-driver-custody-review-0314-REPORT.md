# Parent final95 composed driver custody review

## Disposition

**HOLD. Request one smallest committed-byte correction before durable staging.**

The composed candidate is otherwise the correct minimal driver, but its retained
source identity has one false archive label. At line 51 of
`tests/e2e/local/support/run-parent-manual-drop-evidence.sh`, it records:

```text
public13_archive_sha=sha256:895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30
```

`895c…` is the private App dependency-graph source archive. The immutable public
Composition 0.0.13 archive is `9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.
Change that one value (or otherwise correct the label while preserving the
graph digest separately), then recompute the driver hash. This is an evidence
identity defect, not a product or test-body defect.

## Candidate identity reviewed

- Commit: `45fbfc867686004dbc59de2261b892900250167f`
- Parent/source-guard base: `da6d910f7ab3dfc71142ece7f632d43341238882`
- Parent tree: `6809757f93ca5e166b24b8bc0160ca09005e984a`
- Candidate commit tree: `be8dc85e65f7d0326bdeb0e23c1f50e576a86a24`
- Driver blob: `1e9235496acb53b61f51fb151e9cca7de7a38433`
- Driver SHA-256: `038e73f7b903b31bd073bce2c9f5e84a1beb5991c38c97620e9d920448ef9366`
- Binary diff SHA-256: `29fd05d688409d8af34e66eed0aefb27001393d565167f376de448c6ec853927`

The commit changes only the existing driver. It carries the da6d/tree680 guard
base and only the approved manual selector delta plus the `preflight` entry
point. It does not copy the old fb075 driver, change the source test, pins,
product code, or suite definitions. The candidate itself contains no stale
`78f`, `3c4`, `202`, `a0`, or fb075 identity claims; the `7e85` value is the
approved ancestry anchor, not the stale App tree.

The closed tuple is consistent in the driver/source helper: Agent
`6efc8150`/tree `2ed2b8a1`, Runtime and producer `95bd3c5f`/tree `d3a290b`,
App pin `10fa2ff9`, final95 manifest count 76, and public Composition 0.0.13
with the corrected public archive identity above.

## Guard and selector review

`run` and `preflight` both enter the same driver `run_gate`; the only mode
difference is the argument passed to the copied existing
`normal014-app-central.sh`. That runner performs the exact source, pin,
artifact, import, and provenance checks before its preflight branch, and the
run branch uses the same checks. The driver’s direct ancestry and clean-status
checks also precede either mode. No second validator or alternate source
authority was added.

The transformed runner keeps the structured exact-case verdict guard with the
full manual ADD title, while the actual Playwright selector is the approved
`M2 real mounted manual video drop` substring. The original frozen source test
at `da6d/tree680` remains separate and unchanged. Its body still asserts the
exact 404/not_found refusal, unchanged history/head and clip count, import 201,
selection/verified five-field equality, exact parent `clip.add-media` command
without `afterClipId`/remove/replace fields, V1 at 20, one durable ADD, exact
lost-ACK/reload/restart retry body/key/response, one resulting clip, opaque-data
preservation, exact inverse undo, and zero legacy traffic. Bootstrap and
mixed-selector routes remain outside this parent-only substitution.

## Checks run

Passed:

```text
sh -n candidate driver, normal014-source-common.sh, normal014-app-central.sh
git diff --check 45fbfc867^ 45fbfc867
NORMAL014_RECORD_DIR=<private-temp> sh candidate probe
  failuretrap probe passed
PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers TMPDIR=<private-temp> \
  PWTEST_CACHE_DIR=<private-temp> PLAYWRIGHT_OUTPUT_DIR=<private-temp> \
  node node_modules/playwright/cli.js test \
  --config playwright.three-products.config.ts \
  --grep 'M2 real mounted manual video drop' --list
  exactly 1 case: three-products.spec.ts:1440
old anchored bootstrap selector with the same --list command
  exit 1, Error: No tests found, 0 cases
candidate preflight with clean wrong-tree app-pin-25155ccb
  exit 1 before source preparation/build/browser work
candidate preflight with dirty /home/user/work/app
  exit 1 before source preparation/build/browser work
verify_app_source with wrong clean tree, dirty root, and unknown source role
  all refused
verify_artifacts against the no-HEAD Runtime source root
  refused
```

The selector command was collection-only; no browser, localhost/live socket,
build, install, central service, full suite, or actual mounted ADD run was
performed. The exact positive mounted source preflight was not run because its
existing implementation performs the out-of-scope build/install/collection
work. Therefore no mounted body, recovery, undo, or durable invocation is
qualified by this review.

## Durable next step

After correcting the archive identity and recomputing the hash, copy that exact
file byte-for-byte to the durable driver location, record the new SHA-256, and
review the durable invocation against the same `author0230` source snapshot and
`da6d/tree680` guard. No durable invocation or actual run was authorized or
submitted here.
