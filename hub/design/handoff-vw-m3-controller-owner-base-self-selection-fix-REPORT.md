# Report: App owner-base self-selection custody fix

## Result

Fixed the one process-custody defect in the two allowed controller files:

- `assertAppOwnLeaf` now requires the selected source to be an ancestor of the
  existing `refs/heads/tl/integration` App owner lineage before calculating the
  leaf diff.
- The selected commit's tree is checked against the explicitly supplied tree.
- Candidate `05de08cecabeaea2d0d955475e6190acc685111a` therefore cannot
  self-select as its own unintegrated base and obtain an empty diff.
- The two-controller-file `OWN_LEAF` restriction is unchanged.

The existing `tl/integration` ref is the smallest source-of-truth carrier that
survives normal central Git snapshots; no new selector, SHA allowlist, source
self-certification, framework, or stored authority was added. Historical absent
App defaults and present-but-empty/partial/malformed input rejection remain
unchanged.

Added direct regression coverage for the reviewed candidate self-source
negative and the real owner-base `20ea14c26526fe4924354f10a177aebbaf6002bc` /
`83cfad527f8b2264085571316cede1c6ae482b5f` success.

## Packets and dependency order

1. Apply `original-owner-5-files.patch` and integrate it through the App owner.
2. Record that actual owner-integrated source/tree.
3. Apply `corrected-leaf-2-files.patch` only on that base.

The five-file packet is unchanged from the prior owner/leaf split:
`ccda44301c140388bbd662f42fc1361825d5975802d6302a3669ca122e9aad4a`.
The corrected two-file patch SHA-256 is
`4c69e97b2327cc33dee1a00e60c82c29912561a95334b78b163a4a7cff8fee98`.

## Verification

All passed with pinned Node `v20.19.4` (`43d6cf63f2a460b463eba6b19df5e9a259771c56f11b5130e04178a15bb99490`):

```text
node --check tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs
node --test --test-concurrency=1 tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs
node --test --test-concurrency=1 scripts/testing/current013-integration.test.mjs
node --import tsx --test --test-concurrency=1 tests/e2e/timeline/viewing-parity/source-tuple.test.ts tests/e2e/timeline/viewing-parity/harness.test.ts
node tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs --discover "$PWD"
node_modules/.bin/eslint --no-cache --max-warnings 0 tests/e2e/timeline/viewing-parity/tab-audio.controller.mjs tests/e2e/timeline/viewing-parity/tab-audio.controller.test.mjs
git diff --check
```

Results: controller 1 file passed; integration 1 file passed; source-tuple /
harness 2 files passed; discovery reported exactly 5 current
native-codec-chrome155 parity cases; syntax, ESLint, and whitespace checks
passed. No full, browser/live-socket, grant, signing, capture, render,
install, or `--ready` run was performed. One independent review of this final
custody delta remains required after source/tests.
