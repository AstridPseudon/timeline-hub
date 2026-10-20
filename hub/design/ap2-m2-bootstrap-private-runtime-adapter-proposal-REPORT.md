# AP2-M2 private RuntimeDataProvider bootstrap adapter proposal

Status: **PROPOSAL ONLY; App production source was not changed.**

## Result

The current provider does **not** expose a complete Native Bootstrap V1
operation. `createDefaultTimeline.ts` currently calls the native consumer
directly and only uses a separately constructed `RuntimeDataProvider` for
`loadTimelineCommandBasis` and `commitTimeline`. The current provider
constructor also creates its own `AstridRuntimeClient`, so a transport fixture
can pass without proving that the configured provider owns the native request.

The minimal proposed join is:

1. Add an `@internal` `runtimeClient?: AstridRuntimeClient` constructor option
   and one `initializeNativeBootstrapTimeline` method to
   `RuntimeDataProvider`.
2. Have that method call the existing `initializeBootstrapTimeline` consumer
   with the provider's existing guarded client methods, existing
   `loadTimelineCommandBasis`, and existing `commitTimeline`.
3. Change `createDefaultTimeline`'s private initializer to construct the
   provider around the already configured client and call that adapter.
4. Strengthen one existing native fixture by removing its global `fetch`
   fallback. It then proves create → H0 → native init through the configured
   provider transport, rather than through an injected port or separately
   configured client.

The exact applyable proposal is [ap2-m2-bootstrap-private-runtime-adapter-proposal.patch](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-bootstrap-private-runtime-adapter-proposal.patch), SHA-256
`1e9a2a792a5a3c69a13edcbba8c5aae91c23b09b021284831c6f448d9f33541f`.
The typed method excerpt is [ap2-m2-bootstrap-private-runtime-adapter-proposal.ts](/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-bootstrap-private-runtime-adapter-proposal.ts).

## Contract boundaries preserved

- No endpoint, DTO, schema, generated client operation, store, outbox field,
  or public release pin is proposed.
- `createTimeline`, history, immutable parent reads, and `/commit` remain the
  existing generated/client operations. The exact create request and native
  init request remain reserved in the existing `astrid.command-outbox` before
  their awaits; same-ID recovery and readback stay in
  `bootstrapInitialization.ts`.
- The adapter does not synthesize a head or overwrite opaque content. The
  accepted create receipt supplies the H0 revision/publication pair; the
  existing history read supplies the verified base for init. The existing
  provider basis read refuses a missing history publication pair.
- The existing `RuntimeDataProvider.commitTimeline` checks the project,
  timeline, revision, publication, accepted receipt, canonical document, and
  id map. The adapter adds no alternate commit path.
- The current provider's raw composition-revision read carries immutable
  payload identity but not a usable head publication pair. If the matched
  Runtime carrier cannot provide the accepted H0 pair through create/history,
  that is an exact Runtime prerequisite; this proposal does not invent a
  field or API to fill it.
- The old headed/no-default, canonical-ID/alias, concurrent Main CAS, and
  additional-timeline/lost-response positives remain in the existing test
  file. Strict native route/header/body and legacy-route assertions remain
  unchanged; the new fixture control only removes the global fetch fallback
  for one fresh-create proof.

## Current source evidence

- `src/integrations/runtime/createDefaultTimeline.ts:56-84` directly assembles
  ports around `initializeBootstrapTimeline`; only two ports go through the
  provider today.
- `src/integrations/runtime/dataProvider.ts:91-99,371-374` constructs a new
  client from URL/token/transport and has no native-bootstrap adapter.
- `src/integrations/runtime/dataProvider.ts:680-697` is the existing guarded
  commit boundary; `:803-844` obtains the accepted history head and immutable
  closure.
- `src/integrations/runtime/client.ts:615-646` already wraps the existing
  generated create/commit/history operations; no client endpoint addition is
  needed.
- `src/tools/video-editor/commands/commitOutbox.ts:59-69,280-315` already
  provides durable create reservation, exact request retention, retry identity,
  and initialization checkpointing.

## Qualification boundary

This remains private until the matched Agent `3c4f6de4fa777323b3386c01c7266b619b86af6d`
source and Runtime `202074110717146fc7f08af2306a8dd7f695b0b1` source are
qualified together, then the owner explicitly activates the consumer. No
public 0.2.13 pin or source-public release is implied. The existing Agent
opaque-inverse/native and Runtime null-head/fresh-scope gates remain separate
prerequisites.

## Verification

On the unchanged private App worktree:

```text
node node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --no-cache --maxWorkers=1 --no-file-parallelism src/integrations/runtime/bootstrapInitialization.test.ts src/tools/video-editor/commands/bootstrapCapture.test.ts src/tools/video-editor/commands/commitOutbox.test.ts src/integrations/runtime/createDefaultTimeline.test.ts src/integrations/runtime/client.test.ts src/integrations/runtime/clientSharedSession.test.ts
=> 6 files passed, 158 tests passed

npm run typecheck:strict-probe
=> passed

git diff --check
=> passed; worktree clean

git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/ap2-m2-bootstrap-private-runtime-adapter-proposal.patch
=> passed
```

For proposal-only validation, I applied the patch transiently in this own
worktree, ran `createDefaultTimeline.test.ts` directly (`1 file, 12 tests
passed`), and reverted the source with `apply_patch`; no production change
remains. No browser, localhost/live socket, Runtime Door, full suite, public
pin, dependency install, or activation was run.

## Next step

The App owner should review/apply the paired patch only after the exact
3c4/202 source pair and owner activation decision are available, then run the
existing 158 direct-neighbor lane plus the centrally managed real provider
boundary journey. Do not retire the legacy writer based on this proposal.
