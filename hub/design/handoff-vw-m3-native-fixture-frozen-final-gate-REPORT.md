# Native fixture frozen-pair final attribution gate

## Decision

**APPROVE the current owner-port evidence.** The previously approved App owner
fixture remains test-only. The follow-up is narrowly limited to
`tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts` and adds
frozen Runtime/Agent archive, source-manifest, module-origin, and explicit
`PYTHONPATH` guards. No Composition worktree files changed.

## Attribution verified

- Runtime commit `2c4ac180c2220bdad966bc01e95ad230e99ce26a` resolves to tree
  `7ab412cc4bcbe517efcfa806e092336390312e18`.
- Agent commit `d8749a9ce12a699672faf3ad96b4e4cbea9245c2` resolves to tree
  `75354d38c898729bac09619679f5421faba319ed`.
- Runtime archive SHA-256 is
  `eed22a1b0d1af2045f823ec9f71dbd7cd862ba7935edfd5199171656e3ff1669`;
  its extracted manifest is 413 files,
  `a6ec4c76dbc30bf37fd258f2267410ab591fd605181d21e7338a6dff2d6e3627`.
- Agent archive SHA-256 is
  `91d4d82f4ee2a251ba6c3706d47efa80411d05e683c64c78a05414d4229b3add`;
  its extracted manifest is 3076 files,
  `c436c9e648db306d59dbf728e3294f79d9b971d100ced69fbb1292c17206dada`.
- The approved owner commit is App `dba11c8432cee8df6e8bced4eae4d82e79f2b652`,
  tree `79fca36dcc07d83d457bc2db5f822cad28054d71`, with exactly the five
  expected fixture/harness files. The successful central snapshot is App tree
  `e43c4c34107bb474beb5e86e669cb4d75d961e7a`; compared with the owner tree,
  only `native-fixture.integration.test.ts` changed (111 insertions, 11
  deletions). Its source SHA-256 is
  `b1c43e437b55d11b4dd0845eb89a25332e1c5921c3d31baa49bdb5144c4b967b`.
- The successful log proves `astrid.__file__` is under the extracted Agent
  archive and `runtime_protocol.__file__` under the extracted Runtime archive;
  it also proves the ordered explicit Runtime-then-Agent path entries.

## Central evidence

Successful record:
`vw-m3-native-frame-fixture-frozen-pair-proof-integration-viewing-native-retained-fixture-1020141813-18235`

- Central command: `integration-viewing-native-retained-fixture`; App tree
  `e43c4c34107bb474beb5e86e669cb4d75d961e7a`; **1 pass, 0 fail**.
- Before/after extracted source manifests are byte-for-byte unchanged for both
  Runtime and Agent.
- The authenticated native `/v1` restore fixture keeps the default M1 seed
  disabled, observes zero legacy composition-revision POSTs, and rejects the
  forged task without changing the object list.
- No browser, render, full suite, production media, four-case parity run,
  dimensions, or default M1 seed claim is made here.

The first central record
`vw-m3-native-frame-fixture-frozen-pair-proof-integration-viewing-native-retained-fixture-1020141730-11929`
**stays failed**. Its guard expected `[runtime, agent]` but saw Python’s empty
`-c` script-directory entry followed by Runtime, so it failed before exercising
the Runtime. The repair was to filter `sys.path` to the two explicit archive
roots before asserting their order. The earlier moving-checkout run and the
direct native `2c4`/`d874` witness are retained as separate evidence and are
not relabeled as this HTTP proof.

## Test evidence reviewed

- `npx eslint tests/e2e/timeline/viewing-parity/native-fixture.integration.test.ts --report-unused-disable-directives --max-warnings 0 --no-cache` — PASS.
- `node --import tsx --test tests/e2e/timeline/viewing-parity/harness.test.ts tests/e2e/timeline/viewing-parity/media.test.ts tests/e2e/timeline/viewing-parity/canvas.test.ts tests/e2e/timeline/viewing-parity/authority.test.ts tests/e2e/timeline/viewing-parity/admission.test.ts` — 5 PASS.
- Central named suite above — 1 PASS after the failed guard attempt; no HTTP rerun was performed for this review.

## Blockers and next steps

No blocker for this narrow gate. Browser/render and the original media four-case
qualification remain separately unverified, as required by scope. The successful
central record is sufficient for this attribution gate; do not relabel the
failed first attempt or the direct witness.
