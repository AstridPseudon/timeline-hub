# App Runtime boot-loading owned fix

## Scope and decision

Applied only the authorized `RuntimeConnectionProvider.tsx` hunk from `app-remaining-baseline-proposal.patch`:

```ts
isBooting: outcome === null
```

Permission-null and first-probe pending remain booting. After the first unsuccessful settled probe, the provider is anonymous and no longer booting while its existing `connecting` state and two-reading recovery threshold remain unchanged. Authentication still derives from `isConnected`; `AuthContext.tsx`, `AuthGate.tsx`, and `mediaCrossOrigin.ts` were not changed.

Added four permanent controls in the owned provider test scope:

- pending first permission query does not probe and remains booting;
- pending first probe remains booting and keeps gated children unmounted;
- first failed reading ends boot loading anonymously without mounting gated children;
- a successful second reading recovers and mounts gated children.

Existing prompt/denied, connection, recovery, gate, and AuthContext assertions were preserved unchanged.

## Qualification

The applied tree passed the requested targeted controls with Vitest 4.1.5, standard physical deps8, one worker, runner config loading, and no cache. The worker-local dependency overlay was temporary and removed after the run; the shared dependency tree was not modified.

```sh
node --require /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/managers/app/notes/snapshot-vitest-runner.cjs /tmp/app-m2-coherent-deps8/node_modules/vitest/vitest.mjs run --config config/testing/vitest.config.ts --configLoader=runner --no-cache --maxWorkers=1 --pool=forks src/integrations/runtime/RuntimeConnectionProvider.test.tsx src/integrations/runtime/connection.test.ts src/integrations/runtime/localNetworkPermission.test.ts src/shared/auth/components/__tests__/AuthGate.test.tsx src/shared/contexts/__tests__/AuthContext.gated.test.tsx src/shared/contexts/__tests__/AuthContext.test.tsx
```

Result: **6 test files passed, 100 tests passed, exit 0**. No full suite, build, browser/e2e, project typecheck, install, socket, or pin/wire change was run. This targeted result is not a global baseline claim.

## Ownership and exclusions

Changed product/test files are limited to the App-owned Runtime integration provider and its owned test file. The shared-media proposal remains unapplied and requires its separate owner grant. No AuthContext/AuthGate source edit or auth bypass was needed.
