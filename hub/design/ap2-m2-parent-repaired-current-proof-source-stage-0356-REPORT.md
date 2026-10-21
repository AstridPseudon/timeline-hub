# AP2 M2 parent repaired current proof source stage 0356

## Result

Prepared the source-only packet for the original mounted manual ADD proof on
the newly merged HOME source. No browser, actual mounted ADD, full suite,
native-bootstrap run, hosted build, or live socket was run.

The required repair merge landed during the bounded wait:

- HOME source commit: `5d36b0e53ff0d17ef045e226a6e6ca7584322858`
- HOME source tree: `1b07030d63216294f849422523b0d55a17422f23`
- HOME parents: `1557c312b999ddc0a21c1728acbc64052ef6491f` and approved repair
  `84ec385a463fd4907628e68e87aabbe717202a96`
- Merge subject: `Merge tl/ap2-m2-parent-reviewed-current-delivery-0349`

The worker tree was updated to retain the newer HOME production source, then
changed only the parent proof support and original manual ADD negative:

- `tests/e2e/local/support/run-parent-manual-drop-evidence.sh`
  - carries the durable final95 parent source role and exact Agent/Runtime
    tuple metadata;
  - uses the approved repair `84ec385a...` as its ancestry anchor;
  - retains the `878d` zero-test refusal and failure-trap evidence probe;
  - retains the corrected private dependency-graph label
    `private_dependency_graph_archive_sha`;
  - preserves the existing `run` path and adds the existing shared-preflight
    `preflight` mode, with the actual manual-drop selector and `--list` guard.
- `tests/e2e/local/three-products.spec.ts`
  - restores the original exact wrong-selection assertion: HTTP `404` plus
    `{ code: 'not_found', message: 'selected media is not a managed project
    generation/variant/object' }`;
  - all original native ADD, raw/opaque/order, lost-ACK, reload/restart,
    exact body/key, undo, and zero-legacy assertions remain present.

No new wrapper, graph, install, dependency copy, schema, pin, bootstrap
caller, or legacy assertion conversion was added.

## Frozen driver and source identities

The durable composed driver 0323 remains unchanged and is the existing suite
caller:

```text
driver=/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/workers/ap2-m2-parent-composed-driver-label-durable-stage-0323/run-parent-manual-drop-evidence.sh
driver_sha256=40c7b57b6f327bafa82f26daaa4053f405e89f7bd48b5aacdadd21b2393867f0
suite=app ap2-m2-parent-composed-driver-label-durable-stage-0323-e2e-integration
command=env NORMAL014_PROFILE=final95 NORMAL014_APP_SOURCE=parent sh <durable-driver> run "$PWD"
source_argument=harness snapshot of HOME 5d36b0e53ff0d17ef045e226a6e6ca7584322858/tree 1b07030d63216294f849422523b0d55a17422f23
source_role=parent
```

The changed in-tree support file hash is:

```text
tests/e2e/local/support/run-parent-manual-drop-evidence.sh
sha256=34ee03d1ea6f25ae4f68b8965f5c9b050d8892214416ec3bf551dfa81b17a2d2
```

The shared tuple retained by the driver is Agent
`6efc81500a0e0688c2bb41e736503f0fc3e04abb` / tree
`2ed2b8a12b5b3391ca221ba6ff05390f71a73556`, Runtime and producer
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` / tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`, App pin
`10fa2ff9a8216604aa39e3584f89dc9e7a09080a`, private graph archive
`sha256:895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`,
and official Composition 0.0.13 archive
`sha256:9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`.

## Verification

Passed directly in this worker:

```text
sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh
  passed

NORMAL014_RECORD_DIR=<private worker temp> sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe
  passed; zero-test child was refused, then failure-trap evidence was copied before cleanup

TMPDIR=<private worker temp> PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers \
  node node_modules/playwright/cli.js test \
  --config playwright.three-products.config.ts \
  --grep 'M2 real mounted manual video drop' --list
  passed; exactly 1 test collected at three-products.spec.ts:1440

./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/three-products.spec.ts
  passed

git diff --check
  passed
```

The shared FULL preflight was not run. Its HOME-owned
`normal014-source-common.sh` currently still binds `final95:parent` to the
old `da6d910f7ab3dfc71142ece7f632d43341238882` /
`6809757f93ca5e166b24b8bc0160ca09005e984a` source. That is incompatible with
the required merged source above, so invoking preflight before HOME advances
that closed source guard would only fail at source identity. The helper hash
is unchanged at
`3dc9034586bf8c6fe2ff877b44fd1cbbabfb4eeeb1472fe009bad6d677811014`.

The preflight prerequisites and negatives remain required before any actual:
exact HOME App SHA/tree and clean state; `parent` role; Agent/Runtime/producer
commit and tree tuple; runtime lock, generated contract, schema, artifact and
manifest bytes; private graph/archive and official Composition archive;
wrong-source-role refusal; wrong graph/refusal; wrong argv/required-case
refusal; zero-child refusal; and exactly one manual-drop `--list` result.
Only the last and the zero-child control were executed here. No actual body
qualification is claimed.

## Boundary and next step

The latest HOME source also contains the newer native-bootstrap production
merge from parent `1557c312...`; this worker did not invoke its test or
bootstrap path. This preserves HOME production as requested while keeping
native-bootstrap execution outside this source-only packet.

HOME should first update the closed `final95:parent` source helper to
`APP_ROOT_SHA=5d36b0e53ff0d17ef045e226a6e6ca7584322858` and
`APP_ROOT_TREE=1b07030d63216294f849422523b0d55a17422f23`, then obtain a fresh
source-custody approval/preflight. Only after that approval should the
existing durable command be considered for one separately authorized actual
run. No actual request was submitted here.
