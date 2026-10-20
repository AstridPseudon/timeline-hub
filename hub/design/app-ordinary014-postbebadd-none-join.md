# App ordinary014 normal pin — postbebadd/None branch staging

Status: **source staged only**. No merge, release, activation, integration
adoption, or public pin movement was performed.

## Source tuple

- Pin source: App `ed9728ead0676a04ebd4d413e9f2574da037723c`, tree
  `604f6523a37c4d997afef02dab43421433b175ec`.
- Merge parent supplied by the harness: App `c57dcc26162642f503532f143ceb96bb185273aa`,
  tree `b02e5380cc664bf07e4703e9a388bce0442ff645`.
- Runtime producer: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`, tree
  `4b7dd0fe44be973c344bab3de568eaf0bdd28476`.
- Runtime artifact: package `0.2.14`, version
  `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa`;
  manifest `sha256:ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`.
- Raw edit-command schema: `sha256:6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`,
  55 definitions and 29 command operations. Runtime wire schema:
  `sha256:ce3781c282564b650890456f6c257f3faabe2de3898a84363fecd47e48b30d59`.

The pin commit changes only `runtime.lock.json`,
`src/integrations/runtime/generated-contract-metadata.ts`,
`src/integrations/runtime/generated.ts`, and
`src/integrations/runtime/timeline-commit-types.ts`. The four parent file
hashes are identical at `c57dcc261` and the pin commit's parent, so the
harness merge-parent supplies the current mainbebadd/label/carrier/None base.
App public13 Composition tarball identity remains
`9412ae25c306d5118241f4d631e8eecc6eef9b2fb5a98302d40938e9f6d54738`; its
package/lock bytes and the c57 native-writer changes are outside this four-file
delta and were not edited.

The producer-backed normal updater was used for qualification; no generated
file was hand-edited, no package was installed or repacked, and no archive
bypass was used. It verified all 75 producer artifacts and all 13 consumer
destinations byte-for-byte.

## Tests

Passed:

```text
node scripts/vendor-lock.mjs check runtime.lock.json
node scripts/vendor-lock.mjs check runtime.lock.json --producer /home/user/work/wt/app-m2-runtime014-a0-git-producer-source-keeper
git diff --check
```

Cache-free private Vitest controls, using `--configLoader=runner --no-cache
--maxWorkers=1 --no-file-parallelism`:

```text
src/integrations/runtime/client.test.ts
src/integrations/runtime/clientSharedSession.test.ts
src/integrations/runtime/recordedResponses.test.ts
src/integrations/runtime/timelineCommit.test.ts
src/integrations/paired/pairedRoutePolicy.test.ts
src/integrations/astrid/nativeEditorConnection.test.ts
src/integrations/runtime/opaqueRootWriters.test.tsx
```

Result: **7 files, 2,053 passed**. The selected vendor-lock structural
checks (`consolidates generated types|pins the entire Astrid public boundary`)
passed **2/2**; 11 fixture tests were not selected because their temporary
child-Git setup is sandbox-blocked.

Corrected media-import controls available in this worker checkout:

```text
src/integrations/runtime/mediaImport.test.ts
src/tools/video-editor/hooks/useAssetManagement.mediaImport.test.tsx
```

Result: **2 files, 9 passed**. The c57 merge-parent retains the six-test
corrected42e integration import file; this worker did not materialize c57 by
checkout or merge, so that merge-parent-only test body is not separately
claimed as executed here.

The focused fake-runtime data-provider reproduction was run without changing
tests:

```text
src/integrations/runtime/dataProvider.test.ts
```

Result: **64 passed, 5 failed**. All five failures are the known preexisting
fake-runtime omission for `GET /v1/projects/project-r1/media-selection?...`
at `src/test/fakeWorkspaceRuntime.ts:501`; no assertion was changed, skipped,
weakened, or marked expected-to-fail.

## Remaining gate

This source preparation does not qualify the paired consumer cohort. Before
adoption, qualify Runtime `202074110717146fc7f08af2306a8dd7f695b0b1` (tree
`ee39286bd0eb27d4075074cc4785d6d15e33f243`) with Agent
`3c4f6de4fa777323b3386c01c7266b619b86af6d` (tree
`aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`). Carry the `cd0` strict marker
only on the pre-adoption current-013 path; do not copy its current-schema
parent-ownership refusal into Runtime 0.2.14, whose schema explicitly accepts
`ownership: parent`. No full suite, project tsc, build, install, browser,
network/socket, merge, release, activation, or public pin movement was run.
