# App normal014 private same-cohort qualification

App owner handoff: qualify this exact private cohort only; do not merge it into
`tl/integration`, publish `0.2.14`, activate a writer, or move a frozen ref.

## Exact tuple

- Runtime candidate: `202074110717146fc7f08af2306a8dd7f695b0b1`, tree
  `ee39286bd0eb27d4075074cc4785d6d15e33f243`.
- Immutable Runtime producer: `a0dca16975dfe8f5e762703b99d9791a16cf7fd7`,
  tree `4b7dd0fe44be973c344bab3de568eaf0bdd28476`, package `0.2.14`
  unpublished.
- Runtime artifact version:
  `sha256:f021e7714c1b40011b69ba624d288c217749d58013b8adf0352d283854f20fa0`;
  `contract/artifacts.json` SHA-256
  `ecda762ebe682f266395161af055921c3db33ee9914fb00860626e7e4852d815`;
  75 artifacts.
- Shared Agent/Runtime edit-command schema raw SHA-256
  `6ba7b51e9518e7fb08b27ad5b7225855276b657d0adebf704dd853f699768f2d`;
  55 definitions / 29 command operations.
- Agent source for this request: `3c4f6de4fa777323b3386c01c7266b619b86af6d`,
  tree `aaf49eca6c2b119b21df1d89b0e56df5d1c60f9c`. The older
  `e86f44d04e0a5f183d82d4d1ac307951dd32c44e`
  evidence remains historical and is not relabeled as proof for this source.

The App integration branch remains on its existing Runtime `0.2.13` source.
The qualification worker used a temporary private App copy and the normal
`scripts/vendor-lock.mjs` update/check against a private copy of Runtime
`202074…`; no App `runtime.lock.json`, generated client, package, shared code,
or frozen reference was changed.

## Reproducible owner proposal

1. From a clean App branch, make a private copy of the App tree and a private
   producer checkout at Runtime `202074…`. Change only the private lock's
   `source_commit` selector to `202074…`, then run:

   ```sh
   node scripts/vendor-lock.mjs update runtime.lock.json --producer <private-runtime-202074-checkout>
   node scripts/vendor-lock.mjs check runtime.lock.json --producer <private-runtime-202074-checkout>
   node scripts/vendor-lock.mjs check runtime.lock.json
   ```

   The normal tool must copy the producer's 13 locked files; do not hand-edit
   generated files or add a client shim. Assert the App/producer bytes and the
   exact tuple above before any journey.

2. Run the safe contract/SDK lane on that private copy with cache disabled:

   ```text
   src/integrations/runtime/client.test.ts
   src/integrations/runtime/clientSharedSession.test.ts
   src/integrations/runtime/recordedResponses.test.ts
   src/integrations/runtime/timelineCommit.test.ts
   src/integrations/runtime/dataProvider.test.ts
   src/integrations/runtime/vendorLock.test.ts --testNamePattern='consolidates generated types|pins the entire Astrid public boundary'
   ```

3. Send every socket, provider-backed, browser, restart/reload, lost-ACK,
   retry, undo/redo, and parent-media acceptance journey through the central
   test service. Use the exact Agent `3c4f…` source and Runtime `202074…` /
   producer `a0dca169…`; do not substitute current013 proof or a moving
   integration checkout. No full suite is part of this private request.

## Required marker boundary

Runtime `202074110717146fc7f08af2306a8dd7f695b0b1` carries the old test blob
`183f14dbe64466c9a8c7aec5b34850da9272f107`.
It does not contain the `cd0` owner-strict transition. Before adoption, carry
the test-only transition from `cd0b0dcbea57c2a140e970eda59bea1161d6ff06` /
final `d05e6383f4ccaf7541698a65b2737fbc5f3f0fbb`: a positive
current-schema parent-ownership refusal, plus the complete original
`test_native_parent_clip_swap_route_replaces_parent_media` body retained as a
strict `xfail` with the schema requirement named. Preserve all positive
assertions; do not mutate artifacts, schema, generated clients, or producer
bytes to make the marker pass. This is a Runtime/App-owner prerequisite, not an
App integration change in this handoff.
