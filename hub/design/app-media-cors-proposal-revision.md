# App shared-media CORS proposal revision

Base: App `18becfbede00038830b97e63345445eeef54fa42` (tree `44d514b44c864ff9dbb3b99aba2b0a41891af83f`). Product files were not modified.

## Decision

The revised external patch changes exactly one product path:

`src/shared/lib/media/mediaCrossOrigin.ts`

It adds one small predicate, `isHttpGatewayUrl`, which first requires an actual
`http:` or `https:` URL and then calls the existing `isGatewayUrl`. Both
`mediaCrossOrigin` and `mediaFetchCredentials` use that same predicate alongside
the unchanged `isManagedObjectUrl` predicate.

This keeps the old canonical relative/absolute managed-object behavior and adds
anonymous CORS plus omitted browser credentials only for configured HTTP(S)
gateway URLs. A configured-origin `blob:` URL is not an HTTP(S) URL and therefore
retains its prior mode. No URL is rewritten, no route or authority policy is
changed, and no Runtime handler, managed-media predicate, or response header is
edited.

The boot/auth hunk is deliberately absent. The virtual qualification used the
already-owned App boot hunk only as an explicitly labeled context source so the
existing 76-case proposal probe could be rerun; it is not part of this patch.

Patch: `/tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-media-cors-proposal-revision.patch`

## Mode contract

| Input | `mediaCrossOrigin` | `mediaFetchCredentials(url, 'include')` |
| --- | --- | --- |
| Configured HTTP(S) gateway URL, including the two existing `/objects/*/content` CORS inputs | `anonymous` | `omit` |
| Canonical managed object URL, relative or HTTP(S) loopback | unchanged (`anonymous`) | unchanged (`omit`) |
| Configured-origin `blob:` URL | `undefined` | `include` |
| External blob, data, file, custom, signed HTTPS, protocol-relative, or other-loopback-origin URL | `undefined` | `include` |

The two original gateway CORS tests and every original input/assertion remain
unchanged in the proposal. The current Runtime byte route is not changed; these
checks establish client transport attributes only, not successful byte retrieval.

## Permanent test proposal

After the shared-media ownership grant, add one table-driven test to the existing
`src/shared/lib/media/mediaCrossOrigin.test.ts`. Keep all existing tests byte-for-
byte and add the seven independent unchanged-mode controls from
`workers/app-m4-media-cors-proposal-revision/notes/independent.test.tsx`:

- `blob:http://127.0.0.1:17340/local-object-id` (the proven exception)
- `blob:https://astrid.haus/local-object-id`
- `data:audio/wav;base64,AAAA`
- `https://signed.example/media?signature=abc`
- `custom:media-id`
- `//127.0.0.1:17340/media`
- `http://127.0.0.1:17341/media`

Each row should assert both `mediaCrossOrigin(url) === undefined` and
`mediaFetchCredentials(url, 'include') === 'include'`. The existing two gateway
inputs should continue to assert `anonymous` and `omit`; no auth/boot tests belong
in this shared-media patch.

## Evidence

The external virtual-source run loaded the revised shared-media source and the
explicit prior App-owned boot context, with the original product tests and the
external controls. It passed **8 files / 83 tests**: the original 76-case probe
inputs plus the seven independent mode controls. This demonstrates the two old
media failures are fixed and all transport-mode controls pass, including the
configured-origin blob case.

Command, run from the private probe root, with max workers one, standard deps8,
private cache, runner config, and no cache:

```sh
APPLY_PROPOSAL=1 node --require ../runner.cjs node_modules/vitest/vitest.mjs run \
  --config ../probe.config.ts --configLoader=runner --no-cache \
  src/shared/components/__tests__/HoverScrubVideo.gateway.test.tsx \
  src/shared/components/__tests__/HoverScrubVideo.test.tsx \
  src/shared/lib/media/mediaCrossOrigin.test.ts \
  src/shared/contexts/__tests__/AuthContext.gated.test.tsx \
  src/shared/contexts/__tests__/AuthContext.test.tsx \
  src/integrations/runtime/RuntimeConnectionProvider.test.tsx \
  ../supplemental.test.tsx ../independent.test.tsx --maxWorkers=1
```

Result: exit 0, `Test Files 8 passed (8)`, `Tests 83 passed (83)`, Vitest 4.1.5,
12.16s. The log is at
`workers/app-m4-media-cors-proposal-revision/notes/proposal.log`.

Other checks:

```sh
git apply --check /tmp/claude-0/-home-user-repo/7dc61be1-7066-52e0-a5d0-94f90e61430a/scratchpad/orch/design/app-media-cors-proposal-revision.patch
git diff --check
git status --porcelain=v1
```

All exited 0; the App worktree remained clean. No full suite, build, tsc,
browser, install, localhost listener, live socket, or content-retrieval test was
run. No live media or successful byte response is claimed.
