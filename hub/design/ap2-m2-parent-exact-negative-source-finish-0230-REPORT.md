# AP2-M2 parent mounted ADD exact negative and source finish

## Result

Finished the existing mounted manual ADD negative and its existing evidence
driver only.

- The valid-format mismatch still changes exactly one hex digit of the real
  `sha256:<64-hex>` object ID and preserves the other four selection fields.
- The refusal now asserts exactly HTTP `404` and exactly:

  ```json
  {
    "code": "not_found",
    "message": "selected media is not a managed project generation/variant/object"
  }
  ```

- The old malformed `sha256:wrong-selection` diagnosis was not reintroduced or
  relabelled as final95 evidence.
- The original positive ADD and recovery assertions remain unchanged: the
  five-field selection, parent `clip.add-media`, row/track/position shape,
  no `afterClipId`/replacement/removal fields, lost acknowledgement, restart,
  exact retry, reload, undo, raw/opaque preservation, duplicate prevention,
  and zero legacy traffic.
- The existing driver now forces `final95` + `parent`, records the exact
  final95 source tuple, and requires the observed App HEAD to descend from
  committed source `7e85d89120227f336a2e8dbf8e0ea44d98311da0`. It does not
  embed a self-referential App tree digest.

## Source binding and finalization

The finished two-file consumer content has tree
`6809757f93ca5e166b24b8bc0160ca09005e984a`. The harness will create the final
consumer commit after this worker exits, so its commit SHA cannot be known
here without a self-reference. Before any real run, the manager/reviewer must:

1. Read the harness-created clean App source:

   ```sh
   APP_ROOT=/home/user/work/wt/ap2-m2-parent-exact-negative-source-finish-0230
   APP_SHA=$(git -C "$APP_ROOT" rev-parse HEAD)
   APP_TREE=$(git -C "$APP_ROOT" rev-parse 'HEAD^{tree}')
   test "$APP_TREE" = 6809757f93ca5e166b24b8bc0160ca09005e984a
   test -z "$(git -C "$APP_ROOT" status --porcelain=v1 --untracked-files=all)"
   git -C "$APP_ROOT" merge-base --is-ancestor \
     7e85d89120227f336a2e8dbf8e0ea44d98311da0 "$APP_SHA"
   ```

2. In the shared HOME-owned
   `design/normal014-source-common.sh`, set the `final95:parent` source
   binding literals to the actual `APP_SHA` and the literal tree
   `6809757f93ca5e166b24b8bc0160ca09005e984a`. Keep the ancestry, exact-tree,
   clean-state, pin-byte, artifact-manifest, schema, import, lock, and
   postflight checks intact. Do not use `git rev-parse` or an environment
   override as the checked-in expected value.

The exact existing-driver command after that finalization is:

```sh
sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh run "$PWD"
```

The driver supplies `NORMAL014_PROFILE=final95` and
`NORMAL014_APP_SOURCE=parent` to the existing runner. The central service may
wrap the App in a synthetic commit; the source helper accepts that only when
the committed source remains in ancestry while the exact consumer tree and
clean state still match. Agent `6efc81500a0e0688c2bb41e736503f0fc3e04abb`
(tree `2ed2b8a12b5b3391ca221ba6ff05390f71a73556`), Runtime/producer
`95bd3c5f6d00e9bc8cc8cbe5ef510b68ed660f3c` (tree
`d3a290b407fa61e6ab2d476f50c068073f70df00`), App pin
`10fa2ff9a8216604aa39e3584f89dc9e7a09080a`, and public13 archive
`sha256:895c628ab0727c8975247310fd0319b0f546a8d032a57072c9e364e20965ca30`
remain the required tuple. No import, artifact, schema, or postflight guard
was weakened.

## Live callers

The existing mounted ADD chain is unchanged:

`handleFileDrop` → `dispatchTimelineDrop` → `useTimelineState` →
`useAssetManagement` → native `addClip` facade, with
`useExternalDrop.ts`, `external-drop-utils.ts`,
`useTimelineCommandsService.ts`, and the existing commit-session/outbox path
as its neighboring callers.

## Verification

Passed directly in this worker:

```text
sh -n tests/e2e/local/support/run-parent-manual-drop-evidence.sh
  passed

NORMAL014_RECORD_DIR=<private TMPDIR> sh tests/e2e/local/support/run-parent-manual-drop-evidence.sh probe
  failuretrap probe passed

./node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/local/three-products.spec.ts
  passed

node node_modules/playwright/cli.js test --config playwright.three-products.config.ts \
  --grep 'M2 real mounted manual video drop' --list tests/e2e/local/three-products.spec.ts
  1 test collected

git diff --check
  passed
```

Not run, as required: browser execution, localhost/live sockets, full or
central suites, real gate, dependency installation, or product-source
qualification. The exact final95 source preflight and mounted journey remain
unverified until HOME performs the post-harness source finalization above.
